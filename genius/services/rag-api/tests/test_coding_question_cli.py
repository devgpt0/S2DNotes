from __future__ import annotations

import json
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from fnmatch import fnmatchcase
from typing import cast

import httpx
import pytest
from scripts import audit_coding_question_indexes as audit
from scripts import coding_question as cq

QUESTION_IDS = (
    "00000000-0000-0000-0000-000000000001",
    "00000000-0000-0000-0000-000000000002",
    "00000000-0000-0000-0000-000000000003",
)


def make_record(
    question_id: str,
    *,
    company: str = "Acme",
    topic: str = "Array",
    subtopic: str = "Binary Search",
    difficulty: str = "Medium",
    status: str = "active",
    title: str = "Café Search",
) -> dict[str, object]:
    payload: dict[str, object] = {
        "tags": ["Array", "Search"],
        "hints": ["Split the search range."],
        "title": title,
        "topic": topic,
        "company": company,
        "examples": [
            {
                "input": [1, 2, 3],
                "output": True,
                "explanation": "The target exists.",
            }
        ],
        "subtopic": subtopic,
        "difficulty": difficulty,
        "constraints": ["1 <= n <= 100"],
        "description": "Find a target.",
        "input_format": "An integer array.",
        "output_format": "A boolean.",
        "unknown_payload_field": {"preserved": True},
    }
    return {
        "id": question_id,
        "company_name": company,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "status": status,
        "question_payload": json.dumps(payload),
        "unknown_top_level_field": ["preserved"],
    }


def sample_records() -> list[dict[str, object]]:
    return [
        make_record(QUESTION_IDS[1], title="ＣＡＦÉ   SEARCH"),
        make_record(QUESTION_IDS[0]),
        make_record(
            QUESTION_IDS[2],
            company="Beta",
            topic="Graph",
            subtopic="Breadth-First Search",
            difficulty="Easy",
            title="Shortest Path",
        ),
    ]


class MockUpstash:
    def __init__(self, legacy_json: str) -> None:
        self.strings: dict[str, str] = {cq.QUESTIONS_KEY: legacy_json}
        self.hashes: dict[str, dict[str, str]] = {}
        self.sets: dict[str, set[str]] = {}
        self.commands: list[list[str | int]] = []
        self.fail_command: str | None = None
        self.scards_are_wrong = False

    def handle(self, request: httpx.Request) -> httpx.Response:
        raw_payload = json.loads(request.content)
        if request.url.path.endswith("/pipeline"):
            commands = cast(list[list[str | int]], raw_payload)
            return httpx.Response(
                200,
                json=[self._response(command) for command in commands],
            )
        command = cast(list[str | int], raw_payload)
        return httpx.Response(200, json=self._response(command))

    def _response(self, command: list[str | int]) -> dict[str, object]:
        self.commands.append(command)
        name = cast(str, command[0]).upper()
        if self.fail_command == name:
            self.fail_command = None
            return {"error": "injected failure"}
        return {"result": self._execute(name, command[1:])}

    def _execute(self, name: str, arguments: list[str | int]) -> object:
        key = cast(str, arguments[0])
        if name == "TYPE":
            if key in self.strings:
                return "string"
            if key in self.hashes:
                return "hash"
            if key in self.sets:
                return "set"
            return "none"
        if name == "SCAN":
            pattern = cast(str, arguments[2])
            keys = self.strings.keys() | self.hashes.keys() | self.sets.keys()
            return ["0", sorted(item for item in keys if fnmatchcase(item, pattern))]
        if name == "GET":
            return self.strings.get(key)
        if name == "SET":
            value = cast(str, arguments[1])
            if (
                len(arguments) > 2
                and cast(str, arguments[2]).upper() == "NX"
                and (key in self.strings or key in self.hashes or key in self.sets)
            ):
                return None
            self.strings[key] = value
            return "OK"
        if name == "DEL":
            removed = 0
            for target in arguments:
                target_key = cast(str, target)
                removed += target_key in self.strings
                removed += target_key in self.hashes
                removed += target_key in self.sets
                self.strings.pop(target_key, None)
                self.hashes.pop(target_key, None)
                self.sets.pop(target_key, None)
            return removed
        if name == "HSET":
            target = self.hashes.setdefault(key, {})
            created = 0
            field_values = arguments[1:]
            for index in range(0, len(field_values), 2):
                field = cast(str, field_values[index])
                value = cast(str, field_values[index + 1])
                created += field not in target
                target[field] = value
            return created
        if name == "HGET":
            return self.hashes.get(key, {}).get(cast(str, arguments[1]))
        if name == "HKEYS":
            return list(self.hashes.get(key, {}))
        if name == "HLEN":
            return len(self.hashes.get(key, {}))
        if name == "SADD":
            target_set = self.sets.setdefault(key, set())
            members = {cast(str, member) for member in arguments[1:]}
            added = len(members - target_set)
            target_set.update(members)
            return added
        if name == "SMEMBERS":
            return list(self.sets.get(key, set()))
        if name == "SCARD":
            count = len(self.sets.get(key, set()))
            return count + 1 if self.scards_are_wrong else count
        if name == "RENAME":
            destination = cast(str, arguments[1])
            self.strings.pop(destination, None)
            self.hashes.pop(destination, None)
            self.sets.pop(destination, None)
            if key in self.strings:
                self.strings[destination] = self.strings.pop(key)
            elif key in self.hashes:
                self.hashes[destination] = self.hashes.pop(key)
            elif key in self.sets:
                self.sets[destination] = self.sets.pop(key)
            else:
                raise AssertionError(f"Missing RENAME source {key}.")
            return "OK"
        if name == "SINTER":
            keys = [cast(str, argument) for argument in arguments]
            if not keys:
                return []
            intersection = self.sets.get(keys[0], set()).copy()
            for set_key in keys[1:]:
                intersection.intersection_update(self.sets.get(set_key, set()))
            return list(intersection)
        if name == "EVAL":
            script = cast(str, arguments[0])
            if script == cq.PROMOTE_SCRIPT:
                questions_key = cast(str, arguments[2])
                legacy_key = cast(str, arguments[3])
                staging_key = cast(str, arguments[4])
                if questions_key in self.strings:
                    if legacy_key in self.strings:
                        return None
                    self.strings[legacy_key] = self.strings.pop(questions_key)
                elif questions_key not in self.hashes or legacy_key not in self.strings:
                    return None
                self.hashes[questions_key] = self.hashes.pop(staging_key)
                return 1
            lock_key = cast(str, arguments[2])
            token = cast(str, arguments[3])
            if self.strings.get(lock_key) != token:
                return 0
            del self.strings[lock_key]
            return 1
        raise AssertionError(f"Unsupported Redis command {name}.")


