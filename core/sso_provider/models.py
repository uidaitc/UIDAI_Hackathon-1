from django.db import models
from domain_user.models import CustomUser, Domain
# Create your models here.
class VIDtoDomainMap(models.Model):
    vid = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        db_table = 'vid_domain_map'