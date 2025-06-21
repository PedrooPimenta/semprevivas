FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /semprevivas

# Copia todos os arquivos do projeto para o container
COPY . /semprevivas

# Atualiza o pip
RUN pip install --upgrade pip

# Instala as dependências listadas no requirements.txt (incluindo psycopg2-binary)
RUN pip install -r requirements.txt

# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# Comando para rodar o servidor Django quando o container iniciar
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
