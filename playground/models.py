from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import CharField, DateTimeField

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    collection_title  = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=SET_NULL, null=True, related_name='+')


class Product(models.Model):
    title = models.CharField(max_length=255) #varchar 255
    description = models.TextField() #big text
    price_1 = models.FloatField() #rounding num
    price = models.DecimalField(max_digits=6, decimal_places=2) #1234.56
    inventory = models.IntegerField() #positive integer
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=PROTECT) #products never be deleted by deliting collections
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    Membership_Bronze = 'B' #Bronze level membership
    Membership_Silver = 'S' #Silver level membership
    Membership_Gold = 'G' #Gold level membership
    Membership_Platinum = 'P' #Platinum level membership

    Membership_choices = [
        (Membership_Bronze, 'Bronze'),
        (Membership_Silver, 'Silver'),
        (Membership_Gold, 'Gold'),
        (Membership_Platinum, 'Platinum')
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=Membership_choices, default=Membership_Bronze)

    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)

    Status_Pending = 'P' #payment status pending
    Status_Complite = 'C' #payment status complite
    Status_Failed = 'F' #payment status failed
    Status_choices = [
        (Status_Pending, 'pending'),
        (Status_Complite, 'complite'),
        (Status_Failed, 'failed')
    ]
    payment_status = models.CharField(max_length=1, 
        choices=Status_choices, default=Status_Pending)
    customer = models.ForeignKey(Customer, on_delete=PROTECT) #orders never be deleted by deliting customers


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=PROTECT)
    product = models.ForeignKey(Product, on_delete=PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)


class Adress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    cumstomer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)


class Cart(models.Model):
    created_at = DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveSmallIntegerField()