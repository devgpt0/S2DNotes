# Rust Concurrency Roadmap

Learn synchronous concurrency before async programming. They solve related but different scheduling problems.

1. [Threads, channels, Arc, Mutex, Send, and Sync](11-threads-channels-send-and-sync.md)
2. [Async, futures, Tokio, cancellation, and backpressure](12-async-futures-tokio-and-cancellation.md)

After this section, you should be able to transfer or share ownership safely, bound parallel work, avoid holding locks across `.await`, and design cancellation and completion behavior explicitly.

[Continue to the Rust ecosystem and production](../rust_ecosystem_and_production/00-rust-ecosystem-production-roadmap.md)

