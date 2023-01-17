##Para utilizar o Docker precisamos pegar uma imagem com o comando FROM no https://hub.docker.com ou criamos uma nós mesmos
##Utilizamos o COPY para copiar tudo que esta na pasta web para pasta raiz do apache
##Utilizamos o EXPOSE para abrir uma porta web seguido do numero da porta
##No terminal para contruirmos o docker com o comando  "docker build -t web_apache ." O ponto se refere a pasta que está executando
##Utilizamos o comando docker image ls para ver as imagens do Docker que temos
##Para subir a imagem para o servidor utilizamos o comando "Docker run -d -p 80:80 web_apache" -p = porta da maquina   80= numero da porta: 80 Numero do contanier que vou mapear -d para servidor continuar rodando
## Docker ps para mostrar os contanier ativos
##Docker Stop + CONTAINER ID para parar



FROM httpd
COPY ./web/ /usr/local/apache2/htdocs/
EXPOSE 80
