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
    rid = StringField(required=True)
    url = StringField()