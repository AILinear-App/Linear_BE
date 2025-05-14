from django.db import models

class Case(models.Model):
    case_name = models.CharField(max_length=200)
    officer_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    occurred_at = models.DateTimeField()         
    subject_name = models.CharField(max_length=100) 
    location = models.CharField(max_length=200)      
    memo = models.TextField(blank=True)              

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case_name
