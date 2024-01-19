from django.db import models
import os

class Resume(models.Model):
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.content and self.file:
            if os.path.exists(self.file.path):
                # Read text content from the file and save it to the 'content' field
                with open(self.file.path, 'r', encoding='utf-8', errors='ignore') as file:
                    self.content = file.read().replace('\x00', '')
            else:
                # Handle the case when the file is missing
                print(f"Warning: File not found at {self.file.path}")
                # You can choose to raise an exception, log an error, or provide a default value

        super().save(*args, **kwargs)
