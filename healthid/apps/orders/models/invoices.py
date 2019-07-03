from django.db import models
from healthid.models import BaseModel
from healthid.apps.outlets.models import Outlet
from healthid.apps.orders.models import Order


class Invoice(BaseModel):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )
    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE
    )
    image_url = models.URLField()
