---
name: refine-user-story
description: Refina una historia de usuario antes de implementarla. Lee la historia, explora el código de los frontends, servicios y APIs a los que afecta y comprueba si es lo bastante clara y completa para construirla: valor, alcance, criterios de aceptación, reglas de negocio, casos límite, datos, contratos, diseño, permisos, requisitos no funcionales y dependencias. Señala lo que falta, lo ambiguo y lo que contradice el código actual, hace preguntas agrupadas por quién debe responderlas, en una o dos rondas, y entrega un veredicto y la historia refinada, con criterios de aceptación verificables, notas técnicas, supuestos y preguntas abiertas. Guarda el resultado en un archivo fuera de git y puede actualizarlo cuando el usuario trae una nueva versión de la historia o respuestas a las preguntas abiertas. No modifica código ni estima esfuerzo. Úsala cuando el usuario comparta una historia de usuario, un ticket o un requisito y pida refinarlo, revisarlo, saber si está listo para desarrollo o qué le falta.
---

# refine-user-story

Comprueba si una historia de usuario está lista para implementarse y la convierte en una historia refinada. Funciona con cualquier lenguaje, framework y arquitectura, y con historias que tocan un componente o varios (frontend, servicios, APIs). El resultado es un veredicto y el texto de la historia refinada, guardado en un archivo.

El objetivo no es reescribir la historia más bonita, sino asegurarse de que un desarrollador pueda implementarla y un tester verificarla sin adivinar: cada hueco queda respondido, convertido en un supuesto explícito o como una pregunta abierta visible.

El flujo tiene seis pasos:

1. **Leer** la historia.
2. **Explorar** el código al que afecta.
3. **Diagnosticar** si está lista.
4. **Preguntar** lo que cierra los huecos, en una o dos rondas.
5. **Escribir** la historia refinada y entregarla.
6. **Guardarla** en un archivo.

Una historia ya refinada se puede **actualizar** con una nueva versión de su texto o con respuestas a sus preguntas abiertas (ver "Actualizar una historia refinada").

## Principios

- **Solo lectura.** El refinamiento nunca modifica código, datos ni configuración. El único archivo que escribe es la historia refinada, más la línea del `.gitignore` que la deja fuera de git.
- **La historia describe el comportamiento; el código muestra el estado actual.** Usa el código para saber qué existe ya, qué cambiaría la historia y dónde contradice el comportamiento actual. No conviertas la historia en un diseño técnico.
- **Evidencia del código.** Cada nota técnica y cada contradicción apunta a una ubicación (`ruta:línea` o `ruta`).
- **No inventes requisitos.** Las decisiones de negocio son de quienes llevan la historia. Propón una respuesta para cada pregunta, pero si nadie la confirma es un supuesto y se marca como tal.
- **Visible y no visible.** Lo que está fuera de los repositorios que puedes leer (servicios de otros equipos, terceros, diseños) se lista como "por confirmar", nunca se presenta como seguro.
- **Sin estimados.** El refinamiento dice qué necesita la historia, no cuánto tarda. Para el esfuerzo y el impacto, ofrece la skill `change-impact-analysis`, si está instalada.
- **Dos públicos.** La parte funcional de la historia se escribe para todo el equipo, en lenguaje claro y sin rutas de código. Los detalles técnicos van en una sección aparte.
- **Nunca secretos.** Si encuentras una credencial o un token, menciona su ubicación sin copiar su valor.
- **El idioma de la historia.** Escribe la historia refinada en el idioma de la historia original, salvo que el usuario pida otro.

## 1. Leer la historia

1. **Consigue el texto.** El usuario lo pega, indica un archivo o da el ID de un ticket. Si el agente tiene acceso al gestor de incidencias, puede leer el ticket de ahí; si no, pide al usuario que lo pegue. Conserva el texto original tal cual: va en el archivo guardado.
2. **Identifica el ID** (por ejemplo `PROJ-123`) si la historia lo tiene, y un título corto.
3. **Comprueba si ya se refinó:** busca archivos en `.stories/` cuyo nombre empiece por ese ID o coincida con el título (el paso 6 dice dónde están). Si existe uno, sigue "Actualizar una historia refinada".
4. **Reformula la historia en una o dos frases:** quién, qué y para qué, tal como la entendiste. Separa la necesidad de la solución que la historia imponga ("añadir un botón que exporte a CSV" puede esconder la necesidad "enviar los pedidos a contabilidad").
5. **Identifica los componentes** que implica la historia (frontend web o móvil, servicios, APIs, procesos batch, bases de datos) y dónde está su código:
   - En el repositorio actual o el monorepo, encuéntralos por sus carpetas y nombres.
   - Si un componente está en otro repositorio, pide al usuario su ruta local. Léelo igual, en solo lectura.
   - Un componente que no puedes leer se lista como "por confirmar".
