from datetime import datetime, timedelta
import jwt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.authentication import BaseAuthentication

from config import settings


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = self.decode_jwt_token(request)
        if user is None:
            return None
        return (user, None)

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_JWT(cls, user):
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(days=3)
        payload = {
            'user': user,
            'exp': expiration_datetime
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return jwt_token

    def get_token_from_header(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            token_type, token = authorization_header.split()
            if token_type.lower() != 'bearer':
                return None
            return token
        except ValueError:
            return None

    @classmethod
    def decode_jwt_token(cls, request):
        try:
            jwt_token = request.COOKIES.get('token', None)
            if jwt_token:
                decoded_token = AccessToken(jwt_token)
                decoded_token = decoded_token.payload
                if decoded_token is not None:
                    user = decoded_token.get('user')
                    return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, TokenError):
            return None


def decode_jwt_token(request):
    try:
        jwt_token = request.COOKIES.get('jwt_token', None)
        if jwt_token:
            decoded_token = AccessToken(jwt_token)
            decoded_token = decoded_token.payload
            if decoded_token is not None:
                user = decoded_token.get('user_id')
                return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, TokenError):
        return None
