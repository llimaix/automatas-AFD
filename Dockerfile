# Multi-stage build para Frontend de Automatas AFD
FROM node:18-alpine AS builder

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de npm
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa de producción con Nginx
FROM nginx:alpine

# Remover la configuración por defecto de nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiar archivos construidos desde la etapa builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Crear usuario nginx si no existe
RUN addgroup -g 101 -S nginx && adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx || true

# Exponer puerto 80
EXPOSE 80

# Usar nginx en modo foreground
CMD ["nginx", "-g", "daemon off;"]