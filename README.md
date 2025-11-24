# fastapi-template

## Prioridades de Mejora

### 1. **Autenticación y Autorización**

- Implementar un sistema de autenticación basado en OAuth2 con JWT.
- Definir roles y permisos para controlar el acceso a las rutas.

### 2. **Manejo de Errores Global**

- Crear un middleware para capturar errores no controlados.
- Estandarizar las respuestas de error.

### 3. **Versionado de la API**

- Agregar prefijos como `/v1` o `/v2` para manejar cambios futuros en la API.

### 4. **Paginación y Ordenación Avanzada**

- Permitir múltiples campos de ordenación.
- Agregar soporte para filtros más complejos (e.g., rangos, operadores lógicos).

### 5. **Configuración para Entornos**

- Separar configuraciones por entorno (desarrollo, producción, pruebas).
- Usar variables como `ENV=development` y cargar configuraciones específicas.

### 6. **Soporte para Relaciones entre Modelos**

- Agregar soporte para relaciones en los modelos SQLModel (e.g., un héroe puede tener misiones).

### 7. **Logging Avanzado**

- Configurar logs por nivel (info, warning, error).
- Agregar logs para solicitudes entrantes y salientes.
