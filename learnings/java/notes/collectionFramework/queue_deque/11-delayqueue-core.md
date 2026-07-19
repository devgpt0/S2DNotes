# 11 - DelayQueue Core

## 1) Internal Idea

`DelayQueue<E extends Delayed>` holds elements until their delay expires.

- unbounded blocking queue
- `take()` returns only expired elements
- internally priority-ordered by delay time

## 2) Custom Delayed Element

Concept taught: Implement `Delayed` for time-based scheduling.

```java
class DelayedTask implements Delayed {
    private final String name;
    private final long triggerTime;

    DelayedTask(String name, long delayMs) {
        this.name = name;
        this.triggerTime = System.currentTimeMillis() + delayMs;
    }

    @Override
    public long getDelay(TimeUnit unit) {
        long diff = triggerTime - System.currentTimeMillis();
        return unit.convert(diff, TimeUnit.MILLISECONDS);
    }

    @Override
    public int compareTo(Delayed o) {
        return Long.compare(this.getDelay(TimeUnit.MILLISECONDS), o.getDelay(TimeUnit.MILLISECONDS));
    }

    @Override
    public String toString() { return name; }
}

DelayQueue<DelayedTask> dq = new DelayQueue<>();
dq.put(new DelayedTask("t1", 50));
System.out.println(dq.take());
```

Expected output:

```text
t1
```

(approximately after delay)

## 3) Use Cases

- retry queues
- timeout processing
- delayed job execution

## 4) Summary

`DelayQueue` is ideal for time-gated task release without manual sleep-loop scheduling.
