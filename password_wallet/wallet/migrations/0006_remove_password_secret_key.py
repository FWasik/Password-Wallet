# Generated by Django 4.1.2 on 2022-10-26 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_remove_password_nonce_remove_password_tag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password',
            name='secret_key',
        ),
    ]
