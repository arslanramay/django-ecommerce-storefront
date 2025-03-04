from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)

class TaggedItem(models.Model):
    # What Tag is applied to what item/object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