@contextmanager
def redis_client(server: MockUpstash) -> Iterator[cq.RedisRestClient]:
    with httpx.Client(transport=httpx.MockTransport(server.handle)) as http_client:
        settings = cq.Settings("https://example.upstash.io", "test-token")
        yield cq.RedisRestClient(settings, http_client)


def test_validation_parses_payload_and_preserves_unknown_fields() -> None:
    dataset = cq.validate_legacy_json(json.dumps(sample_records()))

    stored = json.loads(dataset.questions[0].canonical_json)
    assert isinstance(stored["question_payload"], dict)
    assert stored["unknown_top_level_field"] == ["preserved"]
    assert stored["question_payload"]["unknown_payload_field"] == {"preserved": True}
    assert len(dataset.all_ids) == 3
    assert dataset.index_members[f"{cq.INDEX_PREFIX}:topic:array"] == (
        frozenset(QUESTION_IDS[:2])
    )
    assert dataset.index_members[f"{cq.INDEX_PREFIX}:topic:graph"] == frozenset(
        {QUESTION_IDS[2]}
    )
    assert f"{cq.INDEX_PREFIX}:topic:binary_search" not in dataset.index_members
    assert not any(":subtopic:" in key for key in dataset.index_members)


def test_validation_writes_canonical_topic_to_document_and_payload() -> None:
    dataset = cq.validate_legacy_json(
        json.dumps([make_record(QUESTION_IDS[0], topic="Mathematics")])
    )

    stored = json.loads(dataset.questions[0].canonical_json)
    assert stored["topic"] == "math"
    assert stored["question_payload"]["topic"] == "math"
    assert stored["subtopic"] == "Binary Search"


def test_unicode_normalization_and_duplicate_titles_share_an_index() -> None:
    dataset = cq.validate_legacy_json(json.dumps(sample_records()))
    normalized_title = cq.normalize_index_value("  café\tsearch ")
    title_key = f"{cq.INDEX_PREFIX}:title:{normalized_title}"

    assert cq.normalize_index_value("ＣＡＦÉ   SEARCH") == normalized_title
    assert dataset.index_members[title_key] == frozenset(QUESTION_IDS[:2])


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Binary Array", "binary_array"),
        ("Binary-Array", "binary_array"),
        ("  Binary\tArray  ", "binary_array"),
    ],
)
def test_index_values_use_underscores(value: str, expected: str) -> None:
    assert cq.normalize_index_value(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Mathematics", "math"),
        ("DFS", "graph"),
        ("Breadth-First Search", "graph"),
        ("Hash Table", "hashing"),
        ("String Manipulation", "string"),
        ("SQL", "database"),
        ("Arrays", "array"),
    ],
)
def test_topic_values_consolidate_equivalent_names(value: str, expected: str) -> None:
    assert cq.normalize_topic_value(value) == expected


