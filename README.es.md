# Engineering Skills

[🇬🇧 English](README.md) · 🇪🇸 Español

Una colección de skills para agentes de IA, compatibles con [Claude Code](https://claude.com/claude-code), [OpenAI Codex](https://developers.openai.com/codex) y [GitHub Copilot](https://github.com/features/copilot), que puedes reutilizar en distintos proyectos. Las skills siguen el formato abierto [Agent Skills](https://agentskills.io/), así que la misma skill funciona en las tres herramientas. La mayoría de las skills no dependen de una tecnología ni de un lenguaje de programación concretos, así que sirven para frontend, backend, apps móviles y otros tipos de trabajo. Cuando una skill sí está pensada para un lenguaje o stack específico, su fila en la tabla de abajo lo indica.

Cada skill está disponible en dos idiomas:

- [`es/`](es/): español
- [`en/`](en/): inglés

Las dos versiones de una skill tienen el mismo nombre de carpeta y el mismo contenido.

- **Estado:** activo. Las skills nuevas se añaden de una en una.
- **Responsable:** Ricardo Mesa Gallego ([@rimega92](https://github.com/rimega92)).
- **Soporte:** para dudas, ideas o errores, abre un [issue](https://github.com/rimega92/Engineering-Skills/issues).

## Índice

- [Skills](#skills)
  - [readme-docs](#readme-docs)
  - [review-changes](#review-changes)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Instalación](#instalación)
- [Uso](#uso)
- [Cómo contribuir](#cómo-contribuir)
- [Más información](#más-información)
- [Licencia](#licencia)

## Skills

| Skill | Para qué sirve | Stack |
| ----- | -------------- | ----- |
| [`readme-docs`](#readme-docs) | Crear el README.md de un proyecto o actualizarlo después de cambios en el código | Agnóstica |
| [`review-changes`](#review-changes) | Revisar cambios de código antes de un commit o de un pull request, con un informe priorizado y recomendaciones | Agnóstica |

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

**Probada**

- Claude Code: probada en un proyecto de app de iOS (Xcode) y en un microservicio en Java, donde generó una documentación completa.
- OpenAI Codex y GitHub Copilot: todavía sin probar.

### review-changes

Revisa cambios de código antes de un commit o de un pull request para detectar los problemas que importan antes de que lleguen a producción: defectos funcionales, regresiones, riesgos de seguridad, problemas de integridad de datos, problemas de diseño y de estructura, y desviaciones de los estándares del proyecto. Busca hallazgos relevantes y con evidencia, no la lista más larga. Escribe un informe priorizado con una recomendación para cada hallazgo, puede aplicar las correcciones que apruebes y puede volver a revisar la rama para comprobarlas.

**Cuándo usarla**

- Antes de hacer commit, para revisar lo que todavía no has commiteado.
- Antes de abrir un pull request, para revisar la rama completa.
- Para revisar el pull request de otra persona.
- Después de corregir los hallazgos, para comprobar que quedaron corregidos y que no apareció nada nuevo.

**Cómo usarla**

- Pídelo: _"Revisa mis cambios"_, _"Revisa esta rama antes del PR"_, _"Revisa el PR 42"_.
- Para acotar el alcance: _"Revisa solo lo que no he commiteado"_, _"Revisa el último commit"_.
- Para forzar un modo: _"Haz una revisión rápida"_, _"Haz una revisión profunda"_.
- Después del informe: _"Corrige F1 y F3"_, _"Aplica las correcciones P0 y P1"_.
- Para comprobar las correcciones: _"Revisa otra vez"_.

**Cómo funciona**

- Por defecto revisa todo lo que entraría en el pull request: los commits de la rama desde que salió de su rama base, más los cambios sin commit. Para los pull requests usa `gh` o `glab` si están instalados; si no, trae la rama con `git`.
- Primero descubre los estándares del proyecto (`README`, `AGENTS.md`, `CLAUDE.md`, scaffold, reglas de arquitectura, linters, contratos), para juzgar el cambio con ellos y no con convenciones externas. Aplica SOLID, DDD y patrones solo donde aportan valor.
- El tamaño y el riesgo del cambio deciden cuánto hace, así que una corrección pequeña antes de un commit sigue siendo rápida:
  - **Rápida** (cambio pequeño, sin áreas sensibles): checklist básica, comprobaciones rápidas (lint, formato, tipos) e informe corto.
  - **Estándar** (cambio más grande, o uno que toca un área sensible como autenticación, datos, contratos públicos o configuración): añade los apartados de la checklist de las áreas que toca el cambio y las pruebas relacionadas.
  - **Profunda** (sistemas críticos, datos sensibles, operaciones financieras, seguridad): todo lo anterior más el análisis de amenazas y de fallos, la suite completa de pruebas y la compilación.
- La checklist tiene 12 áreas, desde el diseño y la arquitectura hasta el despliegue y el alcance del cambio. Solo lee los apartados de las áreas que toca el cambio.
- Ejecuta las validaciones del propio proyecto, sin nada que modifique archivos, instale dependencias o toque datos, y pregunta antes si son lentas o necesitan servicios externos. El informe dice qué se ejecutó, qué falló y qué no se pudo ejecutar.
- Comprueba cada hallazgo con siete preguntas antes de reportarlo, para evitar falsos positivos. Cada uno tiene una prioridad (🔴 P0, 🟠 P1, 🟡 P2, 🔵 P3 o 💡 Info, o la escala propia del proyecto), un tipo (defecto confirmado o riesgo potencial), un origen (introducido o preexistente), y las condiciones, el impacto, la evidencia y la recomendación. Los hallazgos P3 e Info ocupan una sola línea. La revisión recibe un veredicto: ✅ Listo, ⚠️ Listo con cambios o ❌ Necesita trabajo. Nunca afirma que el código está libre de errores.
- Guarda el informe en `.reviews/<rama>/review-<n>.md` en la carpeta del componente al que pertenecen los cambios (en un monorepo, la raíz del microservicio, la app o el paquete que modifican, o la raíz del repositorio si tocan varios), un archivo por ronda (`review-1.md`, `review-2.md`, ...). La cabecera registra la fecha, la rama, la base y el commit revisado. Deja los informes fuera de los commits y de los push: la primera vez añade `.reviews/` a un `.gitignore` y te recuerda que hagas commit de ese cambio.
- Nunca cambia el código durante la revisión. Al final ofrece aplicar las correcciones y aplica solo las que apruebes, sin hacer commit.
- Una nueva ronda lee el informe de la ronda anterior, marca cada hallazgo anterior como corregido, corregido en parte, abierto o que ya no aplica, y revisa las correcciones y los cambios nuevos. Reutiliza los estándares que encontró la ronda anterior en lugar de buscarlos otra vez.

**Archivos**

- `SKILL.md`: el flujo de trabajo: alcance, contexto, modo de revisión, revisión, validaciones, verificación, informe, correcciones y nueva ronda.
- `references/checklist.md`: la escala de prioridad, los veredictos, los niveles de profundidad que usa cada modo y qué buscar en cada una de las 12 áreas.
- `references/report-template.md`: la estructura del informe, su tamaño en cada modo, y los formatos completo y compacto de los hallazgos.

**Requisitos y limitaciones**

- El proyecto debe usar `git`.
- Revisar un pull request por número funciona mejor con `gh` (GitHub) o `glab` (GitLab) instalado y con la sesión iniciada.
- Solo puede ejecutar las validaciones que el proyecto ya define y que el entorno permite. Lo que no pudo ejecutar aparece en el informe como no verificado.

**Probada**

- Claude Code: probada en un proyecto de app de iOS (Xcode, unas 11.000 líneas de Swift), revisando el proyecto completo en modo Profunda. Ejecutó las pruebas y la compilación de Release, aplicó las reglas propias del proyecto y reportó hallazgos relevantes con evidencia, sin ruido. También probada en un microservicio en Java, con los mismos resultados.
- OpenAI Codex y GitHub Copilot: todavía sin probar.

## Estructura del repositorio

Una skill es Markdown sin más: un archivo `SKILL.md` con frontmatter YAML (`name` y `description`), según el formato [Agent Skills](https://agentskills.io/), más archivos de apoyo opcionales. No hay código que compilar, dependencias que instalar, ni configuración o variables de entorno.

```text
Engineering-Skills/
├── en/                    # Versiones en inglés de las skills
│   └── <nombre-skill>/
│       ├── SKILL.md       # Instrucciones que sigue el agente, con frontmatter
│       └── references/    # Archivos de apoyo que la skill lee cuando los necesita
├── es/                    # Versiones en español, mismas carpetas que en/
├── AGENTS.md              # Convenciones del repositorio para agentes de IA
├── CLAUDE.md              # Importa AGENTS.md para Claude Code
├── LICENSE
├── README.md              # README en inglés
└── README.es.md           # Este archivo
```

No hay pruebas automáticas. Cada skill se prueba a mano en las herramientas (consulta la lista **Probada** en la sección de cada skill).

## Instalación

Una skill es una carpeta que contiene un archivo `SKILL.md`. Para instalar una, copia su carpeta, en el idioma que prefieras, a la carpeta de skills de tu herramienta:

| Herramienta | Un solo proyecto | Todos tus proyectos (personal) |
| ----------- | ---------------- | ------------------------------ |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

Necesitas `git` y al menos una de las herramientas de la tabla.

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

## Más información

- [Agent Skills](https://agentskills.io/): el formato abierto que siguen estas skills.
- [`AGENTS.md`](AGENTS.md): las convenciones del repositorio para skills, idiomas y README.

## Licencia

Publicado bajo la [licencia MIT](LICENSE). Puedes usar, copiar, modificar y compartir las skills, también en proyectos comerciales, siempre que mantengas el aviso de copyright.

<!-- readme-docs:sync commit=22b20d0 date=2026-10-29 -->
