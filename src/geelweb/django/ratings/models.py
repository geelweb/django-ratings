from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

class RatingComment(models.Model):
    user = models.ForeignKey(User, related_name='_')
    content_type = models.ForeignKey(ContentType, related_name="comments")
    object_id = models.PositiveIntegerField()
    score = models.IntegerField(_('Score'))
    comment = models.CharField(_('Comment'), max_length=400)

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.comment
