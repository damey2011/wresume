# Generated by Django 2.2.4 on 2019-08-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0005_template_gjs_components'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='template_path',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='template',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]