from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    @property
    def clearance(self):
        """Easy access to clearance without circular reference"""
        return self.clearance_set.first()

class FeeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_required_for_clearance = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.amount})"

class FeePayment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank Transfer'),
        ('CARD', 'Credit/Debit Card'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHODS, default='BANK')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.fee_category}"

class Clearance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE,unique=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Clearance for {self.student}"