from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

if __package__:
    from . import coding_question as cq
else:
    import coding_question as cq

type JsonObject = dict[str, object]


def _scan_index_keys(redis: cq.RedisRestClient) -> set[str]:
    cursor = "0"
    keys: set[str] = set()
    while True:
        result = redis.execute(
            ["SCAN", cursor, "MATCH", f"{cq.INDEX_PREFIX}:*", "COUNT", 1_000]
        )
        if (
            not isinstance(result, list)
            or len(result) != 2
            or not isinstance(result[0], str)
            or not isinstance(result[1], list)
            or any(not isinstance(key, str) for key in result[1])
        ):
            raise cq.UpstashError("Index SCAN returned an invalid response.")
        cursor = result[0]
        keys.update(result[1])
        if cursor == "0":
            return keys


def _pipeline_results(
    redis: cq.RedisRestClient, commands: Sequence[cq.RedisCommand]
) -> Iterable[object]:
    for start in range(0, len(commands), cq.PIPELINE_COMMAND_LIMIT):
        yield from redis.pipeline(commands[start : start + cq.PIPELINE_COMMAND_LIMIT])


def _key_types(redis: cq.RedisRestClient, keys: Sequence[str]) -> Mapping[str, str]:
    results = _pipeline_results(redis, [["TYPE", key] for key in keys])
    key_types: dict[str, str] = {}
    for key, result in zip(keys, results, strict=True):
        if not isinstance(result, str):
            raise cq.UpstashError(f"TYPE returned an invalid result for {key!r}.")
        key_types[key] = result
    return key_types


def _set_members(
    redis: cq.RedisRestClient, keys: Sequence[str]
) -> Mapping[str, frozenset[str]]:
    results = _pipeline_results(redis, [["SMEMBERS", key] for key in keys])
    members: dict[str, frozenset[str]] = {}
    for key, result in zip(keys, results, strict=True):
        if not isinstance(result, list) or any(
            not isinstance(member, str) for member in result
        ):
            raise cq.UpstashError(f"SMEMBERS returned an invalid result for {key!r}.")
        members[key] = frozenset(result)
    return members


def _expected_members(dataset: cq.Dataset) -> Mapping[str, frozenset[str]]:
    return {
        f"{cq.INDEX_PREFIX}:all": dataset.all_ids,
        **dataset.index_members,
    }


def _topic_aliases() -> Mapping[str, list[str]]:
    aliases: dict[str, set[str]] = {}
    for source_name, canonical_name in cq.TOPIC_ALIASES.items():
        canonical = cq.normalize_index_value(canonical_name)
        aliases.setdefault(canonical, set()).add(source_name)

    return {
        canonical: sorted(source_names)
        for canonical, source_names in sorted(aliases.items())
        if source_names != {canonical}
    }


def _document_mismatch_ids(
    redis: cq.RedisRestClient, dataset: cq.Dataset
) -> tuple[str, list[str]]:
    key_type = redis.execute(["TYPE", cq.QUESTIONS_KEY])
    if not isinstance(key_type, str):
        raise cq.UpstashError("Document TYPE returned an invalid response.")
    if key_type != "hash":
        return key_type, sorted(dataset.all_ids)

    questions = sorted(dataset.questions, key=lambda question: question.question_id)
    commands: list[cq.RedisCommand] = [
        ["HGET", cq.QUESTIONS_KEY, question.question_id] for question in questions
    ]
    results = _pipeline_results(redis, commands)
    mismatches = [
        question.question_id
        for question, result in zip(questions, results, strict=True)
        if result != question.canonical_json
    ]
    return key_type, mismatches


