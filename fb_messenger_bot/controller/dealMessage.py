from model.restaurant import *
from model.userProfile import *
import datetime

class DealMessage(object):
    """docstring for DealMessage"""
    def __init__(self, sender):
        self.catalog = None
        self.sender = sender
        self.min_cost = 0
        self.max_cost = None
        self.location = None
        self.distance = 100

    def set_catalog(self, cata):
        self.catalog = "[" + cata + "]"

    def set_cost(self, min_cost=0, max_cost=100):
        self.min_cost = min_cost
        self.max_cost = max_cost

    def set_location(self, location):
        self.location = location

    def set_distance(self, distance):
        self.distance = distance

    def get_restaurant(self, limit=10):
        result = None
        if self.location is not None:
            if self.catalog is not None:
                if self.max_cost is None:
                    result = Restaurant.objects.search_by_catalog(self.location, self.catalog, self.distance)[:limit]
                else:
                    result = Restaurant.objects.search_by_avgCost_catalog(self.location, self.catalog, self.min_cost,
                                                                  self.max_cost, self.distance)[:limit]
            else :
                if self.max_cost is None:
                    result = Restaurant.objects.search_by_address(self.location, self.distance)[:limit]
                else:
                    result = Restaurant.objects.search_by_avgCost(self.location, self.min_cost,
                                                                  self.max_cost, self.distance)[:limit]
        return result

    def get_all_catalog(self):
        return Restaurant.objects.get_catalog()

    def save_search_set(self):
        UserProfile.objects.insert_or_update(self.sender, [self.min_cost, self.max_cost],
                                             self.catalog, self.location, self.distance)
    
