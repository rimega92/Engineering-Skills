---
name: change-impact-analysis
description: Analiza el impacto de un cambio de código planeado antes de implementarlo, para saber qué módulos, unidades, procesos, contratos, datos, pruebas, configuración y consumidores puede afectar, directa o indirectamente. Explora el código, hace preguntas para acotar lo que de verdad hay que cambiar y entrega en la conversación una valoración de complejidad, riesgo y confianza, un recuento de los archivos y pruebas a modificar o crear, un estimado de esfuerzo con una talla y un rango, qué revisar antes de empezar, un alcance mínimo frente al completo y un orden de implementación sugerido. No modifica el código. Puede guardar el análisis en un archivo del proyecto que queda fuera de git. Úsala cuando el usuario describa un cambio, una funcionalidad, un refactor o una corrección que piensa hacer y pregunte qué implica, qué afecta, qué tan difícil es, cuánto llevará o cómo abordarlo.
---

# change-impact-analysis

Analiza un cambio antes de escribirlo: qué toca, qué puede romperse, qué tamaño tiene y qué conviene decidir antes de empezar. Funciona con cualquier lenguaje, framework y arquitectura. El resultado es un análisis de impacto en la conversación, con evidencia del código, una valoración y un estimado de esfuerzo.

El objetivo no es la lista de archivos más larga, sino una imagen fiable del cambio: qué hay que cambiar de verdad, qué hay que revisar y qué tan seguro es el análisis.

El flujo tiene cinco pasos:

1. **Entender** la petición.
2. **Explorar** el código para encontrar dónde cae el cambio.
3. **Preguntar** lo que decide el alcance.
4. **Analizar** el impacto a fondo, con las respuestas.
5. **Entregar** el análisis en la conversación y, si el usuario quiere, guardarlo en un archivo.

## Principios

- **Solo lectura.** El análisis nunca modifica código, datos ni configuración. Solo lee, busca y ejecuta comandos que no cambian nada.
- **Evidencia del código.** Cada elemento afectado apunta a una ubicación (`ruta:línea`) y dice por qué se ve afectado. No incluyas un archivo porque su nombre suene relacionado.
- **Directo e indirecto.** Separa lo que el cambio edita de lo que se ve afectado a través de él: llamadores, implementaciones, serialización, consumidores.
- **Visible y no visible.** El repositorio no lo muestra todo. Los consumidores en otros repositorios, otros equipos, versiones antiguas de apps, informes o terceros se listan como "por confirmar", nunca se omiten ni se presentan como seguros.
- **El objetivo antes que la solución.** Separa lo que el usuario quiere conseguir de la solución que propone. Si un cambio más pequeño cumple el objetivo, dilo.
- **No inventes requisitos.** Pregunta cuando una decisión le toca al usuario. Si no responde, usa la respuesta por defecto que propusiste y márcala como supuesto.
- **Estimados honestos.** Da rangos, no cifras exactas, y di qué los hace crecer. Nunca escondas la incertidumbre para que el estimado parezca preciso.
- **No infles.** Un cambio no es arriesgado solo por ser grande, y una dimensión sin impacto lleva una línea, no una sección.
- **Nunca secretos.** Si encuentras una credencial o un token, menciona su ubicación sin copiar su valor.
- **El idioma del usuario.** Escribe el análisis en el idioma en el que te habla el usuario.

## 1. Entender la petición

1. **Reformula el cambio en una frase**, tal como lo entendiste.
2. **Separa el objetivo de la solución.** Por ejemplo: objetivo "mostrar los precios en la moneda del cliente"; solución propuesta "añadir un campo `currency` a `Order`".
3. **Identifica el tipo de cambio:** funcionalidad nueva, cambio de comportamiento, refactor, corrección de un error, actualización de dependencias o de plataforma, cambio de datos, cambio de contrato. El tipo orienta dónde buscar primero.
4. Si la petición es demasiado vaga para buscar en el código (por ejemplo, "mejorar los pedidos"), pregunta qué quiere conseguir el usuario antes de explorar.

## 2. Explorar el código

Una pasada rápida y dirigida para encontrar dónde cae el cambio, todavía no el análisis completo:

