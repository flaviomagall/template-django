<!-- markdownlint-disable MD033 -->

# Configuração Padrão (Completa)

## Que eu utilizo em varios projetos

Esse é o padrão de configuração de projeto que utilizo.

### Configurações Iniciais

<details>
    <summary>
        <b>Ambiente Virtual Linux/Windows</b>
    </summary>

* #### Criar o ambiente virtual Linux/Windows

    ```python
    ## Windows
    python -m venv .venv
    source .venv/Scripts/activate # Ativar ambiente
    ## Linux 
    ## Caso não tenha virtualenv. "pip install virtualenv"
    virtualenv .venv
    source .venv/bin/activate # Ativar ambiente
    ```

* #### Instalar os seguintes pacotes

    ```python
    pip install django
    pip install pillow
    ```

* #### Para criar o arquivo *requirements.txt*

    ```python
    pip freeze > requirements.txt
    ```

</details>

<details>
    <summary>
        <b>Criando o Projeto</b>
    </summary>

* #### “core” é nome do seu projeto e quando colocamos um “.” depois do nome do projeto significa que é para criar os arquivos na raiz da pasta. Assim não cria subpasta do projeto

    ```python
    django-admin startproject core .
    ```

* #### Testar a aplicação

    ```python
    python manage.py runserver
    ```

</details>

<details>
    <summary>
        <b>Arquivos Statics</b>
    </summary>

* #### Configurando Arquivos Static

    ```python
    import os 
    
    # base_dir config
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
    STATIC_DIR=os.path.join(BASE_DIR,'static')
    
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
        }
    }
    
    STATIC_ROOT = os.path.join(BASE_DIR,'static')
    STATIC_URL = '/static/' 
    
    MEDIA_ROOT=os.path.join(BASE_DIR,'media')
    MEDIA_URL = '/media/'
    
    # Internationalization
    # Se quiser deixar em PT BR
    LANGUAGE_CODE = 'pt-br'
    TIME_ZONE = 'America/Sao_Paulo'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    ```

* #### Configurando core.urls.py

    ```python
    from django.contrib import admin
    from django.conf import settings
    from django.conf.urls.static import static
    from django.urls import path
    
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto
    ```

</details>

<details>
    <summary>
        <b>Variáveis de Ambiente</b>
    </summary>

