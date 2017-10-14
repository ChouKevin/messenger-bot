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
    def search_by_avgCost(self, location, min_cost=0, max_cost=100, meter = 500):
        return self.filter(Q(avgCost__in=range(min_cost, max_cost+1)) 
                           & Q(location__near=list(location), address__max_distance=meter))
    def search_by_name(self, name):
        return self.filter(name=name)
    def search_by_id(self, rid):
        return self.filter(rid=rid)
    def search_by_address(self, location, order_by='', meter = 500):
        return self.filter(address__near=list(location), address__max_distance=meter)
    def search_by_catelog(self, location, catelog, meter):
        return self.filter(Q(catelog_in=catelog)
                            & Q(location__near=list(location), address__max_distance=meter))
    def list_cate(self):
        return self.distinct('classify')
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
