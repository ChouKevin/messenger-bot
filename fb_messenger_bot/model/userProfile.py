from mongoengine import *
from mongoengine.fields import *
import datetime

class UserProfileQuerySet(QuerySet):
    def search_by_uid(self, uid):
        return self.filter(uid=uid).first()
    def insert_or_update(self, cost=[], catalog=[], location=[], distance=500):
        return self.update_one(True, cost=cost, catalog=catalog,
                               location=list(location), distance=distance, date=datetime.datetime.now())
    def set_status(self, stauts):
        return self.update_one(True, status=stauts)
    def get_status(self, uid):
        return self.filter(uid=uid).first()

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
    location = PointField(required=True)
    distance = FloatField()
    status = StringField()
    date = DateTimeField(required=True)