# Generated by Django 3.0.7 on 2020-08-21 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_auto_20200820_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='items.Item'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]