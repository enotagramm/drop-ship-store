from django.urls import path

from shop import views


urlpatterns = [
    path('fill-database/', views.fill_database, name='fill_database'),
]
