from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Company, User, Jobposting, Apply
from .serializers import CompanySerializer, UserSerializer, JobpostingSerializer, JobpostingCreateSerializer, \
    JobpostingUpdateSerializer, JobpostingDetailSerializer,  ApplymentSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobpostingViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Jobposting.objects.select_related('company').all()
        q = self.request.GET.get('search', '')
        if q:
            queryset = queryset.filter(
                Q(company__name__icontains=q) | Q(company__country__icontains=q) | Q(company__region__icontains=q)
                | Q(content__icontains=q) | Q(position__icontains=q) | Q(reward__icontains=q) | Q(skill__icontains=q)
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return JobpostingSerializer
        if self.action == "retrieve":
            return JobpostingDetailSerializer
        if self.action == "create":
            return JobpostingCreateSerializer
        if self.action in ("update", "partial_update"):
            return JobpostingUpdateSerializer
        return JobpostingDetailSerializer


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplymentSerializer
