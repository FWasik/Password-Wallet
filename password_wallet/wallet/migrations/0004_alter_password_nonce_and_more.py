# Generated by Django 4.1.2 on 2022-10-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_password_nonce_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='password',
            name='nonce',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='password',
            name='password_to_wallet',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='password',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
