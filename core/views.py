import haversine as hs
from django.db.models import Sum

from rest_framework import status as HTTPStatusCode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fastai.vision.all import *
# Local
from .enum import *
from .models import *
from .serializer import *

garbage_model = load_learner("export.pkl")

co2_in_grams_per_kwh = 371.2

co2_in_kg_per_waste_type = {
  "plastic": {
    "emissionperkg": 6.5
  },
  "cardboard": {
    "emissionperkg": 1.75
  },
  "paper": {
    "emissionperkg": 1.5
  },
  "glass": {
    "emissionperkg": 1.85
  },
  "aluminum": {
    "emissionperkg": 12
  },
  "steel": {
    "emissionperkg": 2
  },
  "cotton (textiles)": {
    "emissionperkg": 5
  },
  "food waste": {
    "emissionperkg": 1.5
  },
  "organic matter (compost)": {
    "emissionperkg": 0.3
  },
  "e-waste (electronic waste)": {
    "emissionperkg": 100
  }
}


co2_in_grams_per_mile ={
  "walk": 5,
  "bike": 12.5,
  "gasoline-car": 120,
  "diesel-car": 171,
  "electric-car": 107,
  "bus": 6.25,
  "flight": 83.125
}

co2_in_grams_per_gram_of_food = {
  "beef": 18.36,
  "lamb": 11.95,
  "goat": 6.42,
  "pork": 9.75,
  "cod": 0.55,
  "farmed trout": 1.76,
  "fish": 1.5,
  "herring": 0.29,
  "mackerel": 0.1,
  "roe": 0.29,
  "salmon": 0.82,
  "sardine": 0.29,
  "seabass": 0.82,
  "tuna": 1.47,
  "wild trout": 1.5,
  "crab": 0.05,
  "lobster": 9.17,
  "mussels": 0.05,
  "octopus": 4.5,
  "oyster": 0.05,
  "scallop": 0.05,
  "shrimp": 1.37,
  "squid": 4.5,
  "chicken": 1.28,
  "duck": 1.28,
  "squab": 1.28,
  "quail": 1.28,
  "apple": 0.24,
  "pear": 0.24,
  "avocado": 0.4,
  "banana": 0.33,
  "berrie": 0.55,
  "citrus": 0.33,
  "dried": 2.67,
  "candied fruits": 2.67,
  "fig": 0.33,
  "grape": 0.55,
  "melon": 0.33,
  "pomegranate": 0.33,
  "rhubarb": 0.22,
  "stoned fruit": 0.55,
  "tropical fruit": 0.33,
  "watermelon": 0.33,
  "artichoke": 0.97,
  "asparagus": 3.17,
  "bamboo shoot": 3.17,
  "beets": 0.4,
  "brassica": 0.97,
  "broccoli": 0.97,
  "cauliflower": 0.97,
  "brussel sprout": 0.97,
  "celery": 0.4,
  "chicory": 0.4,
  "corn": 0.26,
  "cucumber": 0.33,
  "fennel": 0.97,
  "eggplant": 0.97,
  "fresh beans": 0.26,
  "garlic": 0.22,
  "herbs": 0.97,
  "kale": 0.97,
  "leeks": 0.22,
  "lettuce": 0.4,
  "mushrooms": 3.17,
  "okra": 3.17,
  "onions": 0.22,
  "pickled vegetable": 1.19,
  "potato": 0.22,
  "radish": 0.4,
  "spinach": 0.4,
  "squash": 0.22,
  "pumpkin": 0.22,
  "tomato": 0.33,
  "truffle": 3.17,
  "yam": 0.22,
  "sweet potato": 0.22,
  "yucca": 0.22,
  "taro": 0.22,
  "root": 0.22,
  "zucchini": 0.26,
  "barley": 0.64,
  "beans": 1.21,
  "chickpeas": 1.21,
  "lentils": 1.21,
  "bread": 0.84,
  "buckwheat": 0.66,
  "cassava": 0.82,
  "tapioca": 0.82,
  "couscous": 1.01,
  "flour": 0.82,
  "maize": 0.66,
  "oats": 0.57,
  "pasta": 1.01,
  "noodles": 1.01,
  "quinoa": 0.66,
  "rice": 2.93,
  "rye": 0.66,
  "soybeans": 1.3,
  "butter": 9.66,
  "cheese": 12.13,
  "cream": 4.56,
  "egg": 4.25,
  "ice cream": 1.08,
  "margarine": 1.04,
  "yogurt": 2.71,
  "sour cream": 2.71,
  "animal fat": 9.68,
  "chocolate": 2.82,
  "cocoa powder": 0.33,
  "curd": 1.17,
  "herbs": 6.53,
  "honey": 1.17,
  "jam": 1.17,
  "marmalade": 1.17,
  "mustard": 1.19,
  "nut butter": 1.17,
  "pepper": 6.53,
  "salad dressing": 1.19,
  "salt": 1.21,
  "soy based meat": 3.04,
  "spices": 6.53,
  "spreadable oil": 7.41,
  "stock": 1.21,
  "sweetener": 0.84,
  "syrup": 0.82,
  "tofu": 3.04,
  "vegetable oil": 3.53,
  "vinegar": 1.21,
  "yeast": 0.84
}


@api_view(['POST'])
def submit_food_activity(request):
    data: dict = request.data
    uid = data.get("uid")
    action_type = ActionType.LOG_FOOD.value
    action_status = ActionStatus.COMPLETED.value
    probable_food_category_list: str = data.get("food_category_list", "").lower().strip()
    probable_food_item_list: str = data.get("probable_food_item_list", "").lower().strip()
    probable_food_category_list = probable_food_category_list.split(",")
    probable_food_item_list = probable_food_item_list.split(",")
    
    quantity_in_grams = data.get("quantity_in_grams", 1)
    carbon_footprint = 0
    if len(probable_food_item_list) > 0:
        for food_item in probable_food_item_list:
            food_item = food_item.strip()
            for key, val in co2_in_grams_per_gram_of_food.items():
                if food_item in key:
                    carbon_footprint = val
                    break

    if carbon_footprint == 0:
        if len(probable_food_category_list) > 0:
            for food_item in probable_food_category_list:
                food_item = food_item.strip()
                for key, val in co2_in_grams_per_gram_of_food.items():
                    if food_item in key:
                        carbon_footprint = val
                        break

    if carbon_footprint <= 0: carbon_footprint = 1
    total_carbon_footprint = carbon_footprint * quantity_in_grams

    user_instance = User.objects.get(uid=uid)
    action_instance = Action.objects.create(
        user=user_instance,
        action_type=action_type,
        action_status=action_status,
        carbon_footprint=total_carbon_footprint,
        weight=quantity_in_grams,
    )
    serialized_data = ActionSerializer(action_instance).data

    return Response(serialized_data, status=HTTPStatusCode.HTTP_201_CREATED)



@api_view(['POST'])
def submit_transit_activity(request):
    data: dict = request.data
    uid = data.get("uid")
    
    action_type = data.get("action_type")
    if action_type == "WALK":
        action_type = ActionType.LOG_WALK.value
        carbon_footprint = co2_in_grams_per_mile["walk"]
    elif action_type == "BIKE":
        action_type = ActionType.LOG_BIKE_RIDE.value
        carbon_footprint = co2_in_grams_per_mile["bike"]
    elif action_type == "CAR_EV":
        action_type = ActionType.LOG_CAR_EV.value
        carbon_footprint = co2_in_grams_per_mile["electric-car"]
    elif action_type == "CAR_GAS":
        action_type = ActionType.LOG_CAR_GAS.value
        carbon_footprint = co2_in_grams_per_mile["gasoline-car"]
    elif action_type == "BUS":
        action_type = ActionType.LOG_BUS.value
        carbon_footprint = co2_in_grams_per_mile["bus"]
    else:
        action_type = ActionType.LOG_FLIGHT.value
        carbon_footprint = co2_in_grams_per_mile["flight"]
    
    action_status = ActionStatus.COMPLETED.value
    origin_lat = data.get("origin").get("lat")
    origin_lng = data.get("origin").get("lng")
    destination_lat = data.get("destination").get("lat")
    destination_lng = data.get("destination").get("lng")
    distance_in_miles = hs.haversine((origin_lat, origin_lng), (destination_lat, destination_lng), unit=hs.Unit.MILES)
    total_carbon_footprint = carbon_footprint * distance_in_miles

    user_instance = User.objects.get(uid=uid)
    action_instance = Action.objects.create(
        user=user_instance,
        action_type=action_type,
        action_status=action_status,
        carbon_footprint=total_carbon_footprint,
        weight=distance_in_miles,
        source_location=f"{origin_lat},{origin_lng}",
        destination_location=f"{destination_lat},{destination_lng}",
    )
    serializer_data = ActionSerializer(action_instance).data

    return Response(serializer_data, status=HTTPStatusCode.HTTP_201_CREATED)


