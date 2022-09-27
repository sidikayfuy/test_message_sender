# Generated by Django 4.1.1 on 2022-09-23 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=250)),
                ('tag', models.CharField(max_length=50)),
                ('time_zone', models.CharField(choices=[('GMT+3', 'Москва'), ('GMT+10', 'Владивосток')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MailList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField()),
                ('text', models.CharField(max_length=250)),
                ('filter_client', models.CharField(max_length=50)),
                ('date_stop', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField()),
                ('status', models.BooleanField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messageapi.client')),
                ('mail_list_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messageapi.maillist')),
            ],
        ),
    ]
