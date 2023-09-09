from django.urls import path
# Local
from .views import *

urlpatterns = [
    path("submit-food-activity/", submit_food_activity, name="submit_food_activity"),
    path("submit-transit-activity/", submit_transit_activity, name="submit_transit_activity"),
    path("submit-power-bill-activity/", submit_power_bill_activity, name="submit_power_bill_activity"),
    path("get-user-activities/", get_user_activities, name="get_user_activities"),
]
