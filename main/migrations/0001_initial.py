# Generated by Django 2.2.7 on 2019-11-05 09:30

from django.db import migrations, models
import djongo.models.fields
import main.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('linked_platforms', djongo.models.fields.ArrayModelField(model_container=main.models.LinkedPlatform, null=True)),
                ('notifications', djongo.models.fields.ArrayModelField(model_container=main.models.Notification, null=True)),
                ('summary_stats', djongo.models.fields.ArrayModelField(model_container=main.models.SummaryStats, null=True)),
            ],
        ),
    ]