import hashlib
import json
import redis

# Redis connection
try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    redis_client.ping()

    REDIS_AVAILABLE = True
    print("REDIS AVAILABLE")

except Exception as e:
    print("REDIS ERROR:", e)
    REDIS_AVAILABLE = False
    print("REDIS AVAILABLE")


# generate cache key
def generate_cache_key(endpoint, user_input):

    raw_key = f"{endpoint}:{user_input}"

    return hashlib.sha256(raw_key.encode()).hexdigest()


# get cached response
def get_cached_response(endpoint, user_input):

    if not REDIS_AVAILABLE:
        print("REDIS NOT AVAILABLE")
        return None

    key = generate_cache_key(endpoint, user_input)

    print(f"CACHE CHECK: {key}")

    cached_data = redis_client.get(key)

    if cached_data:
        print("CACHE HIT")
        return json.loads(cached_data)

    print("CACHE MISS")
    return None


# save response to cache
def save_response_to_cache(endpoint, user_input, response_data):

    if not REDIS_AVAILABLE:
        print("REDIS NOT AVAILABLE")
        return

    key = generate_cache_key(endpoint, user_input)

    redis_client.setex(
        key,
        900,
        json.dumps(response_data)
    )

    print(f"CACHE SAVED: {key}")