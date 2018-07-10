# Generated by Django 2.0.1 on 2018-06-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_testcase_protocol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='protocol',
        ),
        migrations.AddField(
            model_name='testserver',
            name='protocol',
            field=models.CharField(default='http', max_length=50),
            preserve_default=False,
        ),
    ]