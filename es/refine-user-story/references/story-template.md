# Plantilla de la historia refinada

Estructura del archivo que se guarda en `.stories/<historia>.md`. La conversación muestra el veredicto, la parte funcional, las preguntas abiertas y un resumen de las notas técnicas; el archivo lo tiene todo. Escríbelo en el idioma de la historia original. Omite las secciones sin contenido, salvo la historia refinada, la tabla de preparación y la historia original.

## Reglas

- **Parte funcional** (sección "Historia refinada"): lenguaje claro, para todo el equipo, sin rutas de código ni nombres internos. Debe entenderse pegada sola en el gestor de incidencias.
- **Criterios de aceptación:** en formato Dado / Cuando / Entonces, con las palabras clave en el idioma de la historia (por ejemplo, en inglés: Given / When / Then). Un escenario por comportamiento, incluidas las alternativas y los errores. Cada uno observable: qué ve el usuario, qué devuelve o guarda el sistema.
- **Notas técnicas:** cada elemento con una ubicación (`ruta:línea` o `ruta`) y el repositorio o componente al que pertenece.
- **Supuestos:** toda decisión que nadie confirmó. Quien lea debe distinguir de un vistazo las decisiones confirmadas de los supuestos.
- Nunca copies el valor de un secreto.

## Plantilla

````markdown
# <ID>: <título>

| | |
|---|---|
| **Versión** | <1, 2, ...> |
| **Fecha** | <AAAA-MM-DD> |
| **Veredicto** | <✅ Lista | ⚠️ Lista con supuestos | ❌ No lista>: <motivo en una frase> |
| **Componentes** | <frontends, servicios y APIs implicados> |
| **Código analizado** | <repositorio o componente>: `<sha corto>` en `<rama>` <una línea por repositorio> |
| **No visible** | <componentes que no se pudieron leer, o "—"> |

## Historia refinada

**Como** <rol>, **quiero** <acción> **para** <beneficio>.

### Contexto

<Por qué existe esta historia y la situación actual, en pocas frases.>

### Criterios de aceptación

**Escenario 1: <nombre>**

- **Dado** <estado inicial>
- **Cuando** <acción>
- **Entonces** <resultado observable>

**Escenario 2: <nombre>**

- ...

### Reglas de negocio

- <Regla, límite, cálculo o validación.>

### Fuera de alcance

- <Lo que esta historia no incluye, y adónde va si se sabe (otra historia, una fase posterior).>

### División propuesta

<Solo si la historia es demasiado grande. Una línea por parte: título y objetivo.>

## Notas técnicas

| Componente | Ubicación | Qué cambia o qué revisar |
|---|---|---|
| <web-app> | `<ruta:línea>` | <descripción corta> |

- **Contratos:** <endpoints, eventos o esquemas que cambian, y sus consumidores conocidos.>
- **Datos:** <datos nuevos o cambiados, registros existentes.>
- **Contradicciones con el código actual:** <lo que pide la historia frente a lo que hace el código, con ubicación, y cómo se resolvió.>
- **Por confirmar:** <lo que no se pudo verificar y cómo confirmarlo.>

## Preparación

| Área | Estado | Nota |
|---|---|---|
| Valor y usuario | <✅ ⚠️ ❌ ➖> | <una línea> |
| Alcance y tamaño | | |
| Criterios de aceptación | | |
| Reglas de negocio y validaciones | | |
| Casos límite y errores | | |
| Datos | | |
| Contratos e integraciones | | |
| Diseño, textos y experiencia de usuario | | |
| Permisos y seguridad | | |
| Requisitos no funcionales | | |
| Dependencias y despliegue | | |
| Facilidad de prueba | | |

## Decisiones y supuestos

| Tema | Decisión | Origen |
|---|---|---|
| <Registros existentes> | <Mantienen su valor actual> | <Respuesta, ronda 1 | Supuesto> |

## Preguntas abiertas

| # | Pregunta | Para | Bloqueante | Respuesta propuesta |
|---|---|---|---|---|
| P1 | <pregunta> | <Producto | Diseño | Técnico | Equipo X> | <Sí | No> | <respuesta> |

## Historia original

<El texto exactamente como lo dio el usuario, en esta versión.>

## Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 1 | <AAAA-MM-DD> | Primer refinamiento. |
| 2 | <AAAA-MM-DD> | <Qué cambió: texto nuevo, respuestas a P1 y P3, veredicto nuevo.> |

<details>
<summary>Historia original, versión 1</summary>

<El texto original anterior, cuando una versión nueva lo reemplazó.>

</details>
````
