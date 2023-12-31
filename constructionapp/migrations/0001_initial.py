# Generated by Django 4.1.3 on 2023-09-20 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empname', models.CharField(max_length=50, null=True)),
                ('reason', models.CharField(max_length=100, null=True)),
                ('approval', models.BooleanField(default=False, null=True)),
                ('usr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morning_time', models.TimeField(null=True)),
                ('evening_time', models.TimeField(null=True)),
                ('punch_stat', models.TextField(max_length=50, null=True)),
                ('punch_stat_evening', models.TextField(max_length=50, null=True)),
                ('date', models.DateField(null=True)),
                ('working_hour', models.CharField(max_length=50, null=True)),
                ('difference', models.CharField(max_length=50, null=True)),
                ('usr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
