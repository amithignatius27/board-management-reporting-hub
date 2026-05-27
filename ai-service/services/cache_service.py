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

except:
    REDIS_AVAILABLE = False


# generate cache key
def generate_cache_key(endpoint, user_input):

    raw_key = f"{endpoint}:{user_input}"

    return hashlib.sha256(raw_key.encode()).hexdigest()


# get cached response
def get_cached_response(endpoint, user_input):

    if not REDIS_AVAILABLE:
        return None

    key = generate_cache_key(endpoint, user_input)

    cached_data = redis_client.get(key)

    if cached_data:
        return json.loads(cached_data)

    return None


# save response to cache
def save_response_to_cache(endpoint, user_input, response_data):

    if not REDIS_AVAILABLE:
        return

    key = generate_cache_key(endpoint, user_input)

    redis_client.setex(
        key,
        900,  # 15 mins
        json.dumps(response_data)
    )