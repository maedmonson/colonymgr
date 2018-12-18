from django.contrib import admin
from .models import Yard
from .models import Colony
from .models import Queen


# Register your models here.
admin.site.register(Yard)
admin.site.register(Colony)
admin.site.register(Queen)
