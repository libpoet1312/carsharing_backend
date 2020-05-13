from channels.auth import AuthMiddlewareStack
from rest_framework_jwt import authentication
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'JWT':
                    token = JSONWebTokenAuthentication().authenticate(token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except token_key is None:
                scope['user'] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
