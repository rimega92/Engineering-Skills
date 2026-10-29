# Plantilla del informe

Estructura del informe que se guarda en `.reviews/<rama>/review-<n>.md`. Debe ser breve, priorizado y orientado a tomar decisiones. Escríbelo en el idioma del usuario. Omite los apartados sin contenido, salvo la cabecera, el resumen, los hallazgos y las validaciones.

## Tamaño del informe según el modo

- **Rápida:** cabecera, resumen, hallazgos y validaciones. Omite los demás apartados; si algo importante no se verificó, menciónalo en el resumen.
- **Estándar y Profunda:** todos los apartados con contenido.

## Formatos de hallazgo

- **Formato completo** para P0, P1 y P2: ID, prioridad, tipo, origen, ubicación como `ruta:línea` (o `ruta:inicio-fin`), problema, condiciones, impacto, evidencia y recomendación. Consulta F1 en la plantilla.
- **Formato compacto** para P3 e Info: una línea con el ID, la prioridad, la ubicación, el problema y la recomendación. Por ejemplo: F7 · 🔵 P3 · `src/orders/service.ts:88` · `calc` no dice qué calcula → renómbrala a `calculateShippingCost`.

## Reglas

- Ordena los hallazgos por prioridad, de mayor a menor, y dentro de la misma prioridad por archivo.
- La evidencia es lo que sostiene el hallazgo: el código relevante, el flujo de ejecución, el contrato o el comportamiento observado. Mantén los fragmentos cortos: solo las líneas relevantes.
- Muestra código propuesto solo cuando aclare la recomendación.
- Un hallazgo por causa raíz. Agrupa los problemas menores repetidos (por ejemplo, el mismo problema de nombres en cinco sitios) en un solo hallazgo con todas las ubicaciones.
- Los Info son mejoras opcionales. No los conviertas en bloqueantes sin una razón concreta.
- Nunca copies el valor de un secreto en el informe.
- Si no hay defectos relevantes, dilo explícitamente, sin afirmar que el código está libre de errores.

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
| **Modo** | <Rápida | Estándar: áreas revisadas a fondo | Profunda: por qué> |
| **Estándares consultados** | <archivos y reglas usados, por ejemplo `AGENTS.md`, `.eslintrc`, `docs/architecture.md`> |
| **Ronda anterior** | <`review-<n-1>.md`, o "Ninguna"> |

## Resumen

**Veredicto:** <✅ Listo | ⚠️ Listo con cambios | ❌ Necesita trabajo>

<Qué se revisó y qué tipo de cambio es (la intención), el resultado general, los principales riesgos encontrados y los límites relevantes de la revisión. De tres a cinco frases.>

| 🔴 P0 | 🟠 P1 | 🟡 P2 | 🔵 P3 | 💡 Info |
|---|---|---|---|---|
| <n> | <n> | <n> | <n> | <n> |

## Hallazgos anteriores

<Solo a partir de la ronda 2.>

| ID | Hallazgo | Estado | Notas |
|---|---|---|---|
| R<n-1>-F1 | <título corto> | ✅ Corregido | |
| R<n-1>-F2 | <título corto> | 🔄 Corregido en parte | <qué queda> |
| R<n-1>-F3 | <título corto> | ❌ Sigue abierto | Ver F1 en esta ronda |
| R<n-1>-F4 | <título corto> | ➖ Ya no aplica | <por qué> |

## Hallazgos

### F1 · 🔴 P0 · <título corto>

| | |
|---|---|
| **Ubicación** | `<ruta>:<línea>` |
| **Categoría** | <apartado de la checklist, por ejemplo "Persistencia e integridad de datos"> |
| **Tipo** | <Defecto confirmado | Riesgo potencial> |
| **Origen** | <Introducido por el cambio | Preexistente> <· Viene de la corrección de R<n-1>-F<m>, si es el caso> |

**Problema:** <qué está mal y por qué.>

**Condiciones:** <cuándo o cómo ocurre.>

**Impacto:** <la consecuencia funcional, técnica, de seguridad u operativa.>

**Evidencia:** <el código, el flujo, el contrato o el comportamiento que lo sostiene.>

```<lenguaje>
<código relevante>
```

**Recomendación:** <acción concreta para resolverlo o reducir el riesgo.>

```<lenguaje>
<código propuesto, si ayuda>
```

<En un riesgo potencial, añade: **Para confirmarlo:** <qué información o validación lo confirmaría.>>

### F2 · 🟠 P1 · <título corto>

...

### Hallazgos P3

- F6 · 🔵 P3 · `<ruta>:<línea>` · <problema> → <recomendación>

## Mejoras opcionales

- F8 · 💡 Info · `<ruta>:<línea>` · <qué mejorar> → <cómo>

## Validaciones

| Validación | Comando | Resultado |
|---|---|---|
| <Lint> | `<comando>` | <✅ Pasó | ❌ Falló: resumen | ⏭️ No se ejecutó: motivo> |
| <Pruebas> | `<comando>` | <...> |

<Límites del entorno o de la información disponible, si los hay.>

## Riesgos no verificados

- <Riesgos relevantes que no se pudieron confirmar ni validar, y qué evidencia o validación haría falta.>

## Lo que está bien hecho

- <Puntos breves y concretos que conviene mantener.>

## No revisado

- <Archivos generados o de terceros, archivos que recibieron una revisión más ligera en un cambio grande, y lo que queda fuera del alcance.>

## Siguientes pasos

1. <Corregir primero los hallazgos bloqueantes: F1, F2, ...>
2. <Pedir al agente que aplique las correcciones por ID y después hacer una nueva ronda para comprobarlas.>
````
