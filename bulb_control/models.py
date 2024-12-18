from django.db import models

class Bulb(models.Model):
    state = models.BooleanField(default=False)  

    def __str__(self):
        return "On" if self.state else "Off"

