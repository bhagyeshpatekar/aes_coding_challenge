from django.db import models
import uuid

from django.db.models.deletion import CASCADE, PROTECT


# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)


class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)


class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)

# Create your models here.
class Inventory_Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
#    inventory_item = models.ForeignKey(Transaction_LID, on_delete=models.PROTECT)
    article = models.ForeignKey(ArticleMaster, on_delete=models.CASCADE)
    colour = models.ForeignKey(ColorMaster, on_delete=CASCADE)
    company = models.ForeignKey(CompanyLedgerMaster, null=True, on_delete=models.CASCADE)
    gross_quantity = models.DecimalField(max_digits=5,decimal_places=2)
    net_quality = models.DecimalField(max_digits=5,decimal_places=2, default=10)
    u_choices = [
        ('KG', 'KG'),
        ('METER', 'METER'),
    ]
    status = models.CharField(max_length=20,default='KG', choices=u_choices)

#    def __str__(self):
#       return self.id

class Transaction_LID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    item = models.ForeignKey(TransactionModel, on_delete=models.PROTECT)
    article = models.ForeignKey(ArticleMaster, on_delete=models.CASCADE)
    colour = models.ForeignKey(ColorMaster, on_delete=models.CASCADE)
    required_on_date = models.DateField(null=True)
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    rate = models.IntegerField()
    unit_choices = [
        ('KG', 'KG'),
         ('METER', 'METER'),
    ]
    unit = models.CharField(max_length=20,default='KG', choices=unit_choices)
    add_inventory_items = models.ForeignKey(Inventory_Item,default='', on_delete=models.CASCADE)

#    def __str__(self):
#        return self.uid


class TransactionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    #      TRN_number = Review.objects.all().annotate(date=TruncDay('datetime_created')).values("date").annotate(created_count=Count('id')).order_by("-date")
    trn_choices = [
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('CLOSE', 'CLOSE'),
    ]
    status = models.CharField(max_length=20, choices=trn_choices, default='PENDING')
    remarks = models.CharField(max_length=64, blank=True)
    add_transaction_linedetails = models.ForeignKey(Transaction_LID, on_delete=PROTECT,default='')
#    class Meta:
#        managed = False
#        db_table = 'details'
#        ordering = ['id']
#    def __str__(self):
#       return self.id