@api_view(["POST"])
def submit_power_bill_activity(request):
    data: dict = request.data
    uid = data.get("uid")
    kwh = data.get("kwh")

    action_type = ActionType.LOG_POWER_BILL.value
    action_status = ActionStatus.COMPLETED.value
    carbon_footprint = kwh * co2_in_grams_per_kwh

    user_instance = User.objects.get(uid=uid)
    action_instance = Action.objects.create(
        user=user_instance,
        action_type=action_type,
        action_status=action_status,
        carbon_footprint=carbon_footprint,
        energy=kwh,
    )
    serializer_data = ActionSerializer(action_instance).data
    return Response(serializer_data, status=HTTPStatusCode.HTTP_201_CREATED)


@api_view(["POST"])
def submit_recycling_activity(request):
    data: dict = request.data
    uid = data.get("uid")
    image_link = data.get("image_url")
    quantity_in_grams = data.get("quantity_in_grams", 1)
    quantity_in_kg = quantity_in_grams / 1000
    net_carbon_footprint = 0
    pred, idx, prob = garbage_model.predict(PILImage.create(urlopen(image_link)))
    if pred is not None:
        for key, val in co2_in_kg_per_waste_type.items():
            if str(pred).lower() in str(key).lower():
                carbon_footprint = val.get("emissionperkg")
                net_carbon_footprint = carbon_footprint * quantity_in_kg
                break
    Action.objects.create(
        user=User.objects.get(uid=uid),
        action_type=ActionType.LOG_RECYCLING.value,
        action_status=ActionStatus.COMPLETED.value,
        carbon_footprint=net_carbon_footprint,
        weight=quantity_in_grams,
    )
    return Response({"prediction": pred, "probability": float(prob[0]), "carbon_footprint": net_carbon_footprint,}, status=HTTPStatusCode.HTTP_200_OK)


@api_view(["GET"])
def get_user_activities(request):
    uid = request.GET.get("uid")
    action_instance_list = Action.objects.filter(user__uid=uid).order_by("-id")
    serializer_data = ActionSerializer(action_instance_list, many=True).data
    return Response(serializer_data, status=HTTPStatusCode.HTTP_200_OK)


@api_view(["POST"])
def host_carpool_task(request):
    data = request.data
    uid = data.get("uid")
    source_location = data.get("source_location")
    destination_location = data.get("destination_location")
    seats_available = data.get("seats_available")
    allowed_genders = data.get("allowed_genders")
    is_wheelchair_accessible = data.get("is_wheelchair_accessible")
    
    user_instance = User.objects.get(uid=uid)
    if CarpoolTask.objects.filter(user__uid=uid, active=True).exists():
        return Response(
            {"message": "You are already actively hosting a car-pool"},
            status=HTTPStatusCode.HTTP_400_BAD_REQUEST,
        )

    carpool_task_instance = CarpoolTask.objects.create(
        user=user_instance,
        active=True,
        source_location=source_location,
        destination_location=destination_location,
        seats_available=seats_available,
        allowed_genders=allowed_genders,
        pool_uid_list="",
        is_wheelchair_accessible=is_wheelchair_accessible,
    )
    serializer_data = CarpoolTaskSerializer(carpool_task_instance).data
    return Response(serializer_data, status=HTTPStatusCode.HTTP_201_CREATED)


@api_view(["GET"])
def get_active_carpool_hosting(request):
    uid = request.GET.get("uid")
    carpool_task_instance_list = CarpoolTask.objects.filter(user__uid=uid, active=True).last()
    serializer_data = CarpoolTaskSerializer(carpool_task_instance_list).data
    return Response(serializer_data, status=HTTPStatusCode.HTTP_200_OK)


@api_view(["GET"])
def get_leaderboard(request):
    user_total_co2_footprint_dict_list = Action.objects.filter(action_status=ActionStatus.COMPLETED.value).values("user").order_by("user").annotate(total_carbon_footprint=Sum("carbon_footprint"))
    user_total_co2_footprint_dict_list = list(user_total_co2_footprint_dict_list)
    uid_list = [user_total_co2_footprint_dict.get("user") for user_total_co2_footprint_dict in user_total_co2_footprint_dict_list]
    user_instance_list = User.objects.filter(uid__in=uid_list)
    user_instance_dict = {user_instance.uid: dict(UserSerializer(user_instance).data) for user_instance in user_instance_list}
    for idx, val in enumerate(user_total_co2_footprint_dict_list):
        user_total_co2_footprint_dict_list[idx]["user"] = user_instance_dict.get(val.get("user"))
    return Response(user_total_co2_footprint_dict_list, status=HTTPStatusCode.HTTP_200_OK)
