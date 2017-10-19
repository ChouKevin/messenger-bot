from mongoengine import *
from mongoengine.fields import *

class CommentQuerySet(QuerySet):
    """docstring for CommentQuerySet"""
    def search_by_uid(self, uid):
        return self.filter(uid=uid)
    def search_by_rid(self, rid):
        return self.filter(rid=rid)
    def rate_restaurant(self, rid, rate, context=''):
        return self.update_one(True, rid=rid, rate=rate, context=context)
        

class Comment(Document):
    """docstring for Comment"""
    meta = {
        'collection': 'comment',
        'queryset_class': CommentQuerySet,
        'strict': False,
    }
    uid = StringField(required=True)
    rid = IntField(required=True)
    rate = FloatField(required=True, min_value=0, max_value=1)
    context = StringField()