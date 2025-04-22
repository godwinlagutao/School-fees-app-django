from django.contrib import admin
from .models import Student, FeeCategory, FeePayment, Clearance

class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_category', 'amount_paid', 'date_paid')
    search_fields = ('student__name', 'student__student_id')

admin.site.register(Student)
admin.site.register(FeeCategory)
admin.site.register(FeePayment, FeePaymentAdmin)
admin.site.register(Clearance)