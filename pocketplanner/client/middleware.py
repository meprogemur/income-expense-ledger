from django.core.exceptions import ObjectDoesNotExist
from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import get_public_schema_name
from django.contrib.auth.models import User


class RequestIDTenantMiddleware(BaseTenantMiddleware):

    def get_tenant(self, model, hostname, request):
        try:
            public_schema = model.objects.get(
                schema_name=get_public_schema_name())
        except ObjectDoesNotExist:
            public_schema = model.objects.create(
                domain_url=hostname,
                schema_name=get_public_schema_name(),
                name=get_public_schema_name().capitalize(),)
        public_schema.save()
        user = request.user
        print(user)
        try:
            user = User.objects.get(username=user)
        except:
            user = None
        if user is None:
            return public_schema
        else:
            tenant_model = model.objects.get(
                user=User.objects.get(username=user))
            print(tenant_model, public_schema)
            return tenant_model
