from django.conf import settings
from django.db import models

from apps.properties.models import Property


class Enquiry(models.Model):
    id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enquiries")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="enquiries")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Enquiry {self.id} on {self.property_id}"


