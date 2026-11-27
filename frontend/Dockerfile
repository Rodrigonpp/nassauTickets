# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve com nginx
FROM nginx:alpine

# Remove a config padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copia a config customizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia o build do React
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]