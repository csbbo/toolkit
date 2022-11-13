FROM bitnami/openresty:1.21
ADD . /openresty

RUN apt-get update \
    && apt-get install -y python3-certbot-nginx vim \
    && ln -svf /openresty/nginx.conf /etc/nginx/nginx.conf # certbot detection

WORKDIR /openresty

CMD ["openresty", "-c", "/openresty/nginx.conf"]
