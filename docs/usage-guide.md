# Guía de Uso de la API

Esta guía explica cómo utilizar la API, incluyendo filtros, ordenamiento, paginación y todos los endpoints disponibles.

## 📋 Tabla de Contenidos

- [Endpoints Disponibles](#endpoints-disponibles)
- [Sistema de Filtros](#sistema-de-filtros)
- [Sistema de Ordenamiento](#sistema-de-ordenamiento)
- [Paginación](#paginacion)
- [Formato de Respuestas](#formato-de-respuestas)
- [Códigos de Estado](#codigos-de-estado)

## Endpoints Disponibles

### Heroes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/test/heroes` | Lista todos los héroes (con filtros, ordenamiento y paginación) |
| GET | `/test/heroes/{hero_id}` | Obtiene un héroe por ID |
| POST | `/test/heroes` | Crea un nuevo héroe |
| PUT | `/test/heroes/{hero_id}` | Actualiza completamente un héroe |
| PATCH | `/test/heroes/{hero_id}` | Actualiza parcialmente un héroe |
| DELETE | `/test/heroes/{hero_id}` | Elimina un héroe |

## Sistema de Filtros

El sistema de filtros permite filtrar recursos por múltiples campos y operadores.

### Formato

```
campo:operador:valor,campo2:operador2:valor2
```

### Operadores Disponibles

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `eq` | Igual a | `name:eq:Spider-Man` |
| `ne` | Diferente de | `name:ne:Thanos` |
| `gt` | Mayor que | `age:gt:18` |
| `ge` | Mayor o igual | `age:ge:18` |
| `lt` | Menor que | `age:lt:65` |
| `le` | Menor o igual | `age:le:65` |
| `like` | Contiene (case insensitive) | `name:like:Spider` |
| `in` | En lista (separador `;`) | `name:in:Spider-Man;Iron Man;Thor` |
| `not_in` | No en lista (separador `;`) | `name:not_in:Thanos;Loki` |
| `is_null` | Es nulo | `age:is_null:` |
| `is_not_null` | No es nulo | `age:is_not_null:` |

### Ejemplos de Filtros

#### Filtro simple - Igual a

```bash
GET /test/heroes?filter=name:eq:Spider-Man
```

Busca héroes cuyo nombre sea exactamente "Spider-Man".

#### Filtro - Contiene

```bash
GET /test/heroes?filter=name:like:Spider
```

Busca héroes cuyo nombre contenga "Spider" (Spider-Man, Spider-Woman, etc.).

#### Filtro - Mayor que

```bash
GET /test/heroes?filter=age:gt:18
```

Busca héroes mayores de 18 años.

#### Filtro - Rango (múltiples condiciones)

```bash
GET /test/heroes?filter=age:ge:18,age:le:65
```

Busca héroes entre 18 y 65 años (ambos inclusive).

#### Filtro - En lista

```bash
GET /test/heroes?filter=name:in:Spider-Man;Iron Man;Thor
```

Busca héroes cuyo nombre sea Spider-Man, Iron Man o Thor.

> **Nota**: El operador `in` usa punto y coma (`;`) como separador, no coma.

#### Filtro - Combinado

```bash
GET /test/heroes?filter=age:gt:18,name:like:Spider
```

Busca héroes mayores de 18 años cuyo nombre contenga "Spider".

#### Filtro - Es nulo

```bash
GET /test/heroes?filter=age:is_null
```

Busca héroes sin edad definida.

## Sistema de Ordenamiento

El sistema de ordenamiento permite ordenar los resultados por uno o múltiples campos.

### Formato

```
campo:direccion,campo2:direccion2
```

### Direcciones Disponibles

| Dirección | Descripción | Ejemplo |
|-----------|-------------|---------|
| `asc` | Ascendente (A→Z, 0→9) | `name:asc` |
| `desc` | Descendente (Z→A, 9→0) | `age:desc` |

> **Nota**: Si no se especifica dirección, se usa `asc` por defecto.

### Ejemplos de Ordenamiento

#### Ordenar por un campo

```bash
GET /test/heroes?sort=name:asc
```

Ordena por nombre ascendente (A→Z).

```bash
GET /test/heroes?sort=age:desc
```

Ordena por edad descendente (mayor a menor).

#### Ordenar por múltiples campos

```bash
GET /test/heroes?sort=age:desc,name:asc
```

Ordena primero por edad (mayor a menor) y luego por nombre (A→Z).

#### Ordenar sin especificar dirección

```bash
GET /test/heroes?sort=name
```

Ordena por nombre ascendente (dirección por defecto).

## Paginación

Todos los endpoints de listado soportan paginación mediante parámetros de query.

### Parámetros

| Parámetro | Tipo | Descripción | Valor por defecto | Restricciones |
|-----------|------|-------------|-------------------|---------------|
| `page` | int | Número de página | 1 | >= 1 |
| `size` | int | Elementos por página | 10 | 1-100 |

### Ejemplos de Paginación

#### Primera página con 10 elementos

```bash
GET /test/heroes?page=1&size=10
```

#### Segunda página con 20 elementos

```bash
GET /test/heroes?page=2&size=20
```

#### Máximo de elementos por página

```bash
GET /test/heroes?page=1&size=100
```

## Combinando Filtros, Ordenamiento y Paginación

Puedes combinar filtros, ordenamiento y paginación en una sola petición.

### Ejemplo Completo

```bash
GET /test/heroes?filter=age:gt:18,name:like:Spider&sort=age:desc,name:asc&page=1&size=10
```

Esta petición:

1. Filtra héroes mayores de 18 años cuyo nombre contenga "Spider"
2. Ordena por edad descendente, luego por nombre ascendente
3. Devuelve la primera página con 10 resultados

## Formato de Respuestas

Todas las respuestas siguen un formato estandarizado.

### Respuesta Exitosa (con datos)

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Spider-Man",
    "age": 25,
    "secret_name": "Peter Parker",
    "created_at": "2025-11-25T10:00:00",
    "updated_at": "2025-11-25T10:00:00"
  },
  "message": "Hero detail",
  "error": null
}
```

### Respuesta Exitosa (paginada)

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Spider-Man",
      "age": 25,
      "secret_name": "Peter Parker"
    },
    {
      "id": 2,
      "name": "Iron Man",
      "age": 45,
      "secret_name": "Tony Stark"
    }
  ],
  "message": "Heroes list",
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 50,
    "pages": 5
  },
  "error": null
}
```

### Respuesta de Error

```json
{
  "success": false,
  "data": null,
  "message": "Hero not found",
  "error": {
    "code": "HERO_NOT_FOUND",
    "detail": "Hero with ID 999 does not exist"
  }
}
```

## Códigos de Estado

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Petición exitosa (GET, PUT, PATCH) |
| 201 | Created | Recurso creado exitosamente (POST) |
| 204 | No Content | Recurso eliminado exitosamente (DELETE) |
| 400 | Bad Request | Datos inválidos o filtros/ordenamiento mal formados |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Error de validación de datos |
| 500 | Internal Server Error | Error interno del servidor |

## Operaciones CRUD

### Crear un Héroe (POST)

```bash
POST /test/heroes
Content-Type: application/json

{
  "name": "Spider-Man",
  "age": 25,
  "secret_name": "Peter Parker"
}
```

**Respuesta (201 Created):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Spider-Man",
    "age": 25,
    "secret_name": "Peter Parker",
    "created_at": "2025-11-25T10:00:00",
    "updated_at": "2025-11-25T10:00:00"
  },
  "message": "Hero created"
}
```

### Obtener un Héroe (GET)

```bash
GET /test/heroes/1
```

**Respuesta (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Spider-Man",
    "age": 25,
    "secret_name": "Peter Parker"
  },
  "message": "Hero detail"
}
```

### Actualizar Completamente (PUT)

Requiere **todos** los campos.

```bash
PUT /test/heroes/1
Content-Type: application/json

{
  "name": "Spider-Man",
  "age": 26,
  "secret_name": "Peter Parker"
}
```

### Actualizar Parcialmente (PATCH)

Permite enviar **solo los campos a modificar**.

```bash
PATCH /test/heroes/1
Content-Type: application/json

{
  "age": 26
}
```

### Eliminar un Héroe (DELETE)

```bash
DELETE /test/heroes/1
```

**Respuesta (200 OK):**

```json
{
  "success": true,
  "message": "Hero deleted"
}
```

## Validaciones

### Campos Requeridos

Al crear un héroe, los siguientes campos son obligatorios:

- `name` (string)
- `secret_name` (string)

El campo `age` es opcional.

### Validaciones de Filtros

- Los campos deben existir en el modelo
- Los operadores deben ser válidos
- El formato debe ser correcto: `campo:operador:valor`

### Validaciones de Ordenamiento

- Los campos deben existir en el modelo
- Las direcciones deben ser `asc` o `desc`
- El formato debe ser correcto: `campo:direccion`

## Errores Comunes

### Error: Campo no válido en filtro

```json
{
  "success": false,
  "error": {
    "detail": "Invalid filter field: 'invalid_field'"
  }
}
```

**Solución**: Verifica que el campo exista en el modelo.

### Error: Operador no válido

```json
{
  "success": false,
  "error": {
    "detail": "Invalid operator: 'invalid_op'"
  }
}
```

**Solución**: Usa uno de los operadores válidos (eq, ne, gt, ge, lt, le, like, in, not_in, is_null, is_not_null).

### Error: Formato de filtro incorrecto

```json
{
  "success": false,
  "error": {
    "detail": "Invalid filter format"
  }
}
```

**Solución**: Asegúrate de usar el formato `campo:operador:valor`.

## Consejos de Uso

1. **Usa paginación**: Siempre especifica `page` y `size` para controlar el volumen de datos.
2. **Combina filtros**: Puedes usar múltiples filtros separados por coma.
3. **Ordena estratégicamente**: El ordenamiento múltiple se aplica en el orden especificado.
4. **PATCH vs PUT**: Usa PATCH para actualizaciones parciales y PUT para reemplazos completos.
5. **Valida antes de enviar**: Verifica que los datos cumplan con las validaciones antes de hacer la petición.

## Próximos Pasos

- Revisa los [Ejemplos](examples.md) para ver casos de uso prácticos
- Consulta la [Guía de Desarrollo](development-guide.md) si quieres extender la API
