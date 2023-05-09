from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.ListTask.as_view(),name='home'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',views.register,name='register'),
    path('task/<int:pk>/', views.DetailTask.as_view(),name='detail'),
    path('createtask/', views.CreateTask.as_view(),name='create'),
    path('edittask/<int:pk>/', views.UpdateTask.as_view(), name='update'),
    path('deletetask/<int:pk>/', views.DeleteTask.as_view(), name='delete'),



]
