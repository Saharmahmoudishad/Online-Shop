import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from core.API.permissions import OwnerOrReadonly
from core.models import DiscountCode, Province, City
from customers.API.Jwt import decode_jwt_token
# from customers.API.Jwt import decode_jwt_token
from customers.models import Address, CustomUser
from customers.serializers import AddressSerializer, CustomUserSerializer
from orders.cart import Cart
from orders.models import Order, OrderItem
from orders.API.serializers import OrderSerializer, OrderItemSerializer
from product.models import Products, Variants, Size, Brand, Color, Material, Attribute
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class CartProductView(APIView):
    """
    Show products that customer add in cart
    Authentication:
    customer or Anonymous can request to get method
    """
    permission_classes = [AllowAny]
    serializer_class = None

    def get(self, request):
        """
        This method show products that user add to the session

        :param request: None
        :return: the Features of the products (for user's order items) extracted from Variants models and the Order
        number, showed in cart page
        brand, color, size, material and other attributes of product,Plus custom product quantity

        **handle the error** of Product stock, in this method if user order product more than Product stock  or if Product stock==0
         we must show  error
        """
        cart = Cart(request)
        return Response(
            {"cart": cart},
            status=status.HTTP_200_OK)


class CartAddProductView(APIView):
    """
    handle that customer add products to cart
    Authentication:
    customer or Anonymous can request to get method
    """
    permission_classes = [AllowAny]
    serializer_class = None

    def post(self, request, product_id=None, **kwargs):
        """
       :param request:  brand, color, size, material and other attributes for each product,Plus order product quantity

       :param product_id: id of Product model in database

       :return: response ok for post request, return status 200
                response is not ok or post request, return status 400.(param request doesn't choose completely or the product quantity doesn't enough for customers order)
       """
        cart = Cart(request)
        post_data = {key: int(value[0:20]) if value.isdigit() else value[0:20] for key, value in
                     request.data.items()}
        post_data['size'] = Size.objects.filter(code=post_data['size']).first()
        post_data['brand'] = Brand.objects.filter(title=post_data['brand']).first()
        post_data['color'] = Color.objects.filter(name=post_data['color']).first()
        post_data['material'] = Material.objects.filter(name=post_data['material']).first()
        post_data['attribute'] = Attribute.objects.filter(type=post_data['attribute']).first()
        variant_chose = get_object_or_404(Variants, product=product_id,
                                          brand=post_data['brand'],
                                          size=post_data['size'], color=post_data['color'],
                                          material=post_data['material'],
                                          attribute=post_data['attribute'], )
        if post_data['quantity'] > variant_chose.quantity or variant_chose.quantity == 0:
            return Response({
                "message": f"The requested quantity is more than the stock of the product. the stock ={variant_chose.quantity}"},
                status=status.HTTP_400_BAD_REQUEST)
        cart.add(variant=variant_chose,
                 discount_price=post_data['discount'],
                 quantity=post_data['quantity'],
                 brand=post_data['brand'].title,
                 color=post_data['color'].name,
                 size=post_data['size'].code,
                 material=post_data['material'].name,
                 attribute=post_data['attribute'].type, )
        return Response(status=status.HTTP_200_OK)


class CartUpdateProductView(APIView):
    """
    handle that customer update the number of products were ordered in cart
    Authentication:
    customer or Anonymous can request to get method
    """
    permission_classes = [AllowAny]
    serializer_class = None

    def put(self, request, variant_id=None):
        """
        This method is updated the quantity of order for each product in cart dictionary in session
        if quantity get value more than product stock return message

        param variant_id: key of cart dictionary  for each product, used in updating quantity

        return: if response is ok  for put request, return status 200  and message
                if response is not ok  for put request, return status 400 and message
        """
        cart = Cart(request)
        variant_chose = get_object_or_404(Variants, id=variant_id)
        try:
            data = json.loads(request.body)
            new_quantity = int(data['quantity'])
            if new_quantity > variant_chose.quantity or variant_chose.quantity == 0:
                return Response({
                    "message": f"The requested quantity is more than the stock of the product."}, )
            cart.update(variant_id, new_quantity)
            return Response(
                {"message": "Cart updated successfully"},
                status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON data"},
                status=status.HTTP_400_BAD_REQUEST)


