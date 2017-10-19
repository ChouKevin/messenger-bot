from mongoengine import *
from mongoengine.fields import *
import datetime

class UserProfileQuerySet(QuerySet):
    def update_rid(self, rid):
        return self.update_one(True, rid=rid)
    def update_cost(self, min_v, max_v):
        return self.update_one(True, cost=[min_v, max_v], date=datetime.datetime.now())
    def update_location(self, location):
        return self.update_one(True, location=list(location), date=datetime.datetime.now())
    def update_distance(self, distance):
        return self.update_one(True, distance=distance, date=datetime.datetime.now())
    def search_by_uid(self, uid):
        return self.filter(uid=uid).first()
    def insert_or_update(self, cost=[], catalog='', location=[], distance=500):
        return self.update_one(True, cost=cost, catalog=catalog,
                               location=list(location), distance=distance, date=datetime.datetime.now())

class UserProfile(Document):
    meta = {
        'indexs':['#uid'],
        'collection': 'userProfile',
        'queryset_class': UserProfileQuerySet,
        'strict': False,
    }
    uid = StringField(required=True, unique=True)
    cost = ListField()
    catalog = StringField()
    location = PointField(required=True)
    distance = FloatField()
    rid = LongField()
    date = DateTimeField(required=True)