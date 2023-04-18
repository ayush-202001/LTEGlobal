from re import I
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from more_itertools import quantify
from django.db.models import Sum


class tbl_state(models.Model):
    state_name=models.CharField(max_length=100)
    state_shortform=models.CharField(max_length=5)

class tbl_city(models.Model):
    city_name=models.CharField(max_length=100)
    state_id=models.ForeignKey(tbl_state,on_delete=models.CASCADE,null=True,blank=True)
    city_shortform=models.CharField(max_length=5)

class tbl_qualification(models.Model):
    qualification_name=models.CharField(max_length=100)

class tbl_referenceby(models.Model):
    referenceby_name=models.CharField(max_length=100)

class tbl_remisier(models.Model):
    remisier_name=models.CharField(max_length=100)

class tbl_course(models.Model):
    course_name = models.CharField(max_length=100)
    course_fees = models.IntegerField()

class tbl_studenttype(models.Model):
    studenttype = models.CharField(max_length=10)

class tbl_student(models.Model):
    student_course=models.ForeignKey(tbl_course,on_delete=models.CASCADE,null=True,blank=True)
    student_type=models.ForeignKey(tbl_studenttype,on_delete=models.CASCADE,null=True,blank=True)
    student_name=models.CharField(max_length=100)
    student_emailid=models.EmailField()
    student_contactno=models.BigIntegerField()
    student_whatsappno=models.BigIntegerField()
    student_gender=models.CharField(max_length=6)
    student_dateofbirth=models.DateField()
    student_address=models.CharField(max_length=100)
    student_city=models.ForeignKey(tbl_city,on_delete=models.CASCADE,null=True,blank=True)
    student_pincode=models.IntegerField()
    student_state=models.ForeignKey(tbl_state,on_delete=models.CASCADE,null=True,blank=True)
    student_qualification=models.ForeignKey(tbl_qualification,on_delete=models.CASCADE,null=True,blank=True)
    modeofcourse=models.CharField(max_length=10)
    student_occupation=models.CharField(max_length=100)
    reference_by=models.ForeignKey(tbl_referenceby,on_delete=models.CASCADE,null=True,blank=True)

class tbl_firstreceipt(models.Model):
    student_name=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True,blank=True)
    course=models.ForeignKey(tbl_course,on_delete=models.CASCADE,null=True,blank=True)
    total = models.FloatField(default=0)
    discountedfees = models.FloatField(default=0)
    deposit = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)


class tbl_secondreceipt(models.Model):
    student_name = models.ForeignKey(tbl_student, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(tbl_course, on_delete=models.CASCADE, null=True, blank=True)
    firstreceipt = models.ForeignKey(tbl_firstreceipt, on_delete=models.CASCADE,default=0)
    discountedfees = models.FloatField(default=0)
    deposit = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)


################Krunal######################

class tbl_chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    course_id=models.ForeignKey(tbl_course,on_delete=models.CASCADE,null=True,blank=True)
    chapter_name = models.CharField(max_length=50)

class tbl_session(models.Model):
    session_id = models.AutoField(primary_key=True)
    chapter_id=models.ForeignKey(tbl_chapter,on_delete=models.CASCADE,null=True,blank=True)
    session_name = models.CharField(max_length=50)
    file = models.FileField(upload_to='doc/') # for creating file input


class tbl_exfeesdate(models.Model):
    name = models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True,blank=True)
    pending_amt=models.ForeignKey(tbl_firstreceipt,on_delete=models.CASCADE,null=True,blank=True)
    current_date = models.DateField(default=timezone.now)
    paying_date = models.DateField()
    remark =  models.CharField(max_length=200)

