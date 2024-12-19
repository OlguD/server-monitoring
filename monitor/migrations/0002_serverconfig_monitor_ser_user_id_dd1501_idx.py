# Generated by Django 5.1.4 on 2024-12-19 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='serverconfig',
            index=models.Index(fields=['user', 'ip'], name='monitor_ser_user_id_dd1501_idx'),
        ),
    ]