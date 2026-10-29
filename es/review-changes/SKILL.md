---
name: review-changes
description: Revisa cambios de código antes de un commit o de un pull request (cambios sin commit, los commits de una rama o un pull request abierto) en busca de defectos, regresiones, riesgos de seguridad, problemas de diseño y de estructura, y desviaciones de los estándares del proyecto, y genera un informe priorizado con evidencia y una recomendación para cada hallazgo. Ejecuta las pruebas y los linters del proyecto cuando existen, puede aplicar las correcciones que el usuario apruebe y puede volver a revisar los cambios después para comprobar las correcciones y detectar lo nuevo. Úsala cuando el usuario pida revisar sus cambios, revisar el código antes de hacer commit o de abrir un pull request, revisar un pull request, o comprobar si se corrigieron los hallazgos de una revisión anterior.
---

# review-changes

Revisa cambios de código para detectar los problemas que importan antes de que lleguen a producción: defectos funcionales, regresiones, riesgos de seguridad, problemas de integridad de datos, problemas de diseño y de estructura, y desviaciones de los estándares del proyecto. Funciona con cualquier lenguaje, framework y arquitectura. El resultado es un informe priorizado guardado en el proyecto, con evidencia y una recomendación para cada hallazgo.

El objetivo no es encontrar la mayor cantidad posible de observaciones, sino los problemas relevantes, con evidencia suficiente y recomendaciones accionables, sin falsos positivos ni ruido.

El flujo tiene tres pasos:

1. **Revisar:** analizar los cambios, ejecutar las validaciones disponibles y escribir el informe. El tamaño y el riesgo del cambio deciden cuánto hace: una revisión rápida para cambios pequeños y una más profunda para los grandes o sensibles.
2. **Corregir (opcional):** aplicar las correcciones que el usuario apruebe.
3. **Volver a revisar:** ejecutarla de nuevo sobre la misma rama para comprobar qué se corrigió y si apareció algo nuevo.

## Principios

- **Primero el cambio, después su contexto.** Juzga las líneas que cambiaron y después el código relacionado, los consumidores y las integraciones a los que afectan. No conviertas la revisión en una auditoría de todo el repositorio.
- **Los estándares del proyecto, no los tuyos.** Averigua las convenciones del proyecto antes de juzgar si se cumplen. No impongas convenciones externas que las contradigan sin una razón sólida.
- **Defectos reales antes que preferencias.** Prioriza los problemas funcionales, las vulnerabilidades, la corrupción de datos, las regresiones y las violaciones de arquitectura con consecuencias concretas. Las preferencias de estilo no son defectos.
- **Principios según el contexto.** Aplica SOLID, DDD, patrones de diseño y principios parecidos solo donde aporten valor. No exijas capas, interfaces ni abstracciones que el código no necesita.
- **No inventes requisitos.** Basa cada hallazgo en código, contratos, requisitos, documentación o comportamiento verificable. El código no está mal solo porque podría escribirse de otra manera. Cuando falte contexto, di qué información necesitas.
- **Hechos, riesgos y sugerencias son cosas distintas.** Separa los defectos confirmados de los riesgos potenciales y de las mejoras opcionales. Nunca presentes una suposición como un hecho.
- **Introducido o preexistente.** Distingue los problemas que introduce el cambio de los que ya estaban. Reporta los preexistentes solo cuando importen para el cambio, y márcalos.
- **Honestidad con las validaciones.** Nunca afirmes que se ejecutó una prueba, un linter o un análisis que no se ejecutó, y nunca declares que el código está libre de errores. Indica qué se revisó y los límites de la revisión.
- **No toques el código sin aprobación.** La revisión solo lee e informa. Las correcciones se aplican únicamente a los hallazgos que el usuario apruebe.
- **Nunca secretos.** Si los cambios contienen una credencial o un token, reporta su ubicación sin copiar su valor.
- **El idioma del usuario.** Escribe el informe en el idioma en el que te habla el usuario.

## 1. Elegir qué revisar

El alcance por defecto es **todo lo que entraría en el pull request**: los commits de la rama desde que se separó de su base, más los cambios sin commit (staged, sin stage y archivos nuevos sin seguimiento).

El usuario puede acotarlo:

| El usuario pide | Alcance |
|---|---|
| "Revisa mis cambios" / sin más detalle | Commits de la rama frente a la base + cambios sin commit |
| "Revisa lo que no he commiteado" | Solo los cambios sin commit: `git diff HEAD` más los archivos sin seguimiento |
| "Revisa esta rama" / "antes del PR" | Commits de la rama frente a la base, más los cambios sin commit si los hay |
| "Revisa el PR 42" / la URL de un pull request | Los cambios del pull request frente a su rama base |
| "Revisa el último commit" / un rango de commits | Ese commit o ese rango |

**Encuentra la rama base.** Para un pull request, usa su rama base. Si no, usa la rama por defecto del repositorio (`git symbolic-ref refs/remotes/origin/HEAD`, o `main` / `master` si eso falla). Compara contra el punto de separación (`git merge-base <base> HEAD`), no contra la punta de la rama base. Si la base es ambigua, pregunta.

**Pull requests.** Si la CLI de la plataforma está instalada y autenticada (`gh` para GitHub, `glab` para GitLab), úsala para obtener la base, el título, la descripción, los issues enlazados y el diff del pull request. Si no, trae la rama del pull request (`git fetch origin pull/<n>/head:<rama-local>` en GitHub) y compárala con su base. No cambies el árbol de trabajo del usuario a otra rama si tiene cambios sin commit; lee los archivos de la referencia descargada (`git show <ref>:<ruta>`).

**Nada que revisar.** Si el alcance no tiene cambios, dilo y pregunta qué revisar.

## 2. Reunir contexto

Antes de juzgar nada:

1. **Lista los archivos cambiados** con su estado (añadido, modificado, eliminado, renombrado) y el tamaño del cambio. Con esa lista, elige el modo de revisión (paso 3) antes de seguir: decide cuánto del resto de este paso necesitas.
2. **Entiende la intención y los requisitos.** Lee los mensajes de los commits y, en un pull request, su título, su descripción y los issues o criterios de aceptación enlazados. Si la intención no está clara, dedúcela de los cambios y deja tu suposición escrita en el informe.
3. **Descubre los estándares del proyecto.** Busca, cuando existan (no supongas que existen):
   - El `README`, la documentación técnica y los registros de decisiones de arquitectura.
   - Los archivos de instrucciones para agentes: `AGENTS.md`, `CLAUDE.md` y similares.
   - El scaffold: la estructura de directorios, módulos y paquetes, y dónde vive cada tipo de código.
   - Las reglas de arquitectura y de dependencias: capas, límites entre módulos, dependencias permitidas.
   - Las convenciones de nombres y de estilo; la configuración de linters, formateadores y análisis estático.
   - Los estándares de pruebas y los umbrales de cobertura.
   - Los contratos de APIs y de eventos (OpenAPI, esquemas, archivos `.proto`).
   - Las políticas de seguridad y de manejo de datos.
   - La configuración de compilación, CI/CD y despliegue.
   - La escala de severidad o prioridad propia del proyecto, si la tiene.
4. **Lee completos los archivos cambiados**, no solo el diff, y los consumidores y dependencias de las partes cambiadas a los que el cambio pueda afectar.
5. **Ignora los archivos generados y de terceros** (archivos lock, resultados de compilación, código generado, archivos minificados, código de terceros), pero comprueba que el cambio no añada por accidente artefactos de compilación, binarios o archivos temporales.

## 3. Elegir el modo de revisión

El tamaño y el riesgo del cambio deciden cuánto trabajo hace la revisión. Elige el modo después de listar los archivos cambiados y antes de leer nada más:

| Modo | Cuándo | Checklist | Validaciones | Informe |
|---|---|---|---|---|
| **Rápida** | Cambio pequeño (pocos archivos, unas 100 líneas cambiadas o menos) que no toca ningún área sensible | Solo el nivel 1 | Las rápidas: lint, comprobación de formato, comprobación de tipos | Corto: cabecera, resumen, hallazgos, validaciones |
| **Estándar** | Cambio mediano o grande, o uno pequeño que toca un área sensible | Nivel 1 + nivel 2 en las áreas que toca el cambio | Las rápidas + las pruebas relacionadas con el cambio | Completo |
| **Profunda** | Cambios en sistemas críticos, datos sensibles, operaciones financieras, seguridad o componentes de alta disponibilidad | Niveles 1, 2 y 3 | Las rápidas + la suite completa de pruebas y la compilación (pregunta antes si son lentas) | Completo |

