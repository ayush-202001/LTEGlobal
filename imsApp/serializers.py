from rest_framework import serializers
from .models import *
class studentserializers(serializers.ModelSerializer):
    class Meta:
        model= tbl_student
        fields='__all__'

class update_studentserializers(serializers.ModelSerializer):
    class Meta:
        model=tbl_student
        fields=['Student_Name','Student_EmailId','Student_ContactNo','Student_WhatsappNo','Student_Gender','Student_DateOfBirth',
                'Student_Address','Student_City','Student_PinCode','Student_State','Student_Qualification','Student_Courses','Student_Occupation',
                'Refrences_By']