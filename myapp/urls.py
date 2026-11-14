from django.urls import path
from . import views
from .models import profile


urlpatterns = [
    path('add/', views.add_user, name='add_user'),
    path('list/', views.list_users, name='list_users'),
    path('edit/<int:id>/', views.edit_user, name='edit_user'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),

    #charts:--
    path('age-chart/', views.age_chart, name='age_chart'),
    # Chatbot:--
    path('chatbot/', views.chatbot, name='chatbot'),
    path('download-male-csv/', views.download_male_csv, name='download_male_csv' ),
    path('download-female-csv/',views.download_female_csv,name='download_female_csv'),
    path('preview-male/',views.preview_male,name='preview_male'),
    path('preview-female/',views.preview_female,name='preview_female'),
]
