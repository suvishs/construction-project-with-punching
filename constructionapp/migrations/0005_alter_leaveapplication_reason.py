# Generated by Django 4.1.3 on 2023-09-23 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructionapp', '0004_remove_visitingreport_date_and_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='reason',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
