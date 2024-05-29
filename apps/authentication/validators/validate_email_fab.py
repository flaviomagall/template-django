from django.core.exceptions import ValidationError
from django.conf import settings

def validate_fab_email(value):
    domain = settings.EMAIL_DOMAIN_REQUIRED
    if not value.endswith(f'@{domain}'):
        raise ValidationError(f"O e-mail deve estar no domínio {domain}.")
