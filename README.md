# Configuração e Inicialização do Sistema


## 1. Subir os containers do Docker

Para construir e iniciar os containers, execute o comando:

```bash
docker compose up --build
```

## 2. Criar as migrações do Django

Após os containers estarem em execução, crie as migrações com o comando:

```bash
docker compose exec web python manage.py makemigrations
```

## 3. Aplicar as migrações no banco de dados

```bash
docker compose exec web python manage.py migrate
```

## 4. Criar um usuário administrador do sistema

Crie um superusuário para acessar o painel administrativo:

```bash
docker compose exec web python manage.py createsuperuser
```

## 5. Importar os dados iniciais

Importe os dados iniciais necessários para o funcionamento do sistema com o comando:

```bash
docker compose exec web python import_taxons.py
```

## 6. Executar o sistema

Após concluir os passos anteriores, execute o sistema:

```bash
docker compose up
```
