# Rimega Skills

[🇬🇧 English](README.md) · 🇪🇸 Español

Una colección de skills para [Claude Code](https://claude.com/claude-code) que puedes reutilizar en distintos proyectos. La mayoría de las skills no dependen de una tecnología ni de un lenguaje de programación concretos, así que sirven para frontend, backend, apps móviles y otros tipos de trabajo. Cuando una skill sí está pensada para un lenguaje o stack específico, su fila en la tabla de abajo lo indica.

Cada skill está disponible en dos idiomas:

- [`es/`](es/): español
- [`en/`](en/): inglés

Las dos versiones de una skill tienen el mismo nombre de carpeta y el mismo contenido.

## Skills

| Skill | Para qué sirve | Stack |
|-------|----------------|-------|
| _Todavía no hay skills_ | | |

## Instalación

Una skill es una carpeta que contiene un archivo `SKILL.md`. Para instalar una, copia su carpeta, en el idioma que prefieras, a una de estas ubicaciones:

- **Todos tus proyectos (personal):** `~/.claude/skills/`
- **Un solo proyecto:** `.claude/skills/` dentro de ese proyecto

```bash
git clone https://github.com/<usuario>/Rimega-Skills.git

# Instalación personal (versión en español)
cp -r Rimega-Skills/es/<nombre-skill> ~/.claude/skills/

# Instalación en un solo proyecto (versión en inglés)
cp -r Rimega-Skills/en/<nombre-skill> /ruta/al/proyecto/.claude/skills/
```

Instala solo una versión de idioma de cada skill. Las dos versiones comparten el mismo `name`, así que instalar ambas provoca un conflicto.

## Uso

Claude Code activa una skill por su cuenta cuando tu petición coincide con la `description` de la skill. También puedes invocarla directamente escribiendo `/<nombre-skill>`.
