# Generated by Django 2.0.1 on 2018-06-19 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_testsuite_caseids'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsuite',
            name='serverid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
