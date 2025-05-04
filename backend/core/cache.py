import redis.asyncio as redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

async def get_cached_verdict(seed: str, guess: str):
    return await r.get(f"{seed}:{guess}")

async def set_cached_verdict(seed: str, guess: str, verdict: str):
    await r.set(f"{seed}:{guess}", verdict, ex=86400)  # 24-hour TTL
