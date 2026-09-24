import redis
import json
from typing import Optional, Tuple
from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_stats_cache() -> Tuple[Optional[dict], str]:
    """Returns cached stats and X-Cache header value (HIT/MISS)"""
    try:
        cached = redis_client.get("stats:complaints")
        if cached:
            return json.loads(cached), "HIT"
    except redis.exceptions.ConnectionError:
        pass # Fallback to MISS if Redis is down
    return None, "MISS"

def set_stats_cache(stats: dict):
    """Caches the stats dictionary for 30 seconds"""
    try:
        redis_client.setex("stats:complaints", 30, json.dumps(stats))
    except redis.exceptions.ConnectionError:
        pass

def invalidate_stats_cache():
    """Invalidates the stats cache when a write occurs"""
    try:
        redis_client.delete("stats:complaints")
    except redis.exceptions.ConnectionError:
        pass

def check_rate_limit(client_ip: str, limit: int = 10, window_seconds: int = 60) -> Tuple[bool, int]:
    """
    Fixed-window rate limiter using Redis INCR.
    Returns (is_allowed, retry_after_seconds).
    """
    key = f"rate_limit:post_complaints:{client_ip}"
    
    try:
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.ttl(key)
        results = pipe.execute()
        
        current_count = results[0]
        ttl = results[1]
        
        if current_count == 1:
            redis_client.expire(key, window_seconds)
            return True, 0
            
        if current_count > limit:
            retry_after = ttl if ttl > 0 else window_seconds
            return False, retry_after
            
    except redis.exceptions.ConnectionError:
        return True, 0 # Fail open if Redis is down, to avoid complete outage
        
    return True, 0
