from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Attendance(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    morning_time = models.TimeField(null=True)
    evening_time = models.TimeField(null=True)
    punch_stat = models.TextField(max_length=50, null=True)
    punch_stat_evening = models.TextField(max_length=50, null=True)
    date = models.DateField(null=True)
    working_hour = models.CharField(max_length=50, null=True)
    difference = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.usr.username
    
    
class LeaveApplication(models.Model):
    empname = models.CharField(max_length=50, null=True)
    reason = models.CharField(max_length=100, null=True)
    approval = models.BooleanField(default=False, null=True)
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.empname
    
class VisitingReport(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phonenumber = models.CharField(max_length=13)
    summery = models.CharField(max_length=500)
    approval_chance = models.IntegerField()
    visited_date = models.DateField(null=True)
    visited_time = models.TimeField(null=True)
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name