# Generated by Django 3.0.7 on 2020-07-24 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='alias',
            field=models.CharField(blank=True, max_length=75, null=True, unique=True),
        ),
    ]
