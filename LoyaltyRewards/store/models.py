from django.contrib.auth.models import User
from django.db import models
from registration.models import Profile


class StoreOwner(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    profile_image = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = "Public"


class Store(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    slogan = models.TextField(default='')
    contact = models.TextField(default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.TextField(default='')
    owner = models.TextField(default='')
    image = models.ImageField(upload_to='store', null=True)
    qrcode = models.TextField(default='')
    is_active = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    store_owner = models.ForeignKey(StoreOwner, on_delete=models.CASCADE, null=True)
    created_at = models.IntegerField(default=0)
    updated_at = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = "Store"


class StoreOffers(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    banner = models.ImageField(upload_to='store_offers', null=True)
    title = models.TextField(default='')
    description = models.TextField(default='')
    is_valid = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0)
    updated_at = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "StoreOffers"