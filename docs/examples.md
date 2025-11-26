# Ejemplos Prácticos

Esta guía contiene ejemplos prácticos de uso de la API con diferentes herramientas y lenguajes.

## 📋 Tabla de Contenidos

- [Ejemplos con cURL](#ejemplos-con-curl)
- [Ejemplos con Python (requests)](#ejemplos-con-python-requests)
- [Ejemplos con JavaScript (fetch)](#ejemplos-con-javascript-fetch)
- [Casos de Uso Completos](#casos-de-uso-completos)
- [Ejemplos de Testing](#ejemplos-de-testing)

## Ejemplos con cURL

### Crear un Héroe

```bash
curl -X POST http://localhost:8000/test/heroes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Spider-Man",
    "age": 25,
    "secret_name": "Peter Parker"
  }'
```

**Respuesta**:

```json
{
  "status": {
    "code": 201,
    "message": "Hero created"
  },
  "data": {
    "id": 1,
    "name": "Spider-Man",
    "age": 25,
    "secret_name": "Peter Parker",
    "created_at": "2025-11-25T10:00:00",
    "updated_at": "2025-11-25T10:00:00"
  }
}
```

### Listar Todos los Héroes

```bash
curl http://localhost:8000/test/heroes
```

### Filtrar Héroes por Edad

```bash
# Mayores de 18
curl "http://localhost:8000/test/heroes?filter=age:gt:18"

# Entre 18 y 65 años
curl "http://localhost:8000/test/heroes?filter=age:ge:18,age:le:65"
```

### Buscar Héroe por Nombre (parcial)

```bash
curl "http://localhost:8000/test/heroes?filter=name:like:Spider"
```

### Ordenar Héroes

```bash
# Por nombre ascendente
curl "http://localhost:8000/test/heroes?sort=name:asc"

# Por edad descendente
curl "http://localhost:8000/test/heroes?sort=age:desc"

# Por edad descendente, luego nombre ascendente
curl "http://localhost:8000/test/heroes?sort=age:desc,name:asc"
```

### Paginación

```bash
# Primera página, 10 elementos
curl "http://localhost:8000/test/heroes?page=1&size=10"

# Segunda página, 20 elementos
curl "http://localhost:8000/test/heroes?page=2&size=20"
```

### Consulta Completa (Filtro + Ordenamiento + Paginación)

```bash
curl "http://localhost:8000/test/heroes?filter=age:gt:18,name:like:Spider&sort=age:desc&page=1&size=10"
```

### Obtener un Héroe por ID

```bash
curl http://localhost:8000/test/heroes/1
```

### Actualizar Completamente un Héroe (PUT)

```bash
curl -X PUT http://localhost:8000/test/heroes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Spider-Man",
    "age": 26,
    "secret_name": "Peter Parker"
  }'
```

### Actualizar Parcialmente un Héroe (PATCH)

```bash
curl -X PATCH http://localhost:8000/test/heroes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "age": 27
  }'
```

### Eliminar un Héroe

```bash
curl -X DELETE http://localhost:8000/test/heroes/1
```

## Ejemplos con Python (requests)

### Configuración Inicial

```python
import requests
from typing import Dict, List, Any

BASE_URL = "http://localhost:8000"

class HeroClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
```

### Crear un Héroe

```python
def create_hero(name: str, secret_name: str, age: int = None) -> Dict[str, Any]:
    """Crea un nuevo héroe"""
    url = f"{BASE_URL}/test/heroes"
    payload = {
        "name": name,
        "secret_name": secret_name,
        "age": age
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

# Uso
result = create_hero("Spider-Man", "Peter Parker", 25)
print(f"Héroe creado con ID: {result['data']['id']}")
print(f"Status: {result['status']['message']}")
```

### Listar Héroes con Filtros

```python
def get_heroes(
    filter: str = None,
    sort: str = None,
    page: int = 1,
    size: int = 10
) -> Dict[str, Any]:
    """Obtiene lista de héroes con filtros opcionales"""
    url = f"{BASE_URL}/test/heroes"
    params = {
        "page": page,
        "size": size
    }
    
    if filter:
        params["filter"] = filter
    if sort:
        params["sort"] = sort
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Ejemplos de uso
# Todos los héroes (devuelve objeto con 'status' y 'data')
all_heroes = get_heroes()

# Mayores de 18
adults = get_heroes(filter="age:gt:18")

# Nombres que contienen "Spider", ordenados por edad
spider_heroes = get_heroes(
    filter="name:like:Spider",
    sort="age:desc"
)

# Con paginación
page_2 = get_heroes(page=2, size=20)
```

### Buscar Héroe por ID

```python
def get_hero(hero_id: int) -> Dict[str, Any]:
    """Obtiene un héroe por ID"""
    url = f"{BASE_URL}/test/heroes/{hero_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Uso
hero = get_hero(1)
print(f"Héroe: {hero['data']['name']}")
```

### Actualizar Héroe (PUT)

```python
def update_hero_put(
    hero_id: int,
    name: str,
    age: int,
    secret_name: str
) -> Dict[str, Any]:
    """Actualiza completamente un héroe"""
    url = f"{BASE_URL}/test/heroes/{hero_id}"
    payload = {
        "name": name,
        "age": age,
        "secret_name": secret_name
    }
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    return response.json()

# Uso
updated_hero = update_hero_put(1, "Spider-Man", 26, "Peter Parker")
```

### Actualizar Héroe (PATCH)

```python
def update_hero_patch(hero_id: int, **updates) -> Dict[str, Any]:
    """Actualiza parcialmente un héroe"""
    url = f"{BASE_URL}/test/heroes/{hero_id}"
    response = requests.patch(url, json=updates)
    response.raise_for_status()
    return response.json()

# Uso
# Solo actualizar edad
updated_hero = update_hero_patch(1, age=27)

# Actualizar nombre y edad
updated_hero = update_hero_patch(1, name="Spider-Man (Miles Morales)", age=17)
```

### Eliminar Héroe

```python
def delete_hero(hero_id: int) -> Dict[str, Any]:
    """Elimina un héroe"""
    url = f"{BASE_URL}/test/heroes/{hero_id}"
    response = requests.delete(url)
    response.raise_for_status()
    return response.json()

# Uso
result = delete_hero(1)
print(result['status']['message'])  # "Hero deleted"
```

### Clase Cliente Completa

```python
class HeroClient:
    """Cliente Python para la API de héroes"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def create(self, name: str, secret_name: str, age: int = None):
        """Crea un héroe"""
        url = f"{self.base_url}/test/heroes"
        data = {"name": name, "secret_name": secret_name}
        if age is not None:
            data["age"] = age
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result["data"]
    
    def list(self, filter=None, sort=None, page=1, size=10):
        """Lista héroes con filtros"""
        url = f"{self.base_url}/test/heroes"
        params = {"page": page, "size": size}
        if filter:
            params["filter"] = filter
        if sort:
            params["sort"] = sort
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        # Para respuestas paginadas, data contiene {"items": [...], "pagination": {...}}
        return result["data"]["items"], result["data"].get("pagination")
    
    def get(self, hero_id: int):
        """Obtiene un héroe por ID"""
        url = f"{self.base_url}/test/heroes/{hero_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()["data"]
    
    def update(self, hero_id: int, **updates):
        """Actualiza parcialmente un héroe"""
        url = f"{self.base_url}/test/heroes/{hero_id}"
        response = self.session.patch(url, json=updates)
        response.raise_for_status()
        result = response.json()
        return result["data"]
    
    def delete(self, hero_id: int):
        """Elimina un héroe"""
        url = f"{self.base_url}/test/heroes/{hero_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        result = response.json()
        return result

# Uso del cliente
client = HeroClient()

# Crear
hero = client.create("Iron Man", "Tony Stark", 45)
print(f"Creado: {hero['name']} (ID: {hero['id']})")

# Listar
heroes, pagination = client.list(filter="age:gt:18", sort="name:asc")
print(f"Encontrados {pagination['total']} héroes adultos")

# Obtener
hero = client.get(1)
print(f"Héroe: {hero['name']}")

# Actualizar
updated = client.update(1, age=46)
print(f"Edad actualizada: {updated['age']}")

# Eliminar
client.delete(1)
print("Héroe eliminado")
```

## Ejemplos con JavaScript (fetch)

### Crear un Héroe

```javascript
async function createHero(name, secretName, age = null) {
  const response = await fetch('http://localhost:8000/test/heroes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: name,
      secret_name: secretName,
      age: age,
    }),
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const result = await response.json();
  return result.data;
}

// Uso
const hero = await createHero('Spider-Man', 'Peter Parker', 25);
console.log(`Héroe creado con ID: ${hero.id}`);
// El objeto hero solo contiene 'data', no 'status'
```

### Listar Héroes con Filtros

```javascript
async function getHeroes({ filter, sort, page = 1, size = 10 } = {}) {
  const params = new URLSearchParams({
    page: page.toString(),
    size: size.toString(),
  });
  
  if (filter) params.append('filter', filter);
  if (sort) params.append('sort', sort);
  
  const response = await fetch(
    `http://localhost:8000/test/heroes?${params}`
  );
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const result = await response.json();
  return {
    data: result.data,
    pagination: result.pagination,
  };
}

// Ejemplos de uso
// Todos los héroes
const all = await getHeroes();

// Mayores de 18
const adults = await getHeroes({ filter: 'age:gt:18' });

// Con ordenamiento
const sorted = await getHeroes({ 
  filter: 'name:like:Spider',
  sort: 'age:desc',
  page: 1,
  size: 20
});

console.log(`Total: ${sorted.pagination.total}`);
// sorted.data contiene el array de items directamente
sorted.data.forEach(hero => {
  console.log(`${hero.name} - ${hero.age} años`);
});
```

### Clase Cliente Completa

```javascript
class HeroClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }
  
  async create(name, secretName, age = null) {
    const response = await fetch(`${this.baseUrl}/test/heroes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        secret_name: secretName,
        age,
      }),
    });
    
    const result = await response.json();
    if (!response.ok) throw new Error(result.status?.message || 'Error');
    return result.data;
  }
  
  async list({ filter, sort, page = 1, size = 10 } = {}) {
    const params = new URLSearchParams({ page, size });
    if (filter) params.append('filter', filter);
    if (sort) params.append('sort', sort);
    
    const response = await fetch(
      `${this.baseUrl}/test/heroes?${params}`
    );
    
    const result = await response.json();
    if (!response.ok) throw new Error(result.status?.message || 'Error');
    
    // Para respuestas paginadas, data contiene {"items": [...], "pagination": {...}}
    return {
      data: result.data.items,
      pagination: result.data.pagination,
    };
  }
  
  async get(heroId) {
    const response = await fetch(
      `${this.baseUrl}/test/heroes/${heroId}`
    );
    
    const result = await response.json();
    if (!response.ok) throw new Error(result.status?.message || 'Error');
    return result.data;
  }
  
  async update(heroId, updates) {
    const response = await fetch(
      `${this.baseUrl}/test/heroes/${heroId}`,
      {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      }
    );
    
    const result = await response.json();
    if (!response.ok) throw new Error(result.status?.message || 'Error');
    return result.data;
  }
  
  async delete(heroId) {
    const response = await fetch(
      `${this.baseUrl}/test/heroes/${heroId}`,
      { method: 'DELETE' }
    );
    
    const result = await response.json();
    if (!response.ok) throw new Error(result.status?.message || 'Error');
    return result;
  }
}

// Uso
const client = new HeroClient();

// Crear
const hero = await client.create('Iron Man', 'Tony Stark', 45);
console.log(`Creado: ${hero.name}`);

// Listar
const { data, pagination } = await client.list({
  filter: 'age:gt:18',
  sort: 'name:asc',
  page: 1,
  size: 10
});
console.log(`Total: ${pagination.total}`);

// Obtener
const ironMan = await client.get(hero.id);
console.log(ironMan);

// Actualizar
const updated = await client.update(hero.id, { age: 46 });
console.log(`Nueva edad: ${updated.age}`);

// Eliminar
await client.delete(hero.id);
```

## Casos de Uso Completos

### Caso 1: Sistema de Búsqueda de Héroes

```python
# Búsqueda avanzada de héroes
def search_heroes(
    name_contains: str = None,
    min_age: int = None,
    max_age: int = None,
    sort_by: str = "name",
    sort_direction: str = "asc"
) -> List[Dict]:
    """Búsqueda avanzada con múltiples criterios"""
    
    # Construir filtros
    filters = []
    if name_contains:
        filters.append(f"name:like:{name_contains}")
    if min_age:
        filters.append(f"age:ge:{min_age}")
    if max_age:
        filters.append(f"age:le:{max_age}")
    
    filter_str = ",".join(filters) if filters else None
    sort_str = f"{sort_by}:{sort_direction}"
    
    # Realizar búsqueda
    result = get_heroes(filter=filter_str, sort=sort_str, size=100)
    # Para respuestas paginadas, data contiene {"items": [...], "pagination": {...}}
    return result['data']['items']

# Uso
# Buscar héroes con "Spider" en el nombre, entre 18 y 30 años
young_spiders = search_heroes(
    name_contains="Spider",
    min_age=18,
    max_age=30,
    sort_by="age",
    sort_direction="asc"
)

for hero in young_spiders:
    print(f"{hero['name']} - {hero['age']} años")
```

### Caso 2: Importación Masiva de Héroes

```python
def bulk_create_heroes(heroes_data: List[Dict]) -> List[Dict]:
    """Crea múltiples héroes en batch"""
    created_heroes = []
    
    for hero_data in heroes_data:
        try:
            hero = create_hero(**hero_data)
            created_heroes.append(hero['data'])
            print(f"✓ Creado: {hero['data']['name']}")
        except Exception as e:
            print(f"✗ Error creando {hero_data['name']}: {e}")
    
    return created_heroes

# Uso
heroes_to_create = [
    {"name": "Spider-Man", "secret_name": "Peter Parker", "age": 25},
    {"name": "Iron Man", "secret_name": "Tony Stark", "age": 45},
    {"name": "Thor", "secret_name": "Thor Odinson", "age": 1500},
    {"name": "Hulk", "secret_name": "Bruce Banner", "age": 42},
]

created = bulk_create_heroes(heroes_to_create)
print(f"\nCreados {len(created)} de {len(heroes_to_create)} héroes")
```

### Caso 3: Generador de Reportes

```python
def generate_hero_report():
    """Genera reporte estadístico de héroes"""
    # Obtener todos los héroes
    all_heroes = get_heroes(size=1000)
    heroes = all_heroes['data']['items']
    total = all_heroes['data']['pagination']['total']
    
    # Calcular estadísticas
    ages = [h['age'] for h in heroes if h['age']]
    avg_age = sum(ages) / len(ages) if ages else 0
    
    # Agrupar por rango de edad
    young = len([h for h in heroes if h['age'] and h['age'] < 25])
    adult = len([h for h in heroes if h['age'] and 25 <= h['age'] < 60])
    senior = len([h for h in heroes if h['age'] and h['age'] >= 60])
    
    # Imprimir reporte
    print("=== REPORTE DE HÉROES ===")
    print(f"Total de héroes: {total}")
    print(f"Edad promedio: {avg_age:.1f} años")
    print(f"\nDistribución por edad:")
    print(f"  Jóvenes (< 25): {young}")
    print(f"  Adultos (25-59): {adult}")
    print(f"  Mayores (≥ 60): {senior}")
    
    # Top 5 más viejos
    oldest = get_heroes(sort="age:desc", size=5)
    print(f"\nTop 5 más viejos:")
    for i, hero in enumerate(oldest['data']['items'], 1):
        print(f"  {i}. {hero['name']} - {hero['age']} años")

# Uso
generate_hero_report()
```

## Consejos y Mejores Prácticas

### 1. Manejo de Errores

```python
def safe_api_call(func, *args, **kwargs):
    """Wrapper para manejar errores de API"""
    try:
        return func(*args, **kwargs)
    except requests.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        error_data = e.response.json()
        print(f"Message: {error_data.get('status', {}).get('message')}")
        if 'errors' in error_data:
            print(f"Errors: {error_data['errors']}")
        raise
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        raise

# Uso
hero = safe_api_call(get_hero, 1)
```

### 2. Paginación Automática

```python
def get_all_heroes(filter=None, sort=None, page_size=100):
    """Obtiene todos los héroes con paginación automática"""
    all_heroes = []
    page = 1
    
    while True:
        response = get_heroes(
            filter=filter,
            sort=sort,
            page=page,
            size=page_size
        )
        
        # Para respuestas paginadas, data contiene {"items": [...], "pagination": {...}}
        heroes = response['data']['items']
        all_heroes.extend(heroes)
        
        pagination = response['data']['pagination']
        if page >= pagination['pages']:
            break
        
        page += 1
    
    return all_heroes

# Uso
all_adult_heroes = get_all_heroes(filter="age:ge:18")
print(f"Total de héroes adultos: {len(all_adult_heroes)}")
```

### 3. Retry con Backoff

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, backoff_factor=2):
    """Decorator para reintentar con backoff exponencial"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    wait_time = backoff_factor ** retries
                    print(f"Error: {e}. Reintentando en {wait_time}s...")
                    time.sleep(wait_time)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def create_hero_with_retry(name, secret_name, age=None):
    return create_hero(name, secret_name, age)
```

## Conclusión

Estos ejemplos cubren los casos de uso más comunes. Para más información:

- Consulta la [Guía de Uso](usage-guide.md) para detalles de los endpoints
- Revisa la [Guía de Desarrollo](development-guide.md) para extender la API
- Explora la [Arquitectura](architecture.md) para entender el diseño
