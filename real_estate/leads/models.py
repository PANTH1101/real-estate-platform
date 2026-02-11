from django.db import models

from property.models import Property


class BuyerLead(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="leads"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.property_id}"



