from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout',views.logoutuser,name='logout'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('update-password',views.update_password,name='update-password'),
    path('',views.home,name='home-page'),




#######################################################################################
    path('inserttblstudent/',inserttblstudent),
    path('searchtblstudent/',searchtblstudent),
    path('updatetblstudent/<int:id>',updatetblstudent),
    path('deletetblstudent/<int:id>',deletetblstudent),

    path('fninsertstudent/',fninsertstudent),

    path('fninsertstate/',fninsertstate),

    path('fninsertcity/',fninsertcity),

    path('fninsertqualification/',fninsertqualification),

    path('fninsertcources/',fninsertcources),

    path('fninsertreferenceby/',fninsertreferenceby),

    path('student_mgt/',student_mgt),

    path('customerreceipt/<int:stdid>/', views.customerreceipt, name='customerreceipt'),
    path('insertreceipt/', views.savenewreceipt, name='insertreceipt'),



    # path('createfeestransaction/<int:pk>',createfeestransaction),
    path('firstreceipt/<int:pk>',firstreceipt),



###############Krunal##########

    path('courseinsert/', insertcourse),
    path('coursesearch/', searchcourse),
    path('courseupdate/<int:pk>', updatecourse),
    path('coursedelete/<int:pk>', deletecourse),

    path('chapterinsert/', insertchapter),
    path('chaptersearch/', searchchapter),
    path('chapterupdate/<int:pk>', updatechapter),
    path('chapterdelete/<int:pk>', deletechapter),

    path('sessioninsert/', insertsession),
    path('sessionsearch/', searchsession),
    path('sessionupdate/<int:pk>', updatesession),
    path('sessiondelete/<int:pk>', deletesession),

    path('insertlte/', insertlte),
    path('searchpdf/', searchpdf),

    path('fninsertexfeesdate/',fninsertexfeesdate),

]
