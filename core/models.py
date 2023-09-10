from django.db import models
from .enum import *

# Abstract Models
class AutoTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class User(AutoTimeStampModel):
    uid = models.CharField(
        max_length=128,
        null=False,
        unique=True,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(
        max_length=128,
        null=False
    )
    email = models.CharField(
        max_length=128,
        null=True,
        default=None,
    )
    phone = models.CharField(
        max_length=10,
        null=True,
        default=None,
    )
    image_url = models.CharField(
        max_length=256,
        null=True,
        default=None,
    )
    points = models.IntegerField(
        null=False,
        default=0
    )
    fcm_token = models.CharField(
        max_length=255,
        null=True,
        default=None,
    )


class Action(AutoTimeStampModel):
    user = models.ForeignKey(
        User,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    action_type = models.CharField(
        max_length=64,
        choices=ActionType.choices(),
        null=True,
        default=None,
    )
    action_status = models.CharField(
        max_length=64,
        choices=ActionStatus.choices(),
        null=True,
        default=None,
    )
    points_rewarded = models.IntegerField(
        null=False,
        default=0
    )
    carbon_footprint = models.IntegerField(
        null=False,
        default=0
    )
    weight = models.FloatField(
        null=True,
        default=None,
    )
    calories = models.FloatField(
        null=True,
        default=None,
    )
    fabric = models.CharField(
        max_length=128,
        null=True,
        default=None
    )
    energy = models.FloatField(
        null=True,
        default=None,
    )
    source_location = models.CharField(
        max_length=128,
        null=True,
        default=None,
    )
    destination_location = models.CharField(
        max_length=128,
        null=True,
        default=None,
    )


class CarpoolTask(AutoTimeStampModel):
    user = models.ForeignKey(
        User,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    active = models.BooleanField(
        null=False,
        default=True
    )
    source_location = models.CharField(
        max_length=128,
        null=True,
        default=None,
    )
    destination_location = models.CharField(
        max_length=128,
        null=True,
        default=None,
    )
    seats_available = models.IntegerField(
        null=False,
        default=1
    )
    allowed_genders = models.CharField(
        max_length=64,
        null=False,
        default="all",
    )
    pool_uid_list = models.CharField(
        max_length=128,
        null=True,
        default=None,
    )
    is_wheelchair_accessible = models.BooleanField(
        null=False,
        default=False
    )