6. Si el proyecto tiene su propia plantilla de historia o su Definition of Ready (en la documentación del repositorio, en los archivos de instrucciones para agentes o porque el usuario la da), úsala como base de la lista de comprobación y del resultado, y completa los huecos con `references/readiness-checklist.md` y `references/story-template.md`.

## 2. Explorar el código

Una pasada dirigida por cada componente afectado, para saber qué existe hoy:

1. **Lee el contexto del proyecto:** `README`, archivos de instrucciones para agentes (`AGENTS.md`, `CLAUDE.md` y similares), documentación de arquitectura y la estructura de carpetas.
2. **Encuentra lo que toca la historia:** pantallas y componentes, rutas, endpoints y sus modelos de petición y respuesta, eventos, entidades de dominio, validaciones, reglas de negocio, permisos y roles, tablas y columnas, feature flags, textos que ve el usuario y sus traducciones. Busca por las palabras de la propia historia, por los nombres de las entidades que menciona y por los textos visibles.
3. **Anota el comportamiento actual** del que depende la historia o que cambia: una validación que ya existe, un campo obligatorio, un estado que la entidad no puede tener, un rol que no ve la pantalla.
4. **Anota contradicciones y solapes:** la historia pide algo que el código ya hace, algo que no permite, o algo que otra parte del código hace distinto.

No profundices más de lo que el refinamiento necesita. El análisis de impacto completo es cosa de `change-impact-analysis`.

## 3. Diagnosticar

Recorre las áreas de `references/readiness-checklist.md` y da a cada una un estado:

- ✅ **Clara:** la historia lo dice y es coherente con el código.
- ⚠️ **Ambigua:** la historia lo dice, pero se puede leer de más de una forma o contradice el código.
- ❌ **Falta:** la historia no lo dice y la implementación lo necesita.
- ➖ **No aplica.**

Comprueba también el tamaño: si la historia cubre varios comportamientos independientes, varios tipos de usuario o varios componentes que se podrían entregar por separado, propón dividirla, con un título y un objetivo de una línea para cada parte.

## 4. Preguntar

Haz las preguntas cuya respuesta cambia lo que se construye o cómo se verifica, en **dos rondas como máximo**.

**Primera ronda:** un mensaje con:

- Un diagnóstico corto: la historia reformulada, los componentes encontrados y las áreas ⚠️ y ❌, una línea cada una.
- Las preguntas, **ocho como máximo**, las más importantes primero, **agrupadas por quién debe responderlas**: producto o negocio, diseño o UX, técnico, otro equipo o tercero.

Para cada pregunta:

- Básala en lo que encontraste en el código, no en plantillas genéricas. Por ejemplo: "El API rechaza pedidos sin `shippingAddress` (`OrderValidator.java:58`), pero la historia permite recoger en tienda. ¿Los pedidos de recogida deben saltarse esa validación?".
- Di por qué importa, en pocas palabras.
- Márcala como **bloqueante** si la historia no se puede implementar sin la respuesta.
- Propón una respuesta: la que elegirías tú.

Dile al usuario que puede responder algunas preguntas, todas o ninguna, y que lo que quede sin respuesta pasa a ser un supuesto (si tiene respuesta propuesta y no es bloqueante) o una pregunta abierta. Muchas respuestas dependen de personas que no están en la conversación: es normal, y las preguntas abiertas están pensadas para llevárselas.

**Segunda ronda:** solo si las respuestas abren preguntas nuevas o se contradicen entre sí o con el código, y solo con esas preguntas (cuatro como máximo). Si la primera ronda no dejó nada nuevo, sáltala. Nunca una tercera ronda: lo que siga sin respuesta pasa a ser un supuesto o una pregunta abierta.

Si la historia es clara y no hay nada ambiguo, sáltate las preguntas, dilo y ve al paso 5.

## 5. Escribir y entregar

Escribe la historia refinada con la estructura de `references/story-template.md`. Después da el veredicto:

- ✅ **Lista:** ninguna área está en ❌ ni en ⚠️, y no hay preguntas abiertas.
- ⚠️ **Lista con supuestos:** no queda ninguna pregunta bloqueante abierta; los huecos restantes están cubiertos por supuestos o por preguntas abiertas no bloqueantes.
- ❌ **No lista:** queda al menos una pregunta bloqueante abierta, o no se pueden escribir los criterios de aceptación.

Antes de entregar, comprueba que:

1. Cada criterio de aceptación es observable y verificable, y los criterios cubren el flujo principal, las alternativas y los errores que implican la historia o el código.
2. Cada decisión viene de una respuesta o está marcada como supuesto.
3. Cada nota técnica y cada contradicción tiene una ubicación en el código.
4. La parte funcional no tiene rutas de código ni nombres internos que el equipo no entendería.
5. Nada contradice las respuestas que dio el usuario.

