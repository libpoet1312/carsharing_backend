from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

import rest_framework_jwt.utils

from rest_framework import exceptions
import jwt


@database_sync_to_async
def get_user(query_string):
    try:
        params = parse_qs(query_string.decode('utf8'))
        token = params['token'][0]

        if token:
            try:
                payload = jwt_decode_handler(token)
            except jwt.ExpiredSignature:
                msg = 'Token has expired.'
                raise exceptions.AuthenticationFailed(msg)
            except jwt.DecodeError:
                msg = 'Error decoding token.'
                raise exceptions.AuthenticationFailed(msg)

            # print(payload)

            username = rest_framework_jwt.utils.jwt_get_username_from_payload_handler(payload)
            if not username:
                msg = 'Invalid payload.'
                raise exceptions.AuthenticationFailed(msg)

            try:
                User = get_user_model()
                user = User.objects.get_by_natural_key(username)
            except User.DoesNotExist:
                msg = 'Invalid token.'
                raise exceptions.AuthenticationFailed(msg)

            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.AuthenticationFailed(msg)

            # print(user)
            return user

    except query_string is None:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """
    Yeah, this is black magic:
    https://github.com/django/channels/issues/1399
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        query_string = self.scope['query_string']
        # print(query_string)

        if b'token' in self.scope['query_string']:
            self.scope['user'] = await get_user(query_string)
        inner = self.inner(self.scope)
        close_old_connections()
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
