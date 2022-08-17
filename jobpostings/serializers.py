from rest_framework import serializers
from django.db.models import Q

from .models import User, Company, Jobposting, Apply


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['create_time', 'update_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'password', 'username', 'email')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user


# 채용공고 전체 목록
class JobpostingSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    country = serializers.ReadOnlyField(source='company.country')
    region = serializers.ReadOnlyField(source='company.region')

    class Meta:
        model = Jobposting
        exclude = ['create_time', 'update_time']


# 채용공고 등록
class JobpostingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobposting
        exclude = ['create_time', 'update_time']


# 채용공고 수정
class JobpostingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobposting
        exclude = ['create_time', 'update_time']


# 채용공고 상세정보
class JobpostingDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    country = serializers.ReadOnlyField(source='company.country')
    region = serializers.ReadOnlyField(source='company.region')
    other_post = serializers.SerializerMethodField(method_name='get_other_post')

    def get_other_post(self, obj):
        posts = Jobposting.objects.filter(~Q(jobposting_id=obj.jobposting_id), company_id=obj.company_id)
        posts_id = [post.jobposting_id for post in posts]
        return posts_id

    class Meta:
        model = Jobposting
        exclude = ['create_time', 'update_time']


# 채용공고 지원
class ApplymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        exclude = ['create_time', 'update_time']
