# Clasificación del aporte

Cómo clasificar cada commit y cada archivo, qué cuenta como trabajo propio según el rol y qué problemas de calidad buscar.

## Clases de commit

Asigna a cada commit una clase principal. Si un commit mezcla clases, indica la principal y desglosa las líneas, por ejemplo: "🟥 Copia (2.100 líneas) + 🟩 Propio (40 líneas)".

| Clase | Qué es | Cómo reconocerla |
|---|---|---|
| 🟥 **Plantilla o generado** | Archivos creados por una herramienta: scaffold, `init`, generadores, wrappers, lockfiles, código generado | Marcadores de plantilla (`TODO`, `sample`, `my-operation`, `Change this`), clases vacías, estructura idéntica a la que produce la herramienta, categoría `boilerplate` o `test_assets` |
| 🟥 **Copia** | Contenido que ya existía en el repositorio, escrito por otras personas, y que se duplica en otro lugar | Porcentaje de copia ≥ 80% en `summary.md`, confirmado con `git diff -w` contra el origen |
| 🟧 **Adaptación** | Copia con cambios reales: nombres, valores o lógica ajustados al nuevo caso | Copia entre 50% y 80%, y el diff muestra cambios con sentido, no solo renombres |
| 🟧 **Ajuste de configuración** | Cambios pequeños de versión, propiedades, rutas, flags, manifiestos | De 1 a ~20 líneas en archivos `config`, `build` o `deploy_ci`, sin lógica nueva |
| 🟦 **Infraestructura propia** | Trabajo de despliegue, CI, build o plataforma que es nuevo en el repositorio y resuelve un problema real | Copia < 50%, más que un cambio de versión: pipelines, módulos de infraestructura, scripts de despliegue con lógica |
| 🟩 **Código propio** | Lógica nueva, escrita por la persona, que funciona | Copia < 50% en código de producción o de pruebas, sin defectos encontrados |
| 🟨 **Código propio con problemas** | Lógica nueva con defectos | Igual que la anterior, con al menos un problema de la lista de calidad |
| ⬛ **Basura o accidental** | Archivos que nunca debieron entrar en git | Categoría `junk`: logs, binarios compilados, `.env`, carpetas de build, configuración local del IDE |
| ⬜ **Sin contenido** | Renombres, movimientos, merges vacíos | 0 líneas agregadas y eliminadas, o solo renombres |

Reglas:

- **Una copia no es trabajo propio, aunque sea útil.** Crear un microservicio copiando otro puede ser lo que se pidió, pero en el informe las líneas cuentan como copia, no como código escrito. Reconoce la tarea ("dejó creada la estructura del servicio") sin contarla como desarrollo.
- **Una plantilla no es una copia de un compañero.** Si los dos archivos salen de la misma herramienta, di "generado por plantilla", no "copiado de Juan".
- **No sabes quién copió a quién** cuando dos archivos casi iguales aparecen con días de diferencia, o cuando el parecido es con un archivo posterior. Di que comparten origen.
- **Cambios repetidos en varios módulos** (la misma línea en tres servicios) se cuentan una vez como trabajo y se anotan como replicación.

## Qué cuenta como trabajo propio según el rol

| Rol | Cuenta como trabajo propio principal | Cuenta como apoyo |
|---|---|---|
| Desarrollador (backend, frontend, mobile, fullstack) | 🟩 y 🟨 en código de producción y de pruebas | 🟦 y 🟧 |
| DevOps o plataforma | 🟦 (despliegue, CI, build, infraestructura) y scripts | 🟧 y código de producción |
| QA o automatización | Código de pruebas, datos y escenarios de prueba nuevos (< 50% copia) | Código de producción y configuración |
| Líder técnico | Código propio, más revisiones de PR, diseño y decisiones técnicas (fuera de git: consúltalas en el paso 4) | Configuración |
| Practicante o junior | Igual que desarrollador; el informe puede comentar las expectativas del nivel, pero las cifras no cambian | Igual que desarrollador |

