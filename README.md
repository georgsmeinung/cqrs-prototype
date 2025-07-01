# 🧠 `cqrs-prototype`: CQRS Event-Driven Prototype with RabbitMQ

Este repositorio contiene un prototipo de arquitectura **CQRS (Command Query Responsibility Segregation)** orientada a eventos, usando **RabbitMQ** como broker y una separación clara entre el stack de comandos y el stack de consultas.

---

## 📐 Arquitectura General

```
                 [ Frontend / API Gateway ]
                           |
        ┌──────────────────┴──────────────────┐
        |                                     |
 [ Command Stack ]                    [ Query Stack ]
        |                                     |
  POST /users                           GET /users/:email
        |                                     |
  +-------------+                     +------------------+
  | Command API | ──► RabbitMQ ◄───── | Event Consumer   |
  +-------------+        ▲           +------------------+
                         |                    │
                  [ domain_events ]          ▼
                                       MongoDB Projection
```

---

## 🟦 Stack de Comando

### Componentes
- `FastAPI`: API REST para recibir comandos (POST /users)
- `pika`: Cliente RabbitMQ en Python
- `RabbitMQ`: Broker para publicar eventos de dominio

### Flujo
1. Cliente envía un `POST /users`.
2. El comando se convierte en un evento `user.created`.
3. El evento se publica en RabbitMQ (`domain_events` exchange).

---

## 🟩 Stack de Consulta

### Componentes
- `RabbitMQ consumer`: Escucha eventos `user.created`.
- `MongoDB`: Almacena las proyecciones (read models).
- `FastAPI`: API de lectura (GET /users/:email)

### Flujo
1. El consumidor escucha eventos de RabbitMQ.
2. Al recibir `user.created`, guarda la proyección en MongoDB.
3. La API de lectura expone esos datos optimizados para consulta.

---

## 🚀 Cómo ejecutar el prototipo

### 1. Clonar el repo

```bash
git clone https://github.com/tuusuario/cqrs-rabbitmq-prototype.git
cd cqrs-rabbitmq-prototype
```

### 2. Levantar el entorno

```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

Esto levantará:
- API de comandos en `localhost:8000`
- API de lectura en `localhost:9000`
- RabbitMQ Management UI en `localhost:15672` (user: `guest`, pass: `guest`)
- MongoDB en `localhost:27017`

### 3. Probar el flujo

**Crear un usuario (Command Stack):**
```bash
curl -X POST http://localhost:8000/users   -H "Content-Type: application/json"   -d '{"name": "Ada Lovelace", "email": "ada@computing.org"}'
```

**Consultar el usuario (Query Stack):**
```bash
curl http://localhost:9000/users/ada@computing.org
```

---

## 📦 Tecnologías usadas

- 🐍 Python 3.11
- ⚡ FastAPI
- 🐰 RabbitMQ 3.x
- 🧩 MongoDB
- 🐳 Docker + Compose

---

## 📌 Próximos pasos

- Agregar eventos `user.updated` y `user.deleted`.
- Aplicar Event Sourcing en el stack de comandos.
- Autoescalado con HPA o KEDA para el stack de consulta.
- Tests y monitoreo con Prometheus + Grafana.

---

## 🛡 Licencia

MIT License
