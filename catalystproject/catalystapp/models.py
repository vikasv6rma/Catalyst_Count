from django.db import models

# Create your models here.



class CatalystCount(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    company_id = models.CharField(db_column='COMPANY_ID', max_length=20, blank=True, null=True)  
    name = models.CharField(db_column='NAME', max_length=200, blank=True, null=True)  
    domain = models.CharField(db_column='DOMAIN', max_length=200, blank=True, null=True)  
    year_founded = models.TextField(db_column='YEAR_FOUNDED', blank=True, null=True)  
    industry = models.CharField(db_column='INDUSTRY', max_length=500, blank=True, null=True)  
    size_range = models.CharField(db_column='SIZE_RANGE', max_length=100, blank=True, null=True)  
    locality = models.CharField(db_column='LOCALITY', max_length=200, blank=True, null=True)  
    country = models.CharField(db_column='COUNTRY', max_length=200, blank=True, null=True)  
    linkedin_url = models.CharField(db_column='LINKEDIN_URL', max_length=200, blank=True, null=True)  
    current_emp_estimate = models.CharField(db_column='CURRENT_EMP_ESTIMATE', max_length=200, blank=True, null=True)  
    total_emp_estimate = models.CharField(db_column='TOTAL_EMP_ESTIMATE', max_length=200, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'catalyst_count'


class Users(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  
    email_id = models.CharField(db_column='EMAIL_ID', max_length=100, blank=True, null=True)  
    is_active = models.CharField(db_column='IS_ACTIVE', max_length=100, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'users'