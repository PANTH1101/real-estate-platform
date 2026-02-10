from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def total_properties(self) -> int:
        return self.properties.count()




