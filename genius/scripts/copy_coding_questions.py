from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Self
from urllib.parse import urlparse, urlunparse

import httpx
from dotenv import load_dotenv

KEY_PATTERN = "coding_questions*"
SUPPORTED_TYPES = frozenset({"string", "hash", "set"})
STAGING_NAMESPACE = "__coding_questions_copy__"
LOCK_KEY = "__coding_questions_copy_lock__"
LOCK_TTL_SECONDS = 3_600
PIPELINE_COMMAND_LIMIT = 100
PIPELINE_BYTE_LIMIT = 512_000
STRING_CHUNK_CHARACTERS = 64_000
HASH_FIELDS_PER_COMMAND = 20
SET_MEMBERS_PER_COMMAND = 250
SCAN_COUNT = 1_000
RELEASE_LOCK_SCRIPT = (
    "if redis.call('get', KEYS[1]) == ARGV[1] then "
    "return redis.call('del', KEYS[1]) else return 0 end"
)

type RedisArgument = str | int
type RedisCommand = list[RedisArgument]
type StoredValue = str | dict[str, str] | frozenset[str]


class CopyError(Exception):
    """Base error for expected copy failures."""


class ConfigurationError(CopyError):
    """Raised when source or destination configuration is invalid."""


class RedisError(CopyError):
    """Raised when a Redis REST request fails."""


class DataError(CopyError):
    """Raised when source or staged data is invalid."""


@dataclass(frozen=True, slots=True)
class Endpoint:
    url: str
    token: str


@dataclass(frozen=True, slots=True)
class CopySettings:
    source: Endpoint
    destination: Endpoint

    @classmethod
    def from_environment(cls) -> CopySettings:
        load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
        source = _load_endpoint("SRC")
        destination = _load_endpoint("DST")
        if source.url == destination.url:
            raise ConfigurationError(
                "Source and destination Redis URLs must be different."
            )
        return cls(source=source, destination=destination)


@dataclass(frozen=True, slots=True)
class KeyInfo:
    key: str
    redis_type: str
    ttl_ms: int


@dataclass(frozen=True, slots=True)
class Snapshot:
    info: KeyInfo
    value: StoredValue


def _load_endpoint(suffix: str) -> Endpoint:
    url_name = f"UPSTASH_REDIS_REST_URL_{suffix}"
    token_name = f"UPSTASH_REDIS_REST_TOKEN_{suffix}"
    url = os.environ.get(url_name)
    token = os.environ.get(token_name)
    if not url or not token:
        raise ConfigurationError(
            f"{url_name} and {token_name} are both required in genius/.env or "
            "the process environment."
        )
    if url != url.strip() or token != token.strip():
        raise ConfigurationError(
            f"{url_name} and {token_name} must not contain surrounding whitespace."
        )

    parsed = urlparse(url)
    try:
        port = parsed.port
    except ValueError as exc:
        raise ConfigurationError(f"{url_name} has an invalid port.") from exc
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
            f"{url_name} must be an HTTPS URL without credentials, parameters, "
            "a query, or a fragment."
        )
    normalized_url = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", "")
    )
    return Endpoint(normalized_url, token)


class RedisRestClient:
    def __init__(self, endpoint: Endpoint, client: httpx.Client | None = None) -> None:
        self._url = endpoint.url
        self._headers = {"Authorization": f"Bearer {endpoint.token}"}
        self._client = client or httpx.Client(timeout=120.0)
        self._owns_client = client is None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._owns_client:
            self._client.close()

    def execute(self, command: RedisCommand) -> object:
        payload = self._response_json(self._post(self._url, command))
        if not isinstance(payload, dict):
            raise RedisError("Redis returned an invalid command response.")
        return self._result(payload)

    def pipeline(self, commands: Sequence[RedisCommand]) -> list[object]:
        if not commands:
            return []
        payload = self._response_json(
            self._post(f"{self._url}/pipeline", list(commands))
        )
        if not isinstance(payload, list) or len(payload) != len(commands):
            raise RedisError("Redis returned an invalid pipeline response.")
        results: list[object] = []
        for item in payload:
            if not isinstance(item, dict):
                raise RedisError("Redis returned an invalid pipeline item.")
            results.append(self._result(item))
        return results

    def _post(self, url: str, payload: object) -> httpx.Response:
        try:
            response = self._client.post(url, headers=self._headers, json=payload)
        except httpx.RequestError as exc:
            raise RedisError(
                f"Redis request failed with {type(exc).__name__}."
            ) from exc
        if response.status_code < 200 or response.status_code >= 300:
            raise RedisError(f"Redis returned HTTP {response.status_code}.")
        return response

    @staticmethod
    def _response_json(response: httpx.Response) -> object:
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise RedisError("Redis returned non-JSON data.") from exc

    @staticmethod
    def _result(payload: Mapping[str, object]) -> object:
        error = payload.get("error")
        if error is not None:
            if not isinstance(error, str):
                raise RedisError("Redis returned an invalid error response.")
            raise RedisError(f"Redis command failed: {error}")
        if "result" not in payload:
            raise RedisError("Redis response is missing its result.")
        return payload["result"]


