# Generated by Django 2.2 on 2019-10-07 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preference', '0001_initial'),
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('store_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('credit_currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currency', to='preference.Currency')),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallet', to='profiles.Profile')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreCreditWalletHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('current_store_credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit', to='wallet.CustomerCredit')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sales_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sell_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
