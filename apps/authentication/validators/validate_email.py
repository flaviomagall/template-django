from django.core.exceptions import ValidationError

def validate_email(value):
    if not value or "@" not in value:
        raise ValidationError("Por favor, forneça um endereço de e-mail válido.")
