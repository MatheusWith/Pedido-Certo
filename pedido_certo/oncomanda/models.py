from django.db import models

class Tables(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.numero}"


class Resevarions(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, related_name='reservation')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Table {self.table.number} - {self.star_time.strftime('%d/%m %H:%M')}"

    def save(self, *args, **kwargs):
        overlapping = TimeSlot.objects.filter(
            table=self.table,
            start__lt=self.end,
            end__gt=self.start,
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This table already has a reservation during this time.")

        super().save(*args, **kwargs)

class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Products)
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)


    def __str__(self):
        return f"Order {self.id} - Table {self.table.name}"
