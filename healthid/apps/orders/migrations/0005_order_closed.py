# Generated by Django 2.1.7 on 2019-05-23 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
