# Generated by Django 2.1.7 on 2019-04-29 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outlets', '0004_outlet_preference'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_merge_20190425_0954'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockCountTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('assigned_users', models.ManyToManyField(related_name='assigned_to', to=settings.AUTH_USER_MODEL)),
                ('designated_users', models.ManyToManyField(related_name='designated_to', to=settings.AUTH_USER_MODEL)),
                ('outlet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='outlets.Outlet')),
                ('products', models.ManyToManyField(related_name='products_to_count', to='products.Product')),
                ('schedule_time', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
    ]
