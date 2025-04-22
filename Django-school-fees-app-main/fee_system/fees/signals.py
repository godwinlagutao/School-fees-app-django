import logging
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FeePayment, FeeCategory, Clearance , Student # Must import all used models

logger = logging.getLogger(__name__)

def update_clearance_status(student):
    """Helper function to update clearance status"""
    try:
        with transaction.atomic():
            required_fees = set(
                FeeCategory.objects
                .filter(is_required_for_clearance=True)
                .values_list('id', flat=True)
            )
            
            paid_fees = set(
                student.feepayment_set
                .values_list('fee_category_id', flat=True)
            )
            
            clearance, _ = Clearance.objects.get_or_create(
                student=student,
                defaults={'is_approved': False}
            )
            
            clearance.is_approved = paid_fees.issuperset(required_fees)
            clearance.save()
            
    except Exception as e:
        logger.error(f"Clearance update failed for {student}: {str(e)}")

# Signal handlers
@receiver(post_save, sender=FeePayment)
def handle_payment_update(sender, instance, **kwargs):
    update_clearance_status(instance.student)

@receiver(post_delete, sender=FeePayment)
def handle_payment_delete(sender, instance,  **kwargs):
    update_clearance_status(instance.student)


@receiver(post_save, sender=Student)
def create_student_clearance(sender, instance, created, **kwargs):
    if created:
        Clearance.objects.create(student=instance)