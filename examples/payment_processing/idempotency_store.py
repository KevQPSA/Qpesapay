# Simple in-memory idempotency store for demonstration (replace with persistent DB in production)
_idempotency_db = {}

def get_idempotency_record(key):
    return _idempotency_db.get(key)

def set_idempotency_record(key, value):
    _idempotency_db[key] = value

def has_idempotency_key(key):
    return key in _idempotency_db
