# Generated by Django 5.1.4 on 2024-12-19 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['username'], name='user_user_usernam_6d9439_idx'), models.Index(fields=['email'], name='user_user_email_5f6a77_idx')],
            },
        ),
        migrations.CreateModel(
            name='UserConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_notifications_enabled', models.BooleanField(default=True, verbose_name='Email Notifications')),
                ('check_interval', models.IntegerField(choices=[(30, 'Every 30 seconds'), (60, 'Every minute'), (300, 'Every 5 minutes'), (600, 'Every 10 minutes')], default=30, verbose_name='Check Interval')),
                ('response_timeout', models.PositiveIntegerField(default=5, verbose_name='Response Timeout (seconds)')),
                ('log_retention_days', models.PositiveIntegerField(default=7, verbose_name='Log Retention (days)')),
                ('alert_threshold', models.PositiveIntegerField(default=90, verbose_name='Alert Threshold (%)')),
                ('notification_cooldown', models.PositiveIntegerField(default=300, verbose_name='Notification Cooldown (seconds)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='user.user')),
            ],
            options={
                'verbose_name': 'User Configuration',
                'verbose_name_plural': 'User Configurations',
                'indexes': [models.Index(fields=['user'], name='user_userco_user_id_856c97_idx')],
            },
        ),
    ]
