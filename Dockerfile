FROM python:3.6-stretch

LABEL maintainer="daniel@smart-lgt.com"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --fix-missing texlive-full

RUN apt-get install -y locales

ADD ./src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

ADD ./src /code

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENV PYTHONIOENCODING utf8

WORKDIR /code

EXPOSE 5000

ENTRYPOINT [ "gunicorn" ]

CMD ["-w", "2", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--access-logformat", "%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"" , "app:app" ]
