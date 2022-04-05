from email.policy import default
from django.db import models
import datetime

class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    pword = models.CharField(max_length=300)
    email = models.CharField(max_length=50, unique=True)
    add = models.CharField(max_length=100)
    mobile = models.CharField(max_length=13)
    # isVerified = models.BooleanField(default=True)

    class Meta:
        db_table = 'tblUsers'
        
    @property
    def is_authenticated(self):
        return True

class Room(models.Model):
    rmid = models.AutoField(primary_key=True)
    rmtype = models.CharField(max_length=8)
    rmnum = models.CharField(max_length=3)
    rmname = models.CharField(max_length=40)
    rmdesc = models.CharField(max_length=300)
    prc = models.DecimalField(max_digits=7, decimal_places=2)
    cap = models.IntegerField()
    rmimg = models.CharField(max_length=200)    
    
    class Meta:
        db_table = 'tblRoom'

class RoomPics(models.Model):
    rmpixid = models.AutoField(primary_key=True)
    rmpixurl = models.CharField(max_length=200)
    rmid = models.ForeignKey(Room, on_delete=models.CASCADE)
    
class Reserve(models.Model):
    resid = models.AutoField(primary_key=True)
    rmid = models.ForeignKey(Room, on_delete=models.CASCADE)
    uid = models.ForeignKey(Users, on_delete=models.CASCADE)
    resdate = models.DateField(blank=True, null=True)
    tmslt = models.CharField(max_length=40)
    resmadedate = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    pending = models.BooleanField(default=False)
    class Meta:
        db_table = 'tblReserve'