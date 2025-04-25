from django.db import models

# Create your models here.

class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.TextField()
    stringPrice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    ingredients = models.TextField()
    image = models.ImageField(upload_to='/images/')
    rating = models.FloatField()
    comments = models.JSONField(
        default=list,  # پیش‌فرض را یک لیست خالی قرار می‌دهد
        blank=True     # اجازه می‌دهد این فیلد خالی باشد
    )
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        price = self.price
        if price is not None:
            self.stringPrice = str(price)