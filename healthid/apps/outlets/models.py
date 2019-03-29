from django.db import models
from healthid.apps.business.models import Business
<<<<<<< HEAD
from healthid.apps.authentication.models import User
=======
from django.utils.http import int_to_base36
import uuid

def id_gen() -> str:
    """Generates an 8 character long random string"""
    return int_to_base36(uuid.uuid4().int)[:8]
>>>>>>> feat(add_register)- create receipt and register model


class Country(models.Model):
    name = models.CharField(max_length=244, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=244)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("name", "country"))

    def __str__(self):
        return self.name


class OutletKind(models.Model):
    name = models.CharField(max_length=244)

    def __str__(self):
        return self.name


class Outlet(models.Model):
    id = models.AutoField(primary_key=True)
    kind = models.ForeignKey(OutletKind, on_delete=models.CASCADE)
    name = models.CharField(max_length=244)
    address_line1 = models.CharField(max_length=244)
    address_line2 = models.CharField(max_length=244)
    lga = models.CharField(max_length=244)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25)
    date_launched = models.DateField()
    prefix_id = models.CharField(max_length=9, null=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, related_name='users')

    class Meta:
        unique_together = (("name", "business"))

    def __str__(self):
        return self.name

class Receipt(models.Model):
    id = models.CharField(
        max_length=9, primary_key=True, default=id_gen, editable=False
    )
    cashier = models.CharField(max_length=244)
    discount = models.IntegerField()
    subtotal = models.IntegerField()
    tax = models.IntegerField()
    amount_to_pay = models.IntegerField()
    purchase_total = models.IntegerField()
    change_due = models.IntegerField()
    loyal = models.IntegerField()

    def __str__(self):
        return self.cashier

    class Meta:
        ordering = ('cashier',)


class Register(models.Model):
    name = models.CharField(max_length=244)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
