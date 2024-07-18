from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SuperUserSerializer, EmailMessageSerializer
from apps.email_app.models import EmailUserAccount, EmailMessage

User = get_user_model()


class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, email_app!'}, status=status.HTTP_200_OK)


class RegisterSuperUserView(APIView):
    def post(self, request, format=None):
        email_login = request.data.get('email_login')
        try:
            user = EmailUserAccount.objects.get(email_login=email_login)
            return Response(
                {"message": "User already exists.", "user": SuperUserSerializer(user).data},
                status=status.HTTP_200_OK)
        except EmailUserAccount.DoesNotExist:
            serializer = SuperUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {'message': 'User created', 'user': SuperUserSerializer(user).data},
                    status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailMessageListView(APIView):
    def get(self, request, format=None):
        email_messages = EmailMessage.objects.filter(user_id=request.query_params.get('user_id', 1))
        serializer = EmailMessageSerializer(email_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = EmailMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