def test_unknown_topic_is_rejected() -> None:
    with pytest.raises(cq.DataValidationError, match="Unsupported"):
        cq.normalize_topic_value("Unreviewed Topic")


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda records: records.append(records[0].copy()),
            "Duplicate question ID",
        ),
        (
            lambda records: records[0].update({"id": "not-a-uuid"}),
            "valid UUID",
        ),
        (
            lambda records: records[0].update({"difficulty": 2}),
            "difficulty must be a string",
        ),
        (
            lambda records: records[0].update({"difficulty": "Expert"}),
            "difficulty must be Easy",
        ),
        (
            lambda records: records[0].update({"question_payload": "{"}),
            "malformed JSON",
        ),
    ],
)
def test_validation_rejects_invalid_records(
    mutate: Callable[[list[dict[str, object]]], None], message: str
) -> None:
    records = sample_records()
    mutate(records)

    with pytest.raises(cq.DataValidationError, match=message):
        cq.validate_legacy_json(json.dumps(records))


def test_validation_rejects_metadata_mismatch() -> None:
    records = sample_records()
    payload = json.loads(cast(str, records[0]["question_payload"]))
    payload["topic"] = "Different"
    records[0]["question_payload"] = json.dumps(payload)

    with pytest.raises(cq.DataValidationError, match="does not match"):
        cq.validate_legacy_json(json.dumps(records))


def test_dry_run_performs_no_writes() -> None:
    legacy_json = json.dumps(sample_records())
    server = MockUpstash(legacy_json)

    with redis_client(server) as redis:
        summary = cq.migrate(redis, apply=False)

    assert summary["mode"] == "validation-only"
    assert server.strings[cq.QUESTIONS_KEY] == legacy_json
    assert [command[0] for command in server.commands] == ["TYPE", "GET"]


def test_migration_get_queries_pagination_duplicate_title_and_random() -> None:
    legacy_json = json.dumps(sample_records())
    server = MockUpstash(legacy_json)
    server.sets[f"{cq.INDEX_PREFIX}:subtopic:binary%20search"] = {QUESTION_IDS[0]}
    server.sets[f"{cq.INDEX_PREFIX}:v1:old:topic:array"] = {QUESTION_IDS[0]}
    server.strings[f"{cq.INDEX_PREFIX}:active"] = "old"

    with redis_client(server) as redis:
        summary = cq.migrate(redis, apply=True)

        server.commands.clear()
        question = cq.get_question(redis, QUESTION_IDS[0])
        assert sum(command[0] == "HGET" for command in server.commands) == 1

        filtered = cq.query_questions(
            redis,
            {"company": "ACME", "topic": "array", "difficulty": "Medium"},
            offset=1,
            limit=1,
        )
        duplicate_title = cq.query_questions(
            redis, {"title": " café search "}, offset=0, limit=20
        )
        random_result = cq.random_questions(redis, {"company": "Acme"}, count=10)

    assert summary["hash_key"] == cq.QUESTIONS_KEY
    assert server.strings[cq.LEGACY_KEY] == legacy_json
    assert cq.QUESTIONS_KEY not in server.strings
    assert len(server.hashes[cq.QUESTIONS_KEY]) == 3
    assert f"{cq.INDEX_PREFIX}:topic:array" in server.sets
    assert f"{cq.INDEX_PREFIX}:topic:graph" in server.sets
    assert f"{cq.INDEX_PREFIX}:topic:binary_search" not in server.sets
    assert not any(":subtopic:" in key for key in server.sets)
    assert not any("%20" in key for key in server.sets)
    assert not any("-" in key for key in server.sets)
    assert not any(key.startswith(f"{cq.INDEX_PREFIX}:v1:") for key in server.sets)
    assert f"{cq.INDEX_PREFIX}:active" not in server.strings
    assert question["id"] == QUESTION_IDS[0]
    assert [item["id"] for item in filtered] == [QUESTION_IDS[1]]
    assert [item["id"] for item in duplicate_title] == list(QUESTION_IDS[:2])
    assert {item["id"] for item in random_result} == set(QUESTION_IDS[:2])
    assert len({item["id"] for item in random_result}) == len(random_result)
    assert any(command[0] == "SINTER" for command in server.commands)


