# Engineering Skills

[🇬🇧 English](README.md) · 🇪🇸 Español

Una colección de skills para agentes de IA, compatibles con [Claude Code](https://claude.com/claude-code), [OpenAI Codex](https://developers.openai.com/codex) y [GitHub Copilot](https://github.com/features/copilot), que puedes reutilizar en distintos proyectos. Las skills siguen el formato abierto [Agent Skills](https://agentskills.io/), así que la misma skill funciona en las tres herramientas. La mayoría de las skills no dependen de una tecnología ni de un lenguaje de programación concretos, así que sirven para frontend, backend, apps móviles y otros tipos de trabajo. Cuando una skill sí está pensada para un lenguaje o stack específico, su fila en la tabla de abajo lo indica.

Cada skill está disponible en dos idiomas:

- [`es/`](es/): español
- [`en/`](en/): inglés

Las dos versiones de una skill tienen el mismo nombre de carpeta y el mismo contenido.

## Índice

- [Skills](#skills)
  - [readme-docs](#readme-docs)
- [Instalación](#instalación)
- [Uso](#uso)
- [Cómo contribuir](#cómo-contribuir)

## Skills

| Skill | Para qué sirve | Stack |
|-------|----------------|-------|
| [`readme-docs`](#readme-docs) | Crear el README.md de un proyecto o actualizarlo después de cambios en el código | Agnóstica |

### readme-docs

Crea y mantiene el `README.md` de un proyecto siguiendo un estándar de documentación. Cada apartado del estándar está clasificado como obligatorio (`[M]`), condicional (`[C]`, obligatorio cuando aplica al proyecto) u opcional (`[O]`). El estándar cubre identificación, inicio rápido, funcionalidades, arquitectura, APIs e integraciones, calidad, operación y versionado.

**Cuándo usarla**
- Para documentar un proyecto que no tiene README o que tiene uno mínimo.
- Para actualizar el README después de cambiar el código: nuevas dependencias, endpoints, variables de entorno, servicios, etc.

**Cómo usarla**
- Pídelo: _"Documenta este proyecto"_, _"Actualiza el README con los últimos cambios"_.
- Elige el modo sola: el modo crear si no hay un README con contenido real, y el modo actualizar si lo hay. Para forzar un modo, dilo: _"Crea el README desde cero"_, _"Actualiza el README"_.

**Cómo funciona**
- Deduce todo lo que puede del proyecto (manifiestos, scripts, configuración, Docker, CI, pruebas, código). Para los datos que solo conoce el equipo, como el estado, los responsables o el porqué de las decisiones, te hace todas las preguntas en un solo mensaje. Lo que dejes sin responder queda como un marcador visible de `Pendiente`.
- En el modo actualizar lee una marca de sincronización al final del README, `<!-- readme-docs:sync commit=... date=... -->`, revisa los cambios desde ese commit y edita solo los apartados afectados. Conserva el texto escrito por personas y pregunta antes de eliminar un apartado completo.
- Mueve el contenido extenso (referencia completa de la API, modelo de datos, etc.) a archivos dentro de `docs/` con nombres estándar (`architecture.md`, `api.md`, `data-model.md`, ...) y los enlaza desde el README. El modo actualizar también mantiene al día esos archivos. Los archivos de `docs/` escritos por personas se enlazan, pero nunca se modifican.
- Nunca copia secretos y comprueba que los comandos y rutas que documenta existen de verdad.
- Escribe README fáciles de leer. Los apartados para cualquier lector usan lenguaje sencillo, y los que lo necesitan (arquitectura, APIs, operación) usan lenguaje técnico. El Markdown sigue markdownlint y GitHub Flavored Markdown. Los diagramas Mermaid son pequeños y usan una paleta de colores que se lee bien en modo claro y oscuro, con leyenda.
- Mantiene el idioma del README existente. Un README nuevo se escribe en el idioma en el que le hablas.

**Archivos**
- `SKILL.md`: el flujo de trabajo de los dos modos.
- `references/standard.md`: el estándar de documentación, con la clasificación de cada apartado.
- `references/evidence-map.md`: qué archivos de un proyecto activan o afectan cada apartado.
- `references/style.md`: guía de estilo para la redacción, el Markdown y los diagramas Mermaid, con la paleta de colores.

## Instalación

Una skill es una carpeta que contiene un archivo `SKILL.md`. Para instalar una, copia su carpeta, en el idioma que prefieras, a la carpeta de skills de tu herramienta:

| Herramienta | Un solo proyecto | Todos tus proyectos (personal) |
|-------------|------------------|--------------------------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

Primero, clona el repositorio:

```bash
git clone https://github.com/rimega92/Engineering-Skills.git
```

Después, copia la skill para tu herramienta.

### Instalar en Claude Code

```bash
# Instalación personal
cp -r Engineering-Skills/es/<nombre-skill> ~/.claude/skills/

# Instalación en un solo proyecto
cp -r Engineering-Skills/es/<nombre-skill> /ruta/al/proyecto/.claude/skills/
```

### Instalar en OpenAI Codex

```bash
# Instalación personal
cp -r Engineering-Skills/es/<nombre-skill> ~/.codex/skills/

# Instalación en un solo proyecto
cp -r Engineering-Skills/es/<nombre-skill> /ruta/al/proyecto/.agents/skills/
```

### Instalar en GitHub Copilot

```bash
# Instalación personal
cp -r Engineering-Skills/es/<nombre-skill> ~/.copilot/skills/

# Instalación en un solo proyecto
cp -r Engineering-Skills/es/<nombre-skill> /ruta/al/proyecto/.github/skills/
```

Si la carpeta de destino todavía no existe, créala antes con `mkdir -p`. Para la versión en inglés, cambia `es/` por `en/`.

Instala solo una versión de idioma de cada skill. Las dos versiones comparten el mismo `name`, así que instalar ambas provoca un conflicto.

## Uso

Hay dos formas de usar una skill:

- **Automática:** el agente activa la skill por su cuenta cuando tu petición coincide con su `description`. En la mayoría de los casos basta con pedir lo que necesitas.
- **Explícita:** nombras la skill con la sintaxis de tu herramienta. Sirve cuando el agente no la elige solo o cuando quieres asegurarte de que la use.

Los ejemplos usan la skill `readme-docs`.

### Usar en Claude Code

```text
# Automática
Actualiza el README con los últimos cambios

# Explícita
/readme-docs
/readme-docs actualiza el README con los últimos cambios
```

### Usar en OpenAI Codex

```text
# Automática
Actualiza el README con los últimos cambios

# Explícita
$readme-docs actualiza el README con los últimos cambios
```

En Codex CLI y en la extensión del IDE también puedes ejecutar `/skills` para elegir una skill de una lista.

### Usar en GitHub Copilot

```text
# Automática
Actualiza el README con los últimos cambios

# Explícita
/readme-docs actualiza el README con los últimos cambios
Usa la skill /readme-docs para actualizar el README con los últimos cambios
```

En VS Code, escribe `/` en el chat para ver las skills disponibles. En Copilot CLI, incluye `/<nombre-skill>` dentro de tu petición, como en el segundo ejemplo.

## Cómo contribuir

Las contribuciones son bienvenidas: correcciones, mejoras de skills existentes y skills nuevas.

### Antes de empezar

- **Skill nueva:** abre primero un [issue](https://github.com/rimega92/Engineering-Skills/issues) explicando para qué sirve, para acordarla antes de que le dediques trabajo.
- **Corrección o mejora:** puedes abrir el pull request directamente. Si el cambio es grande, conviene abrir antes un issue.

### Flujo de trabajo

1. Haz un fork del repositorio en GitHub (no tienes permiso de escritura en el original, así que tus cambios van a tu copia).
2. Clona tu fork y añade el repositorio original como `upstream`:

   ```bash
   git clone https://github.com/<tu-usuario>/Engineering-Skills.git
   cd Engineering-Skills
   git remote add upstream https://github.com/rimega92/Engineering-Skills.git
   ```

3. Crea una rama a partir de `main` actualizada. Usa un nombre corto con un prefijo que indique el tipo de cambio: `feat/` (skill o funcionalidad nueva), `fix/` (corrección) o `docs/` (solo documentación).

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feat/<nombre-skill>
   ```

4. Haz tus cambios siguiendo las [reglas](#reglas) de abajo.
5. Haz commits con mensajes claros: en inglés, en imperativo y con una primera línea corta (por ejemplo, `Add commit-message skill` o `Fix typo in readme-docs`). Mejor commits pequeños que hagan una sola cosa cada uno.

   ```bash
   git add .
   git commit -m "Add <nombre-skill> skill"
   ```

6. Sube la rama a tu fork:

   ```bash
   git push -u origin feat/<nombre-skill>
   ```

7. Abre un pull request en GitHub contra `main` de este repositorio. En la descripción, explica qué cambia y por qué, y enlaza el issue si lo hay.
8. Atiende los comentarios de la revisión subiendo nuevos commits a la misma rama; el pull request se actualiza solo.

### Reglas

- **Los dos idiomas:** cada skill existe en `es/` y en `en/` con el mismo nombre de carpeta, en inglés y en kebab-case. Cualquier cambio en una versión se aplica también a la otra en el mismo pull request. Traduce el texto, pero deja idénticos el código, los comandos y los nombres de archivo.
- **Frontmatter:** cada `SKILL.md` empieza con `name` (idéntico al nombre de la carpeta, con minúsculas, números y guiones, de 64 caracteres como máximo) y `description` (de 1024 caracteres como máximo, en el idioma de esa carpeta, diciendo qué hace la skill y cuándo usarla).
- **Neutral respecto a la herramienta:** escribe para "el agente". No menciones una herramienta concreta ni dependas de su sintaxis o de sus campos de frontmatter, para que la skill funcione igual en Claude Code, Codex y Copilot.
- **README:** si añades, cambias o eliminas una skill, actualiza `README.md` y `README.es.md`: el índice, la tabla de skills y la sección propia de la skill.
- **Pruébala:** antes de abrir el pull request, instala la skill en al menos una herramienta y comprueba que se activa y hace lo que dice.

[`AGENTS.md`](AGENTS.md) recoge todas las convenciones. Si trabajas con un agente de IA, las lee por su cuenta.
