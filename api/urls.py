from django.urls import path, include
from rest_framework import routers
from api import views


urlpatterns = [
    path('predict/', views.Predict.as_view()),
    path('application/<int:pk>', views.Application.as_view()),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]
