# Generated by Django 2.2.4 on 2019-09-01 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190821_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
