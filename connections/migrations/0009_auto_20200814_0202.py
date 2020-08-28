# Generated by Django 3.0.7 on 2020-08-14 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200724_2108'),
        ('connections', '0008_auto_20200808_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='address',
            field=models.EmailField(default='4fqyXdrmbqg@outtaoffice.work', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topics_created', to='accounts.Profile'),
        ),
    ]
