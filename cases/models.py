from django.db import models

class Case(models.Model):
    case_name = models.CharField(max_length=200)
    officer_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    occurred_at = models.DateTimeField()         
    subject_name = models.CharField(max_length=100) 
         
    memo = models.TextField(blank=True)              

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case_name

class CCTV(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"CCTV at {self.address}"
    class Meta:
        db_table = 'cctv'  # ✅ DB의 실제 테이블명과 일치시킴

