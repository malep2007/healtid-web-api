# Generated by Django 2.2 on 2019-10-07 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import healthid.utils.app_utils.id_generator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '__first__'),
        ('profiles', '0001_initial'),
        ('outlets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('amount_to_pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('change_due', models.DecimalField(decimal_places=2, max_digits=12)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Credit', 'Credit')], max_length=6)),
                ('notes', models.TextField(blank=True, null=True)),
                ('loyalty_earned', models.PositiveIntegerField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.Outlet')),
                ('sales_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SaleReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('return_note', models.CharField(blank=True, max_length=80)),
                ('return_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('refund_compensation_type', models.CharField(max_length=80)),
                ('cashier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cashier', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.Profile')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('outlet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='outlets.Outlet')),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalesPrompt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('prompt_title', models.CharField(max_length=244, unique=True)),
                ('description', models.CharField(default='Sales prompt descripttion:', max_length=244)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.Outlet')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleReturnDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('return_reason', models.CharField(max_length=80)),
                ('is_approved', models.BooleanField(default=False)),
                ('resellable', models.BooleanField(default=False)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product')),
                ('sales_return', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.SaleReturn')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('discount', models.FloatField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('note', models.TextField(blank=True, null=True)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PromotionType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(default=healthid.utils.app_utils.id_generator.id_gen, editable=False, max_length=9, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140, unique=True)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(default=healthid.utils.app_utils.id_generator.id_gen, editable=False, max_length=9, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=140, unique=True)),
                ('description', models.TextField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_approved', models.BooleanField(default=True)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.Outlet')),
                ('products', models.ManyToManyField(blank=True, to='products.Product')),
                ('promotion_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.PromotionType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('item_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='sales.CartItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BatchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('quantity_taken', models.PositiveIntegerField()),
                ('batch_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batch_info_history', to='products.BatchInfo')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quantity_by_batches', to='products.Product')),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_batch_history', to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
