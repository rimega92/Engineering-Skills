# Rimega Skills

[🇬🇧 English](README.md) · 🇪🇸 Español

Una colección de skills para [Claude Code](https://claude.com/claude-code) que puedes reutilizar en distintos proyectos. La mayoría de las skills no dependen de una tecnología ni de un lenguaje de programación concretos, así que sirven para frontend, backend, apps móviles y otros tipos de trabajo. Cuando una skill sí está pensada para un lenguaje o stack específico, su fila en la tabla de abajo lo indica.

Cada skill está disponible en dos idiomas:

- [`es/`](es/): español
- [`en/`](en/): inglés

Las dos versiones de una skill tienen el mismo nombre de carpeta y el mismo contenido.

## Índice

- [Skills](#skills)
  - [readme-docs](#readme-docs)
- [Instalación](#instalación)
- [Uso](#uso)

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
- `/readme-docs`: elige el modo sola. Usa el modo crear si no hay un README con contenido real, y el modo actualizar si lo hay.
- `/readme-docs crear` o `/readme-docs actualizar`: fuerza un modo.
- O simplemente pídelo: _"Documenta este proyecto"_, _"Actualiza el README con los últimos cambios"_.

**Cómo funciona**
- Deduce todo lo que puede del proyecto (manifiestos, scripts, configuración, Docker, CI, pruebas, código). Para los datos que solo conoce el equipo, como el estado, los responsables o el porqué de las decisiones, te hace todas las preguntas en un solo mensaje. Lo que dejes sin responder queda como un marcador visible de `Pendiente`.
- En el modo actualizar lee una marca de sincronización al final del README, `<!-- readme-docs:sync commit=... date=... -->`, revisa los cambios desde ese commit y edita solo los apartados afectados. Conserva el texto escrito por personas y pregunta antes de eliminar un apartado completo.
- Mueve el contenido extenso (referencia completa de la API, modelo de datos, etc.) a `docs/` y lo enlaza desde el README.
- Nunca copia secretos y comprueba que los comandos y rutas que documenta existen de verdad.
- Escribe README fáciles de leer. Los apartados para cualquier lector usan lenguaje sencillo, y los que lo necesitan (arquitectura, APIs, operación) usan lenguaje técnico. El Markdown sigue markdownlint y GitHub Flavored Markdown. Los diagramas Mermaid son pequeños y usan una paleta de colores que se lee bien en modo claro y oscuro, con leyenda.
- Mantiene el idioma del README existente. Un README nuevo se escribe en el idioma en el que le hablas.

**Archivos**
- `SKILL.md`: el flujo de trabajo de los dos modos.
- `references/standard.md`: el estándar de documentación, con la clasificación de cada apartado.
- `references/evidence-map.md`: qué archivos de un proyecto activan o afectan cada apartado.
- `references/style.md`: guía de estilo para la redacción, el Markdown y los diagramas Mermaid, con la paleta de colores.

## Instalación

Una skill es una carpeta que contiene un archivo `SKILL.md`. Para instalar una, copia su carpeta, en el idioma que prefieras, a una de estas ubicaciones:

- **Todos tus proyectos (personal):** `~/.claude/skills/`
- **Un solo proyecto:** `.claude/skills/` dentro de ese proyecto

```bash
git clone https://github.com/rimega92/Rimega-Skills.git

# Instalación personal (versión en español)
cp -r Rimega-Skills/es/<nombre-skill> ~/.claude/skills/

# Instalación en un solo proyecto (versión en inglés)
cp -r Rimega-Skills/en/<nombre-skill> /ruta/al/proyecto/.claude/skills/
```

Instala solo una versión de idioma de cada skill. Las dos versiones comparten el mismo `name`, así que instalar ambas provoca un conflicto.

## Uso

Claude Code activa una skill por su cuenta cuando tu petición coincide con la `description` de la skill. También puedes invocarla directamente escribiendo `/<nombre-skill>`.
