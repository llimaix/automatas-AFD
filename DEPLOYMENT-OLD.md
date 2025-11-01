# � Guía de Despliegue EC2 con Docker

Esta guía te ayudará a configurar el despliegue automático de tu frontend en EC2 usando Docker y GitHub Actions.

## 📋 Prerrequisitos

1. **Servidor EC2** con Ubuntu 20.04+ 
2. **Acceso SSH** al servidor
3. **Repositorio GitHub** con permisos de administrador
4. **Docker** y **Docker Compose** (se instalan automáticamente)

## 🔧 Configuración del Servidor EC2

### Paso 1: Preparar el servidor

Conéctate a tu servidor EC2 y ejecuta el script de configuración:

```bash
# Conectarse al servidor
ssh -i tu-clave.pem ubuntu@tu-ip-ec2

# Descargar y ejecutar script de configuración
wget https://raw.githubusercontent.com/llimaix/automatas-AFD/main/scripts/setup-ec2.sh
chmod +x setup-ec2.sh
./setup-ec2.sh

# IMPORTANTE: Desconectarse y volver a conectar para que los cambios tomen efecto
exit
ssh -i tu-clave.pem ubuntu@tu-ip-ec2
```

O puedes copiar y pegar el script manualmente desde `scripts/setup-ec2.sh`.

### Paso 2: Configurar Security Groups

Asegúrate de que tu EC2 tenga estos puertos abiertos:
- **Puerto 22** (SSH)
- **Puerto 80** (HTTP)
- **Puerto 443** (HTTPS - opcional)

## 🔐 Configuración de GitHub Secrets

Ve a tu repositorio en GitHub → Settings → Secrets and variables → Actions

Agrega estos secrets:

| Secret Name | Descripción | Ejemplo |
|-------------|-------------|---------|
| `EC2_HOST` | IP pública de tu EC2 | `54.123.456.789` |
| `EC2_USER` | Usuario SSH (normalmente `ubuntu`) | `ubuntu` |
| `EC2_SSH_KEY` | Clave privada SSH completa | `-----BEGIN RSA PRIVATE KEY-----...` |
| `EC2_PORT` | Puerto SSH (opcional, default: 22) | `22` |

### Cómo obtener la clave SSH:

```bash
# En tu máquina local, muestra el contenido de tu clave privada
cat ~/.ssh/tu-clave.pem

# Copia TODO el contenido, incluyendo las líneas BEGIN y END
```

## � Arquitectura del Despliegue

### Dockerfile Multi-stage
- **Stage 1**: Build de la aplicación con Node.js
- **Stage 2**: Servir con Nginx optimizado

### Docker Compose
- Gestión de contenedores
- Configuración de red
- Health checks
- Restart automático

## �🚀 Proceso de Despliegue

### Despliegue Automático

El despliegue se activa automáticamente cuando:
- Haces push a las ramas `main` o `front`
- Se crea un Pull Request hacia `main`

### Proceso completo:
1. **Build**: Construye la imagen Docker de la aplicación
2. **Transfer**: Envía la imagen al servidor EC2
3. **Deploy**: Detiene contenedores anteriores y inicia el nuevo
4. **Verify**: Verifica que el contenedor esté funcionando

### Despliegue Manual

También puedes activar el despliegue manualmente desde GitHub:
1. Ve a tu repositorio → Actions
2. Selecciona "Deploy Frontend to EC2 with Docker"
3. Click en "Run workflow"

## 📁 Estructura en el Servidor

```
~/automatas-afd/
├── docker-compose.yml
└── /tmp/automatas-deploy/
    ├── frontend-image.tar
    └── docker-compose.yml

Docker Containers:
└── afd-api:latest
    ├── /usr/share/nginx/html/ (aplicación)
    └── /etc/nginx/conf.d/default.conf
```

## 🔍 Verificar el Despliegue

### Comandos útiles en el servidor:

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs del contenedor
docker logs afd-api

# Verificar estado del contenedor
docker inspect afd-api

# Reiniciar contenedor si es necesario
docker-compose restart

# Ver estadísticas de recursos
docker stats afd-api
```

### Verificar la aplicación:
```bash
# Probar la aplicación
curl -I http://localhost

# Ver respuesta completa
curl http://localhost
```

## 🌐 Acceder a la Aplicación

Después del despliegue exitoso, tu aplicación estará disponible en:
```
http://TU-IP-EC2
```

## 🛠️ Troubleshooting

### Error común: Contenedor no inicia
```bash
# Ver logs detallados
docker logs afd-api --tail 50

# Verificar imagen
docker images | grep automatas-afd

# Reiniciar contenedor
docker-compose down && docker-compose up -d
```

### Error: Puerto ocupado
```bash
# Ver qué está usando el puerto 80
sudo netstat -tulpn | grep :80

# Detener contenedor anterior
docker stop $(docker ps -q --filter "publish=80")
```

### Error de permisos Docker
```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión SSH
exit
ssh -i tu-clave.pem ubuntu@tu-ip-ec2
```

### Error de conexión SSH en GitHub Actions
1. Verifica que la IP en `EC2_HOST` sea correcta
2. Asegúrate de que el Security Group permita SSH desde cualquier IP (0.0.0.0/0)
3. Verifica que la clave SSH esté completa en el secret

## 📈 Monitoreo

### Ver el progreso del despliegue:
1. Ve a GitHub → Actions
2. Selecciona el workflow en ejecución
3. Observa los logs en tiempo real

### Health Check automático:
El contenedor incluye un health check que verifica cada 30 segundos si la aplicación responde correctamente.

```bash
# Ver estado del health check
docker ps --format "table {{.Names}}\t{{.Status}}"
```

## 🔄 Rollback

Si necesitas hacer rollback a una versión anterior:

1. Ve a GitHub Actions
2. Encuentra un despliegue exitoso anterior
3. Click en "Re-run all jobs"

### Rollback manual:
```bash
# Ver imágenes disponibles
docker images

# Detener contenedor actual
docker-compose down

# Cambiar a imagen anterior y reiniciar
docker tag afd-api:backup afd-api:latest
docker-compose up -d
```

## 🧹 Mantenimiento

### Limpieza automática:
El script configura una tarea cron que limpia recursos Docker no utilizados cada domingo a las 2 AM.

### Limpieza manual:
```bash
# Limpiar imágenes no utilizadas
docker image prune -f

# Limpiar todo el sistema
docker system prune -f

# Ver uso de espacio
docker system df
```

## 📊 Ventajas del Despliegue con Docker

✅ **Aislamiento**: La aplicación corre en su propio entorno aislado
✅ **Consistencia**: Mismo entorno en desarrollo y producción
✅ **Escalabilidad**: Fácil de escalar horizontalmente
✅ **Rollback rápido**: Cambios instantáneos entre versiones
✅ **Gestión de dependencias**: Todas las dependencias incluidas en la imagen
✅ **Seguridad**: Aislamiento a nivel de sistema operativo

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de GitHub Actions
2. Verifica los logs del contenedor Docker
3. Asegúrate de que todos los secrets estén configurados correctamente
4. Verifica que Docker esté funcionando en el servidor