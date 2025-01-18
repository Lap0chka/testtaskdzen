import redis
from django.conf import settings
from geoip2.database import Reader
from django.utils.timezone import now
from typing import Optional, Dict, Any

# Initialize Redis client
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def get_country_from_ip(ip: str) -> str:
    """
    Retrieve the country name from an IP address using the GeoIP database.

    Args:
        ip (str): The IP address to lookup.

    Returns:
        str: The country name associated with the IP address, or "Unknown" if lookup fails.
    """
    reader = Reader(settings.GEOIP_PATH)
    response = reader.city(ip)
    return response.country.name or "Unknown"


def save_user_stat(ip: str, language: str) -> Optional[Dict[str, str]]:
    """
    Save user statistics (IP, country, language, timestamp) in Redis.

    Args:
        ip (str): The IP address of the user.
        language (str): The preferred language of the user.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the saved user statistics,
                                  or None if saving fails.
    """
    country = get_country_from_ip(ip)
    timestamp = now().isoformat()

    redis_key = f"user_stat:{ip}"
    try:
        redis_client.hset(
            redis_key,
            mapping={
                "ip_address": ip,
                "country": country,
                "language": language,
                "timestamp": timestamp,
            },
        )
        redis_client.expire(redis_key, 86400)  # Set expiration to 24 hours
        return {
            "ip_address": ip,
            "country": country,
            "language": language,
            "timestamp": timestamp,
        }
    except redis.ConnectionError as e:
        # Log Redis connection error
        print(f"Redis Connection Error: {e}")
        return None


def get_user_stat(ip: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve user statistics from Redis by IP address.

    Args:
        ip (str): The IP address of the user.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the user statistics,
                                  or None if the data is not found or an error occurs.
    """
    try:
        # Fetch user data from Redis
        data = redis_client.hgetall(f"user_stat:{ip}")

        if not data:
            return None

        # Safely decode Redis byte values
        def safe_decode(value: Optional[bytes]) -> Optional[str]:
            return value.decode('utf-8') if value else None

        # Return decoded user statistics
        return {
            "ip_address": safe_decode(data.get(b"ip_address")),  # type: ignore
            "country": safe_decode(data.get(b"country")),  # type: ignore
            "language": safe_decode(data.get(b"language")),  # type: ignore
            "timestamp": safe_decode(data.get(b"timestamp")),  # type: ignore
        }
    except redis.ConnectionError as e:
        # Log Redis connection error
        print(f"Redis Connection Error: {e}")
        return None
    except Exception as e:
        # Log any unexpected exceptions
        print(f"Unexpected Error in get_user_stat: {e}")
        return None
