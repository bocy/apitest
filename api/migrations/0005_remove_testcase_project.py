# Generated by Django 2.0.1 on 2018-05-26 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_testcase_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='project',
        ),
    ]
