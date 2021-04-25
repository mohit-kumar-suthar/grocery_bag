from django.db import models

type_choice= [
    ('brought', 'Brought'),
    ('not available', 'Not Available'),
    ('pending', 'Pending'),
    ]


class product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=type_choice,)
    created_at = models.DateField(auto_now_add=True)