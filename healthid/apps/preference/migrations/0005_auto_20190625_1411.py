# Generated by Django 2.1.7 on 2019-06-25 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import healthid.utils.app_utils.id_generator


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20190523_1327'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('outlets', '0006_remove_outlet_preference'),
        ('preference', '0004_auto_20190523_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessPreference',
            fields=[
                ('id', models.CharField(default=healthid.utils.app_utils.id_generator.id_gen, editable=False, max_length=9, primary_key=True, serialize=False)),
                ('email_preference', models.BooleanField(default=False)),
                ('barcode_preference', models.BooleanField(default=False)),
                ('reorder_point', models.IntegerField(default=3)),
                ('reorder_max', models.IntegerField(default=6)),
                ('retain_user', models.BooleanField(default=True)),
                ('sales_hold', models.IntegerField(default=7)),
                ('sell_inventory_notification', models.BooleanField(default=False)),
                ('payment_method', models.TextField(default='cash')),
                ('minimum_weeks_for_sales_velocity', models.IntegerField(default=1)),
                ('sales_velocity', models.IntegerField(default=1)),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutletPreference',
            fields=[
                ('id', models.CharField(default=healthid.utils.app_utils.id_generator.id_gen, editable=False, max_length=9, primary_key=True, serialize=False)),
                ('email_preference', models.BooleanField(default=False)),
                ('barcode_preference', models.BooleanField(default=False)),
                ('reorder_point', models.IntegerField(default=3)),
                ('reorder_max', models.IntegerField(default=6)),
                ('retain_user', models.BooleanField(default=True)),
                ('sales_hold', models.IntegerField(default=7)),
                ('sell_inventory_notification', models.BooleanField(default=False)),
                ('payment_method', models.TextField(default='cash')),
                ('minimum_weeks_for_sales_velocity', models.IntegerField(default=1)),
                ('sales_velocity', models.IntegerField(default=1)),
                ('outlet', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='outlets.Outlet')),
                ('outlet_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preference.Currency')),
                ('outlet_timezone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preference.Timezone')),
                ('vat_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preference.Vat')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='preference',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='preference',
            name='outlet_currency',
        ),
        migrations.RemoveField(
            model_name='preference',
            name='outlet_timezone',
        ),
        migrations.RemoveField(
            model_name='preference',
            name='vat_rate',
        ),
        migrations.DeleteModel(
            name='Preference',
        ),
    ]
