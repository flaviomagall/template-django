# apps/authentication/views.py
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from apps.authentication.forms import RegisterForm
from django.contrib.auth import get_user_model
from utils.template_layout import TemplateLayout



User = get_user_model()

class RegisterView(TemplateView):
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateLayout.set_layout(TemplateLayout.LayoutsDisplay.layout_blank)  # Passar o nome do layout como string
        context.update({
            "form": RegisterForm(),  # Adiciona o formulário ao contexto se for GET request
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Lógica de criação do usuário
            user = form.save()
            login(request, user)  # Loga o usuário após o registro
            messages.success(request, "Conta criada com sucesso!")
            return redirect('home')

        # Se algo der errado, renderizar novamente o formulário com erros
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
