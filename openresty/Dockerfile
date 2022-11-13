FROM bitnami/openresty:1.21
ADD . /web/openresty

RUN apt-get update \
    && apt-get install -y python3-certbot-nginx vim \
    && ln -svf /web/openresty/nginx.conf /etc/nginx/nginx.conf # certbot detection

WORKDIR /web/openresty

CMD ["openresty", "-c", "/web/openresty/nginx.conf"]
