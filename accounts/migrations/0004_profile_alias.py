# Generated by Django 3.0.7 on 2020-07-23 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='alias',
            field=models.CharField(blank=True, max_length=75, unique=True),
        ),
    ]