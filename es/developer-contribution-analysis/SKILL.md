---
name: developer-contribution-analysis
description: Hace una radiografía del aporte real de un desarrollador a un repositorio git, con datos reales del historial y sin maquillaje. Calcula commits, PRs, líneas agregadas y vigentes (blame de todo el repositorio), separa lo que es código propio de lo que es plantilla, archivo generado, copia de otros archivos del repositorio, ajuste de configuración o basura, revisa commit por commit la calidad de lo que hizo, sigue qué pasó con su código (si sobrevive o si otros lo borraron o reescribieron), lo compara con el resto del equipo y lo califica de 0 a 100 con una rúbrica. Entrega un único Markdown completo y bien estructurado, con gráficas, hallazgos con evidencia, lo que sí aportó y lo que el análisis no ve. No modifica el repositorio. Úsala cuando el usuario quiera saber qué hizo de verdad una persona en un repositorio, evaluar o dar seguimiento a su aporte o hacer un "blame" de un desarrollador.
---

# developer-contribution-analysis

Analiza qué hizo de verdad una persona en un repositorio: cuánto, qué parte es suya, qué parte es plantilla o copia, qué calidad tiene, qué sobrevivió y cómo se compara con el resto del equipo. El resultado es **un único archivo Markdown**, completo y autocontenido, con datos reales, gráficas, una calificación y la evidencia de cada afirmación.

El objetivo no es el número de líneas, que es fácil de inflar con plantillas y copias, sino una imagen honesta del aporte: lo que la persona construyó, lo que dejó a otros y lo que el repositorio no permite ver.

El flujo tiene siete pasos:

1. **Identificar** a la persona y el alcance.
2. **Recolectar** los datos con el script.
3. **Revisar** commit por commit.
4. **Buscar** lo que git no muestra.
5. **Calificar** con la rúbrica.
6. **Escribir** el informe.
7. **Guardar** y entregar.

## Principios

- **Solo datos reales.** Cada cifra del informe sale del script o de un comando git que se pueda citar. No estimes, no redondees a favor ni en contra y no inventes valores para una gráfica. Si un dato no existe o no se pudo calcular, dilo.
- **Sin maquillaje.** Di lo que muestran los datos con palabras claras. Un aporte bajo se llama bajo, y uno alto se llama alto. No suavices ni exageres. "Hoy no queda ninguna línea de lógica suya en el repositorio" es claro; "su aporte tuvo un enfoque más operativo" maquilla.
- **Hechos sobre el trabajo, no juicios sobre la persona.** Describe lo que hizo y lo que no está: "0 commits entre el 21 de septiembre y el 11 de octubre", no "es flojo". Sin adjetivos sobre su carácter, intención o capacidad.
- **Justo.** Reconoce todo lo que sí aportó, por pequeño que sea. Separa la ausencia de evidencia en git (revisiones, diseño, soporte, otros repositorios) de la evidencia de ausencia. Ten en cuenta el rol: el trabajo de infraestructura de alguien de DevOps no es "solo configuración".
- **Evidencia citable.** Cada hallazgo apunta a un commit (`sha`), un archivo (`ruta:línea`) o un PR. Una afirmación sin evidencia no entra en el informe.
- **Confirma antes de afirmar.** El script da indicios (porcentaje de copia, marcadores de plantilla, posibles secretos). Antes de escribir "copiado de" o "error", confírmalo leyendo el diff.
- **Solo lectura.** Nunca modifiques el repositorio: ni commits, ni ramas, ni configuración. Solo lees y ejecutas comandos que no cambian nada.
- **Datos personales.** El análisis evalúa a una persona. Guárdalo fuera de git, no lo envíes a servicios externos y no copies valores de secretos: solo su ubicación.
- **El idioma del usuario.** Escribe el informe en el idioma en el que te habla el usuario.

## 1. Identificar a la persona y el alcance

