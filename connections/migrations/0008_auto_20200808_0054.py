# Generated by Django 3.0.7 on 2020-08-08 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connections', '0007_auto_20200806_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='address',
            field=models.EmailField(default='ZtFuFa-Enq4@outtaoffice.work', max_length=254, unique=True),
        ),
    ]
