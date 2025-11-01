# 📁 Archivos de Ejemplo para AFDs

Esta carpeta contiene 5 archivos de ejemplo diseñados para probar diferentes aspectos del sistema AFD mejorado.

## 🗂️ Descripción de los Archivos

### 1. `ejemplo1_basico.txt` - AFDs Fundamentales
**Propósito**: Casos básicos y completos para pruebas iniciales
- **TERMINA_EN_A**: Acepta cadenas que terminan en 'a'
- **DIV_POR_3**: Acepta números binarios divisibles por 3
- **SOLO_ABC**: Acepta únicamente la cadena "abc"

**Casos de prueba sugeridos**:
```
TERMINA_EN_A: "abba" ✅, "abbb" ❌, "" ❌
DIV_POR_3: "11" ✅, "110" ✅, "111" ❌
SOLO_ABC: "abc" ✅, "ab" ❌, "abcd" ❌
```

### 2. `ejemplo2_incompletos.txt` - AFDs Incompletos
**Propósito**: Probar el manejo de AFDs con función de transición parcial
- **INCOMPLETO_1**: Falta transición desde q1 con 'b'
- **INCOMPLETO_2**: Múltiples transiciones faltantes
- **PARA_MERGE**: AFD parcial que se completa con merge

**Casos de prueba sugeridos**:
```
INCOMPLETO_1: "aa" ✅, "ab" ❌ (transición faltante)
INCOMPLETO_2: "xyz" ❌ (transición faltante)
```

### 3. `ejemplo3_merge.txt` - Testing de Merge
**Propósito**: Probar la funcionalidad de merge y alfabetos grandes
- **PARA_MERGE**: Completa el AFD del archivo anterior
- **PAR_A_Y_B**: Acepta cadenas con número par de 'a' y 'b'
- **ALFABETO_GRANDE**: AFD con alfabeto extendido (letras + números)

**Casos de prueba sugeridos**:
```
PARA_MERGE: "012" ✅ (después del merge)
PAR_A_Y_B: "" ✅, "ab" ✅, "a" ❌
ALFABETO_GRANDE: "a0a" ✅, "b1e" ✅
```

### 4. `ejemplo4_mundo_real.txt` - Validadores Prácticos
**Propósito**: Casos de uso reales para validación de patrones
- **NUMERO_ENTERO**: Valida números enteros (solo dígitos)
- **IDENTIFICADOR**: Valida identificadores (letra + alfanuméricos)
- **COMENTARIO**: Detecta comentarios de línea (//)

**Casos de prueba sugeridos**:
```
NUMERO_ENTERO: "123" ✅, "12a" ❌
IDENTIFICADOR: "var1" ✅, "123" ❌
COMENTARIO: "slashslash" ✅, "slash" ❌
```

### 5. `ejemplo5_casos_extremos.txt` - Límites y Casos Edge
**Propósito**: Probar límites del sistema y casos extremos
- **SOLO_VACIO**: Solo acepta cadena vacía
- **NUNCA_ACEPTA**: Estado final inalcanzable
- **MUCHOS_FINALES**: Múltiples estados finales
- **INICIAL_ES_FINAL**: Estado inicial también es final
- **ESTADOS_LARGOS**: Nombres de estados muy largos

**Casos de prueba sugeridos**:
```
SOLO_VACIO: "" ✅, "a" ❌
NUNCA_ACEPTA: "" ❌, "ab" ❌
INICIAL_ES_FINAL: "" ✅, "go" ❌
```

## 🚀 Cómo Usar los Ejemplos

### 1. Via API (FastAPI)
```bash
# Subir archivo
curl -X POST "http://localhost:8000/upload" \
  -F "file=@examples/ejemplo1_basico.txt"

# Verificar palabra
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{"automata": "TERMINA_EN_A", "word": "abba"}'
```

### 2. Via CLI
```bash
# Cargar y probar
python -m app.cli -f examples/ejemplo1_basico.txt check TERMINA_EN_A abba
```

### 3. Script de Prueba Automatizado
```bash
# Ejecutar todas las pruebas
python test_examples.py
```

## 📊 Características Probadas

- ✅ **AFDs completos e incompletos**
- ✅ **Merge de definiciones de AFDs**
- ✅ **Alfabetos grandes y caracteres especiales**
- ✅ **Validación de nombres y límites**
- ✅ **Casos extremos y edge cases**
- ✅ **Manejo robusto de errores**
- ✅ **Estados iniciales = finales**
- ✅ **Estados inalcanzables**

## 🔧 Funcionalidades Demostradas

1. **Validación de completitud**: Detecta transiciones faltantes
2. **Merge inteligente**: Combina definiciones compatibles
3. **Límites de seguridad**: Previene ataques de denegación de servicio
4. **Simulación robusta**: Maneja símbolos desconocidos y palabras largas
5. **Logging detallado**: Rastrea todas las operaciones
6. **Respuestas informativas**: Incluye metadatos útiles

¡Estos archivos te permitirán explorar todas las capacidades del sistema AFD mejorado! 🎯