1. **Busca sus identidades.** Una persona suele aparecer con varios nombres y correos (`jperez`, `Juan Pérez`, un correo personal). Lista los autores del repositorio:

   ```bash
   python3 -I <carpeta-de-la-skill>/scripts/collect_contribution.py --repo <repo> --list-authors
   ```

   La lista marca las posibles cuentas de servicio y propone, al final, las identidades que parecen ser de la misma persona (mismo nombre o mismo usuario con distinto correo), ya en formato mailmap. Marca las que son de la persona analizada.
2. **Pregunta, en un solo mensaje y con una respuesta por defecto para cada punto**, lo que no esté claro en la petición:
   - **Identidades:** las que encontraste para la persona. ¿Son todas suyas? ¿Falta alguna?
   - **Repositorio y rama:** por defecto, el repositorio actual y su rama principal (`origin/HEAD` si existe; si no, `HEAD`).
   - **Periodo:** por defecto, toda la historia. Si la persona entró o salió del proyecto en fechas concretas, usa esas fechas.
   - **Rol esperado:** desarrollador (por defecto), DevOps o plataforma, QA o automatización, líder técnico, o practicante. El rol cambia qué cuenta como trabajo propio y los pesos de la calificación (`references/scoring.md`).
   - **Plataforma:** si se consultan los PRs y las revisiones en GitHub, Azure DevOps o GitLab (solo lectura, con `gh`, `az` o `glab`). Por defecto, sí, si la CLI de la plataforma está instalada y autenticada. En GitLab hace falta el usuario de la persona; en GitHub el script lo busca a partir de sus commits.
   - **Exclusiones:** carpetas de código de terceros, generado o vendorizado que no deben contar (por ejemplo, `vendor/**` o `**/generated/**`). Los archivos marcados como `linguist-generated` o `linguist-vendored` en `.gitattributes` se excluyen solos.
   - **Dónde guardar el informe:** por defecto, `.contribution-analysis/` en la raíz del repositorio (ver paso 7).
3. Si el usuario ya dio un dato, no lo preguntes. Si no responde algo, usa la respuesta por defecto y anótala como supuesto en el informe.
4. **Identidades duplicadas del equipo.** Si la lista propone unir identidades de otras personas del equipo y la propuesta es correcta, guárdala en un mailmap temporal fuera del repositorio y pásala con `--mailmap`. Así la comparación con el equipo no cuenta a una persona como dos.

## 2. Recolectar los datos

Ejecuta el script desde la carpeta de la skill. Necesita `git` y Python 3.9 o superior, y no instala nada:

```bash
python3 -I <carpeta-de-la-skill>/scripts/collect_contribution.py \
  --repo <repo> \
  --author <correo> --author "<nombre o alias>" \
  --role <developer|devops|qa|lead|intern> --lang es \
  [--since AAAA-MM-DD] [--until AAAA-MM-DD] [--ref <rama>] \
  [--platform auto] [--platform-user <usuario>] \
  [--exclude 'vendor/**'] [--mailmap <archivo>] \
  --out <carpeta-temporal>
```

- `--author` acepta un correo (coincidencia exacta) o un fragmento de nombre. Repítelo para cada identidad.
- `--role` decide qué categorías de archivo cuentan como trabajo propio. `--lang` es el idioma de los anexos y las gráficas: usa el del usuario.
- `--platform auto` detecta la plataforma por el remoto `origin` y consulta, en modo lectura, los PRs de la persona y los PRs de otros que revisó. Si la CLI no está o no está autenticada, el script sigue y lo deja anotado.
- `--out`: una carpeta de trabajo temporal **fuera del repositorio**, por ejemplo la que crea `mktemp -d`. Sus archivos son material de trabajo y no se entregan: todo lo que importa pasa al informe (paso 6), y la carpeta se borra al terminar (paso 7).
- Otras opciones: `--jobs` (procesos de git en paralelo), `--blame-copies` (atribuye las líneas movidas o copiadas entre archivos a su autor original; más justo, pero mucho más lento) y `--no-team-copy` (detecta copia solo para la persona; más rápido, pero la comparación con el equipo deja de ser igual para todos).

El script genera cuatro archivos de trabajo:

