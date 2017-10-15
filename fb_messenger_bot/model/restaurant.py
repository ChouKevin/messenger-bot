from mongoengine import *
from mongoengine.fields import *

class RestaurantQuerySet(QuerySet):
    def search_by_avgCost(self, address, min_cost=0, max_cost=100, meter = 500):
        return self.filter(Q(avgCost__in=range(min_cost, max_cost+1)) 
                           & Q(address__near=list(address), address__max_distance=meter))
    def search_by_avgCost_catalog(self, address, catalog, min_cost=0, max_cost=100, meter = 500):
        return self.filter(Q(avgCost__in=range(min_cost, max_cost+1)) 
                           & Q(address__near=list(address), address__max_distance=meter)
                           & Q(classify=catalog))
    def search_by_name(self, name):
        return self.filter(name=name)
    def search_by_id(self, rid):
        return self.filter(rid=rid)
    def search_by_address(self, address, meter = 500):
        return self.filter(address__near=list(address), address__max_distance=meter)
    def search_by_catalog(self, address, catalog, meter = 500):
        return self.filter(Q(classify=catalog)
                            & Q(address__near=list(address), address__max_distance=meter))
    def get_catalog(self):
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
    classify = StringField(required=True)
    avgCost = IntField(min_value=0)
    address = PointField(required=True)
    hours = ListField()
    name = StringField(required=True)
    rid = LongField(required=True)

# for i in Restaurant.objects.search_by_address((121.56008359778, 25.080193176667)):
#     print(i.name)
