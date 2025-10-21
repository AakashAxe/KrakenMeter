from django.db import models

SHORT_CHAR = 50

# Create your models here.
class ProcessedFiles(models.Model):
    file_name = models.CharField(max_length=255)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class CustomerFlowData(models.Model):           # TODO : Do we need this model?
    customer_id = models.CharField(max_length=SHORT_CHAR)

    def __str__(self):
        return f"Customer {self.customer_id} - Uploaded at {self.uploaded_at}"

class MPANCore(models.Model):
    mpan_core = models.CharField(max_length=13, unique=True)
    bcs_validation_status = models.CharField(max_length=SHORT_CHAR)

    def __str__(self):
        return self.mpan_core

class Meter(models.Model):
    mpan_core = models.ForeignKey(MPANCore, on_delete=models.CASCADE, related_name='meters')
    meter_id = models.CharField(max_length=SHORT_CHAR, unique=True)
    meter_type = models.CharField(max_length=SHORT_CHAR)

    def __str__(self):
        return self.meter_id

class Reading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='meter_readings')
    meter_register_id = models.CharField(max_length=SHORT_CHAR)
    reading_date_time = models.DateTimeField()
    register_reading = models.FloatField()
    reset_date_time = models.DateTimeField(blank=True, null=True)
    md_reset_count = models.IntegerField(blank=True, null=True)
    reading_flag = models.CharField(max_length=SHORT_CHAR, blank=True, null=True)
    reading_method = models.CharField(max_length=SHORT_CHAR)