| Archivo | Contenido |
|---|---|
| `summary.md` | El punto de partida: totales, las métricas de la calificación con su nota sugerida, identidades duplicadas, datos de la plataforma y señales. |
| `annex.md` | Las tablas completas de datos, en el idioma elegido, listas para pegar como anexos del informe. Termina con el comando para reproducirlo y la marca para el seguimiento. |
| `charts.md` | Gráficas en Mermaid y en barras de texto, en el idioma elegido, construidas con los datos reales. |
| `data.json` | Todas las métricas, para comprobaciones. |

Qué mide el script y cómo:

- **Commits y líneas:** commits sin merges de todas las ramas y tags, con las líneas agregadas y eliminadas por archivo.
- **Categoría de cada archivo**, por su ruta: código de producción, código de pruebas, despliegue y CI, build, configuración, documentación, plantillas y datos de prueba, archivos estándar (wrappers, `.gitignore`, lockfiles) y archivos que no deberían estar en git (logs, binarios compilados, `.env`).
- **Copia, para todo el equipo:** para cada archivo de cada commit, compara las líneas agregadas con las versiones anteriores de archivos con el mismo nombre de otras personas, empezando por las rutas más parecidas. El porcentaje es la parte de las líneas significativas que ya existía igual. Para la persona analizada también da el origen y los archivos muy parecidos que otros crearon después.
- **Aspecto de plantilla:** archivos con marcadores de plantilla (`TODO`, `sample`, `my-operation`…) o pequeños y con solo tipos vacíos.
- **Trabajo propio:** líneas en las categorías propias del rol, con menos del 50 % de copia y sin aspecto de plantilla. Se mide igual para todas las personas, así que la comparación con el equipo es justa.
- **Líneas vigentes:** `git blame -w -M` de todos los archivos de texto en la rama analizada, para la persona y para todo el equipo, incluido cuánto trabajo propio sigue en pie.
- **Destino de su código:** para cada archivo que tocó, cuántas líneas suyas quedan, quién tiene el resto y, si el archivo ya no existe, quién lo borró y en qué commit.
- **PRs:** merges que contienen sus commits, separando los PRs de las sincronizaciones de rama; y, con `--platform`, sus PRs en la plataforma (con las horas hasta el merge) y los PRs de otros que revisó.
- **Métricas de la calificación:** D1 (trabajo propio vigente frente a la mediana del equipo, sin cuentas de servicio), D4 (durabilidad del trabajo propio, también la mediana del equipo) y D6 (semanas con commits y días sin commits al final), cada una con su nota sugerida según las anclas.
- **Señales para revisar:** asuntos de commit repetidos el mismo día, commits muy grandes, archivos que no deberían estar en git, marcadores de plantilla, clases o tipos vacíos, pruebas con menos aserciones que casos, posibles secretos, correcciones de un commit propio de los días anteriores y archivos propios que después aparecen casi iguales en otros sitios (posible plantilla).

**Comprueba los datos antes de usarlos:**

1. El número de commits coincide con `git log --branches --remotes --tags --no-merges --author=<correo> --oneline | wc -l` (sumando todas sus identidades).
2. Las identidades del `summary.md` son todas de la persona y no falta ninguna de las que viste en `--list-authors`.
3. Si `summary.md` propone identidades duplicadas del equipo que no unificaste, decide si hacerlo y vuelve a ejecutar.
4. Si un repositorio grande tarda demasiado, acota con `--since`, `--until` o `--exclude`, y dilo en el informe.

Si no hay Python disponible, obtén los mismos datos con git (`git log --numstat`, `git blame --line-porcelain`, `git log --merges`) y di en el informe que no se usó el script.

## 3. Revisar commit por commit

Lee `references/classification.md`. Después:

1. **Decide la profundidad.**
   - Hasta 40 commits: revísalos todos.
   - Más de 40: revisa todos los que tocan código de producción o de pruebas, todos los que aparecen en las señales y los 15 más grandes. Agrupa el resto por tipo, con el recuento y ejemplos.
