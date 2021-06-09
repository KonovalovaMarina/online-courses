FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=0
WORKDIR /usr/src/online-courses

RUN apk update \
 && apk add --no-cache \
    bash \
    libc-dev \
    linux-headers \
    libressl-dev \
    libuuid \
    util-linux-dev \
    libseccomp-dev \
    g++ \
    gcc \
    musl-dev \
    linux-headers \
    postgresql-dev \
    zlib-dev \
    jpeg-dev \
    libmagic

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk add git openssh

COPY . .
ENV FLASK_APP ./app/app.py
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
