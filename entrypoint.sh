#!/bin/sh
# Iniciar o daemon Docker se não estiver rodando
dockerd  &

# Aguardar o daemon Docker iniciar
sleep 5

# Executar o Redis em background
docker run -d -p 6379:6379 -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker redis

# Comando original para manter o contêiner rodando
exec "$@"