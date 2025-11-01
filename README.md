# 🤖 Sistema AFD (Autómatas Finitos Deterministas)

API REST robusta para reconocimiento de palabras usando Autómatas Finitos Deterministas con validaciones avanzadas y persistencia automática.

## 🚀 Características Principales

- ✅ **API REST completa** con FastAPI
- ✅ **Almacenamiento en memoria** durante la sesión
- ✅ **Validaciones robustas** con límites de seguridad
- ✅ **Carga automática** de autómatas por defecto al deploy
- ✅ **Containerización** con Docker
- ✅ **Testing automatizado** 
- ✅ **CI/CD** para deploy automático

## 📊 Comportamiento de Almacenamiento

### 🔄 **Al hacer deploy:**
1. Se cargan automáticamente los autómatas desde `data/automatas.txt`
2. Se inicializa el sistema con autómatas por defecto

### 💾 **Al cargar nuevos autómatas:**
1. Se almacenan en memoria durante la sesión del servidor
2. Permanecen disponibles mientras el servidor esté corriendo
3. Se pueden usar normalmente para verificar palabras

### 🔄 **Al recargar la página:**
1. Los autómatas cargados por el usuario se pierden
2. Solo quedan los autómatas por defecto del sistema
3. Es necesario cargar nuevamente archivos de autómatas

### 🔄 **Al reiniciar el servidor:**
1. Se resetea completamente el store
2. Se cargan únicamente los autómatas por defecto
3. Todos los autómatas subidos por el usuario se pierden

> **Nota:** Este comportamiento es intencional para mantener el sistema limpio y evitar acumulación de autómatas temporales.

## 🛠 Instalación y Uso

### Con Docker (Recomendado)
```bash
# Clonar repositorio
git clone https://github.com/llimaix/automatas-AFD.git
cd automatas-AFD

# Iniciar con Docker Compose
docker-compose up -d

# Verificar estado
./backend-commands.sh status
```

### Desarrollo Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor de desarrollo
./backend-commands.sh dev
```

## 📡 API Endpoints

### Principales
- `GET /automata` - Listar autómatas cargados
- `POST /upload` - Subir archivo de autómatas
- `POST /check` - Verificar palabra
- `GET /automata/{name}/info` - Información detallada

### Administración
- `POST /admin/clear` - Limpiar todos los autómatas
- `POST /admin/reset` - Resetear a autómatas por defecto
- `GET /admin/status` - Estado del sistema

## 📁 Estructura de Archivos

```
app/
├── api.py          # API REST con FastAPI
├── dfa.py          # Clase DFA principal
├── parser.py       # Parser de archivos
└── store.py        # Store en memoria

data/
└── automatas.txt   # Autómatas por defecto

examples/           # 5 archivos de ejemplo
tests/              # Tests automatizados
```

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Probar ejemplos
python test_examples.py

# Demo de mejoras
python demo_improvements.py
```

## 🔧 Gestión del Backend

```bash
# Comandos disponibles
./backend-commands.sh build      # Construir imagen
./backend-commands.sh run        # Ejecutar contenedor
./backend-commands.sh dev        # Servidor de desarrollo
./backend-commands.sh logs       # Ver logs
./backend-commands.sh status     # Estado del sistema
./backend-commands.sh test       # Probar endpoints
```

## 🌐 Deploy

El sistema incluye CI/CD automático para AWS EC2:

1. Push a rama `main` → Deploy automático
2. Configurar secrets en GitHub:
   - `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`
3. El deploy incluye carga automática de autómatas por defecto

## 📝 Formato de Archivos

```plaintext
1:NOMBRE:estado1,estado2,estado3
2:NOMBRE:simbolo1,simbolo2
3:NOMBRE:estado_inicial
4:NOMBRE:estado_final1,estado_final2
5:NOMBRE:estado1,simbolo,estado2;estado2,simbolo,estado1
```

## 🔒 Seguridad

- Límites de tamaño de archivo (5MB)
- Sanitización de nombres e identificadores
- Validación de caracteres permitidos
- Protección contra path traversal
- Límites de procesamiento configurables

---

**Desarrollado con ❤️ para el reconocimiento robusto de patrones usando AFDs**
