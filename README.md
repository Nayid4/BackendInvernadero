# BackendInvernadero

API backend para un sistema de monitoreo y control inteligente para invernaderos. Permite la gestión integral de usuarios (con roles y autenticación JWT), manejo de plantas, sensores, lógica de negocio basada en arquitectura limpia y soporte para refresh token.

Repositorio oficial:
[https://github.com/Nayid4/BackendInvernadero.git](https://github.com/Nayid4/BackendInvernadero.git)

***

## Estructura del Proyecto

```
BackendInvernadero/
│
├── app/
│   └── controllers/                # Rutas y presentación Flask
│
├── application/
│   └── usuarios/                   # Casos de uso (CRUD, login, refresh)
│   └── plantas/                    # Casos de uso (CRUD plantas)
│
├── domain/                         # Entidades principales (Usuario, Planta)
│
├── infrastructure/
│   ├── firebase/                   # Inicialización global de Firebase
│   └── repositories/               # Repositorios: UsuarioRepository, PlantaRepository, etc.
│
├── tests/                          # Pruebas unitarias
├── requirements.txt                # Dependencias Python
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .env.example
└── run.py                          # Entrypoint principal Flask
```


***

## Arquitectura y Patrones de Diseño

- **Arquitectura Limpia:** Separación en capas Presentation, Application, Domain, Infrastructure.
- **CQRS:** Commands y Queries para cada feature encapsulados por carpeta.
- **Mediator Pattern:** Desacoplamiento de lógica usando handlers específicos (librería mediatr).
- **Repository Pattern:** Acceso desacoplado a Firestore por clase y entidad.
- **SOLID:** Principios de diseño asegurados en cada módulo.
- **ProblemDetails:** Error handler global, devolviendo respuestas estándar RFC-7807.
- **JWT \& Refresh Token:** Sesión y autorización segura (access y refresh token).
- **Variables de entorno:** Secrets fuera de código, integración con dotenv.
- **Escalabilidad:** Fácil agregar nuevas entidades/repositorios.

***

## Funcionalidades Principales

### Gestión de Usuarios

- Registro de usuario con validación, hash de contraseña y asignación de rol.
- Login seguro con JWT.
- Endpoint `/me`: dados un token JWT, retorna toda la información del usuario (id, nombre, apellido, correo, teléfono, rol).
- Actualización y eliminación de usuarios vía ID.
- Consulta de usuario por correo y por ID.
- Listado de todos los usuarios.


### Seguridad, Login y Tokens

- Todos los endpoints protegidos salvo registro y login.
- Autenticación JWT (`Bearer token`), usando el ID de usuario como identidad.
- Soporte para **refresh token** (endpoint `/refresh`): permite obtener un nuevo access token sin volver a iniciar sesión.


### Gestión de Plantas

- CRUD completo: crear, consultar, actualizar, eliminar y listar plantas.
- Cada planta almacena: id, nombre, especie, fecha de siembra, ubicación y referencia de usuario.


### Estandarización de Errores

- Respuestas de error uniformes con ProblemDetails (`type`, `title`, `status`, `detail`).

***

## Clonar y Configurar el Entorno

```bash
git clone https://github.com/Nayid4/BackendInvernadero.git
cd BackendInvernadero
```


### 1. Entorno virtual

```bash
python -m venv venv
source venv/bin/activate        # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```


### 2. Variables de entorno

Copia `.env.example` a `.env` y agrega:

```
JWT_SECRET_KEY=clave-super-secreta
FIREBASE_CREDENTIALS=/ruta/al/firebase-key.json
```


***

## Ejecución en Local

```bash
python run.py
```

Accede a la API en `http://localhost:5000`.

***

## Ejecución con Docker

```bash
docker-compose build
docker-compose up
```

El backend queda disponible en `http://localhost:5000`.

***

## Pruebas unitarias

```bash
pytest tests/
```


***

## Endpoints principales

| Endpoints | Descripción |
| :-- | :-- |
| POST   `/api/users/` | Registro usuario |
| POST   `/api/users/login` | Login, retorna access y refresh token |
| POST   `/api/users/refresh` | Renueva access token usando refresh token |
| GET    `/api/users/me` | Información del usuario autenticado |
| GET    `/api/users/<id>` | Consulta usuario por id |
| GET    `/api/users/by-email/<correo>` | Consulta usuario por correo |
| PUT    `/api/users/<id>` | Actualiza usuario por id |
| DELETE `/api/users/<id>` | Elimina usuario por id |
| GET    `/api/users/` | Lista todos los usuarios |
| CRUD   `/api/plantas/` | Gestiona plantas: crear, listar, detalles, editar, eliminar |


***

## Colaboración

- Usa ramas y pull requests.
- Añade pruebas y documentación.
- Mantén el formato de ProblemDetails en errores.

***

**Proyecto académico y de referencia para arquitectura Python/Flask profesional con integración de IoT y servicios cloud (Firebase).**