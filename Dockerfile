FROM python:3.11

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /semprevivas

# Copie os arquivos de código fonte do Django para o contêiner
COPY . /semprevivas

RUN pip install --upgrade pip
# Instale as dependências do aplicativo
RUN pip install -r requirements.txt

# Exponha a porta em que o aplicativo Django será executado
EXPOSE 8000

# Comando para iniciar o servidor Django quando o contêiner for iniciado
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
