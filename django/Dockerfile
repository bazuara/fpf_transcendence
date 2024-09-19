FROM python:3.12.5

COPY ./utils/setup.sh /setup.sh
COPY ./srcs/requirements.txt /requirements.txt

RUN chmod +x /setup.sh && chmod +w /requirements.txt && /setup.sh

WORKDIR /srcs/transcendence

COPY ./utils/entrypoint.sh /entrypoint.sh
CMD bash /entrypoint.sh
