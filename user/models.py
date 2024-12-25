from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
            
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Added this field
    is_superuser = models.BooleanField(default=False)  # Added this field
    is_subscribed = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email'])
        ]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class UserConfig(models.Model):
    INTERVAL_CHOICES = [
        (30, 'Every 30 seconds'),
        (60, 'Every minute'),
        (300, 'Every 5 minutes'),
        (600, 'Every 10 minutes')
    ]
   
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='config')
    email_notifications_enabled = models.BooleanField('Email Notifications', default=True)
    check_interval = models.IntegerField('Check Interval', choices=INTERVAL_CHOICES, default=30)
    response_timeout = models.PositiveIntegerField('Response Timeout (seconds)', default=5)
    log_retention_days = models.PositiveIntegerField('Log Retention (days)', default=7)
    alert_threshold = models.PositiveIntegerField('Alert Threshold (%)', default=90)
    notification_cooldown = models.PositiveIntegerField('Notification Cooldown (seconds)', default=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Configuration'
        verbose_name_plural = 'User Configurations'
        indexes = [models.Index(fields=['user'])]

    @property
    def notification_email(self):
        return self.user.email

    def get_notification_email(self):
        return self.user.email

    def __str__(self):
        return f"{self.user.username}"