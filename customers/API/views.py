from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from core.API.permissions import OwnerOrReadonly
from core.API.serializers import CommentSerializer
from customers.API.Jwt import CustomJWTAuthentication, decode_jwt_token
from customers.models import CustomUser, Address
from customers.serializers import CustomUserSerializer, AddressSerializer
from orders.API.serializers import OrderSerializer
from orders.models import Order
from utils import addprovincecity


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
            response.set_cookie("token", jwt_token, expires=expires)
            return response
        else:
            raise AuthenticationFailed('Invalid phonenumber')


class UserProfileView(APIView):
    """
    This class handle detail of user profile data
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = CustomUserSerializer

    def get(self, request):
        """
        get detail of user profile data for who is login to show in site
        :param request: [first name, last name, phonenumber and email address, adresses and postcodes, orders data]
        :return: response.json(), user, address and orders of each user who is login  and status code 200
        """
        user = CustomUser.objects.get(id=request.user.id)
        user_address = Address.objects.filter(user=user, is_deleted=False)
        user_order = Order.objects.filter(user=user)
        ser_customer = CustomUserSerializer(instance=user)
        ser_addresses = AddressSerializer(instance=user_address, many=True)
        ser_order = OrderSerializer(instance=user_order, many=True)
        data = {"user": ser_customer.data,
                "addresses": ser_addresses.data,
                "order": ser_order.data, }
        return Response(data=data, status=status.HTTP_200_OK)


class UpdateUserProfileView(APIView):
    """
    this class handle updating each user profile detail
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = CustomUserSerializer

    def put(self, request):
        """

        :param request: user profile detail, [first name, last name, phonenumber and email address]
        :return: response.json(), response is ok return new value for each attribute of user models for user who is login and status code 200
        if new value for each user attribute is not valid,response is not ok return errors and status code 400
        """
        user = CustomUser.objects.get(id=request.user.id)
        ser_customer = CustomUserSerializer(instance=user, data=request.data, partial=True)
        if ser_customer.is_valid():
            ser_customer.save()
            return Response(ser_customer.data, status=status.HTTP_200_OK)
        return Response(ser_customer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAddressView(APIView):
    """
    This class handle create,update and deleted Address of users
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = AddressSerializer

    def post(self, request):
        """
        this method add address to list of users address
        :param request: province, city, address and postcode to create new address for user who is login
        :return: response.json(), response is not ok return new address and status code 200
        if values for address attributes are not valid, response is not ok return errors and status code 400
        """
        data = request.data
        data['province'], data['city'] = addprovincecity(data['province'], data['city'])
        data['user'] = request.user.id
        ser_address = AddressSerializer(data=data)
        if ser_address.is_valid():
            ser_address.save()
            return Response(ser_address.data, status=status.HTTP_200_OK)
        return Response(ser_address.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatedAddressView(APIView):
    """
    this class handle updating each address of users who is login
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = AddressSerializer

    def put(self, request, address_id):
        """
        :param request: the fields values of address model for especial address [ province,city,address, postcode]
        :param address_id:id of special address for user who is login
        :return: response.json(),response is ok new value for each attribute of address models for especial user address who is login and status code 200
        if new value for each address attribute is not valid, response is not ok return errors and status code 400
                                 if address doesn't exist return error message and status code 404
        """
        try:
            print("1" * 50, address_id)
            address = Address.objects.get(id=address_id, user=request.user.id)
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)


class DeleteAddressView(APIView):
    """
    This class handle deleted Address of users
    """
    permission_classes = [OwnerOrReadonly]

    def delete(self, request, address_id):
        """
        :param request:
        :param address_id: id of special address for user who is login
        :return: when address deleted successfully return status code 200
        """
        print("1" * 50, address_id)
        address = Address.objects.get(id=address_id, user=request.user.id)
        address.logical_delete()
        return Response({"message": "address successfully"}, status=status.HTTP_200_OK)
