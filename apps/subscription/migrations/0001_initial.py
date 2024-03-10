# Generated by Django 5.0.2 on 2024-03-10 11:45

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EssentialFeatures',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feature', models.CharField(max_length=100)),
                ('remark', models.TextField()),
                ('feature_price', models.FloatField()),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseSubscriptionPlans',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('discription', models.CharField(max_length=150)),
                ('total_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('crop_field_count', models.IntegerField()),
                ('plan_validity', models.IntegerField()),
                ('features', models.ManyToManyField(related_name='base_plan_features', to='subscription.essentialfeatures')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentTransactions',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paid_for', models.CharField(choices=[('BASE_SUBSCRIPTION_PLAN', 'BASE_SUBSCRIPTION_PLAN'), ('ADD_ON_PLAN', 'ADD_ON_PLAN'), ('MENTOR', 'MENTOR'), ('IOT_INTEGRATION', 'IOT_INTEGRATION')], max_length=50)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_pdf', models.FileField(blank=True, max_length=5000, null=True, upload_to='invoices')),
                ('payment_response', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('addon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forme_transactions', to='subscription.essentialfeatures')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_transactions', to=settings.AUTH_USER_MODEL)),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forme_transactions', to=settings.AUTH_USER_MODEL)),
                ('subscription_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchased_set', to='subscription.basesubscriptionplans')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
