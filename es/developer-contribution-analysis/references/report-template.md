# Plantilla del informe

Estructura del informe de aporte. El informe es el único entregable: un solo archivo Markdown, autocontenido, con todo el análisis y todos los datos. Escríbelo en el idioma del usuario. Omite los apartados sin contenido, salvo el veredicto, las cifras, la calificación y lo que el análisis no ve.

## Reglas

- **El veredicto va primero:** la persona que lee debe tener la conclusión en las primeras líneas.
- **Cada cifra se puede rastrear** hasta los anexos del informe o un comando de git.
- **Autocontenido:** los anexos son el contenido de `annex.md` tal cual, en el idioma del informe. Nada remite a archivos que no se entregan.
- **Cada hallazgo tiene evidencia:** `sha` del commit, `ruta` o `ruta:línea`, número de PR.
- **Las gráficas salen de `charts.md`** o de valores de `data.json`. Pon cada gráfica en Mermaid y, debajo, la versión en barras de texto, que se ve en cualquier visor.
- **Lenguaje directo y sin adjetivos sobre la persona.** "Copió", "no hay pruebas", "lo reescribió otra persona", "0 commits en 6 semanas". Nada de "lamentablemente", "parece que", "podría mejorar" ni "es flojo".
- **Lo que sí aportó** se escribe con el mismo detalle que los problemas.
- **Agrupa lo repetido:** el mismo cambio en tres servicios va en una línea con las tres ubicaciones.
- **Nunca copies el valor de un secreto.**

## Leyenda de clases

🟥 Plantilla, generado o copia · 🟧 Adaptación o ajuste de configuración · 🟦 Infraestructura propia · 🟩 Código propio · 🟨 Código propio con problemas · ⬛ Basura o accidental · ⬜ Sin contenido

## Plantilla

````markdown
# Aporte de <nombre> en <repositorio>

| | |
|---|---|
| **Persona** | <nombre> |
| **Identidades en git** | <nombre <correo>>, <alias <correo>> |
| **Repositorio** | <nombre> · rama `<rama>` (`<sha>`) |
| **Periodo analizado** | <AAAA-MM-DD> → <AAAA-MM-DD> |
| **Rol considerado** | <Desarrollador | DevOps | QA | Líder técnico | Practicante> |
| **Fecha del análisis** | <AAAA-MM-DD> |
| **Supuestos** | <respuestas por defecto que se usaron, o "Ninguno"> |

---

## 0. Veredicto

| Nota | Nivel | Confianza |
|---|---|---|
| **<0–100> / 100** | <nivel> | <Alta | Media | Baja> |

<Párrafo 1: qué hizo de verdad en código. Cifras clave: cuánto es propio, cuánto es plantilla o copia, qué sigue vigente y qué le pasó a su código.>

<Párrafo 2: qué otro trabajo sí aportó (configuración, infraestructura, coordinación…), su calidad, su constancia y la conclusión en una frase, sin maquillaje.>

**Hechos clave**

| # | Hecho | Evidencia |
|---|---|---|
| 1 | <hecho con cifra> | <commit, archivo, PR o métrica> |

---

## Cambios desde el informe anterior

<Solo si hay un informe anterior de la misma persona. Compara con su marca `<!-- developer-contribution-analysis: … -->`.>

| | Informe anterior (<fecha>, `<sha>`) | Ahora | Cambio |
|---|---|---|---|
| Nota | <n> | <n> | <±n> |
| Commits | <n> | <n> | <±n> |
| Trabajo propio agregado | <n> | <n> | <±n> |
| Trabajo propio vigente | <n> | <n> | <±n> |
| Semanas con commits | <n> | <n> | <±n> |

<Hallazgos nuevos y hallazgos que ya se resolvieron, con evidencia.>

---

## 1. Cifras

| Métrica | Valor |
|---|---|
| Periodo activo | <primer commit> → <último commit> |
| Commits sin merges | <n> |
| PRs con sus commits / completados por la persona | <n> / <n> |
| Líneas agregadas / eliminadas | +<n> / −<n> |
| Líneas de trabajo propio agregadas (sin plantillas, copias ni basura) | <n> (<%> del total) |
| PRs propios en la plataforma / PRs de otros que revisó | <n> / <n>, o "no consultado" |
| Líneas suyas vigentes hoy | <n> de <total del repositorio> (<%>) |
| De esas, trabajo propio | <n> |
| Semanas con commits / semanas del periodo | <n> / <n> |
| Días desde su último commit hasta el último del repositorio | <n> |

---

## 2. Composición del aporte

<Gráfica: líneas agregadas por categoría (charts.md).>

