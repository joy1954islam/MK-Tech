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

        if search_key:
            product_search = Product.objects.filter(
                name__icontains=search_key
            )
            print('product_search = ', product_search)
            product_search_serializer = ProductSerializer(product_search, many=True)
            dict_response = {
                'error': False,
                'message': 'search result found',
                'data': product_search_serializer.data,
                'total_found': product_search.count()
            }
            return Response(dict_response, status=status.HTTP_200_OK)
        else:
            dict_response = {
                'error': True,
                'message': 'search key required'
            }
            return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)