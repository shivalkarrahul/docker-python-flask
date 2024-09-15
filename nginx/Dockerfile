# Use the official Nginx image version 1.13 based on Alpine Linux, which is lightweight and minimal
FROM nginx:1.13-alpine

# Copy the custom Nginx configuration file from the 'conf' directory on your local machine 
# to the '/etc/nginx/conf.d/default.conf' file inside the container, replacing the default config
COPY conf /etc/nginx/conf.d/default.conf