<Gráfica: copia de archivos existentes frente a líneas nuevas en el repositorio (charts.md).>

| Clase | Líneas agregadas | % | Commits |
|---|---|---|---|
| 🟥 Plantilla, generado o copia | <n> | <%> | `<sha>`, … |
| 🟧 Ajustes de configuración | <n> | <%> | <n> commits |
| 🟦 Infraestructura propia | <n> | <%> | … |
| 🟩 Código propio | <n> | <%> | … |
| 🟨 Código propio con problemas | <n> | <%> | … |
| ⬛ Basura o accidental | <n> | <%> | … |
| **Total** | <n> | 100% | <n> |

---

## 3. Comparación con el equipo

<Gráficas: commits, líneas vigentes y trabajo propio vigente por autor (charts.md).>

| Autor | Commits | Líneas vigentes | Trabajo propio agregado | Trabajo propio vigente | Durabilidad |
|---|---|---|---|---|---|
| **<persona>** | … | … | … | … | … |
| <otro autor> | … | … | … | … | … |

<Una o dos frases: qué muestra la comparación. El trabajo propio se mide igual para todos; las líneas vigentes incluyen plantillas y copias.>

---

## 4. Actividad en el tiempo

<Gráfica y tabla de commits por semana (charts.md).>

<Lectura: en qué semanas se concentró su actividad, huecos largos y cómo se compara con la actividad del equipo.>

---

## 5. Qué pasó con su código

| Commit | Líneas agregadas | Vigentes hoy | Qué son |
|---|---|---|---|
| `<sha>` | <n> | <n> | <descripción> |

| Archivo o parte | Destino | Quién y cuándo | Motivo según el commit |
|---|---|---|---|
| `<ruta>` | <Vigente | Modificado | Reescrito | Borrado> | <autor, `sha`, fecha> | <motivo> |

---

## 6. Análisis commit por commit

### 6.<n> `<sha>` · <AAAA-MM-DD> · "<asunto>" · <clase>

**+<n> / −<n> · <n> archivos · <componente>**

- <Qué hizo, en concreto.>
- <Origen: "92% igual a `<ruta>` de <autor> (`<sha>`, <fecha>)", o "nuevo en el repositorio".>
- <Problemas encontrados, con `ruta:línea`.>
- <Destino: cuántas líneas quedan hoy y quién cambió el resto.>

<Si hay más de 40 commits: un apartado para cada commit importante y una tabla con el resto agrupado por clase.>

---

## 7. Hallazgos de calidad

| # | Hallazgo | Gravedad | Evidencia | ¿Quién lo corrigió? |
|---|---|---|---|---|
| 1 | <qué> | <Alta | Media | Baja> | `<sha>` `<ruta:línea>` | <autor, `sha`> o "Sigue igual" |

---

## 8. Lo que sí aportó

- <Aporte concreto, con evidencia.>

---

## 9. Calificación

| Dimensión | Peso | Nota (1–5) | Aporte | Evidencia |
|---|---|---|---|---|
| D1 Volumen de trabajo propio | <p> | <n> | <p × (n − 1) / 4> | <métrica frente a la mediana del equipo> |
| D2 Complejidad y valor | <p> | <n> | … | … |
| D3 Calidad | <p> | <n> | … | … |
| D4 Durabilidad | <p> | <n> | … | … |
| D5 Pruebas | <p> | <n | No aplica> | … | … |
| D6 Constancia | <p> | <n> | … | … |
| **Total** | 100 | | **<nota>** | **<nivel>** |

**Confianza: <Alta | Media | Baja>.** <Por qué y qué la subiría.>

> La nota describe el aporte en este repositorio y en este periodo, no el valor de la persona como profesional.

---

## 10. Lo que este análisis no ve

- <Revisiones y comentarios de PR: consultados con <herramienta>, o no consultados y cómo obtenerlos.>
- <Trabajo en otros repositorios, tareas asignadas, soporte, diseño, documentación fuera del repositorio.>
- <Limitaciones del método: periodo, ramas, identidades, archivos excluidos, detección de copia solo dentro de este repositorio.>

---

## Anexos

<El contenido de `annex.md` tal cual, con la columna "Revisión" del anexo F completada (Confirmado o Falso positivo, con el motivo) y la marca `<!-- developer-contribution-analysis: … -->` al final. Trae estas secciones:>

- A. Todos los commits
- B. Archivos por commit y su origen
- C. Destino de los archivos que tocó
- D. Equipo
- E. Pull requests (y, si se consultó, los PRs de la plataforma)
- F. Señales del script
- G. Líneas vigentes por archivo
- H. Cómo reproducir
````
