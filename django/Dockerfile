FROM python:3.12.5

COPY ./utils/setup.sh /setup.sh
COPY ./srcs/requirements.txt /requirements.txt
COPY ./utils/entrypoint.sh /entrypoint.sh

RUN chmod +x /setup.sh && chmod +w /requirements.txt && /setup.sh

WORKDIR /srcs/transcendence

CMD sleep infinity
