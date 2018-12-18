from django.db import models
from django.contrib.auth.models import User

class Yard(models.Model):
    created_by = models.ForeignKey(User, related_name='yards' ,on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True )
    description = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class Colony(models.Model):
    created_by = models.ForeignKey(User, related_name='colonies', on_delete=models.PROTECT)
    yard = models.ForeignKey(Yard, related_name='colonys',on_delete=models.PROTECT)
    location = models.CharField(max_length=10, unique=True)
    colony_type = models.CharField(max_length=25)
    start_at = models.DateTimeField(null=True ,blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.location

class Queen(models.Model):
    created_by = models.ForeignKey(User, related_name='queens', on_delete=models.PROTECT)
    yard = models.ForeignKey(Yard, related_name='queens', default=None, on_delete=models.PROTECT)
    colony = models.ForeignKey(Colony, related_name='queens',on_delete=models.PROTECT)
    queen_no = models.CharField(max_length=10, unique=True)
    queen_color = models.CharField(max_length=10)
    cell_install_at = models.DateTimeField(null=True)
    birth_at = models.DateTimeField(null=True)
    laying_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.queen_color + ' ' + self.queen_no

class Colony_log(models.Model):
    colony = models.ForeignKey(Colony, related_name='colony_logs',on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=4000)
    visited_at = models.DateTimeField(null=True)


class Queen_log(models.Model):
    queen = models.ForeignKey(Queen, related_name='queen_logs',on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=4000)
    visited_at = models.DateTimeField(null=True)

