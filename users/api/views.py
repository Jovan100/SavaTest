from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, PasswordReset
from users.api.serializers import UserSerializer, PasswordResetSerializer
from users.api.permissions import IsAdminOrOwner
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid
import os

class GenericModelViewSet(ModelViewSet):
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

class UserViewSet(GenericModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [IsAdminOrOwner],
        'partial_update': [IsAdminOrOwner],
        'destroy': [IsAdminOrOwner]
    }


class PasswordResetViewSet(GenericModelViewSet):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'retireve': [AllowAny],
        'partial_update': [AllowAny]
    }

    def retrieve(self, request, pk=None, **kwargs):
        queryset = PasswordReset.objects.all()
        reset = get_object_or_404(queryset, pk=pk)
        print(datetime.now().date())
        print(reset.created_at.date())
        print(timedelta(hours=2))
        print(datetime.now().date() - reset.created_at.date())
        if datetime.now().date() - reset.created_at.date() > timedelta(days=2):
            return Response(status=403)
        serializer = PasswordResetSerializer(reset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {'email': request.data['email'], 'token': str(uuid.uuid4())}
        serialized = PasswordResetSerializer(data=data)
        user = []
        try:
            user = User.objects.filter(email=data['email'])
        except:
            pass
        if serialized.is_valid() and len(user):
            serialized.save()
            send_email(data)
            return Response(serialized.data, status=201)
        else:
            return Response(serialized.errors, status=201)

    def partial_update(self, request, *args, **kwargs):
        queryset = PasswordReset.objects.all()
        email_object = get_object_or_404(queryset, token=request.data['token'])
        if datetime.now().date() - email_object.created_at.date() < timedelta(hours=2):
            email_object = PasswordResetSerializer(email_object)
            user = User.objects.get(email=email_object.data['email'])
            new_data = {
                "password": request.data['password']
            }
            user = UserSerializer(user, data=new_data, partial=True)
            if user.is_valid():
                user.save()
                PasswordReset.objects.filter(token=request.data['token']).delete()
                return Response(user.data, status=201)
            else:
                return Response(user.errors, status=201)
            return Response(status=200)
        else:
            return Response(status=403)

def send_email(data):
    message = Mail(
            from_email="jovan@kroonstudio.com",
            to_emails= data['email']
        )

    message.dynamic_template_data = {
        'url': 'http://localhost:8000/forgot-password/' + data['token']
    }

    message.template_id = 'd-583ed325485c46328cf6f7e445819bc9'
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
    except Exception as e:
        print("ERROR: ", e)
