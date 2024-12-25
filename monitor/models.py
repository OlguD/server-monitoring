from django.db import models

# Create your models here.
class ServerConfig(models.Model):
    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Server Configuration'
        verbose_name_plural = 'Server Configurations'
        indexes = [
            models.Index(fields=['user', 'ip']),
        ]

    def __str__(self):
        return f"{self.name} ({self.ip})"
