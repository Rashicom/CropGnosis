# Generated by Django 5.0.2 on 2024-03-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounts',
            old_name='is_farm_staff',
            new_name='is_farmer_staff',
        ),
        migrations.AlterField(
            model_name='accounts',
            name='email',
            field=models.EmailField(max_length=150, unique=True),
        ),
    ]
