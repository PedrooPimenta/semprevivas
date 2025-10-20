

# Configuração e Inicialização do Sistema Sempre Vivas

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalados os seguintes softwares:

* **Python 3.x**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **Docker**: [https://www.docker.com/get-started](https://www.docker.com/get-started)
* **PostgreSQL**: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

---

## Executando o sistema com Docker

1. **Subir os containers do Docker**

```bash
docker compose up --build
```

2. **Criar as migrações do Django**

```bash
docker compose exec web python manage.py makemigrations
```

3. **Aplicar as migrações no banco de dados**

```bash
docker compose exec web python manage.py migrate
```

4. **Criar um superusuário do Django**

```bash
docker compose exec web python manage.py createsuperuser
```

Após isso, o painel administrativo estará acessível em:

```
http://localhost:8000/admin
```


* Após criar o superusuário, acesse o painel do Django .
* Cadastre o **administrador que vai gerenciar o sistema** e atribua-o ao grupo “Adm”.
* Esse usuário poderá alterar tipos de usuário diretamente pelo sistema, sem precisar acessar o painel do Django.

5. **Importar os dados iniciais**


Importe os dados iniciais necessários para o funcionamento do sistema com o comando:

```bash
docker compose exec web python import_taxons.py
```

6. **Executar o sistema**

```bash
docker compose up
```

---

## Rodando o sistema sem Docker

1. **Criar e ativar um ambiente virtual**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/macOS
```

2. **Instalar dependências**

```bash
pip install -r requirements.txt
```

3. **Configurar o banco de dados PostgreSQL**

* Crie um banco de dados no PostgreSQL com o nome que será usado no Django.
* No `settings.py` do Django, configure os dados de conexão:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. **Criar as migrações do Django**

```bash
python manage.py makemigrations
```

5. **Aplicar as migrações no banco de dados**

```bash
python manage.py migrate
```

6. **Importar os dados iniciais**


Importe os dados iniciais necessários para o funcionamento do sistema com o comando:

```bash
 python import_taxons.py
```


7. **Criar um superusuário do Django**

```bash
python manage.py createsuperuser
```

* Após criar o superusuário, acesse o painel do Django .
* Cadastre o **administrador que vai gerenciar o sistema** e atribua-o ao grupo “Adm”.
* Esse usuário poderá alterar tipos de usuário diretamente pelo sistema, sem precisar acessar o painel do Django.

8. **Executar o sistema**

```bash
python manage.py runserver
```
