from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Container(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=8)
    frontend_port = models.IntegerField(unique=True)
    backend_port = models.IntegerField()
    couchdb_port = models.IntegerField()
    redis_port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Container for {self.user.email} on port {self.frontend_port}"