class CartRemoveView(APIView):
    """
    This method is removed the order variants in cart dictionary handling in session

    param variant_id: key of cart dictionary for updating quantity

    return: if response is ok return updated cart value after remove and status 200
    """

    def get(self, request, variant_id):
        cart = Cart(request)

        variant = get_object_or_404(Variants, id=variant_id)

        cart.remove(variant)

        return Response({'cart': cart}, status=status.HTTP_200_OK)


class ReceiptCreateView(APIView):
    """
    this class methods fix and save orders of customers in models and pass data in front to show detail of order final
    param:jwt token to manage permission

    permission: user must be authenticated
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer

    def get(self, request):
        """
        fix oder and add data in models of order and orderItem and set order id in cookie for one day
        user have time to compelete their order

        :param request:user authentication token
        :return:order data(json), status code 201
        """
        cart = Cart(request)
        # user_id = decode_jwt_token(request)
        user = get_object_or_404(CustomUser, id=request.user.id)
        order = Order.objects.create(user=user, calculation=cart.get_total_price())
        for item in cart:
            variant = get_object_or_404(Variants, id=item['variant']['id'])
            item = OrderItem.objects.create(order=order, items=variant, quantity=item['quantity'])
        cart.clear()
        ser_data = OrderSerializer(order)
        response = JsonResponse(ser_data.data, status=status.HTTP_201_CREATED)
        expiration_time = datetime.now() + timedelta(days=1)
        response.set_cookie('orderid', order.id, expires=expiration_time)
        return response


class ReceiptAddDiscountView(APIView):
    """
    add discount in user receipt order and update value
    permission: user must Authenticated and must be the owner of receipt
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = OrderSerializer

    def post(self, request):
        """
        this method calculate the final receipt
        :param request: user authentication token, discountcode

        return json data of order after update receipt
        """
        discountcode = request.data['discountcode']
        orderId = request.COOKIES.get('orderid')

        discount_factor = DiscountCode.objects.get(title=discountcode)
        order = Order.objects.get(id=orderId)
        self.check_object_permissions(request, order)

        order.calculation = float(order.calculation) * float(discount_factor.amount)
        order.save()
        ser_order = OrderSerializer(istance=order)
        return Response(data=ser_order.data, status=status.HTTP_201_CREATED)


class ReceiptUpdateView(APIView):
    """
    this class has to method put for update order item from database before receipt fix at the end
    permission: user must Authenticated and must be the owner of receipt
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = OrderItemSerializer

    def put(self, request, order_id):
        """
        owner can update the item of their order
        :param request: user authentication token
        :param order_id: order_id that is not paid
        :return: orderitem after updating as json response
        errors are handled by message response
        """
        order = OrderItem.objects.get(id=order_id)
        self.check_object_permissions(request, order)
        orderitem = OrderItem.objects.filter(order=order_id)

        ser_data = OrderItemSerializer(instance=orderitem, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceiptDeleteView(APIView):
    def delete(self, request, order_id):
        """
        owner can delete the order logically not completely
        :param request: user authentication token
        :param order_id: order_id that is not paid
        :return: message to show order was deleted
        """
        order = Order.objects.get(id=order_id)
        self.check_object_permissions(request, order)
        order.logical_delete()
        return Response('message:orders deleted by user', status=status.HTTP_200_OK)


class CheckOutView(APIView):
    """
    this class has to method get and post for show final receipt and users data. moreover delete method is for remove
    order in checkout page
    permission: user must Authenticated and must be the owner of receipt
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = AddressSerializer, OrderSerializer

    def get(self, request):
        """

        :param request: user authentication token
        :return:
        """
        user_id = decode_jwt_token(request)
        user = get_object_or_404(CustomUser, id=user_id)
        try:
            address = Address.objects.filter(user=user)
        except Address.DoesNotExist:
            raise NotFound("User address not found")
        address_serializer = AddressSerializer(instance=address, many=True)
        user_serializer = CustomUserSerializer(instance=user)
        orderId = request.COOKIES.get('orderid')
        if orderId:
            order = get_object_or_404(Order, id=orderId)
            self.check_object_permissions(request, order)
            ser_order = OrderSerializer(instance=order)
            return Response({
                "user": user_serializer.data,
                "addresses": address_serializer.data,
                "order": ser_order.data,
            }, status=status.HTTP_200_OK)
        return Response({"user": user_serializer.data,
                         "addresses": address_serializer.data,
                         "message": "Your order ID expire Please order again"},
                        status=status.HTTP_200_OK)


