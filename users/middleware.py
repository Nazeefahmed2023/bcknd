from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    try:
        access = AccessToken(token)
        user_id = access.get('user_id') or access.get('user_id') or access.get('user_id')
        return User.objects.get(id=user_id)
    except Exception:
        return None

class JwtAuthMiddleware:
    """
    ASGI middleware that extracts JWT from querystring (token or access_token)
    and sets scope['user'] accordingly.
    Usage in core/routing.py:
        JwtAuthMiddleware(URLRouter(...))
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JwtAuthMiddlewareInstance(scope, self.inner)


class JwtAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = self.scope.get('query_string', b'').decode()
        qs = parse_qs(query_string)
        token_list = qs.get('token') or qs.get('access_token') or []
        user = None
        if token_list:
            token = token_list[0]
            user = await get_user_from_token(token)
        if user is None:
            self.scope['user'] = AnonymousUser()
        else:
            self.scope['user'] = user
        inner = self.inner(self.scope)
        return await inner(receive, send)
