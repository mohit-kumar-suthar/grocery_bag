from django.urls import path
from . import views

urlpatterns = [
    path('add',views.add_view,name='add'),
    path('update/<int:pk>',views.update_view,name='update'),
    path('delete/<int:pk>',views.delete_view,name='delete'),
    path('',views.index_view,name='index'),
    path('filter',views.filter_view,name='filter'),
    path('login',views.login_view,name="login"),
    path('register',views.register_view,name="register"),
    path('otp',views.otp_view,name='otp'),
    path('logout',views.logout_view,name="logout"),
]