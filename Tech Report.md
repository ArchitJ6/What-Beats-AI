## 🛠️ Tech Report – *What Beats AI – GenAI Game*

### ⚡️ Caching Strategy

To optimize LLM usage and reduce latency, a Redis-based caching mechanism is implemented using the `redis.asyncio` client. For every `{seed}:{guess}` pair, we cache the verdict (`YES`/`NO`) for 24 hours (`TTL = 86400s`). Before querying the Groq LLM, the app first checks the cache to avoid redundant API calls. This drastically improves response times for repeated guesses and reduces cost.

### 🔗 Linked List Implementation

Each game session tracks the user's guess chain using a `deque` (double-ended queue) in the `GameSession` class. The list starts with the default seed word `'rock'` and appends each successful new guess if it semantically beats the previous. This mimics a singly linked list structure with append-only logic, enabling history traversal, scoring, and validation efficiently.

### 🔄 Concurrency Handling

The FastAPI backend uses `async`/`await` syntax for all I/O-bound operations including:

* Database queries with `SQLAlchemy`’s `AsyncSession`
* Redis caching
* WebSocket communication

WebSocket sessions are uniquely identified by a `session_id`, and active users are tracked in a shared list `active_connections`. To prevent abuse, a per-IP connection limit of 5 is enforced using `ip_connections`. This ensures fair resource usage under concurrent user load.

### 🎮 Game Logic

The game revolves around semantically "beating" a seed word using a word that scores higher in a context-aware LLM check (`check_if_beats`). Each correct guess:

* Is verified for profanity
* Is validated against previous guesses (no repeats)
* Updates session score and history
* Is globally counted and persisted in the database (`guess_counts` table)

Session expiry is set at 5 minutes of inactivity.

### 📈 Metrics & Persistence

* Global guess popularity is stored in `guess_counts`, incremented via SQLAlchemy.
* Sessions and WebSocket states are managed in-memory.
* Session expiry and cleanup handled via WebSocket lifecycle.

### 🌟 Proposed New Feature – Leaderboard & Timed Mode

We can enhance engagement by introducing:

1. **Leaderboard**: Store top users by high score using Redis sorted sets (`ZADD`, `ZRANGE`).
2. **Timed Mode**: Introduce a countdown timer per guess, adding urgency and increasing replayability. This could be implemented client-side with periodic server validation for fairness.