# Generated by Django 2.0.1 on 2018-06-25 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20180622_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsuite',
            name='casenames',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