* #### Variáveis de Ambiente

    Para configurar variáveis de ambiente vamos utilizar biblioteca **python-dotenv.** Existem outras concorrentes, mas eu gosto de usar o python-dotenv.*

    **Alternativas:**

  * [Honcho](https://github.com/nickstenning/honcho)
  * [django-dotenv](https://github.com/jpadilla/django-dotenv)
  * [django-environ](https://github.com/joke2k/django-environ)
  * [django-environ-2](https://github.com/sergeyklay/django-environ-2)
  * [django-configuration](https://github.com/jezdez/django-configurations)
  * [dump-env](https://github.com/sobolevn/dump-env)
  * [environs](https://github.com/sloria/environs)
  * [dynaconf](https://github.com/rochacbruno/dynaconf)
  * [parse_it](https://github.com/naorlivne/parse_it)

* #### Link: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)

    “*Python-dotenv lê pares chave-valor de um arquivo `.env` e pode defini-los como variáveis de ambiente. Ajuda no desenvolvimento de aplicações seguindo os princípios dos [12 fatores](http://12factor.net/)”*

    Da uma olhada nos 12 fatores é interessante.

    Vamos lá. Primeiramente vamos instalar essa biblioteca na aplicação.

    ```bash
    pip install python-dotenv
    ```

    Feito isso vamos criar um arquivo chamado **“.env”**.

    Nesse arquivo vamos colocar as variáveis importantes como:
    ***senha do banco de dados, secret_key do django, api_key, chave cloud*** tudo que tem credenciais.

    Exemplo:

    ```python
    ## Não precisa colocar "" aspas
    SECRET_KEY=django-insecure-q(ge$586x7o9n)3w+6d_^t(m!ib&9%_m8&6@=m=sy@^7qf)#*_
    DEBUG=True
    SUPER_USER=ADMIN
    EMAIL=leticiateste@gmail.com
    
    NAME_DB=db.sqlite3
    USER_DB=root
    PASSWORD_DB=
    HOST_DB=localhost
    PORT_DB=3306
    
    EMAIL_HOST = 'smtp.office365.com' 
    EMAIL_HOST_USER = 'email@hotmail.com' 
    EMAIL_HOST_PASSWORD = 'sua senha' 
    EMAIL_PORT = 587 
    EMAIL_USE_TLS = True 
    DEFAULT_FROM_EMAIL = 'email@hotmail.com'
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    ```

    Sempre envio um arquivo exemplo **(sem as informações reais)** como esse exemplo “**_env**” no *commit*. Assim quando eu abaixo o repositório eu preencho somente as informações e renomeio o arquivo para “.**env**”. Lembrando o arquivo “.**env**” não vai nos *commits*. Essa informação deve estar no .*gitignore*. Caso for um servidor real ai você cria esse arquivo no servidor.  

    Feito isso pessoal. Vamos configurar no **core/settings.py**

    É assim que chamamos as variáveis.

    ```python
    # importar a biblioteca
    from dotenv import load_dotenv
    
    # adicionar essa tag para que nosso projeto encontre o .env
    load_dotenv(os.path.join(BASE_DIR, ".env"))
    
    # chamar as variaveis assim
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    DEBUG = os.getenv('DEBUG')
    
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, os.getenv('NAME_DB')),
       #'USER':os.getenv('USER_DB')
       #'PASSWORD': os.getenv('PASSWORD_DB')
       #'HOST':os.getenv('HOST_DB')
       #'PORT':os.getenv('PORT_DB')
    
     }
    }
    
    # Se tiver configuração de email
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') 
    EMAIL_PORT = os.getenv('EMAIL_PORT') 
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') 
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    
    ```

</details>

<details>
    <summary>
        <b>CORS HEADERS</b>
    </summary>

* #### Configuração

    Para configurar os Cors Headers precisamos instalar uma biblioteca.

    [https://pypi.org/project/django-cors-headers/](https://pypi.org/project/django-cors-headers/)

    *“Adicionar cabeçalhos CORS permite que seus recursos sejam acessados em outros domínios. É importante que você entenda as implicações antes de adicionar os cabeçalhos, pois você pode estar abrindo involuntariamente os dados privados do seu site para outras pessoas.”*

    Instalar a Biblioteca na nossa aplicação

    ```bash
    pip install django-cors-headers
    ```

    ```python
    # Adicionar no core.settings.py

    from corsheaders.defaults import default_headers
    ```

    ```python
    INSTALLED_APPS = [
        ...,
        "corsheaders",
        ...,
    ]
    ```

    ```python
    MIDDLEWARE = [
        ...,
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        ...,
    ]
    ```

    ```python
    ALLOWED_HOSTS = [ 
      'localhost', 
      '127.0.0.1',  
    ]
    
    CORS_ALLOW_HEADERS = list(default_headers) + [
         'X-Register',
    ]
    
    # CORS Config
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = False
    ```

    SSL and Cookies Vamos deixar configurado tambem.
    doc: [https://docs.djangoproject.com/en/4.1/ref/settings/](https://docs.djangoproject.com/en/4.1/ref/settings/)

    ```python
    if not DEBUG:
     SECURE_SSL_REDIRECT = True
     ADMINS = [(os.getenv('SUPER_USER'), os.getenv('EMAIL'))]
     SESSION_COOKIE_SECURE = True
     CSRF_COOKIE_SECURE = True
    ```

</details>

<details>
    <summary>
        <b>LOGS</b>
    </summary>

* #### Vamos configurar os Logs

    Precisamos Instalar essa biblioteca.

    Documentação: [https://pypi.org/project/django-requestlogs/](https://pypi.org/project/django-requestlogs/)

    ```bash
    pip install django-requestlogs
    ```

    Adicionar no ***core.settings.py***

    ```python
    # core.settings.py

    MIDDLEWARE = [
        ...
        'requestlogs.middleware.RequestLogsMiddleware',
        ...
    ]
    ```

    ```python
    REST_FRAMEWORK={
        ...
        'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
    }
    ```

    Documentação: [https://docs.djangoproject.com/en/4.1/topics/logging/#topic-logging-parts-loggers](https://docs.djangoproject.com/en/4.1/topics/logging/#topic-logging-parts-loggers)

    ```python
    # Logs
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'requestlogs_to_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'info.log',
            },
        },
        'loggers': {
            'requestlogs': {
                'handlers': ['requestlogs_to_file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    
    REQUESTLOGS = {
        'SECRETS': ['password', 'token'],
        'METHODS': ('PUT', 'PATCH', 'POST', 'DELETE'),
    }
    ```

</details>

<details>
    <summary>
        <b>Timeout</b>
    </summary>

* #### Vamos utilizar a biblioteca **Django Session Timeout:**

    doc: [https://pypi.org/project/django-session-timeout/](https://pypi.org/project/django-session-timeout/)

    Instalar Biblioteca.

    **`pip install django-session-timeout`**

    ```python
    MIDDLEWARE_CLASSES = [
        # ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django_session_timeout.middleware.SessionTimeoutMiddleware',
        # ...
    ]
    ```

    ```python
    # timeout tempo de inatividate no sistema
    SESSION_EXPIRE_SECONDS = 1800 
    SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
    #SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60  
    SESSION_TIMEOUT_REDIRECT = 'http://localhost:8000/'
    ```

    ```python
    LOGIN_URL = 'login'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'
    ```

</details>

<details>
    <summary>
        <b>Arquivo Context Processors</b>
    </summary>

* #### Essa configuração permite criar um contexto Global no seu projeto. Assim você pode chamar esse contexto em qualquer aplicativo do seu projeto

    Primeiro criar um arquivo ***context_processors.py*** na pasta do seu projeto.

    ```python
    # from myapp import models
    
    def context_social(request):
        return {'social': 'Exibir este contexto em qualquer lugar!'}
    ```

    Ai precisamos registar as funções aqui.

    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    # Apps
                    'core.context_processors.context_social', 
                ],
            },
        },
    ]
    ```

    Feito essa configuração o contexto “social” se torna Global no seu projeto. Assim você pode chamado em qualquer aplicativo do seu projeto.

</details>

<details>
    <summary>
        <b>Aplicativo Base (templates, statics)</b>
    </summary>

* #### Aplicativo Base (templates, statics)

    **Vamos criar nosso aplicativo base no Django.**

    Aplicação *base* vamos deixar os arquivos base que é utilizado no projeto inteiro. Como templates e arquivos statics como css, js e até images estáticas.

    ```python
    python manage.py startapp base
    ```

    Agora precisamos registrar nossa aplicação no *INSTALLED_APPS* localizado em *settings.py*.

    Apos criar app base pode criar as pastas nessa estrutura.

    1- pasta ***“templates”*** dentro dela colocar **base.html** (vazia por enquanto)

    2 - pasta ***“static”*** dentro dela criar pastas **css, image, js.** Cria os arquivos, style.css e javascript.js.

* ### Template Base

    No arquivo ***base.html*** colocar esse template

    É aqui que vamos renderizar nosso conteúdo. Para não ter que repetir esse template em todas as paginas que criarmos, então fazemos um base e utilizamos *extends* para usar nos outros templates.

    *base/templates/base.html*

    ```python
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
     <meta charset="UTF-8">
     <meta http-equiv="X-UA-Compatible" content="IE=edge">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>{% block title %}{% endblock %}</title>
     
     <!-- CSS -->
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
     
     <link rel="stylesheet" href="{% static 'css/style.css' %}">
     
    </head>
    <body>  
     
     {% block content %}
     
     {% endblock %} 
     
     <!-- JS-->
     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
     <script src="{% static 'js/scripts.js' %}"></script>
    </body>
    </html>
    ```

</details>

<details>
    <summary>
        <b>Django Message</b>
    </summary>

* #### Configura mensagem

    Documentação: [https://docs.djangoproject.com/en/4.1/ref/contrib/messages/](https://docs.djangoproject.com/en/4.1/ref/contrib/messages/)

    Nossa biblioteca tem essas configurações de mensagens ativas. Que funciona perfeitamente, mas precisamos renderizar isso no *frontend*. Como estamos utilizando *bootstrap* precisamos adicionar essa configuração no *settings.py* do seu projeto. Adicionando essa configuração as mensagens de alerta aparecerá com as classes do bootstrap.

    ***core/settings.py***

    ```python
    # --- Messages --- #
    from django.contrib.messages import constants
    
    MESSAGE_TAGS = {
     constants.ERROR: 'alert-danger',
     constants.WARNING: 'alert-warning',
     constants.DEBUG: 'alert-info',
     constants.SUCCESS: 'alert-success',
     constants.INFO: 'alert-info',
    }
    ```

    ***base/templates/message.html***

    ```python
    {% if messages %}
    <div class="messages">
        {% for message in messages %}
        <div {% if message.tags %} class="alert {{ message.tags }}"{% endif %} role="alert">{{ message }}</div>
        {% endfor %}
    </div>
    {% endif %}
    ```

    Adiciona na base

    ```python
    <body> 
     {% include 'message.html' %} ## adiciona isso.
     {% block content %}
     {% endblock %} 
    </body>
    ```

</details>

<details><summary><b>Criando Aplicativo</b></summary>

* ####     **Vamos criar nosso aplicativo no Django.**

    Para criar a aplicação no Django rode comando abaixo. “myapp” é nome do seu **Aplicativo**.

    ```python
    python manage.py startapp myapp
    ```

    Agora precisamos registrar nossa aplicação no *INSTALLED_APPS* localizado em *settings.py*.

    *myapp*/*templates*/*index.html*

    ```html
    {% extends 'base.html' %}
    {% block title %}Pagina 1{% endblock %}
    {% block content %}
     <h1>Pagina 1</h1>
     <p>Testando o context Global</p>
     <p>{{social}}</p>
    {% endblock %}
    ```

    *myapp*/*views.py*

    ```python
    from django.shortcuts import render
    
    # Create your views here.
    def index(request):
        return render(request, 'index.html')
    ```

    criar arquivo *myapp*/*urls.py*

    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        path('', views.index, name='index'), 
    ]
    ```

    urls.py do projeto. ***core/urls.py***

    ```python
    from django.contrib import admin
    from django.urls import path, include # adicionar include
    from django.conf import settings
    from django.conf.urls.static import static 
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('myapp.urls')), # url do app
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto
    ```

    Rodar o projeto para ver como está.

    ```python
    python manage.py makemigrations && python manage.py migrate
    python manage.py runserver
    ```

</details>

<details>

<summary><b>Criando Permissões</b></summary>

* #### **Vamos configurar nossas permissões dos usuários**

    Para implementar o role_permissions no seu projeto Django e permitir a gestão de permissões através do painel de administração, você pode seguir os passos abaixo:

    **Instalando a Biblioteca**

    ```python
    pip install django-role-permissions
    ```

    **Configurar o settings.py**

    Adicione rolepermissions ao seu arquivo settings.py na lista de INSTALLED_APPS:

    ```python
    INSTALLED_APPS = [
    ...
    'rolepermissions',
    ...
    ]
    ```

    Configure também o módulo:

    ```python
    ROLEPERMISSIONS_MODULE = 'core.roles'  # Caminho para o módulo onde as roles são definidas
    ```

    **Defina as Permissões**

    Crie um arquivo permissions.py dentro do app core e defina suas permissões:

    ```python
    # core/permissions.py

    CONSULTAR_ITEM = 'consultar_item'
    CRIAR_PEDIDO = 'criar_pedido'
    ```

    **Definir as Roles**

    Crie um arquivo roles.py dentro do app core e defina suas roles:

    ```python
    # core/roles.py

    from rolepermissions.roles import AbstractUserRole
    from core.permissions import CONSULTAR_ITEM, CRIAR_PEDIDO

    class Usuario(AbstractUserRole):
        available_permissions = {
            CONSULTAR_ITEM: True,
        }

    class Cliente(AbstractUserRole):
        available_permissions = {
            CONSULTAR_ITEM: True,
            CRIAR_PEDIDO: True,
        }
    ```

    **Sincronizar as Permissões**

    Você precisa sincronizar as permissões definidas no role_permissions com o banco de dados. Execute o comando a seguir:

    ```bash
    python manage.py sync_roles
    ```

</details>

<details>

<summary>
    <b>Criando Testes</b>
</summary>

* #### Instalar pytest-django

    Primeiro, instale a biblioteca pytest-django se ainda não tiver instalado:

    ```bash
    pip install pytest-django
    ```

* #### Configurar pytest-django

    Crie um arquivo pytest.ini no diretório raiz do seu projeto e adicione as seguintes configurações:

    ```ini
    [pytest]
    DJANGO_SETTINGS_MODULE = seu_projeto.settings
    ```

* #### Escrever os Testes

  * Teste Roles

    Crie um arquivo test_roles.py dentro do seu app core e adicione os testes para verificar as permissões.

    ```python
    # core/tests/test_roles.py

    import pytest
    from django.contrib.auth import get_user_model
    from rolepermissions.roles import assign_role, clear_roles
    from rolepermissions.checkers import has_permission
    from core.permissions import CONSULTAR_ITEM, CRIAR_PEDIDO

    User = get_user_model()

    @pytest.mark.django_db
    def test_usuario_permissao_consultar_item():
        user = User.objects.create_user(username='usuario', password='password')
        assign_role(user, 'usuario')

        assert has_permission(user, CONSULTAR_ITEM)
        assert not has_permission(user, CRIAR_PEDIDO)

    @pytest.mark.django_db
    def test_cliente_permissao_consultar_item_e_criar_pedido():
        user = User.objects.create_user(username='cliente', password='password')
        assign_role(user, 'cliente')

        assert has_permission(user, CONSULTAR_ITEM)
        assert has_permission(user, CRIAR_PEDIDO)

    @pytest.mark.django_db
    def test_alterar_role_do_usuario():
        user = User.objects.create_user(username='usuario', password='password')
        assign_role(user, 'usuario')

        assert has_permission(user, CONSULTAR_ITEM)
        assert not has_permission(user, CRIAR_PEDIDO)

        # Alterar a role do usuário
        clear_roles(user)
        assign_role(user, 'cliente')

        assert has_permission(user, CONSULTAR_ITEM)
        assert has_permission(user, CRIAR_PEDIDO)
    ```

  * Teste Models

    Os testes de modelos verificam se as operações do banco de dados relacionadas aos modelos estão funcionando corretamente.

    ```python
    # core/tests/test_models.py

    import pytest
    from django.contrib.auth import get_user_model

    User = get_user_model()

    @pytest.mark.django_db
    def test_create_user():
        user = User.objects.create_user(username='testuser', password='password')
        assert user.username == 'testuser'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    @pytest.mark.django_db
    def test_create_superuser():
        admin_user = User.objects.create_superuser(username='admin', password='password')
        assert admin_user.username == 'admin'
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser
    ```

  * Teste Forms

    Os testes de forms verificam se os formulários estão validando os dados corretamente.

    ```python
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
    ```

* #### Executar os Testes

    Para executar os testes, use o comando:

    ```bash
    pytest
    ```

</details>
