# Plantilla del informe

Estructura del informe que se guarda en `.reviews/<rama>/review-<n>.md`. Escríbelo en el idioma del usuario. Omite los apartados sin contenido, salvo la cabecera, el resumen y los hallazgos.

## Reglas

- Cada hallazgo tiene un ID (`F1`, `F2`, ...), una ubicación como `ruta:línea` (o `ruta:inicio-fin`), el problema, por qué importa y una propuesta de solución.
- Ordena los hallazgos por severidad y, dentro de la misma severidad, por archivo.
- Muestra el código actual y el propuesto solo cuando aclare la solución. Mantén los fragmentos cortos: solo las líneas relevantes.
- Agrupa los problemas menores repetidos (por ejemplo, el mismo problema de nombres en cinco sitios) en un solo hallazgo con todas las ubicaciones.
- Las preguntas (hallazgos que no pudiste confirmar) van bajo su severidad y empiezan por **Pregunta:**.
- Nunca copies el valor de un secreto en el informe.

## Plantilla

````markdown
# Revisión de código: <rama> · ronda <n>

| | |
|---|---|
| **Fecha** | <AAAA-MM-DD HH:MM> |
| **Rama** | `<rama>` → `<rama base>` |
| **Commit revisado** | `<sha corto>` <+ cambios sin commit, si se incluyeron> |
| **Rango** | `<sha corto del punto de separación>..<sha corto>` (<n> commits) |
| **Pull request** | <#número y título, si lo hay> |
| **Archivos** | <n> revisados (<+añadidas> / <-eliminadas> líneas) |
| **Ronda anterior** | <`review-<n-1>.md`, o "Ninguna"> |

## Resumen

**Veredicto:** <✅ Listo | ⚠️ Listo con cambios | ❌ Necesita trabajo>

<Dos o tres frases: qué hace el cambio (la intención) y la valoración general.>

| 🔴 Crítico | 🟠 Importante | 🟡 Menor | 💡 Sugerencia |
|---|---|---|---|
| <n> | <n> | <n> | <n> |

## Hallazgos anteriores

<Solo a partir de la ronda 2.>

| ID | Hallazgo | Estado | Notas |
|---|---|---|---|
| R<n-1>-F1 | <título corto> | ✅ Corregido | |
| R<n-1>-F2 | <título corto> | 🔄 Corregido en parte | <qué queda> |
| R<n-1>-F3 | <título corto> | ❌ Sigue abierto | Ver F1 en esta ronda |
| R<n-1>-F4 | <título corto> | ➖ Ya no aplica | <por qué> |

## Hallazgos

### 🔴 Críticos

#### F1 · <título corto>

**Ubicación:** `<ruta>:<línea>`
**Categoría:** <Diseño y estructura | Clean code | Errores y lógica | Manejo de errores | Seguridad | Pruebas | Rendimiento>

<Qué está mal, en una o dos frases.>

**Por qué importa:** <la consecuencia: qué se rompe, qué se vuelve más difícil, qué riesgo abre.>

**Propuesta de solución:** <qué hacer.>

```<lenguaje>
<código propuesto, si ayuda>
```

### 🟠 Importantes

#### F2 · <título corto>

...

### 🟡 Menores

...

### 💡 Sugerencias

...

## Lo que está bien hecho

- <Puntos breves y concretos que conviene mantener.>

## No revisado

- <Archivos generados o de terceros, archivos que recibieron una revisión más ligera en un cambio grande, y todo lo que no pudiste comprobar.>

## Siguientes pasos

1. <Corregir primero los hallazgos Críticos e Importantes: F1, F2, ...>
2. <Pedir al agente que aplique las correcciones por ID y después hacer una nueva ronda para comprobarlas.>
````
