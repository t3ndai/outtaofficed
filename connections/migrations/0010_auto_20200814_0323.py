# Generated by Django 3.0.7 on 2020-08-14 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200724_2108'),
        ('connections', '0009_auto_20200814_0202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailboxdetail',
            old_name='profile',
            new_name='member',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='creator',
        ),
        migrations.AddField(
            model_name='topicdetail',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topics_created', to='accounts.Profile'),
        ),
        migrations.AlterField(
            model_name='mailbox',
            name='address',
            field=models.EmailField(default='2tmz8X0wbEM@outtaoffice.work', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='mailbox',
            name='members',
            field=models.ManyToManyField(related_name='mailboxes', through='connections.MailboxDetail', to='accounts.Profile'),
        ),
        migrations.AlterField(
            model_name='mailbox',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailboxes_owned', to='accounts.Profile'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='member',
            field=models.ManyToManyField(related_name='topics', through='connections.TopicDetail', to='accounts.Profile'),
        ),
    ]
