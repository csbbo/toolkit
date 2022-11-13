# Generated by Django 4.1.3 on 2022-11-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('key', models.CharField(db_index=True, max_length=20, unique=True)),
                ('value', models.TextField()),
                ('category', models.CharField(max_length=20, null=True)),
                ('remark', models.TextField(default='')),
            ],
            options={
                'ordering': ('-update_time',),
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('type', models.IntegerField()),
                ('info', models.JSONField(default=dict)),
            ],
            options={
                'ordering': ('-create_time',),
            },
        ),
    ]
