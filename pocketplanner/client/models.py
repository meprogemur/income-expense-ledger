from django.db import models
from django.contrib.auth.models import User
from tenant_schemas.models import TenantMixin
import os


class Client(TenantMixin):
    REQUIRED_FIELDS = ('user', 'name')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    domain_url = models.URLField(
        blank=True, null=True, default=os.getenv('DOMAIN'))
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