1. **Lee el contexto del proyecto:** `README`, archivos de instrucciones para agentes (`AGENTS.md`, `CLAUDE.md` y similares), documentación de arquitectura y estructura de directorios.
2. **Encuentra los puntos de entrada:** las unidades (clases, módulos, componentes, funciones), modelos, endpoints, eventos, tablas y configuración que el cambio nombra o implica. Busca por identificadores, rutas, nombres de eventos, nombres de tablas y columnas, y textos que ven los usuarios.
3. **Sigue el primer nivel de dependencias:** quién usa esos puntos de entrada y de qué dependen.
4. **Elige el modo** (el paso 3 explica cuándo).

## 3. Elegir el modo

| Modo | Cuándo | Dimensiones | Preguntas | Resultado |
|---|---|---|---|---|
| **Rápido** | Cambio local: un módulo, pocos archivos, sin contratos, datos ni áreas sensibles de por medio | Código y Pruebas a fondo; una línea para cada una de las demás, diciendo si aplica | 0 a 2 | Corto: resumen, decisiones, impacto, recuento, estimado, antes de empezar |
| **Profundo** | Varios módulos, un contrato público, datos o migraciones, un área sensible, o mucha incertidumbre | Todas, a fondo | 3 a 6 | Completo |

**Áreas sensibles:** autenticación y autorización, secretos y criptografía, datos personales o financieros, persistencia y migraciones, contratos públicos de API o de eventos, concurrencia, configuración e infraestructura. Un cambio que toque cualquiera de ellas es Profundo.

Reglas:

- El usuario puede forzar un modo ("análisis rápido", "análisis profundo"). Respétalo, pero si un análisis rápido encuentra un área sensible, dilo y sugiere el Profundo.
- Si el cambio resulta más grande de lo que parecía, pasa a Profundo y dilo.

## 4. Preguntar

Haz **una sola vez, en un solo mensaje**, las preguntas cuya respuesta cambia el alcance, el esfuerzo o el riesgo. Básalas en lo que encontraste en el código, no en plantillas genéricas. Por ejemplo: "`Order` se serializa en 3 endpoints públicos y en el evento `OrderCreated`; ¿el campo nuevo debe aparecer en todos o solo en el endpoint interno?".

Para cada pregunta:

- Di por qué importa (qué cambia según la respuesta).
- Propón una respuesta por defecto, la que elegirías tú.

Temas habituales, solo cuando apliquen:

- **Alcance:** qué pantallas, endpoints, consumidores o tipos de usuario cubre el cambio.
- **Datos existentes:** qué pasa con los registros creados antes del cambio (valor por defecto, backfill, dejarlos como están).
- **Compatibilidad:** si los consumidores actuales deben seguir funcionando sin cambios o se acepta una versión incompatible.
- **Despliegue:** de una vez, detrás de un feature flag o de forma gradual.
- **Versión mínima:** si basta con un cambio más pequeño por ahora (propónlo si ves uno).
- **Requisitos no funcionales:** volumen, rendimiento, seguridad o cumplimiento normativo que cambien la solución.

En modo Rápido, si nada es ambiguo, sáltate las preguntas y declara tus supuestos en el resultado. Si el usuario responde solo algunas preguntas, usa tus respuestas por defecto para el resto y márcalas como supuestos.

## 5. Analizar

Con las respuestas, recorre las dimensiones de `references/impact-checklist.md` según el modo. Para cada elemento afectado, anota:

- **Ubicación:** `ruta:línea` o `ruta`.
- **Qué cambia**, en breve.
- **Tipo de impacto:** directo (se edita) o indirecto (se ve afectado a través de otra cosa).
- **Evidencia:** la llamada, el import, la serialización, la consulta, la configuración o el contrato que lo une al cambio.
- **Visibilidad:** confirmado en el código, o por confirmar (fuera del repositorio o no verificable).

Después:

1. **Cuenta** los archivos y unidades a modificar, crear y eliminar, separando código de producción, pruebas, migraciones y scripts, configuración e infraestructura, y documentación.
2. **Valora** la complejidad, el riesgo y la confianza, y **estima** el esfuerzo, con `references/estimation.md`.
3. **Define el alcance:** el cambio mínimo que cumple el objetivo y el completo, si son distintos, con lo que incluye cada uno y su estimado.
4. **Lista lo que hay que revisar antes de empezar:** decisiones pendientes, coordinación con otros equipos o consumidores, datos que inspeccionar, pruebas que faltan en la zona y conviene escribir primero.
5. **Propón un orden de implementación**, en pasos que se puedan integrar y, cuando sea posible, desplegar por separado (por ejemplo: migración compatible, luego el código que escribe el campo nuevo, luego los consumidores, luego la limpieza).

