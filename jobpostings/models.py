from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import TimeStampModel


# 회사 model
class Company(TimeStampModel):
    company_id = models.BigAutoField(primary_key=True, verbose_name="회사_id")
    name = models.CharField(max_length=20, verbose_name="회사명")
    country = models.CharField(max_length=20, verbose_name="국가")
    region = models.CharField(max_length=20, verbose_name="지역")

    class Meta:
        verbose_name = "회사"
        verbose_name_plural = "회사 목록"
        db_table = 'company'

    def __str__(self):
        return f'{self.name} - {self.country} {self.region} '


# 채용공고 model
class Jobposting(TimeStampModel):
    jobposting_id = models.BigAutoField(primary_key=True, verbose_name="채용공고_id")
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='company_jobpostings'
    )
    position = models.CharField(max_length=100, verbose_name="채용포지션")
    reward = models.IntegerField(verbose_name="채용보상금")
    content = models.TextField(verbose_name="채용내용")
    skill = models.CharField(max_length=100, verbose_name="사용기술")
    apply = models.ManyToManyField(
        'User',
        through='Apply',
        related_name='appliers',
        blank=True,
        verbose_name="지원자"
    )  # 지원 내역을 확인을 위한 테이블

    class Meta:
        verbose_name = "채용공고"
        verbose_name_plural = "채용공고 목록"
        db_table = 'jobposting'

    def __str__(self):
        return self.content


# 지원 model
class Apply(TimeStampModel):
    apply_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='applys', db_column='user_id')
    jobposting_id = models.ForeignKey(
        Jobposting,
        on_delete=models.CASCADE,
        related_name='applys',
        db_column='jobposting_id')

    class Meta:
        verbose_name = "지원"
        verbose_name_plural = "지원 목록"
        db_table = 'apply'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'jobposting_id'],
                name="unique applys"
            ),
        ]

    def __str__(self):
        return f'user id {self.user_id} apply at {self.jobposting_id}'


# 사용자 model
class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, verbose_name="사용자_id")

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        db_table = 'user'

    def __str__(self):
        return self.username
