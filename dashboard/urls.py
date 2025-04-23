from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('start-shift/', views.start_shift, name='start_shift'),
    path('end-shift/', views.end_shift, name='end_shift'),
    path('time-entries/', views.time_entries, name='time_entries'),
    path('time-entries/create/', views.create_time_entry, name='create_time_entry'),
    path('time-entries/<int:entry_id>/delete/', views.delete_time_entry, name='delete_time_entry'),
    path('time-entries/<int:entry_id>/edit/', views.edit_time_entry, name='edit_time_entry'),
    path('admin/time-entries/', views.admin_time_entries, name='admin_time_entries'),
] 