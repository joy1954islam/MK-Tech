from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db.models import Q


class CustomerRegisterViewSet(ViewSet):

    def create(self, request):

        try:
            print('request data = ', request.data)

            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            confirm_password = request.data['confirm_password']

            if username == '':
                dict_response = {
                    'error': True,
                    'message': 'username required',
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

            if email == '':
                dict_response = {
                    'error': True,
                    'message': 'email required',
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

            check_email = User.objects.filter(email=email)
            if len(check_email) != 0:
                dict_response = {
                    'error': True,
                    'message': 'This email already used',
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

            if len(password) < 8:
                dict_response = {
                    'error': True,
                    'message': 'password must be 8 length'
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

            if password != confirm_password:
                dict_response = {
                    'error': True,
                    'message': 'password not match',
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

            user_registration = {}
            user_registration['email'] = email
            user_registration['username'] = username
            user_registration['password'] = password

            user_registration_serializer = RegisterSerializer(data=user_registration, context={'request': request})
            user_registration_serializer.is_valid(raise_exception=True)
            user_registration_serializer.save()

            user_id = user_registration_serializer.data['id']

            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()

            dict_response = {
                'error': False,
                'message': 'registration successfully',
            }
            return Response(dict_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict_response = {
                'error': True,
                'message': 'somethings is wrong . try again',
                'data': str(e)
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(ViewSet):

    def create(self, request):
        try:
            print('request.data = ', request.data)
            username = request.data["username"]
            password = request.data["password"]

            user_authentication = authenticate(request, username=username, password=password)
            print('user_authentication = ', user_authentication)
            if user_authentication:
                if user_authentication.is_active:
                    user_serializer = UserSerializer(user_authentication, context={"request": request})
                    dict_response = {
                        "error": False,
                        "message": "Successfully Login",
                        "data": user_serializer.data
                    }
                    return Response(dict_response, status=status.HTTP_200_OK)
                else:
                    user_serializer = UserSerializer(user_authentication, context={"request": request})
                    dict_response = {
                        "error": True,
                        "message": "Your account is not activated",
                        "data": user_serializer.data
                    }
                    return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
            else:
                dict_response = {
                    "error": True,
                    "message": "Email or password wrong!",
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            dict_response = {
                "error": True,
                "message": "Email and Password Wrong",
            }
            return Response(dict_response, status=status.HTTP_502_BAD_GATEWAY)


class ProductSearchViewSet(ViewSet):

    def list(self, request):

        search_key = self.request.query_params.get('search_key')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        print('search_key = ', search_key)
        if search_key:
            product_search = Product.objects.filter(
                name__icontains=search_key
            )
            print('product_search = ', product_search)
        if min_amount:
            product_search = Product.objects.filter(
                price__gte=min_amount
            )
            print('product_search = ', product_search)
        if max_amount:
            product_search = Product.objects.filter(
                price__lte=max_amount
            )
            print('product_search = ', product_search)
        if search_key and min_amount:
            product_search = product_search = Product.objects.filter(
                name__icontains=search_key,
                price__gte=min_amount,
            )
        if search_key and max_amount:
            product_search = Product.objects.filter(
                name__icontains=search_key,
                price__lte=max_amount,
            )
        if min_amount and max_amount:
            product_search = Product.objects.filter(
                price__gte=min_amount,
                price__lte=max_amount,
            )
        if search_key and min_amount and max_amount:
            product_search = Product.objects.filter(
                name__icontains=search_key,
                price__gte=min_amount,
                price__lte=max_amount,
            )
            print('product_search = ', product_search)
        if search_key == '' and min_amount == '' and max_amount == '':
            product_search = Product.objects.all()

        product_search_serializer = ProductSerializer(product_search, many=True)
        dict_response = {
            'error': False,
            'message': 'search result found',
            'data': product_search_serializer.data,
            'total_found': product_search.count()
        }
        return Response(dict_response, status=status.HTTP_200_OK)


class AllCustomerListViewSet(ViewSet):

    def retrieve(self, request, pk=None):

        user = User.objects.filter(id=pk, is_superuser=True)
        if len(user) != 0:
            all_customer = User.objects.filter(is_staff=False)
            all_customer_serializer = UserSerializer(all_customer, many=True)
            dict_response = {
                'error': False,
                'message': 'all customer list',
                'data': all_customer_serializer.data,
                'total_customer': all_customer.count()
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderViewSet(ViewSet):

    def create(self, request):
        print('request data = ', request.data)
        user_id = request.data['user_id']
        product_id = request.data['product_id']
        quantity = request.data['quantity']

        if user_id == '':
            dict_response = {
                'error': True,
                'message': 'user required'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

        product_id_split = product_id.split(',')
        print('product_id_split = ', product_id_split)
        quantity_split = quantity.split(',')
        print('quantity_split = ', quantity_split)

        if len(product_id_split) == len(quantity_split):
            order_create = {}
            order_create['user_id'] = user_id
            order_create_serializer = OrderSerializer(data=order_create)
            order_create_serializer.is_valid(raise_exception=True)
            order_create_serializer.save()

            order_id = order_create_serializer.data['id']

            for p in range(0, len(product_id_split)):
                product_value = product_id_split[p]
                product_quantity = quantity_split[p]
                product = Product.objects.filter(id=product_value)
                order_details_create = {}
                order_details_create['order_id'] = order_id
                order_details_create['product_id'] = product_value
                order_details_create['quantity'] = product_quantity
                total_price = float(product[0].price) * float(product_quantity)
                order_details_create['price'] = float(total_price)

                order_details_create_serializer = OrderDetailSerializer(
                    data=order_details_create, context={'request': request})

                order_details_create_serializer.is_valid(raise_exception=True)
                order_details_create_serializer.save()

            dict_response = {
                'error': False,
                'message': 'order create successfully'
            }
            return Response(dict_response, status=status.HTTP_201_CREATED)
        else:
            dict_response = {
                'error': True,
                'message': 'order not create'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusChangeViewSet(ViewSet):

    def update(self, request, pk=None):
        user = User.objects.filter(id=pk, is_superuser=True)
        if len(user) != 0:
            order_status = request.data['order_status']
            order_id = request.data['order_id']
            order = Order.objects.filter(id=order_id)
            if len(order) != 0:
                order = order[0]
                print('order = ', order)
                print('order id = ', order.id)
                if order_status == 'delivered':
                    order_details = OrderDetails.objects.filter(order_id=order.id)
                    print('order_details = ', order_details)
                    if len(order_details) != 0:
                        for o in range(0, len(order_details)):
                            order_detail = order_details[o]
                            order_detail_product_id = order_detail.product_id.id
                            order_detail_quantity = order_detail.quantity
                            product = Product.objects.get(id=order_detail_product_id)
                            if product.stock >= order_detail_quantity:
                                print('if condition work')
                                available_stock = product.stock - order_detail_quantity
                                product.stock = available_stock
                                product.save()
                                order_detail.is_delivered = True
                                order_detail.save()
                            else:
                                order_detail.is_delivered = False
                                order_detail.save()
                            print('order_detail_product_id = ', order_detail_product_id)
                            print('order_detail_quantity = ', order_detail_quantity)
                            print('order_details = ', order_detail)
                        order.order_status = 'delivered'
                        order.save()
                else:
                    order.order_status = 'returned'
                    order.save()
            dict_response = {
                'error': False,
                'message': 'order status change'
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)


class AdminViewAllOrderList(ViewSet):

    def retrieve(self, request, pk=None):
        user = User.objects.filter(id=pk, is_superuser=True)
        if len(user) != 0:
            order = Order.objects.all()
            order_serializer = AdminViewOrderListSerializer(order, many=True)
            dict_response = {
                'error': False,
                'message': 'all order list',
                'data': order_serializer.data
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(ViewSet):

    def list(self, request):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.filter(id=user_id, is_superuser=True)
        if len(user) != 0:
            product = Product.objects.all()
            product_serializer = ProductSerializer(product, many=True)
            dict_response = {
                'error': False,
                'message': 'product data list',
                'data': product_serializer.data
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.filter(id=user_id, is_superuser=True)
        if len(user) != 0:
            name = request.data['name']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            stock = request.data['stock']
            price = request.data['price']
            if name == '':
                dict_response = {
                    'error': True,
                    'message': 'product name required'
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
            if image1 == '' and image2 == '':
                dict_response = {
                    'error': True,
                    'message': 'image required'
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
            if stock == '':
                dict_response = {
                    'error': True,
                    'message': 'stock required'
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
            if price == '':
                dict_response = {
                    'error': True,
                    'message': 'stock required'
                }
                return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

            product_create = {}
            product_create['name'] = name
            product_create['image1'] = image1
            product_create['image2'] = image2
            product_create['stock'] = stock
            product_create['price'] = price

            product_create_serializer = ProductSerializer(data=product_create, context={'request': request})
            product_create_serializer.is_valid(raise_exception=True)
            product_create_serializer.save()

            dict_response = {
                'error': False,
                'message': 'product create successfully'
            }
            return Response(dict_response, status=status.HTTP_201_CREATED)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.filter(id=user_id, is_superuser=True)
        if len(user) != 0:
            product = Product.objects.filter(id=pk)
            product_serializer = ProductSerializer(product[0])
            dict_response = {
                'error': False,
                'message': 'product retrieve data',
                'data': product_serializer.data
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        print('request data = ', request.data)
        user_id = self.request.query_params.get('user_id')
        user = User.objects.filter(id=user_id, is_superuser=True)
        if len(user) != 0:
            product = Product.objects.filter(id=pk)
            name = request.data['name']
            image1 = request.data['image1']
            image2 = request.data['image2']
            stock = request.data['stock']
            price = request.data['price']
            order_update = {}
            if name == '':
                order_update['name'] = product[0].name
            else:
                order_update['name'] = name
            if image1 == '':
                pass
            else:
                order_update['image1'] = image1
            if image2 == '':
                pass
            else:
                order_update['image2'] = image2
            if stock == '':
                order_update['stock'] = product[0].stock
            else:
                order_update['stock'] = stock
            if price == '':
                order_update['price'] = product[0].price
            else:
                order_update['price'] = price
            product_update_serializer = ProductSerializer(product[0], data=order_update, partial=True, context={'request': request})
            product_update_serializer.is_valid(raise_exception=True)
            product_update_serializer.save()

            dict_response = {
                'error': False,
                'message': 'product update successfully',
                'data': product_update_serializer.data
            }
            return Response(dict_response, status=status.HTTP_201_CREATED)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_id = self.request.query_params.get('user_id')
        user = User.objects.filter(id=user_id, is_superuser=True)
        if len(user) != 0:
            product = Product.objects.filter(id=pk)
            product[0].delete()
            dict_response = {
                'error': False,
                'message': 'product deleted'
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'you are not admin'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