2. **Lee el diff de cada commit** (`git show --stat <sha>` y `git show <sha> -- <archivo>`). Con el anexo B (copia, origen, «propia», plantilla) y el diff, clasifica el commit según `references/classification.md` y anota qué hizo en una o dos frases concretas.
3. **Confirma las copias importantes.** Para los archivos con mucho peso que el script marca como copia, compara el archivo con su origen (`git diff -w <sha-origen>:<ruta-origen> <sha>:<ruta>`). Si dos archivos parecidos tienen fechas muy próximas o el parecido es con un archivo posterior, no afirmes quién copió a quién: di que comparten origen.
4. **Distingue plantilla de copia.** Un archivo generado por una herramienta (scaffold, `init`, generadores de código) o un archivo estándar no es una copia de un compañero, aunque tampoco es trabajo propio. Llama a cada cosa por su nombre.
5. **Corrige la marca «propia» si hace falta.** El script decide por reglas. Si al leer el diff un archivo marcado como propio resulta ser plantilla, o al revés, dilo en el análisis del commit y usa tu clasificación en la calificación, explicando la diferencia. Presta atención a la señal "Propio, pero repetido casi igual después": suele aparecer cuando la persona creó el primer componente con una plantilla sin marcadores. Antes de descontarlo, confirma en el diff que es plantilla y no código suyo que otros copiaron. Los casos habituales están en `references/classification.md`.
6. **Revisa la calidad del código propio** con la lista de `references/classification.md`: errores, valores fijos, parámetros sin usar, código comentado, pruebas que no prueban nada, archivos que no deberían estar en git, configuración contradictoria, ensayo y error en PRs.
7. **Revisa cada señal del script** y decide si se confirma o es un falso positivo, con el motivo. Esa decisión va en la columna "Revisión" del anexo F.
8. **Sigue el destino de su código.** En el anexo C, mira qué partes suyas borraron o reescribieron otras personas y lee esos commits (`git log --format='%h %an %ad %s' -- <ruta>`) para entender por qué: un error, un refactor o un cambio de requisitos. No es lo mismo un código reemplazado porque estaba mal que uno reemplazado porque cambió el negocio.

## 4. Buscar lo que git no muestra

El historial no recoge todo el trabajo: revisiones de PR, comentarios, diseño, soporte, documentación en wikis, trabajo en otros repositorios, pair programming o tareas asignadas.

- **Revisiones y comentarios de PR.** Con `--platform`, el script ya los trae. Si no se pudo (sin CLI, sin autenticación o plataforma no soportada), dilo en el informe y explica cómo obtenerlos: instalar y autenticar `gh`, `az` (con la extensión `azure-devops`) o `glab`, y volver a ejecutar.
- **Coautoría.** El script cuenta los commits de otras personas con `Co-authored-by` de esta persona.
- **Contexto del usuario.** Pregunta solo si cambia la conclusión. Por ejemplo, si la persona tuvo tareas fuera del repositorio, vacaciones o una baja en el periodo, o si cambió de rol.

Todo lo que no pudiste verificar va a la sección "Lo que este análisis no ve" y baja la confianza de la calificación.

## 5. Calificar

Aplica `references/scoring.md`: seis dimensiones de 1 a 5 con anclas concretas, pesos según el rol, una nota de 0 a 100, un nivel y una confianza.

- **D1, D4 y D6** salen de las métricas de `summary.md`, que ya traen la nota sugerida según las anclas. Úsala, salvo que la revisión del paso 3 cambie el trabajo propio; en ese caso, recalcula y explica por qué.
- **D2, D3 y D5** salen de la revisión commit por commit.

Cada nota cita las métricas o los commits que la justifican. No ajustes una nota para que el resultado "se vea mejor" o "se vea peor": si la rúbrica no encaja con un caso, dilo y explica el ajuste.

## 6. Escribir el informe

Sigue `references/report-template.md`. Reglas:

