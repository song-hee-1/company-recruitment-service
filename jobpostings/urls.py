from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('jobpostings', views.JobpostingViewSet, basename='jobpostings')
router.register('user', views.UserViewSet)
router.register('company', views.CompanyViewSet)
router.register('apply', views.ApplyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
