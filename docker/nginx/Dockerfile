FROM jonasal/nginx-certbot:3.0.0-nginx1.21.3-alpine

COPY user-entrypoint.d /docker-entrypoint.d
COPY user_conf.d /etc/nginx/user_conf.d
COPY templates /etc/nginx/templates
COPY robots /var/www/robots