class CheckOutSetAddressView(APIView):
    """
    this class has to method post for show final receipt and users data.
    permission: user must Authenticated and must be the owner of receipt
    """
    permission_classes = [OwnerOrReadonly]
    serializer_class = AddressSerializer, OrderSerializer

    def post(self, request):
        """
        select one of addresses by owner for send items by shop
        :param request: user authentication token
        :return: order
        """
        selected_address = request.POST.get('selected-address', '')
        orderId = request.COOKIES.get('orderid')
        order = Order.objects.get(id=orderId)
        order.delivery_address = selected_address
        order.save()
        ser_order = OrderSerializer(instance=order)
        return Response(data=ser_order.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
        owner can delete the order completely in checkout page too

        :param order_id: order_id that is not paid
        :param request: user authentication token
        :return: message to show order was deleted

        """
        orderId = request.COOKIES.get('orderid')
        order = Order.objects.get(id=orderId)
        self.check_object_permissions(request, order)
        order.delete()
        return Response({"message": "your order is canceled"}, status=status.HTTP_200_OK)


class NewAddressView(APIView):
    permission_classes = [OwnerOrReadonly]
    serializer_class = AddressSerializer

    def post(self, request):
        """

        :param request: user authentication token
        :return:
        """
        orderId = request.COOKIES.get('orderid')
        order = Order.objects.get(id=orderId)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        try:
            province = Province.objects.get(name=data['province'])
        except province.DoesNotExist:

            province = Province.objects.create(name=data['province'])
        try:
            city = City.objects.get(name=data['city'], province=province)
        except City.DoesNotExist:
            city = City.objects.create(name=data['city'], province=province)
        data['province'], data['city'] = province.id, city.id
        data = {'user': request.user.id, 'address': data['new_address'],
                'city': city.id, 'province': province.id, 'postcode': data['postcode']}
        ser_address = AddressSerializer(data=data)
        if ser_address.is_valid():
            address = Address.objects.create(address=ser_address.validated_data['address'],
                                             province=ser_address.validated_data['province'],
                                             city=ser_address.validated_data['city'],
                                             postcode=ser_address.validated_data['postcode'],
                                             user=ser_address.validated_data['user'])
            order.delivery_address = address.id
            order.save()
            ser_order = OrderSerializer(instance=order)
            return Response({'order': ser_order.data, 'address': ser_address.data},
                            status=status.HTTP_201_CREATED)
        return Response(ser_address.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryMethodView(APIView):
    permission_classes = [OwnerOrReadonly]
    serializer_class = OrderSerializer
    """
    this class handle method and cost of delivery
    """

    def put(self, request):
        """
        :param request: user authentication token
        :return:if response is ok return order and status code 200
                if response is not ok return error and status code 400

        """
        orderId = request.COOKIES.get('orderid')
        order = Order.objects.get(id=orderId)
        ser_order = OrderSerializer(instance=order, data=request.data, partial=True)
        if ser_order.is_valid():
            ser_order.save()
            return Response({'order': ser_order.data, },
                            status=status.HTTP_200_OK)
        return Response(ser_order.errors, status=status.HTTP_400_BAD_REQUEST)
