
# Alpine compilato con glibc, per phantomjs
FROM frolvlad/alpine-glibc

WORKDIR /code

COPY requirements.txt .
COPY src/ .

# Installa phantomjs già compilato per raspberry
RUN apk --no-cache add gcc curl py-cryptography fontconfig freetype-dev && \
    curl -o /tmp/phantomjs -sSL https://github.com/fg2it/phantomjs-on-raspberry/releases/download/v2.1.1-wheezy-jessie/phantomjs && \
    mv /tmp/phantomjs /usr/local/bin/phantomjs && \
    chmod a+x /usr/local/bin/phantomjs && \
    rm -rf /tmp/phantomjs

# Installa python e librerie associate
RUN apk add --no-cache python3 py3-pip && \
    pip3 install -r requirements.txt

CMD ["python3", "./main.py"]
