FROM nginx:alpine
WORKDIR /app
COPY nginx.docker.conf /etc/nginx/nginx.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]