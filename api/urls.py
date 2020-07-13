from django.urls import path, include
from rest_framework import routers
from api import views


urlpatterns = [
    path('predict/', views.predict),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]
