from mongoengine import *
from mongoengine.fields import *
import datetime

class UserProfileQuerySet(QuerySet):
    def search_by_uid(self, uid):
        return self.filter(uid=uid)
    def insert_or_update(self, uid, cost=[], catalog=[], location=[], distance=500):
        return self.update_one(True, uid=uid, cost=cost, catalog=catalog,
                               location=location, distance=distance, date=datetime.datetime.now())

class UserProfile(Document):
    meta = {
        'indexs':['#uid'],
        'collection': 'userProfile',
        'queryset_class': UserProfileQuerySet,
        'strict': False,
    }
    uid = StringField(required=True, unique=True)
    cost = ListField()
    catalog = ListField()
    location = PointField()
    distance = FloatField()
    date = DateTimeField(required=True)