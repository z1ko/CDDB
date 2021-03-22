
############################# BASE #############################
# Installa requisiti progetto                                      #
################################################################

FROM python:3.8.5-slim AS base

RUN apt-get update && apt-get install -y git

# Crea ambiente di lavoro.
WORKDIR /app
COPY ./requirements.txt /app/

# Installa librerie progetto.
RUN pip3 install -r requirements.txt
 
# Installa anche la versione corretta di prestapyt
RUN pip3 install --ignore-installed git+https://github.com/prestapyt/prestapyt.git@master

############################# PROD #############################
# Carica file sorgenti di python                               #
################################################################

FROM base AS prod

COPY ./src/ /app/
CMD python3 /app/main.py
