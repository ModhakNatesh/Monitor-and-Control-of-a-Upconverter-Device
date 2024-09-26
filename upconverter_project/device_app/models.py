from django.db import models
from django.contrib.auth.models import User

class DeviceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action} - {self.status}"

class Device(models.Model):
    frequency = models.IntegerField(default = 0.0)
    gain = models.IntegerField(default = 0.0)
    mute = models.BooleanField(default = False)  # 1 for ON, 0 for OFF
    frequency_step = models.IntegerField(default = 0.0)

    def __str__(self):
        return (f"Device - Frequency: {self.frequency} MHz, Gain: {self.gain} dB, Mute: {self.mute}, Frequency Step: {self.frequency_step}")