El script aplica esta tabla con `--role`. Marca un archivo como **propio** cuando está en las categorías principales del rol, tiene menos del 50 % de copia y no tiene aspecto de plantilla, y como **plantilla** cuando tiene marcadores de plantilla o es pequeño y solo tiene tipos vacíos. Mide igual a todas las personas del equipo. Son reglas, no lectura del código: confírmalas con el diff y corrígelas en el análisis cuando no acierten.

## Casos que el script no resuelve solo

- **Quien crea los primeros componentes.** Si la persona fue la primera en generar un componente con una plantilla (scaffold, `init`), los archivos de la plantilla que no tienen marcadores (por ejemplo, la clase principal o una prueba de configuración) salen como propios: no había nada anterior con qué compararlos. El script los marca con la señal "Propio, pero repetido casi igual después" cuando reaparecen en dos o más sitios. Confírmalo en el diff, descuéntalos del trabajo propio y di cuántas líneas descontaste.
- **Código temporal en la rama principal.** Código escrito para avanzar mientras falta algo (una firma de integración, un backend) o para pasar una puerta de calidad (cobertura de Sonar). Clasifícalo como 🟨 provisional, di quién lo reemplazó y no lo cuentes como un defecto si se hizo a propósito y se reemplazó.
- **Pruebas de aceptación.** Viven en `acceptance-test/` y el script las cuenta como plantillas y datos de prueba, igual para todo el equipo. No son trabajo propio para D1, pero sí cuentan para D5 y van en "Lo que sí aportó".
- **Código cambiado para esquivar una herramienta.** Por ejemplo, partir una cadena para que un escáner deje de avisar. Anótalo como hallazgo de forma de trabajo: lo correcto es marcar el falso positivo en la herramienta.

## Problemas de calidad que buscar

Revisa el código propio (🟩, 🟨, 🟦) con esta lista. Cada problema que encuentres va al informe con el commit, la ruta y, si aplica, la línea.

**Errores**

- Valores fijos donde debería usarse un parámetro o una configuración, sobre todo timeouts, URLs, credenciales o límites.
- Unidades equivocadas (segundos frente a milisegundos, bytes frente a KB).
- Parámetros inyectados o recibidos que no se usan.
- Manejo de errores que traga la excepción, devuelve vacío o pierde información.
- Lógica de plantilla sin implementar que llega a la rama principal (`return Mono.empty()`, `pass`, `TODO`).
- Cambios en código de otras personas que rompen o borran su funcionalidad sin coordinarlo.

**Seguridad y datos**

- Secretos, tokens o contraseñas en el código o en la configuración. Informa solo de la ubicación, nunca del valor.
- Archivos que no deberían estar en git: logs, `.env`, certificados, binarios, carpetas de build.

**Mantenibilidad**

- Código comentado en lugar de borrado.
- Configuración duplicada o contradictoria (la misma dependencia forzada a dos versiones distintas).
- Módulos o dependencias copiados que el componente no necesita.
- Modelos o clases con campos que no corresponden al caso (copiados de otro contexto).

**Pruebas**

- Pruebas que no verifican comportamiento: solo comprueban que algo no lanza una excepción, o que una plantilla devuelve vacío.
- Lógica nueva sin ninguna prueba.

**Forma de trabajo**

- Ensayo y error en la rama principal: varios commits o PRs el mismo día para la misma línea.
- Commits que corrigen el commit anterior de la misma persona.
- Commits muy grandes con mensajes que no describen el contenido.
- Mensajes de commit que no dicen qué cambió ni por qué.

## Destino del código

Para cada parte importante de su código propio, anota qué pasó después:

| Destino | Qué significa |
|---|---|
| **Vigente** | Sigue en la rama analizada, con la mayor parte de sus líneas |
| **Modificado por otros** | Sigue, pero otras personas cambiaron una parte importante |
| **Reescrito por otros** | El archivo existe, pero casi todas sus líneas ahora son de otras personas |
| **Borrado** | El archivo ya no existe. Anota quién lo borró, cuándo y el motivo que dice el commit |

Lee los commits de quien modificó o borró su código. Separa los reemplazos por defectos de los reemplazos por un cambio de requisitos o un refactor general.
