# Generated by Django 3.2.4 on 2021-07-09 07:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blacklist', models.CharField(db_index=True, max_length=512)),
            ],
            options={
                'db_table': 'blacklist_tokens',
            },
        ),
        migrations.CreateModel(
            name='RegisterTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered', models.CharField(max_length=512)),
                ('user_id', models.IntegerField(unique=True)),
            ],
            options={
                'db_table': 'register_tokens',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(db_index=True, max_length=128)),
                ('lastname', models.CharField(db_index=True, max_length=128)),
                ('email', models.CharField(db_index=True, max_length=255, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2021, 7, 9, 13, 22, 23, 384961), max_length=256)),
            ],
            options={
                'db_table': 'credentials',
            },
        ),
    ]
