from model.comment import *

class UserRate(object):
    def __init__(self, sender):
        self.sender = sender

    def get_rated_restaurant(self, rid=None):
        if rid is not None:
            return Comment.objects(uid=self.sender).search_by_rid(rid)
        else:
            return Comment.objects(uid=self.sender)
    def rate_restaurant(self, rid, score):
        Comment.objects(uid=self.sender).rate_restaurant(rid, score)