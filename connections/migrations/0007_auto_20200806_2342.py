# Generated by Django 3.0.7 on 2020-08-06 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connections', '0006_auto_20200806_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='address',
            field=models.EmailField(default='CaoTdu-ISYk@outtaoffice.work', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(editable=False, max_length=75),
        ),
    ]
