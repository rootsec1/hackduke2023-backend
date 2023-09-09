from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return sorted(tuple((i.name, i.value) for i in cls))
    

class ActionType(BaseEnum):
    LOG_FOOD = "LOG_FOOD"
    LOG_DELIVERY = "LOG_DELIVERY"
    LOG_RECYCLING = "LOG_RECYCLING"
    SEARCH_CARPOOL = "SEARCH_CARPOOL"
    HOST_CARPOOL = "HOST_CARPOOL"
    LOG_CAR_GAS = "LOG_CAR_GAS"
    LOG_CAR_EV = "LOG_CAR_EV"
    LOG_BIKE_RIDE = "LOG_BIKE_RIDE"
    LOG_FLIGHT = "LOG_FLIGHT"
    LOG_WALK = "LOG_WALK"
    LOG_BUS = "LOG_BUS"
    LOG_POWER_BILL = "LOG_POWER_BILL"

class ActionStatus(BaseEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