**Áreas sensibles:** autenticación y autorización, secretos y criptografía, datos personales o financieros, persistencia y migraciones, contratos públicos de APIs o eventos, concurrencia, configuración e infraestructura. Un cambio que toque cualquiera de ellas es, como mínimo, Estándar.

Reglas:

- El usuario puede forzar un modo ("revisión rápida", "revisión profunda"). Respétalo, pero si una revisión rápida encuentra un área sensible, díselo y sugiere una Estándar.
- Si al revisar el cambio resulta más arriesgado de lo que parecía, sube de modo e indícalo en el informe.
- Si el cambio es muy grande, revisa a fondo los archivos de más riesgo e indica en el informe qué recibió una revisión más ligera.
- El modo también limita el contexto que reúnes: en modo Rápida, lee solo los archivos de instrucciones para agentes (`AGENTS.md`, `CLAUDE.md`), la configuración del linter y el código alrededor del cambio; sáltate el resto de la búsqueda de estándares del paso 2.

## 4. Revisar

Recorre los cambios con `references/checklist.md`, según el modo:

- **Nivel 1** (todos los modos) es una lista corta al principio de la checklist. Recórrela entera.
- **Nivel 2** (Estándar y Profunda): lee solo los apartados de la checklist de las áreas que toca el cambio. Un cambio sin código de base de datos no necesita el apartado de persistencia. Dentro de un apartado, aplica solo los puntos relevantes para el cambio; no los recorras uno a uno buscando algo que reportar.
- **Nivel 3** (solo Profunda): los puntos adicionales que la checklist indica para cambios críticos.

Para cada hallazgo, registra:

- **Prioridad:** con la escala de la checklist (de P0 a P3, o Info), según el impacto, el alcance, la probabilidad y las salvaguardas que ya existen. Si el proyecto tiene su propia escala, usa esa.
- **Tipo:** defecto confirmado, riesgo potencial o sugerencia.
- **Origen:** introducido por el cambio o preexistente.
- **Ubicación, problema, condiciones, impacto, evidencia y recomendación**, como se describe en `references/report-template.md`.

Anota también, brevemente, lo que está bien hecho. Le dice al autor qué debe seguir haciendo.

## 5. Ejecutar las validaciones disponibles

Ejecuta las comprobaciones que el proyecto ya define, para respaldar la revisión con resultados reales. Usa los comandos del propio proyecto (scripts de `package.json`, `Makefile`, tareas de Gradle o Maven, configuración de CI, etc.) y ejecuta solo lo que pide el modo (consulta la tabla del paso 3):

- **Comprobaciones rápidas**, en todos los modos: linters, comprobaciones de formato (en modo verificación) y comprobaciones de tipos. Limítalas a los archivos cambiados cuando la herramienta lo permita.
- **Pruebas relacionadas**, a partir del modo Estándar: las pruebas de los módulos cambiados, si las herramientas del proyecto permiten ejecutarlas por separado. Si no, la suite completa cuenta como una comprobación lenta.
- **Suite completa y compilación**, en modo Profunda.

Límites:

- No ejecutes nada que modifique archivos (formateadores en modo escritura, `--fix`), instale dependencias, migre o altere datos, despliegue, o necesite credenciales o servicios de producción.
- Si las pruebas son lentas, necesitan servicios externos (bases de datos, contenedores) o no estás seguro de que un comando sea seguro, pregunta antes de ejecutarlo.
- Si una validación falla por el entorno (una herramienta que falta, un servicio caído), dilo y no lo reportes como un defecto del código.
- Registra qué se ejecutó y su resultado, qué falló y qué no se pudo ejecutar, y por qué.

## 6. Verificar los hallazgos

Antes de escribir el informe, comprueba cada hallazgo con estas preguntas:

1. ¿Existe un problema concreto?
2. ¿Puedes explicar cuándo ocurre?
3. ¿El impacto es relevante?
4. ¿Hay evidencia suficiente?
5. ¿Corresponde al cambio, o a un efecto del cambio?
6. ¿La recomendación resuelve el problema sin añadir complejidad innecesaria, y encaja con las convenciones del proyecto?
7. ¿Ya lo cubre otro hallazgo? Une los hallazgos que comparten causa raíz.

Si no puedes responderlas con suficiente confianza, no presentes el hallazgo como un defecto confirmado: repórtalo como riesgo potencial e indica qué lo confirmaría, o descártalo. Comprueba que la prioridad no esté inflada: incumplir un principio de diseño no hace crítico un hallazgo por sí solo.

