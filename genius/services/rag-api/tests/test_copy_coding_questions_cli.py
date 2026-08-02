from __future__ import annotations

import fnmatch
import json
from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast

import httpx
import pytest
from scripts import copy_coding_questions as copy


class MockRedis:
    def __init__(self) -> None:
        self.strings: dict[str, str] = {}
        self.hashes: dict[str, dict[str, str]] = {}
        self.sets: dict[str, set[str]] = {}
        self.ttls: dict[str, int] = {}
        self.commands: list[list[str | int]] = []
        self.fail_command: str | None = None

    def handle(self, request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        if request.url.path.endswith("/pipeline"):
            commands = cast(list[list[str | int]], payload)
            return httpx.Response(
                200, json=[self._response(command) for command in commands]
            )
        return httpx.Response(200, json=self._response(cast(list[str | int], payload)))

    def _response(self, command: list[str | int]) -> dict[str, object]:
        self.commands.append(command)
        name = cast(str, command[0]).upper()
        if self.fail_command == name:
            self.fail_command = None
            return {"error": "injected failure"}
        return {"result": self._execute(name, command[1:])}

    def _execute(self, name: str, arguments: list[str | int]) -> object:
        key = cast(str, arguments[0])
        if name == "SCAN":
            pattern = cast(str, arguments[2])
            keys = sorted(
                candidate
                for candidate in self._all_keys()
                if fnmatch.fnmatchcase(candidate, pattern)
            )
            return ["0", keys]
        if name == "TYPE":
            if key in self.strings:
                return "string"
            if key in self.hashes:
                return "hash"
            if key in self.sets:
                return "set"
            return "none"
        if name == "PTTL":
            if key not in self._all_keys():
                return -2
            return self.ttls.get(key, -1)
        if name == "GET":
            return self.strings.get(key)
        if name == "SET":
            value = cast(str, arguments[1])
            if (
                len(arguments) > 2
                and cast(str, arguments[2]).upper() == "NX"
                and key in self._all_keys()
            ):
                return None
            self._delete(key)
            self.strings[key] = value
            return "OK"
        if name == "APPEND":
            value = cast(str, arguments[1])
            self.strings[key] = self.strings.get(key, "") + value
            return len(self.strings[key].encode("utf-8"))
        if name == "HSCAN":
            items: list[str] = []
            for field, value in sorted(self.hashes.get(key, {}).items()):
                items.extend((field, value))
            return ["0", items]
        if name == "HSET":
            target = self.hashes.setdefault(key, {})
            created = 0
            for index in range(1, len(arguments), 2):
                field = cast(str, arguments[index])
                value = cast(str, arguments[index + 1])
                created += field not in target
                target[field] = value
            return created
        if name == "SMEMBERS":
            return sorted(self.sets.get(key, set()))
        if name == "SADD":
            target = self.sets.setdefault(key, set())
            members = {cast(str, value) for value in arguments[1:]}
            added = len(members - target)
            target.update(members)
            return added
        if name == "PEXPIRE":
            if key not in self._all_keys():
                return 0
            self.ttls[key] = cast(int, arguments[1])
            return 1
        if name == "RENAME":
            destination = cast(str, arguments[1])
            self._rename(key, destination)
            return "OK"
        if name == "STRLEN":
            return len(self.strings.get(key, "").encode("utf-8"))
        if name == "HLEN":
            return len(self.hashes.get(key, {}))
        if name == "SCARD":
            return len(self.sets.get(key, set()))
        if name == "DEL":
            removed = 0
            for value in arguments:
                removed += self._delete(cast(str, value))
            return removed
        if name == "EVAL":
            lock_key = cast(str, arguments[2])
            token = cast(str, arguments[3])
            if self.strings.get(lock_key) != token:
                return 0
            self._delete(lock_key)
            return 1
        raise AssertionError(f"Unsupported Redis command {name}.")

    def _all_keys(self) -> set[str]:
        return set(self.strings) | set(self.hashes) | set(self.sets)

    def _delete(self, key: str) -> int:
        existed = key in self._all_keys()
        self.strings.pop(key, None)
        self.hashes.pop(key, None)
        self.sets.pop(key, None)
        self.ttls.pop(key, None)
        return int(existed)

    def _rename(self, source: str, destination: str) -> None:
        ttl = self.ttls.get(source)
        self._delete(destination)
        if source in self.strings:
            self.strings[destination] = self.strings.pop(source)
        elif source in self.hashes:
            self.hashes[destination] = self.hashes.pop(source)
        elif source in self.sets:
            self.sets[destination] = self.sets.pop(source)
        else:
            raise AssertionError(f"Missing rename source {source}.")
        self.ttls.pop(source, None)
        if ttl is not None:
            self.ttls[destination] = ttl


def source_state() -> MockRedis:
    state = MockRedis()
    state.hashes["coding_questions"] = {
        "id-1": '{"id":"id-1","difficulty":"Easy"}',
        "id-2": '{"id":"id-2","difficulty":"Medium"}',
    }
    state.strings["coding_questions:legacy"] = '[{"title":"Café"}]'
    state.strings["coding_questions:index:active"] = "old-version"
    state.sets["coding_questions:index:all"] = {"id-1", "id-2"}
    state.sets["coding_questions:index:difficulty:easy"] = {"id-1"}
    state.ttls["coding_questions:index:active"] = 60_000
    return state


@contextmanager
def clients(
    source: MockRedis, destination: MockRedis
) -> Iterator[tuple[copy.RedisRestClient, copy.RedisRestClient]]:
    with (
        httpx.Client(transport=httpx.MockTransport(source.handle)) as source_http,
        httpx.Client(
            transport=httpx.MockTransport(destination.handle)
        ) as destination_http,
    ):
        source_client = copy.RedisRestClient(
            copy.Endpoint("https://source.example.com", "source-token"), source_http
        )
        destination_client = copy.RedisRestClient(
            copy.Endpoint("https://destination.example.com", "destination-token"),
            destination_http,
        )
        yield source_client, destination_client


def test_dry_run_does_not_write_destination() -> None:
    source = source_state()
    destination = MockRedis()

    with clients(source, destination) as (source_client, destination_client):
        result = copy.copy_coding_questions(
            source_client, destination_client, apply=False
        )

    assert result["mode"] == "validation-only"
    assert result["source_key_count"] == 5
    assert destination._all_keys() == set()


def test_apply_copies_all_types_overwrites_matches_and_preserves_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(copy, "STRING_CHUNK_CHARACTERS", 4)
    source = source_state()
    destination = MockRedis()
    destination.hashes["coding_questions"] = {"old": "value"}
    destination.strings["coding_questions:destination-only"] = "keep"

    with clients(source, destination) as (source_client, destination_client):
        result = copy.copy_coding_questions(
            source_client, destination_client, apply=True
        )

    assert result["mode"] == "applied"
    assert result["copied_key_count"] == 5
    assert destination.hashes["coding_questions"] == source.hashes["coding_questions"]
    assert (
        destination.strings["coding_questions:legacy"]
        == source.strings["coding_questions:legacy"]
    )
    assert (
        destination.sets["coding_questions:index:all"]
        == source.sets["coding_questions:index:all"]
    )
    assert destination.strings["coding_questions:destination-only"] == "keep"
    assert destination.ttls["coding_questions:index:active"] == 60_000
    assert copy.LOCK_KEY not in destination.strings
    assert not any(
        key.startswith(copy.STAGING_NAMESPACE) for key in destination._all_keys()
    )


def test_failed_staging_write_preserves_destination_and_releases_lock() -> None:
    source = source_state()
    destination = MockRedis()
    destination.hashes["coding_questions"] = {"old": "value"}
    destination.fail_command = "HSET"

    with (
        clients(source, destination) as (source_client, destination_client),
        pytest.raises(copy.RedisError, match="injected failure"),
    ):
        copy.copy_coding_questions(source_client, destination_client, apply=True)

    assert destination.hashes["coding_questions"] == {"old": "value"}
    assert copy.LOCK_KEY not in destination.strings
    assert not any(
        key.startswith(copy.STAGING_NAMESPACE) for key in destination._all_keys()
    )


def test_settings_reject_same_source_and_destination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL_SRC", "https://same.example.com")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN_SRC", "source-token")
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL_DST", "https://same.example.com")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN_DST", "destination-token")

    with pytest.raises(copy.ConfigurationError, match="must be different"):
        copy.CopySettings.from_environment()
