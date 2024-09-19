FROM python:3.12.5

COPY ./utils/setup.sh /setup.sh
COPY ./srcs/requirements.txt /requirements.txt

RUN chmod +x /setup.sh && chmod +w /requirements.txt && /setup.sh && \
    openssl genpkey -algorithm RSA -out /key.pem -pkeyopt rsa_keygen_bits:2048 && \
    openssl req -new -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout /key.pem -out /cert.pem \
        -subj "/C=SP/ST=Madrid/L=Madrid/O=42-fpf_transcendence/OU=42Madrid/CN=transcendence.com"

WORKDIR /srcs/transcendence

COPY ./utils/entrypoint.sh /entrypoint.sh
CMD bash /entrypoint.sh
