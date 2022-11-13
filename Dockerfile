FROM ubuntu:22.10

ADD ./ /web

WORKDIR /web

ENV PACKAGE gcc libpq-dev vim curl python3.11 python3-pip supervisor

RUN apt-get update \
    && apt-get install -y ${PACKAGE} \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /web/requirements.txt

CMD ["/usr/bin/supervisord", "-c", "/web/supervisor/supervisord.conf", "-n"]
