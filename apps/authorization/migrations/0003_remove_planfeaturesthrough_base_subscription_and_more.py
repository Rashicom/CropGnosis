# Generated by Django 5.0.2 on 2024-04-21 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_initial'),
        ('subscription', '0002_accountsubscription_mentorbasesubscriptionplans_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planfeaturesthrough',
            name='base_subscription',
        ),
        migrations.RemoveField(
            model_name='mentorbasesubscriptionplans',
            name='mentor',
        ),
        migrations.RemoveField(
            model_name='mentorsubscriptions',
            name='mentor_base_plan',
        ),
        migrations.RemoveField(
            model_name='mentorsubscriptions',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='mentorsubscriptions',
            name='mentor',
        ),
        migrations.RemoveField(
            model_name='planfeaturesthrough',
            name='subscription_features',
        ),
        migrations.DeleteModel(
            name='AccountSubscription',
        ),
        migrations.DeleteModel(
            name='MentorBaseSubscriptionPlans',
        ),
        migrations.DeleteModel(
            name='MentorSubscriptions',
        ),
        migrations.DeleteModel(
            name='PlanFeaturesThrough',
        ),
    ]