def test_failed_write_preserves_source_string_and_releases_owned_lock() -> None:
    legacy_json = json.dumps(sample_records())
    server = MockUpstash(legacy_json)
    server.fail_command = "HSET"

    with (
        redis_client(server) as redis,
        pytest.raises(cq.UpstashError, match="injected failure"),
    ):
        cq.migrate(redis, apply=True)

    assert server.strings[cq.QUESTIONS_KEY] == legacy_json
    assert cq.LOCK_KEY not in server.strings


def test_failed_verification_preserves_source_string() -> None:
    legacy_json = json.dumps(sample_records())
    server = MockUpstash(legacy_json)
    server.scards_are_wrong = True

    with (
        redis_client(server) as redis,
        pytest.raises(cq.DataValidationError, match="count verification failed"),
    ):
        cq.migrate(redis, apply=True)

    assert server.strings[cq.QUESTIONS_KEY] == legacy_json


def test_failed_promotion_preserves_source_string() -> None:
    legacy_json = json.dumps(sample_records())
    server = MockUpstash(legacy_json)
    server.fail_command = "EVAL"

    with (
        redis_client(server) as redis,
        pytest.raises(cq.UpstashError, match="injected failure"),
    ):
        cq.migrate(redis, apply=True)

    assert server.strings[cq.QUESTIONS_KEY] == legacy_json
    assert cq.LOCK_KEY not in server.strings


def test_identical_migration_is_idempotent() -> None:
    server = MockUpstash(json.dumps(sample_records()))

    with redis_client(server) as redis:
        first = cq.migrate(redis, apply=True)
        first_sets = {key: value.copy() for key, value in server.sets.items()}
        second = cq.migrate(redis, apply=True)

    assert first == second
    assert server.sets == first_sets
    assert len(server.hashes[cq.QUESTIONS_KEY]) == 3
    assert cq.STAGING_KEY not in server.hashes


def test_dry_run_after_promotion_reads_backup_without_writes() -> None:
    server = MockUpstash(json.dumps(sample_records()))

    with redis_client(server) as redis:
        applied = cq.migrate(redis, apply=True)
        server.commands.clear()
        validation = cq.migrate(redis, apply=False)

    assert validation["source_sha256"] == applied["source_sha256"]
    assert [command[0] for command in server.commands] == [
        "TYPE",
        "TYPE",
        "GET",
    ]


def test_lock_is_token_owned() -> None:
    server = MockUpstash(json.dumps(sample_records()))
    server.strings[cq.LOCK_KEY] = "owner-token"

    with redis_client(server) as redis:
        cq._release_lock(redis, "different-token")
        assert server.strings[cq.LOCK_KEY] == "owner-token"
        with pytest.raises(cq.UpstashError, match="migration is running"):
            cq._acquire_lock(redis, "new-token")


def test_get_missing_question_fails() -> None:
    server = MockUpstash(json.dumps(sample_records()))

    with redis_client(server) as redis:
        cq.migrate(redis, apply=True)
        with pytest.raises(cq.NotFoundError, match="was not found"):
            cq.get_question(redis, "00000000-0000-0000-0000-000000000099")


def test_index_audit_applies_and_verifies_topic_aliases() -> None:
    records = [
        make_record(
            QUESTION_IDS[0],
            topic="Math",
            subtopic="Abbreviation Generation",
        ),
        make_record(
            QUESTION_IDS[1],
            topic="Mathematics",
            subtopic="Abbreviation",
        ),
    ]
    server = MockUpstash(json.dumps(records))

    with redis_client(server) as redis:
        result = audit.run_audit(redis, apply=True)

    before = cast(dict[str, object], result["before"])
    after = cast(dict[str, object], result["after"])
    aliases = cast(dict[str, list[str]], before["topic_aliases"])
    assert "mathematics" in aliases["math"]
    assert "numbers" in aliases["math"]
    assert after["is_clean"] is True
    assert after["document_mismatch_count"] == 0
    assert after["canonical_topic_count"] == 1
    assert after["canonical_topics"] == ["math"]
    assert f"{cq.INDEX_PREFIX}:topic:math" in server.sets
    stored = json.loads(server.hashes[cq.QUESTIONS_KEY][QUESTION_IDS[1]])
    assert stored["topic"] == "math"
    assert stored["question_payload"]["topic"] == "math"
