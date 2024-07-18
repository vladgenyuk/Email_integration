from rest_framework import serializers

from apps.email_app.models import EmailMessage, EmailUserAccount


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailUserAccount
        fields = ['id', 'email_login', 'email_password']
        extra_kwargs = {'email_password': {'write_only': True}}

    def create(self, validated_data):
        user = EmailUserAccount.objects.create_superuser(
            email_login=validated_data.get('email_login'),
            email_password=validated_data.get('email_password'),
        )
        return user


class EmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = ('id', 'to_email', 'from_email', 'subject', 'body', 'sent_at', 'received_at', 'attachments', 'user')
