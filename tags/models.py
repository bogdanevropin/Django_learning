from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import GenericIPAddressField

# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    #What tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=CASCADE)
    #type 
    #ID
    content_type = models.ForeignKey(ContentType, on_delete=CASCADE)

