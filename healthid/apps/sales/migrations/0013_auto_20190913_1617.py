# Generated by Django 2.2 on 2019-09-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_batchhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Credit', 'Credit')], max_length=6),
        ),
    ]
