# Plantilla del análisis

Estructura del análisis de impacto. Úsala para la respuesta en la conversación y, si el usuario lo pide, para el archivo guardado en `.impact/<cambio>.md`; los dos tienen el mismo contenido. Escríbelo en el idioma del usuario. Omite los apartados sin contenido, salvo el resumen, el impacto y el estimado.

## Tamaño según el modo

- **Rápido:** resumen, decisiones y supuestos, impacto por área (una línea por cada dimensión que no aplica), recuento, estimado y antes de empezar.
- **Profundo:** todos los apartados con contenido.

## Reglas

- Empieza por el resumen: el usuario debe tener la respuesta en las primeras líneas.
- Cada elemento afectado tiene una ubicación (`ruta:línea` o `ruta`) y una razón corta.
- Agrupa los elementos repetidos (por ejemplo, el mismo cambio en ocho DTO) en una línea con todas las ubicaciones.
- Una dimensión sin impacto lleva una línea que dice qué se comprobó: "Sin impacto: ningún consumidor lee `orders.status` fuera de este módulo (buscado en `src/`, `scripts/` e `infra/`)".
- Lo que no pudiste verificar va en "Por confirmar", con cómo confirmarlo.
- Nunca copies el valor de un secreto.

## Plantilla

````markdown
# Análisis de impacto: <título corto del cambio>

| | |
|---|---|
| **Fecha** | <AAAA-MM-DD> |
| **Proyecto** | <nombre del repositorio o del servicio> |
| **Componentes** | <en un monorepo, los componentes que toca el cambio> |
| **Commit analizado** | `<sha corto>` en `<rama>` <+ cambios sin commit, si los hay> |
| **Modo** | <Rápido | Profundo: por qué> |
| **Petición** | <el cambio tal como lo describió el usuario> |
| **Entendido como** | <objetivo y solución, en una o dos frases> |

## Resumen

| Talla | Estimado | Complejidad | Riesgo | Confianza |
|---|---|---|---|---|
| <XS–XL> | <rango, por ejemplo "de 2 a 4 días"> | <Baja–Muy alta> | <Bajo–Muy alto> | <Alta | Media | Baja> |

<Qué implica el cambio, los impactos principales, el mayor riesgo y qué decidir antes de empezar. De tres a cinco frases.>

**Complejidad:** <justificación en una frase.>
**Riesgo:** <justificación en una frase.>
**Confianza:** <justificación en una frase, y qué la subiría.>

## Decisiones y supuestos

| Tema | Decisión | Origen |
|---|---|---|
| <Datos existentes> | <Los pedidos existentes reciben `currency = EUR`> | <Respuesta del usuario | Supuesto> |

## Alcance

| | Mínimo | Completo |
|---|---|---|
| **Incluye** | <qué> | <qué> |
| **Deja fuera** | <qué> | <—> |
| **Estimado** | <rango> | <rango> |

<Recomendación: cuál hacer primero y por qué.>

## Impacto por área

### Código

| Ubicación | Qué cambia | Impacto | Evidencia |
|---|---|---|---|
| `<ruta>:<línea>` | <breve> | <Directo | Indirecto> | <llamada, import, serialización...> |

### Procesos y flujos

...

### Contratos

<Para cada contrato: qué cambia y si es compatible o incompatible.>

### Datos

...

### Pruebas

| Ubicación | Acción | Por qué |
|---|---|---|
| `<ruta>` | <Modificar | Crear> | <breve> |

### Consumidores

| Consumidor | Visible | Qué necesita |
|---|---|---|
| <frontend web, `web/src/orders/`> | ✅ En el repositorio | <Mostrar el campo nuevo> |
| <servicio de facturación> | ❓ Por confirmar | <Comprobar si lee `OrderCreated`> |

### Configuración, infraestructura, seguridad, operación y documentación

<Solo lo que aplique; una línea para el resto.>

## Recuento

| Tipo | Modificar | Crear | Eliminar |
|---|---|---|---|
| Archivos de producción | <n> | <n> | <n> |
| Pruebas | <n> | <n> | <n> |
| Migraciones y scripts | <n> | <n> | <n> |
| Configuración e infraestructura | <n> | <n> | <n> |
| Documentación | <n> | <n> | <n> |
| **Total** | <n> | <n> | <n> |

<Unidades afectadas, si es útil: por ejemplo "7 clases, 2 interfaces, 1 componente".>

## Estimado de esfuerzo

| Actividad | Estimado | Notas |
|---|---|---|
| Implementación | <rango> | |
| Pruebas | <rango> | |
| Migraciones y backfill | <rango> | |
| Contratos y consumidores | <rango> | |
| Revisión y correcciones | <rango> | |
| **Total** | **<rango>** | Talla <XS–XL>, confianza <nivel> |

**Qué lo hace crecer:** <hechos concretos que lo subirían.>
**No incluido:** <tiempos de espera, coordinación, QA, despliegue.>

## Antes de empezar

- [ ] <Decisión que tomar, datos que inspeccionar, consumidor que confirmar, prueba que escribir primero...>

## Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| <Las versiones antiguas de la app fallan con el campo nuevo> | <Baja | Media | Alta> | <Bajo | Medio | Alto> | <Hacer el campo opcional> |

## Orden sugerido

1. <Paso que se puede integrar por sí solo, por ejemplo "migración compatible: columna que admite nulos">
2. <...>

## Por confirmar

- <Elemento que no se puede verificar desde el repositorio, y cómo confirmarlo.>
````
