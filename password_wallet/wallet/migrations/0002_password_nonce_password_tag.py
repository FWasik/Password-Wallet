# Generated by Django 4.1.2 on 2022-10-24 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='password',
            name='nonce',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AddField(
            model_name='password',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]