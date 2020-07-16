from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'applications', views.ApplicationViewSet)

urlpatterns = [
    path('predict/', views.Predict.as_view()),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('', include(router.urls))
]
