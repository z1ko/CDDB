
############################# BASE #############################
# Installa requisiti progetto                                      #
################################################################

FROM python:3.9.2-slim AS base

RUN apt-get update

# Crea ambiente di lavoro.
WORKDIR /app
COPY ./requirements.txt /app/

# Installa librerie progetto.
RUN pip3 install -r requirements.txt
 
############################# PROD #############################
# Carica file sorgenti di python                               #
################################################################

FROM base AS prod

COPY ./src/ /app/
CMD python3 /app/main.py