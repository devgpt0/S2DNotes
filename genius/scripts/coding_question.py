from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Never, Self
from urllib.parse import quote, urlparse, urlunparse
from uuid import UUID

import httpx
from dotenv import load_dotenv

QUESTIONS_KEY = "coding_questions"
LEGACY_KEY = "coding_questions:legacy"
STAGING_KEY = "coding_questions:migration"
INDEX_PREFIX = "coding_questions:index"
LOCK_KEY = "coding_questions:migration:lock"
INDEX_FIELDS = ("company", "topic", "subtopic", "difficulty", "status", "title")
DIFFICULTIES = frozenset({"Easy", "Medium", "Hard"})
MAX_RESULT_COUNT = 1_000
PIPELINE_COMMAND_LIMIT = 100
PIPELINE_BYTE_LIMIT = 512_000
HASH_FIELDS_PER_COMMAND = 20
SET_MEMBERS_PER_COMMAND = 250
LOCK_TTL_SECONDS = 1_800
RELEASE_LOCK_SCRIPT = (
    "if redis.call('get', KEYS[1]) == ARGV[1] then "
    "return redis.call('del', KEYS[1]) else return 0 end"
)
PROMOTE_SCRIPT = (
    "local function key_type(key) local value = redis.call('type', key); "
    "if type(value) == 'table' then return value.ok; end; return value; end; "
    "local questions_type = key_type(KEYS[1]); "
    "local legacy_type = key_type(KEYS[2]); "
    "if key_type(KEYS[3]) ~= 'hash' then "
    "return redis.error_reply('migration key must be a hash'); end; "
    "if questions_type == 'string' then "
    "if legacy_type ~= 'none' then "
    "return redis.error_reply('legacy backup already exists'); end; "
    "redis.call('rename', KEYS[1], KEYS[2]); "
    "elseif questions_type == 'hash' then "
    "if legacy_type ~= 'string' then "
    "return redis.error_reply('legacy backup must be a string'); end; "
    "else return redis.error_reply('coding_questions must be a string or hash'); end; "
    "redis.call('rename', KEYS[3], KEYS[1]); return 1"
)

type JsonObject = dict[str, object]
type RedisArgument = str | int
type RedisCommand = list[RedisArgument]


class CodingQuestionError(Exception):
    """Base error for expected CLI failures."""


class ConfigurationError(CodingQuestionError):
    """Raised when Redis configuration is missing or invalid."""


class DataValidationError(CodingQuestionError):
    """Raised when coding-question data violates its schema."""


class UpstashError(CodingQuestionError):
    """Raised when Upstash rejects a command or returns invalid data."""


class NotFoundError(CodingQuestionError):
    """Raised when a requested question does not exist."""


@dataclass(frozen=True, slots=True)
class Settings:
    redis_url: str
    redis_token: str

    @classmethod
    def from_environment(cls) -> Settings:
        load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
        redis_url = os.environ.get("UPSTASH_REDIS_REST_URL")
        redis_token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
        if not redis_url or not redis_token:
            raise ConfigurationError(
                "UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN are both "
                "required in genius/.env or the process environment."
            )
        if redis_url != redis_url.strip() or redis_token != redis_token.strip():
            raise ConfigurationError(
                "Redis credentials contain surrounding whitespace."
            )

        parsed = urlparse(redis_url)
        try:
            port = parsed.port
        except ValueError as exc:
            raise ConfigurationError(
                "UPSTASH_REDIS_REST_URL has an invalid port."
            ) from exc
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.params
            or parsed.query
            or parsed.fragment
            or port is not None
            and (port < 1 or port > 65_535)
        ):
            raise ConfigurationError(
                "UPSTASH_REDIS_REST_URL must be an HTTPS URL without credentials, "
                "parameters, a query, or a fragment."
            )
        normalized_url = urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", "")
        )
        return cls(normalized_url, redis_token)


