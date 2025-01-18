from typing import Any

from graphene_django.views import GraphQLView
from utils import redis_client


class CustomGraphQLView(GraphQLView):  # type: ignore
    """
    Custom GraphQLView with additional logging of user IP and language to Redis.
    """

    def execute_graphql_request(self, *args: Any, **kwargs: Any) -> Any:
        """
        Executes a GraphQL request while logging the user's IP and language to Redis.

        Args:
            *args: Positional arguments passed to the GraphQL request.
            **kwargs: Keyword arguments passed to the GraphQL request.

        Returns:
            Any: The result of the GraphQL request execution.
        """
        # Extract IP and language from the request
        ip: str = self.request.META.get("REMOTE_ADDR", "0.0.0.0")
        language: str = self.request.headers.get("Accept-Language", "Unknown").split(",")[0]

        # Log to Redis
        redis_key: str = f"stat:{ip}"
        try:
            redis_client.hset(redis_key, mapping={"ip_address": ip, "language": language})
            redis_client.expire(redis_key, 86400)  # Set key to expire after 24 hours
        except Exception as e:
            # Log error (replace print with a proper logging mechanism)
            print(f"Error logging to Redis: {e}")

        # Proceed with the GraphQL request execution
        return super().execute_graphql_request(*args, **kwargs)
