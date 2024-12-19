from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email'])
        ]
    
    def __str__(self):
        return f"{self.username} {self.is_active} {self.is_admin}"

class UserConfig(models.Model):
    INTERVAL_CHOICES = [
        (30, 'Every 30 seconds'),
        (60, 'Every minute'),
        (300, 'Every 5 minutes'),
        (600, 'Every 10 minutes')
    ]
   
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='config')
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