def _redis_string(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise DataError(f"{label} did not return a string.")
    return value


def _redis_integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise DataError(f"{label} did not return an integer.")
    return value


def _redis_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise DataError(f"{label} did not return an array of strings.")
    return value


def _scan_result(value: object, label: str) -> tuple[str, list[str]]:
    if not isinstance(value, list) or len(value) != 2:
        raise DataError(f"{label} returned an invalid scan response.")
    cursor = value[0]
    items = value[1]
    if not isinstance(cursor, str):
        raise DataError(f"{label} returned an invalid cursor.")
    return cursor, _redis_strings(items, label)


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
            raise DataError("A generated Redis command exceeds the pipeline limit.")
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


def _scan_keys(redis: RedisRestClient) -> list[str]:
    cursor = "0"
    keys: set[str] = set()
    while True:
        cursor, items = _scan_result(
            redis.execute(["SCAN", cursor, "MATCH", KEY_PATTERN, "COUNT", SCAN_COUNT]),
            "SCAN",
        )
        keys.update(items)
        if cursor == "0":
            return sorted(keys)


def _key_infos(redis: RedisRestClient, keys: Sequence[str]) -> list[KeyInfo]:
    types = _run_pipeline(redis, (["TYPE", key] for key in keys))
    ttls = _run_pipeline(redis, (["PTTL", key] for key in keys))
    infos: list[KeyInfo] = []
    for key, redis_type_value, ttl_value in zip(keys, types, ttls, strict=True):
        redis_type = _redis_string(redis_type_value, "TYPE")
        ttl_ms = _redis_integer(ttl_value, "PTTL")
        if redis_type not in SUPPORTED_TYPES:
            raise DataError(f"Key {key!r} has unsupported Redis type {redis_type!r}.")
        if ttl_ms == -2:
            raise DataError(f"Key {key!r} disappeared while it was inspected.")
        infos.append(KeyInfo(key, redis_type, ttl_ms))
    return infos


def _read_hash(redis: RedisRestClient, key: str) -> dict[str, str]:
    cursor = "0"
    fields: dict[str, str] = {}
    while True:
        cursor, items = _scan_result(
            redis.execute(["HSCAN", key, cursor, "COUNT", SCAN_COUNT]),
            "HSCAN",
        )
        if len(items) % 2 != 0:
            raise DataError(f"HSCAN returned invalid field/value pairs for {key!r}.")
        for index in range(0, len(items), 2):
            field = items[index]
            value = items[index + 1]
            existing = fields.get(field)
            if existing is not None and existing != value:
                raise DataError(f"Hash field {field!r} changed while being copied.")
            fields[field] = value
        if cursor == "0":
            return fields


def _read_snapshots(redis: RedisRestClient, infos: Sequence[KeyInfo]) -> list[Snapshot]:
    snapshots: dict[str, Snapshot] = {}
    string_infos = [info for info in infos if info.redis_type == "string"]
    hash_infos = [info for info in infos if info.redis_type == "hash"]
    set_infos = [info for info in infos if info.redis_type == "set"]

    for info in string_infos:
        value = _redis_string(redis.execute(["GET", info.key]), "GET")
        snapshots[info.key] = Snapshot(info, value)
    for info in hash_infos:
        snapshots[info.key] = Snapshot(info, _read_hash(redis, info.key))

    set_results = _run_pipeline(redis, (["SMEMBERS", info.key] for info in set_infos))
    for info, result in zip(set_infos, set_results, strict=True):
        snapshots[info.key] = Snapshot(
            info, frozenset(_redis_strings(result, "SMEMBERS"))
        )
    return [snapshots[info.key] for info in infos]


def _chunks[T](values: Sequence[T], size: int) -> Iterable[Sequence[T]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _staging_key(run_id: str, source_key: str) -> str:
    digest = hashlib.sha256(source_key.encode("utf-8")).hexdigest()
    return f"{STAGING_NAMESPACE}:{run_id}:{digest}"


def _write_commands(
    snapshots: Sequence[Snapshot], staging_keys: Mapping[str, str]
) -> Iterable[RedisCommand]:
    for snapshot in snapshots:
        staging_key = staging_keys[snapshot.info.key]
        if snapshot.info.redis_type == "string":
            value = snapshot.value
            if not isinstance(value, str):
                raise DataError("String snapshot has an invalid value.")
            yield ["SET", staging_key, ""]
            for start in range(0, len(value), STRING_CHUNK_CHARACTERS):
                yield [
                    "APPEND",
                    staging_key,
                    value[start : start + STRING_CHUNK_CHARACTERS],
                ]
        elif snapshot.info.redis_type == "hash":
            value = snapshot.value
            if not isinstance(value, dict):
                raise DataError("Hash snapshot has an invalid value.")
            fields = sorted(value)
            for field_chunk in _chunks(fields, HASH_FIELDS_PER_COMMAND):
                command: RedisCommand = ["HSET", staging_key]
                for field in field_chunk:
                    command.extend((field, value[field]))
                yield command
        elif snapshot.info.redis_type == "set":
            value = snapshot.value
            if not isinstance(value, frozenset):
                raise DataError("Set snapshot has an invalid value.")
            members = sorted(value)
            for member_chunk in _chunks(members, SET_MEMBERS_PER_COMMAND):
                yield ["SADD", staging_key, *member_chunk]
        else:
            raise DataError(f"Unsupported snapshot type {snapshot.info.redis_type!r}.")


def _verify_staging(
    destination: RedisRestClient,
    snapshots: Sequence[Snapshot],
    staging_keys: Mapping[str, str],
) -> None:
    staging_infos = [
        KeyInfo(staging_keys[snapshot.info.key], snapshot.info.redis_type, -1)
        for snapshot in snapshots
    ]
    staged_snapshots = _read_snapshots(destination, staging_infos)
    for source, staged in zip(snapshots, staged_snapshots, strict=True):
        if (
            source.info.redis_type != staged.info.redis_type
            or source.value != staged.value
        ):
            raise DataError(f"Staged verification failed for {source.info.key!r}.")


def _apply_ttls(
    destination: RedisRestClient,
    snapshots: Sequence[Snapshot],
    staging_keys: Mapping[str, str],
) -> None:
    commands = (
        ["PEXPIRE", staging_keys[snapshot.info.key], snapshot.info.ttl_ms]
        for snapshot in snapshots
        if snapshot.info.ttl_ms >= 0
    )
    for result in _run_pipeline(destination, commands):
        if _redis_integer(result, "PEXPIRE") != 1:
            raise DataError("Destination rejected a copied key TTL.")


def _verify_destination_counts(
    destination: RedisRestClient, snapshots: Sequence[Snapshot]
) -> None:
    type_results = _run_pipeline(
        destination, (["TYPE", snapshot.info.key] for snapshot in snapshots)
    )
    size_commands: list[RedisCommand] = []
    expected_sizes: list[int] = []
    for snapshot in snapshots:
        if snapshot.info.redis_type == "string":
            value = snapshot.value
            if not isinstance(value, str):
                raise DataError("String snapshot has an invalid value.")
            size_commands.append(["STRLEN", snapshot.info.key])
            expected_sizes.append(len(value.encode("utf-8")))
        elif snapshot.info.redis_type == "hash":
            value = snapshot.value
            if not isinstance(value, dict):
                raise DataError("Hash snapshot has an invalid value.")
            size_commands.append(["HLEN", snapshot.info.key])
            expected_sizes.append(len(value))
        else:
            value = snapshot.value
            if not isinstance(value, frozenset):
                raise DataError("Set snapshot has an invalid value.")
            size_commands.append(["SCARD", snapshot.info.key])
            expected_sizes.append(len(value))
    size_results = _run_pipeline(destination, size_commands)

    for snapshot, type_result, size_result, expected_size in zip(
        snapshots, type_results, size_results, expected_sizes, strict=True
    ):
        if _redis_string(type_result, "TYPE") != snapshot.info.redis_type:
            raise DataError(
                f"Destination type verification failed for {snapshot.info.key!r}."
            )
        if _redis_integer(size_result, "size verification") != expected_size:
            raise DataError(
                f"Destination size verification failed for {snapshot.info.key!r}."
            )


def _acquire_lock(destination: RedisRestClient, token: str) -> None:
    result = destination.execute(["SET", LOCK_KEY, token, "NX", "EX", LOCK_TTL_SECONDS])
    if result != "OK":
        raise RedisError("Another coding-question copy is running.")


def _release_lock(destination: RedisRestClient, token: str) -> None:
    result = destination.execute(["EVAL", RELEASE_LOCK_SCRIPT, 1, LOCK_KEY, token])
    if _redis_integer(result, "copy lock release") not in (0, 1):
        raise RedisError("Copy lock release returned an invalid result.")


def _cleanup_staging(
    destination: RedisRestClient, staging_keys: Mapping[str, str]
) -> None:
    _run_pipeline(destination, (["DEL", key] for key in staging_keys.values()))


def _summary(
    source_infos: Sequence[KeyInfo],
    destination_keys: Sequence[str],
    mode: str,
) -> dict[str, object]:
    source_keys = {info.key for info in source_infos}
    return {
        "mode": mode,
        "source_key_count": len(source_infos),
        "source_types": dict(
            sorted(Counter(info.redis_type for info in source_infos).items())
        ),
        "destination_existing_key_count": len(destination_keys),
        "destination_extra_key_count": len(set(destination_keys) - source_keys),
        "copied_key_count": len(source_infos) if mode == "applied" else 0,
    }


def copy_coding_questions(
    source: RedisRestClient,
    destination: RedisRestClient,
    *,
    apply: bool,
) -> dict[str, object]:
    source_keys = _scan_keys(source)
    if not source_keys:
        raise DataError(f"Source has no keys matching {KEY_PATTERN!r}.")
    source_infos = _key_infos(source, source_keys)
    destination_keys = _scan_keys(destination)
    if not apply:
        return _summary(source_infos, destination_keys, "validation-only")

    lock_token = secrets.token_urlsafe(32)
    run_id = secrets.token_hex(16)
    staging_keys = {info.key: _staging_key(run_id, info.key) for info in source_infos}
    _acquire_lock(destination, lock_token)
    try:
        snapshots = _read_snapshots(source, source_infos)
        write_results = _run_pipeline(
            destination, _write_commands(snapshots, staging_keys)
        )
        for result in write_results:
            if not isinstance(result, (int, str)) or isinstance(result, bool):
                raise DataError("Destination returned an invalid write result.")
        _verify_staging(destination, snapshots, staging_keys)
        _apply_ttls(destination, snapshots, staging_keys)

        rename_results = _run_pipeline(
            destination,
            (
                ["RENAME", staging_keys[snapshot.info.key], snapshot.info.key]
                for snapshot in snapshots
            ),
        )
        if any(result != "OK" for result in rename_results):
            raise RedisError("Destination did not acknowledge every key promotion.")
        _verify_destination_counts(destination, snapshots)
        return _summary(source_infos, destination_keys, "applied")
    finally:
        try:
            _cleanup_staging(destination, staging_keys)
        finally:
            _release_lock(destination, lock_token)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Copy every coding_questions* key between Upstash databases."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Stage, verify, and copy matching keys to the destination.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        settings = CopySettings.from_environment()
        with (
            RedisRestClient(settings.source) as source,
            RedisRestClient(settings.destination) as destination,
        ):
            result = copy_coding_questions(source, destination, apply=arguments.apply)
        sys.stdout.write(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
        )
        sys.stdout.write("\n")
        return 0
    except CopyError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
