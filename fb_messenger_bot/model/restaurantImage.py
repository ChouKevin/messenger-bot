from mongoengine import *
from mongoengine.fields import *

class ImageQuerySet(QuerySet):
    def search_by_rid(self, rid):
        return self.filter(rid=rid).first()

# 偷懶一下
class RestaurantImage(Document):
    meta = {
        'collection': 'restaurantImage',
        'queryset_class': ImageQuerySet,
        'strict': False,
    }
    rid = LongField(required=True)
    url = StringField()