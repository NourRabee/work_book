import json

from django.core.exceptions import BadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workbook.components.sign_in_service import SignInService
from workbook.components.sign_up_service import SignUpService
from workbook.serializers.sign_up_serializer import SignUpSerializer


class SignInView(APIView):
    def __init__(self):
        self.sign_in_service = SignInService()

    def post(self, request):
        session_id = request.GET.get('sid')

        if not session_id:
            email = request.data.get('email')
            password = request.data.get('password')
            result = self.sign_in_service.authenticate_user(email, password)
        else:
            result = self.sign_in_service.authenticate_session(session_id)

        if result:
            return Response({"token": result})
        else:
            return Response({"message": "Sign in again"}, status=401)  # Return a 401 status if authentication fails


class SignUpView(APIView):
    def __init__(self):
        self.sign_up_service = SignUpService()

    def post(self, request):
        data = json.loads(request.body)

        email_validation_result = self.sign_up_service.email_existence_check(data['email'])

        if email_validation_result:
            raise BadRequest(email_validation_result)

        user_serializer = SignUpSerializer(data=data)

        user_serializer.is_valid_raise()

        created_user = self.sign_up_service.create(user_serializer)

        return Response(created_user, status=status.HTTP_201_CREATED)
