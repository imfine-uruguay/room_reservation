# My Python Project (`roombooking_agent`)

This project uses **[uv](https://github.com/astral-sh/uv)** as a package and virtual environment manager. `uv` is an extremely fast Python project manager written in Rust, designed to replace tools like `pip`, `pip-tools`, `poetry`, `pipenv`, and `virtualenv`.

---

## Why `uv`? Key Advantages

- **Extremely fast performance:** 10x to 100x faster than `pip` or `poetry`.
- **Integrated management:** Handles Python versions, virtual environments, and dependencies from `pyproject.toml`.
- **Deterministic locking (`uv.lock`):** Generates fast and universal lock files to ensure exact reproducibility.
- **Space efficiency:** Uses a global deduplicated cache to avoid duplicating packages on disk.

---

## Project Initialization

### 1. Install `uv`

If you don't have it installed yet:

```bash
# macOS/Linux:
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (PowerShell):
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

## 2. Initialize the project

```bash
#Wherever operating system you are on, run the following command to initialize the project
uv sync

## To set up the project, a .env file must be created:

```python
# ── LLM ──
LLM_MODEL_IN_GROP=llama-3.3-70b-versatile
LLM_MODEL_URL=https://api.groq.com/openai/v1
LLM_MODEL_TEMPERATURE=0.0
LLM_MODEL_PROVIDER=GROQ
LLM_MODEL_API_KEY=your_api_key_here

DB_ENGINE=sqlite
SQLITE_DB_PATH=utils/database/call_agent_ai_sqlite.db

BACKEND_CORS_ORIGINS="*"

PROJECT_NAME=Call_Agent_AI
API_STR=/api

ROOT_PATH=/call_agent_ai

SSL_ENABLED=false


PYTHONPATH=.


APP_NAME=call_agent_ai
APP_ENV=production
LOG_ENABLED=true
LOG_STDOUT=false
LOG_DIR=./logs
LOG_PRIMARY_DIR=/var/log/call_agent_ai

# Demo: Cubo Itaú — Meeting Room Assistant

Ejemplo de interacción con el asistente conversacional para reserva de salas de reuniones.

**Usuario:** User One
**Contraseña:** `User1Pass!`

---

```
=== Cubo Itau meeting room assistant ===
Username: User One
Password: User1Pass!
You're connected. Type 'exit' to quit.
```

**You:** Quien eres?

**Assistant:** Soy tu asistente de reservas para las salas de reuniones Cubo Itaú. Puedo ayudarte a crear, consultar y cancelar tus reservas. ¿En qué puedo asistirte hoy?

---

**You:** quiero que me agendes una reunion

**Assistant:** ¡Claro! Para reservar la sala, necesito algunos detalles:

1. **Sala** (A, B, C, D o E)
2. **Fecha** (formato YYYY-MM-DD)
3. **Hora de inicio** (formato HH:MM, 24 h)
4. **Hora de fin** (formato HH:MM, 24 h)
5. **Título de la reunión**
6. **Número de asistentes**

Con esa información podré confirmar la disponibilidad y crear la reserva. ¡Quedo atento!

---

**You:** A, 2026-09-03, 12H, 15H, Mostrar el MAS Sistema de gestion multiagentes, 30 personas

**Assistant:** Perfecto. Para confirmar:

- **Sala:** A
- **Fecha:** 2026-09-03
- **Hora de inicio:** 12:00
- **Hora de fin:** 15:00
- **Título:** "Mostrar el MAS Sistema de gestión multiagentes"
- **Asistentes:** 30

¿Todo correcto? Si lo es, procederé a crear la reserva.

---

**You:** Si

**Assistant:** Lo siento, pero la sala A solo admite 4 personas y tu reunión requiere 30 asistentes.

Podrías:
- Elegir otra sala con mayor capacidad (por ejemplo, B, C, D o E).
- Reducir el número de asistentes (si es posible).

¿Te gustaría intentar con otra sala o ajustar el número de participantes?

---

**You:** la E

**Assistant:** ¡Entendido! Confirmemos los detalles:

- **Sala:** E
- **Fecha:** 2026-09-03
- **Hora de inicio:** 12:00
- **Hora de fin:** 15:00
- **Título:** "Mostrar el MAS Sistema de gestión multiagentes"
- **Asistentes:** 30

¿Todo correcto? Si lo es, crearé la reserva.

---

**You:** Si

**Assistant:** Lo siento, pero la sala E solo admite 12 personas y tu reunión requiere 30 asistentes.

Para continuar, puedes:
1. **Elegir otra sala** con mayor capacidad (por ejemplo, B, C o D).
2. **Reducir el número de asistentes** a 12 o menos.

¿Con cuál opción te gustaría proceder?

---

**You:** Ok 12 personas

**Assistant:** ¡Perfecto! Confirmemos los datos finales:

- **Sala:** E
- **Fecha:** 2026-09-03
- **Hora de inicio:** 12:00
- **Hora de fin:** 15:00
- **Título:** "Mostrar el MAS Sistema de gestión multiagentes"
- **Asistentes:** 12

¿Todo correcto? Si lo es, crearé la reserva.

---

**You:** Si

**Assistant:** ¡Reserva confirmada!

📅 **Fecha:** 2026-09-03
🕒 **Hora:** 12:00 – 15:00
🏢 **Sala:** E
👥 **Asistentes:** 12
📝 **Título:** Mostrar el MAS Sistema de gestión multiagentes

Tu reserva tiene el ID **1**. Si necesitas hacer algún cambio o cancelar, avísame. ¡Que tengas una excelente reunión!