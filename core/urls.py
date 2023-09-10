from django.urls import path
# Local
from .views import *

urlpatterns = [
    path("submit-food-activity/", submit_food_activity, name="submit_food_activity"),
    path("submit-transit-activity/", submit_transit_activity, name="submit_transit_activity"),
    path("submit-power-bill-activity/", submit_power_bill_activity, name="submit_power_bill_activity"),
    path("submit-recycling-activity/", submit_recycling_activity, name="submit_recycling_activity"),
    path("get-user-activities/", get_user_activities, name="get_user_activities"),
    path("host-carpool-task/", host_carpool_task, name="host_carpool_task"),
    path("get-active-carpool-hosting/", get_active_carpool_hosting, name="get_active_carpool_hosting"),
    path("get-leaderboard/", get_leaderboard, name="get_leaderboard"),
]
