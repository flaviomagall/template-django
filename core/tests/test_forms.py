# core/tests/test_forms.py

from django import forms

class CustomTestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

def test_form_valid_data():
    form = CustomTestForm(data={'name': 'Test Name', 'email': 'test@example.com'})
    assert form.is_valid()

def test_form_invalid_data():
    form = CustomTestForm(data={'name': '', 'email': 'not-an-email'})
    assert not form.is_valid()
    assert form.errors['name'] == ['Este campo é obrigatório.']
    assert form.errors['email'] == ['Informe um endereço de email válido.']
