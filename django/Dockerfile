FROM python:3.9.19

COPY ./utils/setup.sh /setup.sh
COPY ./srcs/requirements.txt /requirements.txt

RUN chmod +x /setup.sh
RUN chmod +w /requirements.txt

RUN /setup.sh

WORKDIR /srcs/transcendence

CMD sleep infinity
