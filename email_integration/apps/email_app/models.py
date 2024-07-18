from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email_login, email_password=None, **extra_fields):
        if not email_login:
            raise ValueError('The Email Login field must be set')
        email_login = self.normalize_email(email_login)
        user = self.model(email_login=email_login, **extra_fields)
        user.set_password(email_password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_login, email_password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email_login, email_password, **extra_fields)


class EmailUserAccount(AbstractBaseUser):
    email_login = models.EmailField(unique=True)
    email_password = models.CharField(max_length=128, verbose_name='email password')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email_login'
    REQUIRED_FIELDS = ['email_password']

    def __str__(self):
        return self.email_login

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return self.user_permissions.filter(content_type__app_label=app_label).exists()

    def has_perm(self, perm):
        if self.is_superuser:
            return True
        return self.user_permissions.filter(codename=perm).exists()

    class Meta:
        verbose_name = 'EmailUserAccount'
        verbose_name_plural = 'EmailUserAccounts'


class EmailMessage(models.Model):
    EMAIL_SERVICE_CHOICES = [
        ('imap.yandex.ru', 'Yandex'),
        ('imap.gmail.com', 'Gmail'),
        ('imap.mail.ru', 'Mail.ru'),
    ]

    user = models.ForeignKey(EmailUserAccount, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, verbose_name='Subject')
    sent_at = models.DateTimeField(verbose_name='Sent Date')
    received_at = models.DateTimeField(verbose_name='Received Date', default=timezone.now)
    body = models.TextField(verbose_name='Body')
    to_email = models.CharField(max_length=256, verbose_name='Email to')
    from_email = models.CharField(max_length=256, verbose_name='Email from')
    attachments = models.JSONField(default=list, verbose_name='Attachments in json')
    email_service = models.CharField(max_length=50, choices=EMAIL_SERVICE_CHOICES, verbose_name='Email Service')

    def __str__(self):
        return f'{self.subject} ({self.email_service})'