En la conversación, muestra el veredicto con su motivo, la parte funcional de la historia refinada (lista para copiar al gestor de incidencias), las preguntas abiertas y un resumen de las notas técnicas en pocas líneas. El contenido completo va al archivo.

Al final, ofrece los siguientes pasos:

- Llevar las preguntas abiertas a quien deba responderlas y volver con las respuestas o con una nueva versión de la historia para actualizar el refinamiento.
- Analizar el impacto y el esfuerzo de la historia (por ejemplo, con la skill `change-impact-analysis`, si está instalada).
- Implementarla. No empieces sin la aprobación del usuario.

## 6. Guardar la historia refinada

Guárdala siempre: el archivo es el entregable.

**Ubicación:** `.stories/<historia>.md`, en esta carpeta:

- **Repositorio de un solo proyecto:** la raíz del repositorio.
- **Monorepo, historia en un solo componente:** la carpeta raíz de ese microservicio, app o paquete (por ejemplo, `services/orders/.stories/`).
- **Monorepo, historia en varios componentes:** la raíz del repositorio.
- **Varios repositorios:** la raíz del repositorio actual (en el que empezó la conversación). Lista todos los repositorios en la cabecera del archivo.
- **Sin git:** la carpeta raíz del proyecto.

A partir de aquí, `<carpeta>` es esa carpeta.

- `<historia>` es el ID seguido de un título corto en kebab-case y en inglés (`PROJ-123-export-orders-csv`), o solo el título si la historia no tiene ID.
- Si ya existe un archivo con ese nombre pero es de otra historia, pide otro nombre.

**Mantén las historias fuera de git.** Son archivos de trabajo y nunca deben entrar en un commit ni subirse. Antes de escribir el archivo:

1. Comprueba si la carpeta está ignorada: `git check-ignore -q <carpeta>/.stories/`.
2. Si no lo está, añade `.stories/` a un `.gitignore`: el de `<carpeta>` si tiene uno; si no, el de la raíz del repositorio (créalo si no existe). Ponlo en su propia línea y con un comentario: `# Refined user stories (refine-user-story)` seguido de `.stories/`. En el `.gitignore` de la raíz, el patrón no lleva `/` al principio, así que también cubre las carpetas `.stories/` de los demás servicios de un monorepo. No cambies nada más del archivo.
3. Avisa al usuario de qué `.gitignore` cambió y de que tiene que hacer commit de ese cambio. No lo hagas tú.
4. Si `.stories/` ya estaba en un commit (`git ls-files <carpeta>/.stories` lista archivos), ignorarla no basta: avisa al usuario y sugiere `git rm -r --cached <carpeta>/.stories` para dejar de seguirla sin borrar los archivos.

**Dile al usuario dónde quedó el archivo.** Cuando esté escrito, da su ruta relativa a la raíz del repositorio y su ruta absoluta, por ejemplo: "La historia refinada quedó en `.stories/PROJ-123-export-orders-csv.md` (`/home/usuario/proyectos/tienda/.stories/PROJ-123-export-orders-csv.md`)".

## Actualizar una historia refinada

Usa este flujo cuando ya existe un archivo en `.stories/` para la historia y el usuario trae una nueva versión de su texto (por ejemplo, después de que el product owner la cambiara), respuestas a preguntas abiertas, o ambas cosas.

1. **Lee el archivo guardado:** la historia refinada, las decisiones, los supuestos, las preguntas abiertas y el texto original.
2. **Compara el texto nuevo con el original anterior.** Lista lo que se añadió, se quitó o cambió, en pocas líneas.
3. **Revisa las decisiones y los supuestos anteriores.** Conserva los que siguen valiendo, actualiza los que el texto nuevo o las respuestas resuelven y quita los que ya no aplican, diciendo por qué.
4. **Vuelve a mirar el código solo donde caen los cambios.** Si el código cambió desde el último refinamiento (compara con el commit de la cabecera), comprueba si eso cambia alguna nota técnica.
5. **Diagnostica de nuevo** y haz solo las preguntas nuevas, con la misma regla de dos rondas como máximo.
6. **Actualiza el archivo:** historia refinada nueva, número de versión más uno, el texto nuevo en "Historia original", el original anterior dentro de la entrada del historial y una línea en el historial con lo que cambió. No crees un archivo nuevo.
7. **Entrega** como en el paso 5, empezando por lo que cambió desde la versión anterior y si cambió el veredicto.

Si el usuario trae solo respuestas, sin texto nuevo, sáltate los pasos 2 y 4.
