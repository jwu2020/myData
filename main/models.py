from django.forms import Field
from djongo import models
from django import forms
import uuid
from django.utils import timezone


class Notification(models.Model):
    type = models.CharField(max_length=20, null=True)
    message = models.CharField(max_length=200, null=True)

    time_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True


class Data(models.Model):
    raw_data = models.CharField(max_length=2000)
    spent_minutes = models.FloatField()
    timestamp_epoch = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.raw_data)


class FacebookEntry(models.Model):
    total_minutes = models.IntegerField(default=0)
    message_minutes = models.IntegerField(default=0)
    posts_minutes = models.IntegerField(default=0)
    comments_minutes = models.IntegerField(default=0)
    likes_minutes = models.IntegerField(default=0)
    groups_minutes = models.IntegerField(default=0)
    other_minutes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.total_minutes


class YTEntry(models.Model):
    total_minutes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.total_minutes


class GoogleEntry(models.Model):
    total_minutes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return  self.total_minutes


class NetflixEntry(models.Model):
    total_minutes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.total_minutes


class SummaryStats(models.Model):
    timestamp = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    fb = models.EmbeddedModelField(model_container=FacebookEntry)
    yt = models.EmbeddedModelField(model_container=YTEntry)
    netflix = models.EmbeddedModelField(model_container=GoogleEntry)
    google = models.EmbeddedModelField(model_container=NetflixEntry)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.timestamp)


class LinkedPlatform(models.Model):
    platform = models.CharField(max_length=200)
    goal = models.IntegerField()
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    link = models.BooleanField(default=True)

    data = models.ArrayModelField(
        model_container=Data,
        null=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.platform


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    linked_platforms = models.ArrayModelField(
        model_container=LinkedPlatform,
        null=True
    )

    notifications = models.ArrayModelField(
        model_container=Notification,
        null=True
    )

    summary_stats = models.ArrayModelField(
        model_container=SummaryStats,
        null=True
    )

    def __str__(self):
        return "UID: " + str(self.uid) + ", Username: " + self.username + ", Password: " + self.password
