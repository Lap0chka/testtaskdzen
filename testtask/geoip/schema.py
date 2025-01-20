from typing import Any, Optional

from graphene import Field, Mutation, ObjectType, Schema, String

from geoip.utils import get_user_stat, save_user_stat


class UserStatType(ObjectType):  # type: ignore
    """
    GraphQL type representing user statistics.
    """

    ip_address = String()  # Удаляем Optional
    country = String()
    language = String()
    timestamp = String()


class CreateUserStat(Mutation):  # type: ignore
    """
    Mutation to create a new user statistic entry.

    Fields:
        success (String): A message indicating success or failure.
        user_stat (UserStatType): The created user statistic entry, if successful.
    """

    class Arguments:
        ip_address = String(required=True)  # Удаляем аннотацию типа
        language = String(required=True)

    success = String()
    user_stat = Field(lambda: UserStatType)

    def mutate(self, info: Any, ip_address: str, language: str) -> "CreateUserStat":
        """
        Handles the mutation to create a new user statistic.

        Args:
            info (Any): The GraphQL execution context.
            ip_address (str): The IP address of the user.
            language (str): The preferred language of the user.

        Returns:
            CreateUserStat: The mutation result containing success message and created user statistic.
        """
        try:
            result = save_user_stat(ip_address, language)
            if result:
                return CreateUserStat(success="User stat added", user_stat=UserStatType(**result))
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error saving user stat: {e}")
        return CreateUserStat(success="Failed to add user stat", user_stat=None)


class Query(ObjectType):  # type: ignore
    """
    Query for retrieving user statistics.
    """

    user_stat = Field(
        UserStatType,
        ip_address=String(required=True),
        description="Retrieve user statistics by IP address.",
    )

    def resolve_user_stat(self, info: Any, ip_address: str) -> Optional[UserStatType]:
        """
        Resolves user statistics for a given IP address.

        Args:
            info (Any): The GraphQL execution context.
            ip_address (str): The IP address to query.

        Returns:
            Optional[UserStatType]: The user statistics or None if not found.
        """
        try:
            result = get_user_stat(ip_address)
            if result:
                return UserStatType(**result)
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error retrieving user stat: {e}")
        return None


class RootMutation(ObjectType):  # type: ignore
    """
    Root mutation for the schema.
    """

    create_user_stat = CreateUserStat.Field()


schema = Schema(query=Query, mutation=RootMutation)
