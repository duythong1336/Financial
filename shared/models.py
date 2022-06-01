from django.db import models

class BaseModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null = True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null = True)
    
    class Meta:
        abstract = True
        
class SoftDeleteModel(models.Model):

    isDeleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.isDeleted = True
        # partial update
        self.save(update_fields = ['isDeleted'])

    def restore(self):
        self.isDeleted = False
        self.save(update_fields = ['isDeleted'])

    class Meta:
        abstract = True