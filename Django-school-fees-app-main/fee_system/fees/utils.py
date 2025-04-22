from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Student, FeeCategory, FeePayment

def generate_clearance_pdf(student):
    # Check if all required fees are paid
    required_categories = FeeCategory.objects.filter(is_required_for_clearance=True)
    paid_categories = FeePayment.objects.filter(
        student=student,
        fee_category__in=required_categories
    ).values_list('fee_category', flat=True)

    if not set(required_categories.values_list('id', flat=True)).issubset(set(paid_categories)):
        return None  # Not all fees paid

    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # PDF Content (customize as needed)
    p.drawString(100, 800, "OFFICIAL CLEARANCE CERTIFICATE")
    p.drawString(100, 750, f"This certifies that {student.name} (ID: {student.student_id})")
    p.drawString(100, 730, f"of {student.department} {student.level} has paid all required fees")
    p.drawString(100, 710, "and is cleared to take examinations.")
    p.drawString(100, 650, "Signed: _________________________")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer