# Focus300 150: LeetCode 920 - Number of Music Playlists

**Source:** [LeetCode 920](https://leetcode.com/problems/number-of-music-playlists/)  
**Difficulty:** Hard  
**Pattern:** sequence DP by used distinct songs

## Exact contract

Count playlists of length `goal` made from exactly `song_count` distinct songs,
where every song appears at least once and a song can repeat only after at least
`cooldown` other songs have played. Return the count modulo `1_000_000_007`.

## First principles

After a prefix with `used` distinct songs, append a new song in
`song_count - used` ways. Or replay one of the `used - cooldown` songs not
blocked by the recent cooldown window. The identities of recent songs do not
matter because they are distinct and exactly `cooldown` of them are blocked.

## Cases that decide correctness

- Every one of the `song_count` songs must appear by the end.
- A new song is never blocked by cooldown.
- Replaying is impossible while `used <= cooldown`.
- `cooldown = 0` permits an immediate repeat.
- Source bounds satisfy `0 <= cooldown < song_count <= goal`.

## Brute force: enumerate every playlist

```python
from itertools import product


def num_music_playlists_brute(
    song_count: int,
    goal: int,
    cooldown: int,
) -> int:
    if not 0 <= cooldown < song_count <= goal:
        raise ValueError("expected 0 <= cooldown < song_count <= goal")

    answer = 0
    for playlist in product(range(song_count), repeat=goal):
        if len(set(playlist)) != song_count:
            continue
        if all(
            playlist[index] not in playlist[max(0, index - cooldown) : index]
            for index in range(goal)
        ):
            answer += 1
    return answer % 1_000_000_007
```

This examines `song_count^goal` sequences.

## Better solution: full prefix-by-distinct-count table

```python
def num_music_playlists_table(
    song_count: int,
    goal: int,
    cooldown: int,
) -> int:
    if not 0 <= cooldown < song_count <= goal:
        raise ValueError("expected 0 <= cooldown < song_count <= goal")

    modulus = 1_000_000_007
    counts = [[0] * (song_count + 1) for _ in range(goal + 1)]
    counts[0][0] = 1
    for length in range(1, goal + 1):
        for used in range(1, min(length, song_count) + 1):
            add_new = counts[length - 1][used - 1] * (song_count - used + 1)
            replay = counts[length - 1][used] * max(0, used - cooldown)
            counts[length][used] = (add_new + replay) % modulus
    return counts[goal][song_count]
```

The table takes `O(goal * song_count)` time and space.

## Expert solution: retain one playlist-length row

```python
def num_music_playlists(
    song_count: int,
    goal: int,
    cooldown: int,
) -> int:
    if not 0 <= cooldown < song_count <= goal:
        raise ValueError("expected 0 <= cooldown < song_count <= goal")

    modulus = 1_000_000_007
    counts = [0] * (song_count + 1)
    counts[0] = 1
    for length in range(1, goal + 1):
        next_counts = [0] * (song_count + 1)
        for used in range(1, min(length, song_count) + 1):
            add_new = counts[used - 1] * (song_count - used + 1)
            replay = counts[used] * max(0, used - cooldown)
            next_counts[used] = (add_new + replay) % modulus
        counts = next_counts
    return counts[song_count]
```

Both transitions read only the previous prefix length, so older rows cannot
affect the answer and can be discarded.

**Complexity:** `O(goal * song_count)` time and `O(song_count)` space.
