
############################# BASE #############################
# Immagien base per avere selenium, firefox, geckodriver       #
################################################################

FROM selenium/standalone-chrome AS base

USER root
RUN apt-get update && apt-get install -y python3-pip 

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

