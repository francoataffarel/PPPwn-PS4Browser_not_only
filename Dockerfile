# Use a versão mais recente de Docker DinD como base
FROM docker:latest

# Instala Python 3.8 e pip
RUN apk add --no-cache python3 py3-pip python3-dev pcre-dev bash nano gcc musl-dev linux-headers

# Define o diretório de trabalho no container
WORKDIR /app

# Cria um ambiente virtual no container
RUN python3 -m venv /app/venv

# Ativa o ambiente virtual
ENV PATH="/app/venv/bin:$PATH"


# Copie o arquivo de requisitos primeiro para aproveitar o cache da camada Docker
COPY requirements.txt /app/

# Instale as dependências do Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o diretório de trabalho
COPY app.py /app/
COPY pppwn /usr/local/bin/pppwn
COPY 1100/stage1.bin /app/data/1100/stage1.bin
COPY 1100/stage2.bin /app/data/1100/stage2.bin

# Define o comando para iniciar a aplicação
RUN chmod +x /usr/local/bin/pppwn
USER root
# Iniciar o aplicativo Python quando o container for iniciado
CMD ["python3", "app.py"]
