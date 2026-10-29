---
name: review-changes
description: Revisa cambios de código antes de un commit o de un pull request (cambios sin commit, los commits de una rama o un pull request abierto) en busca de malas prácticas, problemas de clean code, de diseño y de estructura, y errores, y genera un informe con una propuesta de solución para cada hallazgo. Puede aplicar las correcciones cuando el usuario las aprueba, y volver a revisar los cambios después para comprobar las correcciones y detectar lo nuevo. Úsala cuando el usuario pida revisar sus cambios, revisar el código antes de hacer commit o de abrir un pull request, revisar un pull request, o comprobar si se corrigieron los hallazgos de una revisión anterior.
---

# review-changes

Revisa cambios de código como lo haría un compañero sénior cuidadoso: primero el diseño y la estructura, después el clean code, los errores y las buenas prácticas. Funciona con cualquier lenguaje y tecnología. El resultado es un informe guardado en el proyecto, con una propuesta de solución para cada hallazgo.

El flujo tiene tres pasos:

1. **Revisar:** analizar los cambios y escribir el informe.
2. **Corregir (opcional):** aplicar las correcciones que el usuario apruebe.
3. **Volver a revisar:** ejecutarla de nuevo sobre la misma rama para comprobar qué se corrigió y si apareció algo nuevo.

## Principios

- **Revisa el cambio, en su contexto.** Juzga las líneas que cambiaron, pero lee el código de alrededor lo suficiente para entenderlas. No reportes problemas de código que el cambio no tocó, salvo que el cambio los empeore o dependa de ellos.
- **Sigue las convenciones del proyecto.** Antes de sugerir un estilo o un patrón, comprueba cómo lo hace ya el proyecto. Una sugerencia que va en contra del resto del código no es una mejora.
- **Cada hallazgo está verificado.** Reporta algo solo después de comprobarlo en el código. Si no estás seguro, dilo y márcalo como pregunta en lugar de afirmarlo.
- **Cada hallazgo tiene solución.** Di qué está mal, por qué importa y cómo arreglarlo, con código cuando ayude.
- **Proporcional y útil.** Prioriza lo que importa. No llenes el informe de comentarios triviales; agrupa los problemas menores repetidos en un solo hallazgo.
- **No toques el código sin aprobación.** La revisión solo lee. Las correcciones se aplican únicamente a los hallazgos que el usuario apruebe.
- **Nunca secretos.** Si los cambios contienen una credencial o un token, repórtalo sin copiar su valor en el informe.
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

**Pull requests.** Si la CLI de la plataforma está instalada y autenticada (`gh` para GitHub, `glab` para GitLab), úsala para obtener la base, el título, la descripción y el diff del pull request. Si no, trae la rama del pull request (`git fetch origin pull/<n>/head:<rama-local>` en GitHub) y compárala con su base. No cambies el árbol de trabajo del usuario a otra rama si tiene cambios sin commit; lee los archivos de la referencia descargada (`git show <ref>:<ruta>`).

**Nada que revisar.** Si el alcance no tiene cambios, dilo y pregunta qué revisar.

## 2. Reunir contexto

Antes de juzgar nada:

1. **Lista los archivos cambiados** con su estado (añadido, modificado, eliminado, renombrado) y el tamaño del cambio.
2. **Entiende la intención.** Lee los mensajes de los commits y, en un pull request, su título y descripción. Si la intención no está clara, dedúcela de los cambios y deja tu suposición escrita en el informe.
3. **Lee las convenciones del proyecto:** la configuración de linters y formateadores, `.editorconfig`, `AGENTS.md`, `CONTRIBUTING.md`, la documentación de arquitectura y cómo está escrito el código parecido en el resto del proyecto.
4. **Lee completos los archivos cambiados**, no solo el diff, y el código que llama a las partes cambiadas o al que estas llaman, cuando importe para la revisión.
5. **Ignora los archivos generados y de terceros** (archivos lock, resultados de compilación, código generado, archivos minificados, código de terceros). Menciónalos en el informe como no revisados.

Si el cambio es muy grande, revisa a fondo los archivos más importantes (lógica de negocio, interfaces públicas, código sensible para la seguridad) e indica en el informe qué recibió una revisión más ligera.

## 3. Revisar

Recorre los cambios con `references/checklist.md`, en su orden de prioridad:

1. Diseño y estructura
2. Clean code
3. Errores y lógica
4. Manejo de errores
5. Seguridad
6. Pruebas
7. Rendimiento

Clasifica cada hallazgo con la escala de severidad de la checklist (🔴 Crítico, 🟠 Importante, 🟡 Menor, 💡 Sugerencia). Si el proyecto tiene reglas propias (en `AGENTS.md`, `CONTRIBUTING.md` o la configuración del linter), incumplirlas también es un hallazgo.

