from model.restaurant import *
from model.userProfile import *
from model.restaurantImage import *
import datetime

class DealMessage(object):
    """docstring for DealMessage"""
    def __init__(self, sender):
        self.catalog = None
        self.sender = sender
        self.min_cost = 0
        self.max_cost = 50000
        self.location = None
        self.distance = 100

    def set_catalog(self, cata):
        self.catalog = "[" + cata + "]"

    def set_cost(self, min_cost=0, max_cost=100):
        self.min_cost = int(min_cost)
        self.max_cost = int(max_cost)

    def set_location(self, location):
        self.location = location

    def set_distance(self, distance):
        self.distance = distance

    def get_restaurant(self, limit=10):
        result = None
        if self.location is None:
            self.location = self.search_sender(self.sender).location['coordinates']
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
        if self.location is None:
            sender_data = self.search_sender(self.sender)
            if sender_data is None:
                raise Exception('Not Find User')
            else :
                self.location = sender_data.location['coordinates']
        return UserProfile.objects(uid=self.sender).insert_or_update([self.min_cost, self.max_cost],
                                             self.catalog, self.location, self.distance)
    def search_sender(self, sender):
        return UserProfile.objects.search_by_uid(sender)

    def get_rid_image(self, rid):
        img = RestaurantImage.objects.search_by_rid(rid)
        if img is None :
            return  "https://tctechcrunch2011.files.wordpress.com/2015/03/messenger-developer.png"
        return img.url