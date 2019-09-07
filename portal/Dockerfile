FROM python:3.6-jessie
RUN mkdir /app
RUN mkdir /app/static
WORKDIR /app
ADD requirements.txt /app
RUN pip install -U pip && pip install -r requirements.txt
ADD . /app
ARG API_HOST
ENV API_HOST="$API_HOST"
CMD ./run.sh