- **Empieza por el veredicto:** nota, nivel, confianza y dos párrafos sin maquillaje sobre el aporte real.
- **Un solo archivo, autocontenido.** Todo va en el informe: el análisis, las gráficas de `charts.md` y, como anexos, el contenido de `annex.md` tal cual, con la columna "Revisión" de las señales completada. No dejes ningún `<por revisar>`. Quien lo lea no debe necesitar ningún otro archivo.
- **Usa las gráficas de `charts.md`.** Pega las que apliquen. Si haces otra gráfica, constrúyela solo con valores de `data.json` o de un comando que cites.
- **Cada cifra debe poder rastrearse** hasta los anexos del informe o un comando de git.
- **Incluye lo que sí aportó**, con la misma precisión que los problemas.
- **Seguimiento.** Si en la carpeta de informes ya hay uno anterior de la misma persona, lee la marca `<!-- developer-contribution-analysis: … -->` del final y añade la sección "Cambios desde el informe anterior": nota, commits, trabajo propio, líneas vigentes y hallazgos nuevos o resueltos.
- **Solo el análisis.** El informe no incluye preguntas para la persona, guiones de conversación ni recomendaciones sobre qué hacer con ella. Si el usuario pide algo así, hazlo aparte, fuera del informe.

## 7. Guardar y entregar

**El entregable es un solo archivo:** el informe. Por defecto va en la raíz del repositorio analizado:

```text
.contribution-analysis/<persona>-<AAAA-MM-DD>.md
```

`<persona>` es el nombre de la persona en kebab-case y sin tildes (`juan-perez`). Si el usuario pide otra ubicación (por ejemplo, el escritorio), úsala. Si ya existe un informe con ese nombre, pregunta si reemplazarlo o crear `<persona>-<AAAA-MM-DD>-2.md`.

**Borra la carpeta temporal del script** cuando el informe esté escrito. No dejes `data.json`, `summary.md`, `annex.md` ni `charts.md` en ningún sitio: el único archivo que queda es el informe.

**Mantén el análisis fuera de git.** Evalúa a una persona y nunca debe entrar en un commit. Si lo guardas dentro del repositorio:

1. Comprueba si la carpeta está ignorada: `git check-ignore -q .contribution-analysis/`.
2. Si no lo está, añade `.contribution-analysis/` al `.gitignore` de la raíz (créalo si no existe), en su propia línea y con el comentario `# Developer contribution analyses (developer-contribution-analysis)`. No cambies nada más del archivo.
3. Avisa al usuario de que cambiaste el `.gitignore` y de que tiene que hacer commit de ese cambio. No lo hagas tú.
4. Si `.contribution-analysis/` ya estaba en un commit, avisa al usuario y sugiere `git rm -r --cached .contribution-analysis` para dejar de seguirla sin borrar los archivos.

**Entrega.** Al terminar, di en la conversación:

- La nota, el nivel y la confianza, con el veredicto en dos o tres frases.
- La ruta del informe, relativa y absoluta.
- Cómo abrirlo: en un editor con vista previa de Markdown. Las gráficas Mermaid se ven en GitHub, GitLab, Azure DevOps Wiki y VS Code (con una extensión de Mermaid); las barras de texto se ven en cualquier visor.
- Qué quedó sin verificar y cómo completarlo, por ejemplo las revisiones de PR.

## Verificar antes de entregar

1. Las cifras del veredicto, las tablas, las gráficas y los anexos coinciden entre sí y con `data.json`.
2. Cada afirmación de copia, plantilla o error está confirmada en el diff, no solo en el porcentaje del script.
3. Cada nota de la calificación tiene su evidencia, y la nota final es la que sale de la fórmula.
4. "Lo que sí aportó" está completo y no se omitió nada a favor de la persona.
5. Las limitaciones están escritas: periodo, ramas, identidades, lo que no se pudo consultar.
6. El texto no tiene juicios sobre la persona ni palabras que suavicen o exageren los datos.
7. No hay valores de secretos en el informe.
8. El resultado es un único archivo Markdown autocontenido, y la carpeta temporal del script está borrada.
9. El anexo F no tiene ningún `<por revisar>`, y la marca `<!-- developer-contribution-analysis: … -->` sigue al final del informe.