Anota también, brevemente, lo que está bien hecho. Le dice al autor qué debe seguir haciendo.

## 4. Verificar los hallazgos

Antes de escribir el informe, repasa cada hallazgo:

- **¿Es real?** Vuelve a leer el código de alrededor. Comprueba que el caso que describes puede ocurrir de verdad (por ejemplo, que un valor realmente puede ser nulo ahí) y que no está ya resuelto en otro sitio.
- **¿Encaja con el proyecto?** Comprueba que la solución propuesta sigue las convenciones del proyecto y funciona con su versión del lenguaje y sus dependencias.
- **¿La severidad es correcta?** No la infles. Un problema de nombres no es Importante.
- **¿Está en el cambio?** Descarta los hallazgos sobre código que el cambio no tocó ni afecta.

Descarta lo que no se sostenga. Deja los dudosos solo como preguntas ("¿Puede `user` ser nulo aquí? Si es así, ...").

## 5. Escribir el informe

Usa `references/report-template.md`.

**Ubicación:** `.reviews/<rama>/review-<n>.md` en la raíz del repositorio.

- `<rama>` es el nombre de la rama con `/` cambiado por `-` (`feat/login` → `feat-login`). Para un pull request revisado sin tener su rama activa, usa `pr-<número>`. Con un HEAD desacoplado, usa `commit-<sha corto>`.
- `<n>` es el siguiente número de ronda: `1` para la primera revisión de esa rama, `2` para la siguiente, y así sucesivamente.
- La cabecera del informe registra la fecha, la rama, la base, el commit revisado y si se incluyeron cambios sin commit.

**Mantén los informes fuera de git.** Los informes son archivos de trabajo personales. La primera vez, comprueba si `.reviews/` está ignorada (`git check-ignore -q .reviews/`). Si no lo está, añade `.reviews/` a `.git/info/exclude`: ese archivo es local a la copia del usuario, así que el `.gitignore` del proyecto no se toca. Díselo al usuario.

**IDs de los hallazgos.** Numera los hallazgos `F1`, `F2`, ... por orden de severidad. Los IDs empiezan de nuevo en cada ronda; las rondas posteriores se refieren a los hallazgos anteriores con el número de ronda delante (`R1-F3` es el hallazgo F3 de la ronda 1).

Cuando el informe esté escrito, dale al usuario un resumen corto en la conversación: el veredicto, el número de hallazgos por severidad, los más importantes y la ruta del informe. No pegues el informe completo.

## 6. Corregir (con aprobación)

Después del resumen, ofrece aplicar las correcciones. Pregunta cuáles: todas, por severidad (por ejemplo, "las Críticas y las Importantes") o por ID ("F1, F3 y F4"). Si el usuario no quiere ninguna, termina aquí.

Cuando el usuario apruebe:

- Aplica solo los hallazgos aprobados, siguiendo la solución propuesta en el informe. Si una corrección resulta necesitar otro enfoque, explícalo antes de aplicarlo.
- No hagas otros cambios de paso.
- No hagas commit. El usuario decide cuándo hacerlo.
- Al terminar, lista lo que cambiaste por cada hallazgo y sugiere hacer una nueva ronda de revisión.

## 7. Volver a revisar

Cuando el usuario pida revisar de nuevo (por ejemplo, "revisa otra vez", "comprueba si quedó corregido") y ya exista un informe para la rama:

1. **Lee el informe anterior** (`review-<n-1>.md`): sus hallazgos y el commit que revisó.
2. **Revisa de nuevo el mismo alcance** del paso 1, con el estado actual del código.
3. **Comprueba cada hallazgo anterior** y márcalo:
   - ✅ **Corregido:** el problema desapareció y la corrección no introduce ningún problema nuevo.
   - 🔄 **Corregido en parte:** mejoró, pero queda algo. Di qué.
   - ❌ **Sigue abierto:** sin cambios.
   - ➖ **Ya no aplica:** el código se eliminó o se reescribió, así que el hallazgo ya no aplica.
4. **Revisa lo nuevo:** los cambios desde el commit de la ronda anterior y las propias correcciones. Reporta los hallazgos nuevos con IDs nuevos; marca los que vienen de una corrección.
5. **Escribe `review-<n>.md`** con el apartado "Hallazgos anteriores" completo, y resume el avance al usuario (por ejemplo, "4 de 6 corregidos, 1 Menor nuevo").

El ciclo de corregir y volver a revisar se puede repetir las veces que haga falta. Los informes anteriores nunca se editan; cada ronda es un archivo nuevo.
