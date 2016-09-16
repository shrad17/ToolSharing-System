"""toolshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/','users.views.register',name='register'),
    url(r'^$','users.views.login',name='login'),
    url(r'^up$','users.views.user_profile',name="profile"),
    url(r'^logout$','users.views.logout',name="logout"),
    url(r'^edit_profile$','users.views.edit_profile',name="edit_profile"),
    url(r'^tools/$','users.views.tools',name="tools"),
    url(r'^listtools/$','users.views.listtools',name="list_tools"),
    url(r'^toolsinzip$','users.views.toolsinzip',name="Tools_zip_avaliable"),
    url(r'^shed$','users.views.shed_creation',name="Shed_creation"),
    url(r'^tid/(?P<tid>[0-9]+)$','users.views.request_share',name="Request_Share"),
    url(r'^messages$','users.views.User_Messages',name="User_Messages"),
    url(r'^borrowed_tools$','users.views.borrowed_tools',name="BorrowedTools"),
    url(r'^edit_tools/(?P<tid>[0-9]+)$','users.views.edit_tools',name="EditTools"),
    url(r'^shedshare/(?P<tid>[0-9]+)$','users.views.ShedShare',name="ShedShare"),
    url(r'^addAdmin$','users.views.addAdmin',name="addAdmin"),
    url(r'^edit_shed$','users.views.edit_shed',name="EditShed"),
    url(r'^manage_users$','users.views.manage_users',name="ManageUsers"),
    url(r'^statistics$','users.views.statistics',name="Statistics"),
    url(r'^reserve/(?P<tid>[0-9]+)$','users.views.makeReservation',name="Reservation"),
    url(r'^reserveShed/(?P<tid>[0-9]+)$','users.views.reserveShed',name="Reserve_Shed"),
    url(r'^populate_notifications$','users.views.populate_notifications',name="Populate_Notifications"),
    url(r'^get_notifications$','users.views.get_notifications',name="Get_Notifications"),
    url(r'^media/(?P<media>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),]
