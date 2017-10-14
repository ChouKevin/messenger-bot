from model.restaurant import *


class DealMessege(object):
    """docstring for DealMessege"""
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
        self.location = set_location

    def set_distance(self, distance):
        self.distance = distance

    def get_restaurant(self):
        result = None
        if self.location is not None:
            if self.catalog is not None:
                if max_cost is None:
                    result = Restaurant.objects.search_by_catalog(self.location, self.catalog, self.distance)
                else:
                    result = Restaurant.objects.search_by_avgCost(self.location, self.catalog, min_cost,
                                                                  max_cost, self.distance)
            else :
                if max_cost is None:
                    result = Restaurant.objects.search_by_address(self.location, self.distance)
                else:
                    result = Restaurant.objects.search_by_avgCost(self.location, min_cost,
                                                                  max_cost, self.distance)
        return result

    def get_all_catalog(self):
        return Restaurant.objects.get_catalog()