def audit_indexes(redis: cq.RedisRestClient) -> JsonObject:
    dataset = cq.load_dataset(redis)
    expected = _expected_members(dataset)
    actual_keys = _scan_index_keys(redis)
    sorted_actual_keys = sorted(actual_keys)
    key_types = _key_types(redis, sorted_actual_keys)
    invalid_types = {
        key: key_type for key, key_type in key_types.items() if key_type != "set"
    }

    comparable_keys = sorted(
        key for key in actual_keys & expected.keys() if key_types.get(key) == "set"
    )
    actual_members = _set_members(redis, comparable_keys)
    membership_mismatches = sorted(
        key for key in comparable_keys if actual_members[key] != expected[key]
    )
    missing_keys = sorted(expected.keys() - actual_keys)
    unexpected_keys = sorted(actual_keys - expected.keys())
    hyphenated_keys = sorted(key for key in actual_keys if "-" in key)
    subtopic_keys = sorted(key for key in actual_keys if ":subtopic:" in key)
    percent_space_keys = sorted(key for key in actual_keys if "%20" in key)
    document_key_type, document_mismatch_ids = _document_mismatch_ids(redis, dataset)
    aliases = _topic_aliases()
    canonical_topics = sorted(
        key.removeprefix(f"{cq.INDEX_PREFIX}:topic:")
        for key in expected
        if key.startswith(f"{cq.INDEX_PREFIX}:topic:")
    )
    is_clean = not any(
        (
            invalid_types,
            membership_mismatches,
            missing_keys,
            unexpected_keys,
            hyphenated_keys,
            subtopic_keys,
            percent_space_keys,
            document_key_type != "hash",
            document_mismatch_ids,
        )
    )
    return {
        "is_clean": is_clean,
        "record_count": len(dataset.questions),
        "actual_index_key_count": len(actual_keys),
        "expected_index_key_count": len(expected),
        "invalid_types": invalid_types,
        "membership_mismatch_keys": membership_mismatches,
        "missing_keys": missing_keys,
        "unexpected_keys": unexpected_keys,
        "hyphenated_keys": hyphenated_keys,
        "subtopic_keys": subtopic_keys,
        "percent_space_keys": percent_space_keys,
        "document_key_type": document_key_type,
        "document_mismatch_count": len(document_mismatch_ids),
        "document_mismatch_ids": document_mismatch_ids,
        "topic_alias_group_count": len(aliases),
        "topic_aliases": aliases,
        "canonical_topic_count": len(canonical_topics),
        "canonical_topics": canonical_topics,
    }


def run_audit(redis: cq.RedisRestClient, *, apply: bool) -> JsonObject:
    before = audit_indexes(redis)
    if not apply:
        return {"mode": "audit-only", "audit": before}

    migration = cq.migrate(redis, apply=True)
    after = audit_indexes(redis)
    if after["is_clean"] is not True:
        raise cq.DataValidationError("Post-migration index audit failed.")
    return {
        "mode": "applied",
        "before": before,
        "migration": migration,
        "after": after,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit and normalize coding-question Redis indexes."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rebuild indexes with canonical names and verify the result.",
    )
    parser.add_argument(
        "--topics-output",
        type=Path,
        help="Write the sorted canonical topic names to this UTF-8 text file.",
    )
    return parser


def _write_topics(path: Path, result: JsonObject, *, apply: bool) -> None:
    audit_key = "after" if apply else "audit"
    audit = result.get(audit_key)
    if not isinstance(audit, dict):
        raise cq.DataValidationError("Audit result is missing topic names.")
    topics = audit.get("canonical_topics")
    if not isinstance(topics, list) or any(
        not isinstance(topic, str) for topic in topics
    ):
        raise cq.DataValidationError("Audit returned invalid topic names.")
    try:
        path.write_text("\n".join(topics) + "\n", encoding="utf-8")
    except OSError as exc:
        raise cq.ConfigurationError(f"Could not write topic list to {path}.") from exc


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        with cq.RedisRestClient(cq.Settings.from_environment()) as redis:
            result = run_audit(redis, apply=arguments.apply)
        if arguments.topics_output is not None:
            _write_topics(arguments.topics_output, result, apply=arguments.apply)
        sys.stdout.write(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
        )
        sys.stdout.write("\n")
        if arguments.apply:
            return 0
        audit = result["audit"]
        return 0 if isinstance(audit, dict) and audit.get("is_clean") is True else 1
    except cq.CodingQuestionError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
