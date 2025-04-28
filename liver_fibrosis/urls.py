"""
URL configuration for liver_fibrosis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from userapp import views as user_views
from adminapp import views as admin_views
from mainapp import views as main_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main 
    path('admin/', admin.site.urls),
    path("", main_views.index, name="index"),
    path("about",main_views.about, name="about"),
    path("contact",main_views.contact, name="contact"),
    path("login",main_views.login, name="login"),
    path("otp",main_views.otp, name="otp"),
    path("register",main_views.signup, name="signup"),
    path("admin-login",main_views.adminlogin, name="adminlogin"),
    # User
    path("user-dashboard", user_views.user_dashboard, name="user_dashboard"),
    path("detection", user_views.detection, name="detection"),
    path("user-feedback", user_views.user_feedback, name="user_feedback"),
    path("profile", user_views.profile, name="profile"),
    # Admin
    path("admin-dashboard",admin_views.admin_dash, name="admin_dash"),
    path("all-users",admin_views.allusers, name="allusers"),
    path("pending-users",admin_views.pendingusers, name="pendingusers"),
    path("dataset-overview",admin_views.datasetoverview , name="datasetoverview"),
    path("dataset-info", admin_views.datasetinfo, name="datasetinfo"),
    path("test-split",admin_views.testsplit, name="testsplit"),
    path("test-split-result",admin_views.testsplitresult, name="testsplitresult"),
    path("cnn",admin_views.cnn, name="cnn"),
    path("cnn-result",admin_views.cnnresult, name="cnnresult"),
    path("densenet",admin_views.densenet, name="densenet"),
    path("densenet-result",admin_views.densenetresult, name="densenetresult"),
    path("mobilenet",admin_views.mobilenet, name="mobilenet"),
    path("mobilenet-result",admin_views.mobilenetresult, name="mobilenetresult"),
    path("admin-feedback",admin_views.feedback, name="feedback"),
    path("graph-comparison",admin_views.graphcomparison, name="graphcomparison"),
    path("sentiment-analysis",admin_views.sentimentanalysis, name="sentimentanalysis"),
    path("sentiment-analysis-graph",admin_views.sentimentanalysisgraph, name="sentimentanalysisgraph"),
    path('delete-user/<int:user_id>/', admin_views.delete_user, name='delete_user'),
    path('accept-user/<int:id>', admin_views.accept_user, name = 'accept_user'),
    path('reject-user/<int:id>', admin_views.reject_user, name = 'reject'),
    path('change-status/<int:id>', admin_views.change_status, name = 'change_status'),
    path('admin-logout',admin_views.adminlogout,name='adminlogout'),
    path('user-logout',user_views.user_logout,name='user_logout'),
    path("detection-result",user_views.detection_result , name="detection_result")

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