Puedes ejecutar comandos que no cambian nada para respaldar el análisis: búsquedas, `git log` para ver con qué frecuencia cambia una zona, listados de pruebas, árboles de dependencias. No ejecutes nada que modifique archivos, instale dependencias o toque datos, y no ejecutes la batería de pruebas: el análisis describe las pruebas, no las ejecuta.

## 6. Verificar

Antes de entregar, comprueba que:

1. Cada elemento afectado tiene evidencia. Quita los que no la tienen, o pásalos a "por confirmar" y di qué los confirmaría.
2. Los impactos indirectos siguen una cadena real (A llama a B, B serializa C), no solo un nombre parecido.
3. Buscaste los usos que el compilador no ve: cadenas de texto, reflexión, archivos de configuración, plantillas, SQL, nombres serializados, rutas, scripts.
4. El recuento coincide con los elementos listados.
5. El estimado y la valoración son coherentes con el impacto encontrado, y la confianza refleja lo que no se pudo verificar.

## 7. Entregar

Escribe el análisis en la conversación con la estructura de `references/report-template.md` (versión corta en modo Rápido, completa en Profundo). Empieza por el resumen: talla, estimado, complejidad, riesgo y confianza, para que el usuario tenga la respuesta de un vistazo.

Al final, ofrece los siguientes pasos:

- **Guardar el análisis** en un archivo (ver abajo).
- **Implementar el cambio**, siguiendo el orden sugerido. No empieces sin la aprobación del usuario.
- Después de implementarlo, revisar los cambios (por ejemplo, con la skill `review-changes`, si está instalada).

## 8. Guardar el análisis (si el usuario lo pide)

**Ubicación:** `.impact/<cambio>.md` en la carpeta del proyecto al que va el cambio:

- **Repositorio de un solo proyecto:** la raíz del repositorio.
- **Monorepo:** la carpeta del microservicio, la app o el paquete que el cambio modifica (por ejemplo, `services/orders/.impact/`), no la raíz del repositorio. Si el cambio abarca varios, usa la carpeta del principal y menciona los demás en el análisis; si ninguno es claramente el principal, pregunta.
- **Sin git:** la carpeta raíz del proyecto.

A partir de aquí, `<carpeta>` es esa carpeta.

- `<cambio>` es un nombre corto del cambio en kebab-case y en inglés (`add-order-currency`).
- Si ya existe un archivo con ese nombre (un análisis anterior del mismo cambio), pregunta si reemplazarlo o crear `<cambio>-2.md`.
- La cabecera del archivo registra la fecha y el commit analizado.

**Mantén los análisis fuera de git.** Son archivos de trabajo personales y nunca deben entrar en un commit ni subirse. Antes de escribir el archivo:

1. Comprueba si la carpeta está ignorada: `git check-ignore -q <carpeta>/.impact/`.
2. Si no lo está, añade `.impact/` a un `.gitignore`: el de `<carpeta>` si tiene uno; si no, el de la raíz del repositorio (créalo si no existe). Ponlo en su propia línea y con un comentario: `# Change impact analyses (change-impact-analysis)` seguido de `.impact/`. En el `.gitignore` de la raíz, el patrón no lleva `/` al principio, así que también cubre las carpetas `.impact/` de los demás servicios de un monorepo. No cambies nada más del archivo.
3. Avisa al usuario de qué `.gitignore` cambió y de que tiene que hacer commit de ese cambio. No lo hagas tú.
4. Si `.impact/` ya estaba en un commit (`git ls-files <carpeta>/.impact` lista archivos), ignorarla no basta: avisa al usuario y sugiere `git rm -r --cached <carpeta>/.impact` para dejar de seguirla sin borrar los archivos.

**Dile al usuario dónde quedó el archivo.** Cuando esté escrito, da su ruta relativa a la raíz del repositorio y su ruta absoluta, por ejemplo: "El análisis quedó en `services/orders/.impact/add-order-currency.md` (`/home/usuario/proyectos/tienda/services/orders/.impact/add-order-currency.md`)".
