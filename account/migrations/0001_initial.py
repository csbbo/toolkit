# Generated by Django 4.1.3 on 2022-11-13 06:52

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('username', models.CharField(db_index=True, max_length=120, unique=True)),
                ('phone', models.CharField(db_index=True, max_length=11, unique=True)),
                ('email', models.CharField(db_index=True, max_length=11, unique=True)),
                ('name', models.CharField(default='', max_length=120)),
                ('password', models.CharField(default='', max_length=128)),
                ('signature', models.CharField(default='', max_length=120)),
                ('last_login_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'account_user',
                'ordering': ('-create_time',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
