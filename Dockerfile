FROM python:3

LABEL MAINTAINER Vee Zhang <veezhang@126.com>

WORKDIR /create-features-demo

COPY src /create-features-demo

RUN pip3 install -r /create-features-demo/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

EXPOSE 8888

WORKDIR /create-features-demo

ENTRYPOINT python server.py