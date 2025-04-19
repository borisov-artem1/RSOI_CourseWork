FROM node:20-alpine as build

WORKDIR /frontend

COPY ./frontend/package*.json ./
RUN npm config set legacy-peer-deps true
RUN npm ci --silent

COPY ./frontend/ .
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /frontend/build /usr/share/nginx/html
COPY --from=build /frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