class RedisRestClient:
    def __init__(self, settings: Settings, client: httpx.Client | None = None) -> None:
        self._url = settings.redis_url
        self._headers = {"Authorization": f"Bearer {settings.redis_token}"}
        self._client = client or httpx.Client(timeout=60.0)
        self._owns_client = client is None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._owns_client:
            self._client.close()

    def execute(self, command: RedisCommand) -> object:
        payload = self._response_json(self._post(self._url, command))
        if not isinstance(payload, dict):
            raise UpstashError("Upstash returned an invalid command response.")
        return self._result(payload)

    def pipeline(self, commands: Sequence[RedisCommand]) -> list[object]:
        if not commands:
            return []
        payload = self._response_json(
            self._post(f"{self._url}/pipeline", list(commands))
        )
        if not isinstance(payload, list) or len(payload) != len(commands):
            raise UpstashError("Upstash returned an invalid pipeline response.")
        results: list[object] = []
        for item in payload:
            if not isinstance(item, dict):
                raise UpstashError("Upstash returned an invalid pipeline item.")
            results.append(self._result(item))
        return results

    def _post(self, url: str, payload: object) -> httpx.Response:
        try:
            response = self._client.post(url, headers=self._headers, json=payload)
        except httpx.RequestError as exc:
            raise UpstashError(
                f"Upstash request failed with {type(exc).__name__}."
            ) from exc
        if response.status_code < 200 or response.status_code >= 300:
            raise UpstashError(f"Upstash returned HTTP {response.status_code}.")
        return response

    @staticmethod
    def _response_json(response: httpx.Response) -> object:
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise UpstashError("Upstash returned non-JSON data.") from exc

    @staticmethod
    def _result(payload: Mapping[str, object]) -> object:
        error = payload.get("error")
        if error is not None:
            if not isinstance(error, str):
                raise UpstashError("Upstash returned an invalid error response.")
            raise UpstashError(f"Upstash command failed: {error}")
        if "result" not in payload:
            raise UpstashError("Upstash response is missing its result.")
        return payload["result"]


@dataclass(frozen=True, slots=True)
class Question:
    question_id: str
    canonical_json: str


@dataclass(frozen=True, slots=True)
class Dataset:
    source_sha256: str
    questions: tuple[Question, ...]
    all_ids: frozenset[str]
    index_members: Mapping[str, frozenset[str]]


def _reject_json_constant(value: str) -> Never:
    raise DataValidationError(f"JSON contains invalid constant {value}.")


