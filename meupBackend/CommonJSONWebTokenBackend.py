from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.shortcuts import get_user_by_token
from graphql_jwt.utils import get_credentials
from rest_framework.authentication import BaseAuthentication


class CommonJSONWenTokenBackend(BaseAuthentication):
    def authenticate(self, request=None, **kwargs):

        if request is None or getattr(request, "_jwt_token_auth", False):
            return None

        token = get_credentials(request, **kwargs)

        try:  # +++
            if token is not None:
                user = get_user_by_token(token, request)
                return user, None
        except JSONWebTokenError:  # +++
            pass  # +++

        return None