## 7. Escribir el informe

Usa `references/report-template.md`. En modo Rápida, escribe el informe corto que describe la plantilla. En todos los modos, los hallazgos P0, P1 y P2 usan el formato completo, y los P3 e Info el formato compacto de una línea.

**Ubicación:** `.reviews/<rama>/review-<n>.md` en la raíz del repositorio.

- `<rama>` es el nombre de la rama con `/` cambiado por `-` (`feat/login` → `feat-login`). Para un pull request revisado sin tener su rama activa, usa `pr-<número>`. Con un HEAD desacoplado, usa `commit-<sha corto>`.
- `<n>` es el siguiente número de ronda: `1` para la primera revisión de esa rama, `2` para la siguiente, y así sucesivamente.
- La cabecera del informe registra la fecha, la rama, la base, el commit revisado y si se incluyeron cambios sin commit.

**Mantén los informes fuera de git.** Los informes son archivos de trabajo personales. La primera vez, comprueba si `.reviews/` está ignorada (`git check-ignore -q .reviews/`). Si no lo está, añade `.reviews/` a `.git/info/exclude`: ese archivo es local a la copia del usuario, así que el `.gitignore` del proyecto no se toca. Díselo al usuario.

**IDs de los hallazgos.** Numera los hallazgos `F1`, `F2`, ... por orden de prioridad. Los IDs empiezan de nuevo en cada ronda; las rondas posteriores se refieren a los hallazgos anteriores con el número de ronda delante (`R1-F3` es el hallazgo F3 de la ronda 1).

Si no hay defectos relevantes, dilo explícitamente, sin afirmar que el código está libre de errores.

Cuando el informe esté escrito, dale al usuario un resumen corto en la conversación: el modo, el veredicto, el número de hallazgos por prioridad, los más importantes, las validaciones que se ejecutaron y la ruta del informe. No pegues el informe completo.

## 8. Corregir (con aprobación)

Después del resumen, ofrece aplicar las correcciones. Pregunta cuáles: todas, por prioridad (por ejemplo, "las P0 y P1") o por ID ("F1, F3 y F4"). Si el usuario no quiere ninguna, termina aquí.

Cuando el usuario apruebe:

- Aplica solo los hallazgos aprobados, siguiendo la recomendación del informe. Si una corrección resulta necesitar otro enfoque, explícalo antes de aplicarlo.
- No refactorices ni cambies nada más de paso.
- Vuelve a ejecutar las validaciones relevantes, con los mismos límites del paso 5.
- No hagas commit. El usuario decide cuándo hacerlo.
- Al terminar, lista lo que cambiaste por cada hallazgo y sugiere hacer una nueva ronda de revisión.

## 9. Volver a revisar

Cuando el usuario pida revisar de nuevo (por ejemplo, "revisa otra vez", "comprueba si quedó corregido") y ya exista un informe para la rama:

1. **Lee el informe anterior** (`review-<n-1>.md`): sus hallazgos, el commit que revisó, su modo y los estándares que consultó.
2. **Revisa de nuevo el mismo alcance** del paso 1, con el estado actual del código, y vuelve a ejecutar las validaciones. Reutiliza los estándares que lista el informe anterior en lugar de buscarlos otra vez; vuelve a mirar solo los que cambiaron desde ese commit. Elige otra vez el modo para el cambio actual: puede subir o bajar.
3. **Comprueba cada hallazgo anterior** y márcalo:
   - ✅ **Corregido:** el problema desapareció y la corrección no introduce ningún problema nuevo.
   - 🔄 **Corregido en parte:** mejoró, pero queda algo. Di qué.
   - ❌ **Sigue abierto:** sin cambios.
   - ➖ **Ya no aplica:** el código se eliminó o se reescribió, así que el hallazgo ya no aplica.
4. **Revisa lo nuevo:** los cambios desde el commit de la ronda anterior y las propias correcciones. Reporta los hallazgos nuevos con IDs nuevos; marca los que vienen de una corrección.
5. **Escribe `review-<n>.md`** con el apartado "Hallazgos anteriores" completo, y resume el avance al usuario (por ejemplo, "4 de 6 corregidos, 1 P3 nuevo").

El ciclo de corregir y volver a revisar se puede repetir las veces que haga falta. Los informes anteriores nunca se editan; cada ronda es un archivo nuevo.
