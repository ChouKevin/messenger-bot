from mongoengine import *
from mongoengine.fields import *

class CommentQuerySet(QuerySet):
    """docstring for CommentQuerySet"""
    def __init__(self):
        super(CommentQuerySet, self).__init__()
    def search_by_uid(self, uid):
        return self.filter(uid=uid)
    def search_by_rid(self, rid):
        return self.filter(rid=rid)
        

class Comment(Document):
    """docstring for Comment"""
    meta = {
        'collection': 'restaurant',
        'queryset_class': CommentQuerySet,
        'strict': False,
    }
    uid = StringField(required=True)
    rid = LongField(required=True, min_value=0, max_value=1)
    rate = FloatField(required=True, min_value=0, max_value=1)
    context = StringField()