def _parse_json(value: str, label: str) -> object:
    def unique_object(pairs: list[tuple[str, object]]) -> JsonObject:
        result: JsonObject = {}
        for key, item in pairs:
            if key in result:
                raise DataValidationError(f"{label} contains duplicate key {key!r}.")
            result[key] = item
        return result

    try:
        return json.loads(
            value,
            object_pairs_hook=unique_object,
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as exc:
        raise DataValidationError(f"{label} is malformed JSON: {exc.msg}.") from exc


def _required_string(
    value: Mapping[str, object],
    key: str,
    label: str,
    *,
    allow_empty: bool = False,
) -> str:
    item = value.get(key)
    if not isinstance(item, str):
        raise DataValidationError(f"{label}.{key} must be a string.")
    if not allow_empty and not item:
        raise DataValidationError(f"{label}.{key} must not be empty.")
    return item


def _validate_string_list(value: Mapping[str, object], key: str, label: str) -> None:
    items = value.get(key)
    if not isinstance(items, list):
        raise DataValidationError(f"{label}.{key} must be an array.")
    if any(not isinstance(item, str) for item in items):
        raise DataValidationError(f"Every item in {label}.{key} must be a string.")


def _validate_payload(payload: JsonObject, label: str) -> None:
    for key in ("tags", "hints", "constraints"):
        _validate_string_list(payload, key, label)
    for key in (
        "title",
        "topic",
        "company",
        "subtopic",
        "difficulty",
        "description",
        "input_format",
        "output_format",
    ):
        _required_string(payload, key, label, allow_empty=key != "title")

    examples = payload.get("examples")
    if not isinstance(examples, list):
        raise DataValidationError(f"{label}.examples must be an array.")
    for index, example in enumerate(examples):
        example_label = f"{label}.examples[{index}]"
        if not isinstance(example, dict):
            raise DataValidationError(f"{example_label} must be an object.")
        if "input" not in example or "output" not in example:
            raise DataValidationError(
                f"{example_label} must contain input and output fields."
            )
        _required_string(example, "explanation", example_label, allow_empty=True)

    if _required_string(payload, "difficulty", label) not in DIFFICULTIES:
        raise DataValidationError(f"{label}.difficulty must be Easy, Medium, or Hard.")


def _canonical_uuid(value: str, label: str) -> str:
    try:
        parsed = UUID(value)
    except ValueError as exc:
        raise DataValidationError(f"{label} must be a valid UUID.") from exc
    canonical = str(parsed)
    if canonical != value:
        raise DataValidationError(f"{label} must use canonical lowercase UUID format.")
    return canonical


def normalize_index_value(value: str) -> str:
    normalized = " ".join(unicodedata.normalize("NFKC", value).split()).lower()
    if not normalized:
        raise DataValidationError("Index values must not be empty or whitespace-only.")
    return quote(normalized, safe="")


def validate_legacy_json(raw_json: str) -> Dataset:
    parsed = _parse_json(raw_json, QUESTIONS_KEY)
    if not isinstance(parsed, list):
        raise DataValidationError(f"{QUESTIONS_KEY} must contain a JSON array.")

    questions: list[Question] = []
    all_ids: set[str] = set()
    indexes: dict[str, set[str]] = {}
    for record_index, item in enumerate(parsed):
        label = f"{QUESTIONS_KEY}[{record_index}]"
        if not isinstance(item, dict):
            raise DataValidationError(f"{label} must be an object.")

        question_id = _canonical_uuid(
            _required_string(item, "id", label), f"{label}.id"
        )
        if question_id in all_ids:
            raise DataValidationError(f"Duplicate question ID {question_id}.")
        company = _required_string(item, "company_name", label)
        topic = _required_string(item, "topic", label)
        subtopic = _required_string(item, "subtopic", label)
        difficulty = _required_string(item, "difficulty", label)
        status = _required_string(item, "status", label)
        if difficulty not in DIFFICULTIES:
            raise DataValidationError(
                f"{label}.difficulty must be Easy, Medium, or Hard."
            )

        payload_value = _parse_json(
            _required_string(item, "question_payload", label),
            f"{label}.question_payload",
        )
        if not isinstance(payload_value, dict):
            raise DataValidationError(f"{label}.question_payload must be an object.")
        _validate_payload(payload_value, f"{label}.question_payload")

        metadata = (
            ("company_name", company, "company"),
            ("topic", topic, "topic"),
            ("subtopic", subtopic, "subtopic"),
            ("difficulty", difficulty, "difficulty"),
        )
        for top_key, top_value, payload_key in metadata:
            payload_value_item = _required_string(
                payload_value,
                payload_key,
                f"{label}.question_payload",
                allow_empty=True,
            )
            if top_value != payload_value_item:
                raise DataValidationError(
                    f"{label}.{top_key} does not match question_payload.{payload_key}."
                )

        title = _required_string(payload_value, "title", f"{label}.question_payload")
        stored_record = dict(item)
        stored_record["question_payload"] = payload_value
        canonical_json = json.dumps(
            stored_record,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )

        all_ids.add(question_id)
        questions.append(Question(question_id, canonical_json))
        field_values = {
            "company": company,
            "topic": topic,
            "subtopic": subtopic,
            "difficulty": difficulty,
            "status": status,
            "title": title,
        }
        for field, display_value in field_values.items():
            key = f"{INDEX_PREFIX}:{field}:{normalize_index_value(display_value)}"
            indexes.setdefault(key, set()).add(question_id)

    questions.sort(key=lambda question: question.question_id)
    return Dataset(
        source_sha256=hashlib.sha256(raw_json.encode("utf-8")).hexdigest(),
        questions=tuple(questions),
        all_ids=frozenset(all_ids),
        index_members={key: frozenset(value) for key, value in indexes.items()},
    )


def _redis_string(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise UpstashError(f"{label} did not return a string.")
    return value


def _redis_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise UpstashError(f"{label} did not return an integer.")
    return value


def _redis_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise UpstashError(f"{label} did not return an array of strings.")
    return value


def load_dataset(redis: RedisRestClient) -> Dataset:
    questions_type = redis.execute(["TYPE", QUESTIONS_KEY])
    if questions_type == "string":
        raw_json = _redis_string(redis.execute(["GET", QUESTIONS_KEY]), "GET")
    elif questions_type == "hash":
        if redis.execute(["TYPE", LEGACY_KEY]) != "string":
            raise DataValidationError(f"Rollback key {LEGACY_KEY!r} is missing.")
        raw_json = _redis_string(redis.execute(["GET", LEGACY_KEY]), "legacy GET")
    else:
        raise DataValidationError(
            f"{QUESTIONS_KEY!r} must exist as the source string or migrated hash."
        )
    return validate_legacy_json(raw_json)


def _chunks[T](values: Sequence[T], size: int) -> Iterable[Sequence[T]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _pipeline_batches(commands: Iterable[RedisCommand]) -> Iterable[list[RedisCommand]]:
    batch: list[RedisCommand] = []
    batch_bytes = 2
    for command in commands:
        command_bytes = len(
            json.dumps(command, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        if command_bytes > PIPELINE_BYTE_LIMIT:
            raise DataValidationError("A Redis command exceeds the migration limit.")
        if batch and (
            len(batch) >= PIPELINE_COMMAND_LIMIT
            or batch_bytes + command_bytes + 1 > PIPELINE_BYTE_LIMIT
        ):
            yield batch
            batch = []
            batch_bytes = 2
        batch.append(command)
        batch_bytes += command_bytes + 1
    if batch:
        yield batch


def _run_pipeline(
    redis: RedisRestClient, commands: Iterable[RedisCommand]
) -> list[object]:
    results: list[object] = []
    for batch in _pipeline_batches(commands):
        results.extend(redis.pipeline(batch))
    return results


def _write_commands(dataset: Dataset) -> Iterable[RedisCommand]:
    for question_chunk in _chunks(dataset.questions, HASH_FIELDS_PER_COMMAND):
        command: RedisCommand = ["HSET", STAGING_KEY]
        for question in question_chunk:
            command.extend((question.question_id, question.canonical_json))
        yield command

    for member_chunk in _chunks(sorted(dataset.all_ids), SET_MEMBERS_PER_COMMAND):
        yield ["SADD", f"{INDEX_PREFIX}:all", *member_chunk]
    for index_key in sorted(dataset.index_members):
        members = sorted(dataset.index_members[index_key])
        for member_chunk in _chunks(members, SET_MEMBERS_PER_COMMAND):
            yield ["SADD", index_key, *member_chunk]


def _verify_hash(redis: RedisRestClient, dataset: Dataset, key: str) -> None:
    expected_count = len(dataset.questions)
    if _redis_int(redis.execute(["HLEN", key]), "HLEN") != expected_count:
        raise DataValidationError(f"Hash count verification failed for {key!r}.")
    stored_ids = set(_redis_strings(redis.execute(["HKEYS", key]), "HKEYS"))
    if stored_ids != dataset.all_ids:
        raise DataValidationError(f"Hash key verification failed for {key!r}.")

    sample_positions = sorted({0, expected_count // 2, expected_count - 1})
    samples = [dataset.questions[position] for position in sample_positions]
    results = redis.pipeline(
        [["HGET", key, question.question_id] for question in samples]
    )
    for question, result in zip(samples, results, strict=True):
        if result != question.canonical_json:
            raise DataValidationError(
                f"Stored question verification failed for {question.question_id}."
            )


def _verify_indexes(redis: RedisRestClient, dataset: Dataset) -> None:
    all_key = f"{INDEX_PREFIX}:all"
    if _redis_int(redis.execute(["SCARD", all_key]), "SCARD") != len(dataset.all_ids):
        raise DataValidationError("All-ID index count verification failed.")
    stored_ids = set(_redis_strings(redis.execute(["SMEMBERS", all_key]), "SMEMBERS"))
    if stored_ids != dataset.all_ids:
        raise DataValidationError("All-ID index membership verification failed.")

    keys = sorted(dataset.index_members)
    results = _run_pipeline(redis, (["SCARD", key] for key in keys))
    for key, result in zip(keys, results, strict=True):
        if _redis_int(result, "SCARD") != len(dataset.index_members[key]):
            raise DataValidationError(f"Index count verification failed for {key!r}.")


def _acquire_lock(redis: RedisRestClient, token: str) -> None:
    result = redis.execute(["SET", LOCK_KEY, token, "NX", "EX", LOCK_TTL_SECONDS])
    if result != "OK":
        raise UpstashError("Another coding-question migration is running.")


def _release_lock(redis: RedisRestClient, token: str) -> None:
    result = redis.execute(["EVAL", RELEASE_LOCK_SCRIPT, 1, LOCK_KEY, token])
    if _redis_int(result, "migration lock release") not in (0, 1):
        raise UpstashError("Migration lock release returned an invalid result.")


def _promote(redis: RedisRestClient) -> None:
    questions_type = redis.execute(["TYPE", QUESTIONS_KEY])
    legacy_type = redis.execute(["TYPE", LEGACY_KEY])
    if questions_type == "string" and legacy_type != "none":
        raise DataValidationError(
            "The legacy backup already exists; refusing promotion."
        )
    if questions_type == "hash" and legacy_type != "string":
        raise DataValidationError("The migrated hash is missing its legacy backup.")
    result = redis.execute(
        ["EVAL", PROMOTE_SCRIPT, 3, QUESTIONS_KEY, LEGACY_KEY, STAGING_KEY]
    )
    if _redis_int(result, "migration promotion") != 1:
        raise UpstashError("Migration promotion returned an invalid result.")


def migration_summary(dataset: Dataset, mode: str) -> JsonObject:
    return {
        "mode": mode,
        "record_count": len(dataset.questions),
        "source_sha256": dataset.source_sha256,
        "hash_key": QUESTIONS_KEY,
        "legacy_backup_key": LEGACY_KEY,
        "index_key_count": len(dataset.index_members) + 1,
    }


def migrate(redis: RedisRestClient, *, apply: bool) -> JsonObject:
    if not apply:
        return migration_summary(load_dataset(redis), "validation-only")

    token = secrets.token_urlsafe(32)
    _acquire_lock(redis, token)
    try:
        dataset = load_dataset(redis)
        _redis_int(redis.execute(["DEL", STAGING_KEY]), "DEL")
        for result in _run_pipeline(redis, _write_commands(dataset)):
            _redis_int(result, "migration write")
        _verify_hash(redis, dataset, STAGING_KEY)
        _verify_indexes(redis, dataset)
        _promote(redis)
        _verify_hash(redis, dataset, QUESTIONS_KEY)
        return migration_summary(dataset, "applied")
    finally:
        _release_lock(redis, token)


def _parse_question(value: object, question_id: str) -> JsonObject:
    if not isinstance(value, str):
        raise DataValidationError(f"Stored question {question_id} is not JSON text.")
    parsed = _parse_json(value, f"stored question {question_id}")
    if not isinstance(parsed, dict):
        raise DataValidationError(f"Stored question {question_id} is not an object.")
    return parsed


def get_question(redis: RedisRestClient, question_id: str) -> JsonObject:
    canonical_id = _canonical_uuid(question_id, "id")
    result = redis.execute(["HGET", QUESTIONS_KEY, canonical_id])
    if result is None:
        raise NotFoundError(f"Question {canonical_id} was not found.")
    return _parse_question(result, canonical_id)


def _matching_ids(redis: RedisRestClient, filters: Mapping[str, str]) -> list[str]:
    unknown = set(filters) - set(INDEX_FIELDS)
    if unknown:
        raise DataValidationError(f"Unsupported filters: {', '.join(sorted(unknown))}.")
    keys = [
        f"{INDEX_PREFIX}:{field}:{normalize_index_value(value)}"
        for field, value in filters.items()
    ]
    if not keys:
        result = redis.execute(["SMEMBERS", f"{INDEX_PREFIX}:all"])
    elif len(keys) == 1:
        result = redis.execute(["SMEMBERS", keys[0]])
    else:
        result = redis.execute(["SINTER", *keys])
    ids = _redis_strings(result, "question index query")
    for question_id in ids:
        _canonical_uuid(question_id, "indexed question ID")
    return sorted(ids)


def _fetch_questions(
    redis: RedisRestClient, question_ids: Sequence[str]
) -> list[JsonObject]:
    results = _run_pipeline(
        redis, (["HGET", QUESTIONS_KEY, question_id] for question_id in question_ids)
    )
    questions: list[JsonObject] = []
    for question_id, result in zip(question_ids, results, strict=True):
        if result is None:
            raise DataValidationError(
                f"Index references missing question {question_id}."
            )
        questions.append(_parse_question(result, question_id))
    return questions


def query_questions(
    redis: RedisRestClient,
    filters: Mapping[str, str],
    *,
    offset: int,
    limit: int,
) -> list[JsonObject]:
    ids = _matching_ids(redis, filters)
    return _fetch_questions(redis, ids[offset : offset + limit])


def random_questions(
    redis: RedisRestClient, filters: Mapping[str, str], *, count: int
) -> list[JsonObject]:
    ids = _matching_ids(redis, filters)
    selected = secrets.SystemRandom().sample(ids, k=min(count, len(ids)))
    return _fetch_questions(redis, selected)


def _non_negative_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be at least 0")
    return parsed


def _positive_bounded_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1 or parsed > MAX_RESULT_COUNT:
        raise argparse.ArgumentTypeError(f"must be between 1 and {MAX_RESULT_COUNT}")
    return parsed


def _add_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--company")
    parser.add_argument("--topic")
    parser.add_argument("--subtopic")
    parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES))
    parser.add_argument("--status")
    parser.add_argument("--title")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Migrate and query coding questions.")
    commands = parser.add_subparsers(dest="command", required=True)

    migrate_parser = commands.add_parser("migrate")
    migrate_parser.add_argument(
        "--apply", action="store_true", help="Apply the string-to-hash migration."
    )

    get_parser = commands.add_parser("get")
    get_parser.add_argument("--id", required=True)

    query_parser = commands.add_parser("query")
    _add_filters(query_parser)
    query_parser.add_argument("--offset", type=_non_negative_integer, default=0)
    query_parser.add_argument("--limit", type=_positive_bounded_integer, default=20)

    random_parser = commands.add_parser("random")
    _add_filters(random_parser)
    random_parser.add_argument("--count", type=_positive_bounded_integer, default=1)

    list_parser = commands.add_parser("list")
    list_parser.add_argument("--offset", type=_non_negative_integer, default=0)
    list_parser.add_argument("--limit", type=_positive_bounded_integer, default=100)
    return parser


def _filters(arguments: argparse.Namespace) -> dict[str, str]:
    return {
        field: value
        for field in INDEX_FIELDS
        if (value := getattr(arguments, field, None)) is not None
    }


def _write_json(value: object) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))
    sys.stdout.write("\n")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        with RedisRestClient(Settings.from_environment()) as redis:
            if arguments.command == "migrate":
                result: object = migrate(redis, apply=arguments.apply)
            elif arguments.command == "get":
                result = get_question(redis, arguments.id)
            elif arguments.command == "query":
                result = query_questions(
                    redis,
                    _filters(arguments),
                    offset=arguments.offset,
                    limit=arguments.limit,
                )
            elif arguments.command == "random":
                result = random_questions(
                    redis, _filters(arguments), count=arguments.count
                )
            elif arguments.command == "list":
                result = query_questions(
                    redis, {}, offset=arguments.offset, limit=arguments.limit
                )
            else:
                raise AssertionError(f"Unhandled command {arguments.command!r}.")
        _write_json(result)
        return 0
    except CodingQuestionError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
