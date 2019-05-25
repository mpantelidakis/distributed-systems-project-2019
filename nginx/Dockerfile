FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

# link media and static access logs with stdout. Neat for debugging.
RUN ln -sf /dev/stdout /var/log/nginx/mediafiles.access.log && \
    ln -sf /dev/stdout /var/log/nginx/staticfiles.access.log