
############################# BASE #############################
# Immagien base per avere selenium, firefox, geckodriver       #
################################################################

FROM ubuntu:groovy AS base

# Evitiamo di compilare con rust il pacchetto crypthography, 
# troppo lungo da fare su un raspberry
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# Installa backbone: pip e firefox
RUN apt-get update -y --fix-missing && apt-get install -y \
    build-essential                                       \
    libssl-dev                                            \
    libffi-dev                                            \
    python-dev                                            \
    python3-pip                                           \
    firefox-geckodriver                                   \
    firefox						  \
    xvfb

# Crea ambiente di lavoro
WORKDIR /app
COPY ./requirements.txt /app/

# Installa librerie progetto
RUN pip3 install -r requirements.txt
 
############################# PROD #############################
# Carica file sorgenti di python                               #
################################################################

FROM base AS prod

COPY ./src/ /app/
CMD python3 /app/main.py

