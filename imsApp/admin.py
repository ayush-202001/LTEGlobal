from django.contrib import admin
from imsApp.models import *  # Category, Product, Stock, Invoice, Invoice_Item

# Register your models here.
admin.site.register(tbl_student)
admin.site.register(tbl_state)
admin.site.register(tbl_city)
admin.site.register(tbl_qualification)
admin.site.register(tbl_course)
admin.site.register(tbl_referenceby)
admin.site.register(tbl_remisier)
admin.site.register(tbl_firstreceipt)
admin.site.register(tbl_secondreceipt)
admin.site.register(tbl_chapter)
admin.site.register(tbl_session)
admin.site.register(tbl_studenttype)