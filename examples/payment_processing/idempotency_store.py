# Simple in-memory idempotency store for demonstration (replace with persistent DB in production)
_idempotency_db = {}

def get_idempotency_record(key):
    val = _redis.get(key)
    if val:
        return json.loads(val)
    return None

def set_idempotency_record(key, value):
    # Enforce size limit
    if _redis.dbsize() >= _IDEMPOTENCY_MAX_SIZE:
        # Remove a random key (or implement LRU/other policy as needed)
        for k in _redis.scan_iter():
            _redis.delete(k)
            break
    _redis.setex(key, ttl, json.dumps(value))

def has_idempotency_key(key):
    return _redis.exists(key) == 1

# Redis-based idempotency store for production
import redis
import json

_redis = redis.StrictRedis.from_url('redis://localhost:6379/0')
_IDEMPOTENCY_TTL = 3600  # 1 hour
_IDEMPOTENCY_MAX_SIZE = 10000
