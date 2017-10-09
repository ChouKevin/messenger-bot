from mongoengine import *
from mongoengine.fields import *
from settings import db_config

register_connection(
    alias='default',
    name = db_config['DB'],
    host = db_config['HOST'],
    port = db_config['PORT'],
    username = db_config['USER'],
    password = db_config['PASSWD'],
    authentication_source = 'admin'
    )

class RestaurantQuerySet(QuerySet):
    def get_by_avgCost(self, min, max):
        return self.filter(avgCost__in=range(min, max+1))
    def get_by_name(self, name):
        return self.filter(name=name)
    def get_by_id(self, rid):
        return self.filter(rid=rid)
    def search_by_address(self, address, meter = 500):
        return self.filter(address__near=list(address), address__max_distance=meter)
    
class Restaurant(Document):
    meta = {
        'collection': 'restaurant',
        'queryset_class': RestaurantQuerySet,
        'strict': False,
    }
    environmentRate = FloatField(min_value=0)
    serviceRate = FloatField(min_value=0)
    tasteRate = FloatField(min_value=0)
    classify = ListField(required=True)
    avgCost = IntField(min_value=0)
    address = PointField(required=True)
    hours = ListField()
    name = StringField(required=True)
    rid = LongField(required=True)

# for i in Restaurant.objects.search_by_address((121.56008359778, 25.080193176667)):
#     print(i.name)
