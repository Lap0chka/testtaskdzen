from typing import Optional

from django.http import HttpRequest, HttpResponse

from geoip.utils import save_user_stat


class UserStatsMiddleware:
    """
    Middleware to log user statistics such as IP address and preferred language.
    """

    def __init__(self, get_response: HttpResponse) -> None:
        """
        Initializes the middleware.

        Args:
            get_response: The next middleware or view in the chain.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Processes the request to save user statistics.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        try:
            ip = self.get_client_ip(request)
            if ip:
                language = request.headers.get("Accept-Language", "Unknown").split(",")[
                    0
                ]

                # Save user statistics using the external utility
                save_user_stat(ip, language)
        except Exception as e:
            # Log any unexpected exceptions (logging can be added here if needed)
            print(f"Error in UserStatsMiddleware: {e}")

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request: HttpRequest) -> Optional[str] | None:
        """
        Retrieves the client's IP address from the HTTP request.

        Args:
            request: The HTTP request object.

        Returns:
            str | None: The client's IP address, or None if unavailable.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "").strip()

        return ip if ip else None
