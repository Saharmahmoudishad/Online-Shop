from datetime import datetime, timedelta

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.API.Jwt import CustomJWTAuthentication


class HandlingToken(APIView):
    serializer_class = None

    def get(self, request):
        print("123" * 50, request.user)
        user = self.request.session.get('phonenumber', None)
        if user:
            jwt_token = CustomJWTAuthentication.create_JWT(user)
            response = Response({'token': jwt_token})
            current_datetime = datetime.now()
            expires = current_datetime + timedelta(days=3)
            response.set_cookie("token", jwt_token,expires=expires)
            return response
        else:
            raise AuthenticationFailed('Invalid phonenumber')
