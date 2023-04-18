from email import message
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect

from .function import handle_uploaded_file
from .models import *
from .customresponse import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework .response import Response
from .serializers import *
from django.db.migrations import serializer
from django.template.loader import get_template
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from ims_django.settings import MEDIA_ROOT, MEDIA_URL
from django.core import serializers
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from imsApp.forms import *  # SaveStock, UserRegistration, UpdateProfile, UpdatePasswords, SaveCategory, SaveProduct, SaveInvoice, SaveInvoiceItem
from imsApp.models import *  # Category, Product, Stock, Invoice, Invoice_Item
# from cryptography.fernet import Fernet
from django.conf import settings
import base64
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

context = {
    'page_title': 'File Management System',
}
dataget = {}


# login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):
    context['page_title'] = 'Home'
    return render(request, 'home.html', context)





def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username=username, password=pwd)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request, 'register.html', context)


@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id=request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
        # print(form)
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form

    return render(request, 'manage_profile.html', context)


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request, 'update_password.html', context)


@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# rutuja
@api_view(['post'])
def inserttblstudent(request):
    serializers=studentserializers(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response("Inserted successfully",status.HTTP_200_OK,False)
    return Response("Data not found",status=status.HTTP_400_BAD_REQUEST)

@api_view(['get'])
def searchtblstudent(request):
    searchtblstudent=tbl_student.objects.all()
    if len(searchtblstudent)!=0:
        serializers=studentserializers(searchtblstudent,many=True)
        return Response(serializers.data,status.HTTP_200_OK,False)
    return Response("Data not found",status=status.HTTP_404_NOT_FOUND)

@api_view(['Post'])
def updatetblstudent(request,id):
    updatetblstudent=tbl_student.objects.get(id=id)
    serializers=update_studentserializers(instance=updatetblstudent,data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response("Data updated successfully",status=status.HTTP_200_OK)
    return Response("invalid data",status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deletetblstudent(request,id):
    try:
        deletetblstudent=tbl_student.objects.get(id=id)
        x=deletetblstudent.delete()
        if len(x) !=0:
            print(len(x))
            return Response("Data Deleted Successfully",status=status.HTTP_200_OK)
        return Response("Data Not Found Here",status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response("Internal server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#################################################################################################
""" HTML FORM VIEWS STUDENT REG. """
##################################################################
def fninsertstudent(request):
    studenttype_insert = tbl_studenttype.objects.all()
    state_insert = tbl_state.objects.all()
    city_insert = tbl_city.objects.all()
    qualification_insert = tbl_qualification.objects.all()
    course_insert = tbl_course.objects.all()
    reference_insert = tbl_referenceby.objects.all()
    form = insertstudentform()
    if request.method == "POST":
        form = insertstudentform(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("Data inserted successfully")
    return render(request, "registration.html", {'form': form,'state_insert':state_insert,'city_insert':city_insert,'qualification_insert':qualification_insert,'course_insert':course_insert,'reference_insert':reference_insert,'studenttype_insert':studenttype_insert})

def fnsearchstudent(request):
    student_search = tbl_student.objects.all()
    return render(request, "studentsearch.html", {'student_search': student_search})

###################################################################

#######################################################
def fninsertcity(request):
    state_insert = tbl_state.objects.all()
    if request.method=="POST":
        form= cityform(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request,"cityinsert.html", {'form': form,'state_insert':state_insert})
    form =cityform()
    return render(request, "cityinsert.html", {'form': form,'state_insert':state_insert})


def fnsearchcity(request):
    city_search= tbl_city.objects.all()
    return render(request, "citysearch.html", {'city_search': city_search})
#
# def fnupdatecity(request,pk):
#     city_update = tbl_city.objects.get(pk=pk)
#     state_insert = tbl_state.objects.filter(pk=pk)
#     state_all = tbl_state.objects.all()
#     state=tbl_state.objects.get(pk=pk)
#     form=cityupdateform(request.POST,instance=state)
#     print(form.is_valid())
#     print("form")
#     if form.is_valid():
#         tbl_city.objects.filter(pk=pk).update(city_name=request.POST['city_name'])
#         form.save()
#         return HttpResponse('Updated Successfully')
#     return render(request,'cityupdate.html',{'state':state})
#
# def fndeletecity(request,pk):
#     employee=tbl_city.objects.get(pk=pk)
#     employee.delete()
#     return redirect("/citysearch")

####################################################

def fninsertstate(request):
    if request.method=="POST":
        form= stateform(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request,"stateinsert.html", {'form': form})
    form =stateform()
    return render(request, "stateinsert.html", {'form': form})


def fnsearchstate(request):
    employees= tbl_city.objects.all()
    return render(request, "citysearch.html", {'employees': employees})

# def fnupdatestate(request,pk):
#     form=stateupdateform(request.POST)
#     print(form.is_valid())
#     print("form")
#     if form.is_valid():
#         form.save()
#         return HttpResponse('Updated Successfully')
#     return render(request,'stateupdate.html',{})
#
# def fndeletestate(request,pk):
#     employee=tbl_state.objects.get(pk=pk)
#     employee.delete()
#     return redirect("/statesearch")

####################################################


def fninsertqualification(request):
    if request.method=="POST":
        form= qualificationform(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request,"qualificationinsert.html", {'form': form})
    form =qualificationform()
    return render(request, "qualificationinsert.html", {'form': form})


def fnsearchqualification(request):
    employees= tbl_qualification.objects.all()
    return render(request, "qualificationsearch.html", {'employees': employees})
#
# def fnupdatequalification(request,pk):
#     form=qualificationupdateform(request.POST)
#     print(form.is_valid())
#     print("form")
#     if form.is_valid():
#         form.save()
#         return HttpResponse('Updated Successfully')
#     return render(request,'qualificationupdate.html',{})
#
# def fndeletequalification(request,pk):
#     employee=tbl_qualification.objects.get(pk=pk)
#     employee.delete()
#     return redirect("/qualificationsearch")

####################################################


def fninsertcources(request):
    if request.method=="POST":
        form= courceform(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request,"courseinsert.html", {'form': form})
    form =courceform()
    return render(request, "courseinsert.html", {'form': form})


def fnsearchcources(request):
    employees= tbl_course.objects.all()
    return render(request, "courcessearch.html", {'employees': employees})

# def fnupdatecources(request,pk):
#     form=courcesupdateform(request.POST)
#     print(form.is_valid())
#     print("form")
#     if form.is_valid():
#         form.save()
#         return HttpResponse('Updated Successfully')
#     return render(request,'courcesupdate.html',{})
#
# def fndeletecources(request,pk):
#     employee=tbl_cources.objects.get(pk=pk)
#     employee.delete()
#     return redirect("/courcessearch")

####################################################


def fninsertreferenceby(request):
    if request.method=="POST":
        form= referencebyform(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request,"referencebyinsert.html", {'form': form})
    form =referencebyform()
    return render(request, "referencebyinsert.html", {'form': form})


def fnsearchreferenceby(request):
    employees= tbl_course.objects.all()
    return render(request, "courcessearch.html", {'employees': employees})
#
# def fnupdatereferenceby(request,pk):
#     form=referencebyupdateform(request.POST)
#     print(form.is_valid())
#     print("form")
#     if form.is_valid():
#         form.save()
#         return HttpResponse('Updated Successfully')
#     return render(request,'referencebyupdate.html',{})
#
# def fndeletereferenceby(request,pk):
#     employee=tbl_referenceby.objects.get(pk=pk)
#     employee.delete()
#     return redirect("/referencebysearch")
#
###############################################################################################


def fninsertstudenttype(request):
    if request.method=="POST":
        form= studenttypeform(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request,"studenttypeinsert.html", {'form': form})
    form =studenttypeform()
    return render(request, "studenttypeinsert.html", {'form': form})


def fnsearchstudenttype(request):
    studenttype= tbl_studenttype.objects.all()
    return render(request, "studenttypesearch.html", {'studenttype': studenttype})
#
# def fnupdatereferenceby(request,pk):
#     form=referencebyupdateform(request.POST)
#     print(form.is_valid())
#     print("form")
#     if form.is_valid():
#         form.save()
#         return HttpResponse('Updated Successfully')
#     return render(request,'referencebyupdate.html',{})
#
# def fndeletereferenceby(request,pk):
#     employee=tbl_referenceby.objects.get(pk=pk)
#     employee.delete()
#     return redirect("/referencebysearch")
#
#
# def load_courses(request):
#     student_id = request.GET.get('student_id')
#     print(student_id)
#     course = tbl_course.objects.filter(student_id=student_id).all()
#     return render(request, 'courses_dropdown_list_options.html', {'course': course})


def columndata(tablename, dataid, columnname, query):
    import sqlite3

    # Connecting to sqlite
    conn = sqlite3.connect('db.sqlite3')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    sqlquery = ""
    if query == "":
        sqlquery = "select " + str(columnname) + " from " + str(tablename) + " where id = " + str(dataid)
    else:
        sqlquery = query
    # printt(sqlquery)
    x = cursor.execute(str(sqlquery))
    # printt("+++++++Cursor data+++++++++++++++++")
    # printt(type(x))
    # printt(x)
    if query == "":
        # Fetching 1st row from the table
        result = cursor.fetchone();
        # printt("+++++++Cursor data1+++++++++++++++++")
        # printt(result)
        return result
    else:
        # Fetching 1st row from the table
        result = cursor.fetchall();
        # printt("+++++++Cursor data All+++++++++++++++++")
        # printt(type(result))
        return result






def student_mgt(request):
    context['page_title'] = "student"
    # students = tbl_student.objects.all()
    dataquery = """ 		
		select std.id, std.student_name as student, std.student_contactno as number,crs.course_name as course from imsApp_tbl_student as std
    	join imsapp_tbl_course as crs
        ON crs.id = std.student_course_id;"""
    context['students'] = columndata("", "", "", dataquery)
    return render(request, 'selectstudent.html', context)


# def createfeestransaction(request,pk):
#
#     context['page_title'] = "student"
#     # students = tbl_student.objects.all()
#     dataquery = """select student_name as student, student_contactno as number, course_name as course, course_fees as fees from imsapp_tbl_student
#     	join imsapp_tbl_course as crs
#         ON crs.id = imsapp_tbl_student.student_course_id
#         where imsapp_tbl_student.id  = """ + str(pk) + """;"""
#     context['students'] = columndata("", "", "", dataquery)
#     return render(request, 'createfirsttransaction.html', context)




def showreceiptentry(request,pk):
    dataquery = """select student_name as student, course_name as course from imsapp_tbl_student
	join imsapp_tbl_course as crs
    ON crs.id = imsapp_tbl_student.student_course_id
    where imsapp_tbl_student.id  = """ + str(pk) + """ ;"""
    context['students'] = columndata("", "", "", dataquery)
    return render(request, 'showreceiptentry.html', context)


# def firstentry(request):
#     if request.method == "POST":
#         form = firstreceiptform(request.POST)
#         print(form.is_valid())
#         if form.is_valid():
#             form.save()
#             # receipt_form = secondreceiptform()
#             return HttpResponse("data inserted")
#         return render(request, "createfirsttransaction.html", {'form': form})
#     form = courceform()
#     return render(request, "createfirsttransaction.html", {'form': form})
#
#





###############Krunal###################################


def insertcourse(request):
    form = courseform()
    if request.method == "POST":
        form = courseform(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("data inserted")
    return render(request, "courseinsert.html", {'form': form})

def searchcourse(request):
    course_search= tbl_course.objects.all()
    return render(request, "coursesearch.html", {'course_search': course_search})

def updatecourse(request,pk):
    course_update=tbl_course.objects.get(pk=pk)
    form= courseupdateform(request.POST,instance=course_update)
    print(form.is_valid())
    if form.is_valid():
       tbl_course.objects.filter(pk=pk).update(course_name=request.POST['course_name'])
       form.save()
       return HttpResponseRedirect("/coursesearch/")
    return render(request,'courseupdate.html',{'course_update':course_update})


def deletecourse(redirect,pk):
    course_delete=tbl_course.objects.get(pk=pk)
    course_delete.delete()
    return HttpResponseRedirect("/coursesearch/")

#########################################################
def insertchapter(request):
    course_insert = tbl_course.objects.all()
    if request.method == "POST":
        form = chapterform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("data inserted")
        return render(request, "chapterinsert.html", {'form': form,'course_insert':course_insert})
    form=chapterform()
    return render(request, "chapterinsert.html", {'form': form, 'course_insert': course_insert})

def searchchapter(request):
    chapter_search= tbl_chapter.objects.all()
    return render(request, "chaptersearch.html", {'chapter_search': chapter_search})

def updatechapter(request,pk):
    chapter_update=tbl_chapter.objects.get(pk=pk)
    form= chapterupdateform(request.POST,instance=chapter_update)
    print(form.is_valid())
    if form.is_valid():
       # tbl_chapter.objects.filter(pk=pk).update(course_name=request.POST['course_name'])
       tbl_chapter.objects.filter(pk=pk).update(chapter_name=request.POST['chapter_name'])
       form.save()
       return HttpResponse('data updated')
    return render(request,'chapterupdate.html',{'chapter_update':chapter_update})


def deletechapter(redirect,pk):
    chapter_delete=tbl_chapter.objects.get(pk=pk)
    chapter_delete.delete()
    return HttpResponseRedirect("/chaptersearch/")

##################################################################

def insertsession(request):
    chapter_insert = tbl_chapter.objects.all()
    # lastvideo = tbl_session.objects.last()
    # videofile = lastvideo.videofile
    if request.method == "POST":
        form = sessionform(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            form.save()
            return HttpResponse("data inserted")
        return render(request, "sessioninsert.html", {'form': form,'chapter_insert':chapter_insert,})
    form=sessionform()
    return render(request, "sessioninsert.html", {'form': form, 'chapter_insert': chapter_insert,})


def searchsession(request):
    session_search= tbl_session.objects.all()
    return render(request, "sessionsearch.html", {'session_search': session_search})

def updatesession(request,pk):
    session_update=tbl_session.objects.get(pk=pk)
    form= sessionupdateform(request.POST,instance=session_update)
    print(form.is_valid())
    if form.is_valid():
       tbl_session.objects.filter(pk=pk).update(session_name=request.POST['session_name'])
       # tbl_session.objects.filter(pk=pk).update(chapter_name=request.POST['chapter_name'])
       form.save()
       return HttpResponse('Udated Succesfully')
    return render(request,'sessionupdate.html',{'session_update':session_update})


def deletesession(redirect,pk):
    session_delete=tbl_session.objects.get(pk=pk)
    session_delete.delete()
    return HttpResponseRedirect("/sessionsearch/")


def insertlte(request):
    course_insert = tbl_course.objects.all()
    chapter_insert = tbl_chapter.objects.all()
    session_insert = tbl_session.objects.all()
    return render(request, "insertlte.html", {'course_insert': course_insert,'chapter_insert':chapter_insert,'session_insert':session_insert})

def searchpdf(request):
    search_pdf= tbl_session.objects.all()
    return render(request, "searchpdf.html", {'search_pdf': search_pdf})






























#
# def studentreceipt(request, stdid, crsid):
#     context['page_title'] = 'Fees'
#     dataquery = """SELECT sum(deposit) FROM imsApp_tbl_secondreceipt as sec
#     WHERE sec.student_name_id =  """ + str(stdid) + """ AND sec.course_id = """ + str(crsid) + """ ;"""
#     deposites = columndata("", "", "", dataquery)
#     context['deposites'] = 0 if deposites[0][0] == None else deposites[0][0]
#
#     ###########################
#     dataquery = """SELECT sum(total) FROM imsApp_tbl_secondreceipt as sec
#     WHERE sec.student_name_id =  """ + str(stdid) + """ AND sec.course_id = """ + str(crsid) + """ ;"""
#     totamt = columndata("", "", "", dataquery)
#     context['deposites'] = 0 if deposites[0][0] == None else deposites[0][0]
#
#     dataquery = """SELECT name from imsApp_customer where id =
#        """ + str(custid) + """;"""
#     cust = columndata("", "", "", dataquery)


# def firstreceipt(request,pk):
#     # student_name = stu.objects.filter(fieldname=value)
#     context['page_title'] = "student"
#     # students = tbl_student.objects.all()
#     dataquery = """select student_name as student, student_contactno as number, course_name as course, course_fees as fees from imsapp_tbl_student
#         	join imsapp_tbl_course as crs
#             ON crs.id = imsapp_tbl_student.student_course_id
#             where imsapp_tbl_student.id  = """ + str(pk) + """;"""
#     context['students'] = columndata("", "", "", dataquery)
#     print(dataquery)
#     firstforms = firstreceiptform()
#     print("qweddeded")
#     if request.method == 'POST':
#         print("rgregergtg")
#         firstform = firstreceiptform(request.POST)
#         secondform = secondreceiptform(request.POST)
#         print("first formmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
#         print(firstform.is_valid())
#         print(secondform.is_valid())
#         print("second formmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
#         if firstform.is_valid() and secondform.is_valid():
#             print(firstform.is_valid)
#             print(secondform.is_valid)
#             firstform.save()
#             secondform.save()
#             return HttpResponse("Saved")
#         context['firstforms']=firstforms
#     return render(request, 'createfirsttransaction.html', context)


def firstreceipt(request, pk):
    # Retrieve the student instance based on the pk
    student = tbl_student.objects.get(id=pk)

    context['page_title'] = "student"
    dataquery = """select student_name as student, student_contactno as number, course_name as course, course_fees as fees from imsapp_tbl_student
        	join imsapp_tbl_course as crs
            ON crs.id = imsapp_tbl_student.student_course_id
            where imsapp_tbl_student.id  = """ + str(pk) + """;"""
    context['students'] = columndata("", "", "", dataquery)

    if request.method == 'POST':
        # Create instances of both form classes with request.POST data
        firstform = firstreceiptform(request.POST)
        secondform = secondreceiptform(request.POST)

        # Check if both forms are valid
        if firstform.is_valid() and secondform.is_valid():
            # Create instances of the two models
            firstreceipt_instance = firstform.save(commit=False)
            secondreceipt_instance = secondform.save(commit=False)

            # Assign the foreign key fields to the student and course instances
            firstreceipt_instance.student_name = student
            firstreceipt_instance.course = student.student_course
            secondreceipt_instance.student_name = student
            secondreceipt_instance.course = student.student_course

            # Save both instances
            firstreceipt_instance.save()
            secondreceipt_instance.save()

            return HttpResponse("Saved")

    context['firstforms'] = student

    return render(request, 'createfirsttransaction.html', context)


# def process_second_receipt(request):
#     # Check if the form was submitted
#     if request.method == 'POST':
#         # Get the form data from the request
#         student_id = request.POST.get('student_id')
#         course = request.POST.get('course')
#         fees = float(request.POST.get('fees'))
#         discount = float(request.POST.get('discount'))
#         discounted_fees = float(request.POST.get('discounted_fees'))
#         deposit = float(request.POST.get('deposit'))
#         balance = float(request.POST.get('balance'))
#
#         # Perform any necessary calculations
#         total = fees - discount
#         if discounted_fees != total:
#             return HttpResponse('Discounted fees does not match the calculated total.')
#         if deposit > discounted_fees:
#             return HttpResponse('Deposit cannot be greater than the discounted fees.')
#         if balance < 0:
#             return HttpResponse('Balance cannot be negative.')
#
#         # Create a new receipt object and save it to the database
#         receipt = Receipt.objects.create(
#             student_id=student_id,
#             course=course,
#             fees=fees,
#             discount=discount,
#             discounted_fees=discounted_fees,
#             deposit=deposit,
#             balance=balance
#         )
#         receipt.save()
#
#         # Redirect the user to a success page
#         return redirect('receipt_success')
#
#     # If the form was not submitted, render the receipt form
#     return render(request, 'addreceiptentry.html')



def customerreceipt(request, stdid):

    context['page_title'] = 'Invoices'
    dataquery = """SELECT sum(deposit) from imsApp_tbl_secondreceipt as recept
    where recept.student_name_id = """ + str(stdid) + """;"""
    deposites = columndata("", "", "", dataquery)
    context['deposites'] = 0 if deposites[0][0] == None else deposites[0][0]
    print(context['deposites'])

    dataquery = """select sum(discountedfees) as total
    From imsApp_tbl_firstreceipt as first where first.student_name_id = """ + str(stdid) + """;"""
    totamt = columndata("", "", "", dataquery)
    print(totamt)

    dataquery = """SELECT student_name from imsApp_tbl_student where id =
       """ + str(stdid) + """;"""
    stud = columndata("", "", "", dataquery)
    print(stud)

    context['totals'] = 0 if totamt[0][0] == None else int(totamt[0][0])
    context['customers'] = 0 if stud[0][0] == None else stud[0][0]
    context['balances'] = int(context['totals']) - int(context['deposites'])
    # pdf = render_to_pdf('customerallbillpdf.html', context)
    return render(request, 'addreceiptentry.html', context)


def savenewreceipt(request):
    print(savenewreceipt)
    resp = {'status': 'failed', 'msg': ''}
    if request.method == "POST":
        print(" ithe aala ahe ")
        dataquery = """SELECT id from tbl_student where student_name = '""" + request.POST['student_name'].strip() + """';"""
        stdid = columndata("", "", "", dataquery)
        dataquery = """SELECT id from tbl_course where course_name = '""" + request.POST['firstreceipt'].strip() + """';"""
        courseid = columndata("", "", "", dataquery)
        firstreceipt = tbl_firstreceipt.objects.last()
        datareceipt = {
            'firstreceipt': firstreceipt.id,
            'student': stdid[0][0],
            'course': courseid[0][0],
            'discountedfees': int(request.POST['discountedfees']),
            'deposit': int(request.POST['deposit']),
            'balance': int(request.POST['balance']) - int(request.POST['deposit'])
        }
        if int(request.POST['deposit'])>0:
            form = secondreceiptform(data=datareceipt)
            print(datareceipt)
            print(form.is_valid())

            if form.is_valid():
                form.save()
                datareceipt["customername"] =request.POST['customer'].strip()
                datareceipt["date"] = datetime.now().today()
                pdf = render_to_pdf('customerallbillpdfreceipt.html', datareceipt)
                return HttpResponse(pdf, content_type='application/pdf')
                # return render(request, 'customerallbillpdf.html', {'form': form, 'success': " Data Inserted Successfully!"})
            else:
                return render(request, 'customerallbillpdf.html', {'form': form, 'error': "Insert Correct Value Here!"})
        else:
            resp['msg'] = 'Enter Deposit Amount greater than 0 !.'
            return HttpResponse(json.dumps(resp), content_type='application/json')

    resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')



###########################################################
def fninsertexfeesdate(request):
#     context['feesdates'] = feesdate
#     dataquery = """SELECT student_name as name , balance
# FROM imsApp_tbl_student
# JOIN imsApp_tbl_secondreceipt as fir
# ON imsApp_tbl_student.id = fir.student_name_id
# WHERE student_type_id =1 AND  balance>0;"""
#     context['feesdates'] = columndata("", "", "", dataquery)
    studenname_insert = tbl_student.objects.filter(student_type__studenttype="EX")
    print(studenname_insert)
    pendingamt_insert = tbl_secondreceipt.objects.all()
    reference_insert = tbl_referenceby.objects.all()
    form = insertstudentform()
    if request.method == "POST":
        form = insertstudentform(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("Data inserted successfully")
    return render(request, "registration.html", {'form': form,'state_insert':state_insert,'city_insert':city_insert,'qualification_insert':qualification_insert,'course_insert':course_insert,'reference_insert':reference_insert,'studenttype_insert':studenttype_insert})








