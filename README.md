# Instalação do projeto

### Pré-instalação

Caso você já tenha o VirtualEnv instalado, pode pular essa etapa.

Para instalar, antes é preciso criar um ambiente virtual. Considere instalar o virtualenvwrapper:

    $ sudo pip install virtualenvwrapper

Reinicie seu terminal ou execute:

    $ source /usr/local/bin/virtualenvwrapper.sh

### Instalação

Crie o virtualenv:

    $ mkvirtualenv proxy_github_api

     
Instale os pacotes necessários, lembre-se de estar dentro do virtualenv criado:

    $ pip install -r requirements.txt
    $ pip install -r requirements_dev.txt

    
Reinicie seu terminal e vai pra galera.
