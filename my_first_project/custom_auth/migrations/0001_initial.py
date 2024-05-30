# Generated by Django 5.0.2 on 2024-04-24 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PseudoUser',
            fields=[
                ('email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password_hash', models.CharField(max_length=32)),
                ('role', models.CharField(max_length=10)),
                ('role_id', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('date_expired', models.DateTimeField()),
                ('token', models.CharField(max_length=128)),
            ],
        ),
    ]