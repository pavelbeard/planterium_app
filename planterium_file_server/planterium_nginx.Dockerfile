FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/conf.d/default.conf; apk add apache2-utils
COPY config/nginx.conf /etc/nginx/nginx.conf