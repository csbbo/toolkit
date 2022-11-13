FROM bitnami/openresty:1.21
ADD . /openresty

WORKDIR /openresty

CMD ["openresty", "-c", "/openresty/nginx.conf"]
