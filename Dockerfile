# Use a versão mais recente de Docker DinD como base
FROM docker:latest

# Instala Python 3.8 e pip
RUN apk add --no-cache python3 py3-pip supervisor python3-dev pcre-dev supervisor bash
# Define o diretório de trabalho no container
WORKDIR /app

# Create a virtual environment in the container
RUN python3 -m venv /app/venv

# Activate virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copie o arquivo de requisitos primeiro para aproveitar o cache da camada Docker
COPY requirements.txt /app/

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o diretório de trabalho
COPY app.py /app/
COPY pppwn /usr/local/bin/pppwn
COPY 1100/stage1.bin /data/stage1.bin
COPY 1100/stage2.bin /data/stage2.bin

# Expõe a porta que a aplicação Flask usará
EXPOSE 3000

# Configurar o Supervisor para gerenciar os processos

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Define o comando para iniciar a aplicação
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
USER root
ENTRYPOINT ["entrypoint.sh"]
# Iniciar o Supervisor quando o container for iniciado
CMD ["sh", "-c", "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
