# Generated by Django 3.0.7 on 2020-08-04 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200724_2108'),
        ('connections', '0003_auto_20200803_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='address',
            field=models.EmailField(default='NKppI8aq3Z4@outtaoffice.work', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='mailbox',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailboxes', to='accounts.Profile'),
        ),
    ]
