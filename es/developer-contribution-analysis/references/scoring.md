# Calificación

Cómo calificar el aporte de una persona en un repositorio. Seis dimensiones de 1 a 5, con anclas concretas, pesos según el rol, una nota de 0 a 100, un nivel y una confianza.

## Datos de referencia del equipo

Varias dimensiones comparan a la persona con el equipo. El script calcula estas referencias y las deja en la sección "Scoring inputs" de `summary.md`:

- **Personas activas:** autores con al menos 5 commits en el periodo, sin contar a la persona analizada ni a las cuentas de servicio o bots (`svc…`, `bot`, `jenkins`, `azure-pipelines`, `dependabot`…). Revisa la lista: si el script tomó por persona una cuenta de servicio, o al revés, recalcula la mediana con la tabla D de los anexos.
- **Mediana del equipo:** la mediana de una métrica entre las personas activas. Si hay menos de 2, no hay comparación: califica con las anclas absolutas y dilo.

El trabajo propio se mide igual para todas las personas: líneas en las categorías propias del rol, con menos del 50 % de copia y sin aspecto de plantilla. Con `--no-team-copy`, la copia solo se detecta para la persona analizada; en ese caso, las cifras del equipo incluyen sus plantillas y copias, y la comparación favorece a la persona. Dilo en el informe.

## Dimensiones

### D1. Volumen de trabajo propio

Cuánto trabajo propio produjo, sin contar plantillas, copias, basura ni archivos estándar. Qué cuenta como propio depende del rol (`references/classification.md`).

**Métrica:** líneas vigentes de trabajo propio de la persona frente a la mediana del equipo, medida igual (`d1` en `summary.md`, con la nota sugerida). Si en la revisión commit por commit corregiste qué es propio, recalcula con tus cifras.

| Nota | Ancla |
|---|---|
| 5 | ≥ 100% de la mediana del equipo |
| 4 | Del 60% al 99% |
| 3 | Del 30% al 59% |
| 2 | Del 10% al 29% |
| 1 | < 10%, o sin trabajo propio vigente |

### D2. Complejidad y valor

Qué tan difícil y qué tan importante para el producto es lo que hizo. Se califica con la revisión commit por commit.

| Nota | Ancla |
|---|---|
| 5 | Funcionalidades de negocio completas, integraciones difíciles, diseño de componentes o decisiones técnicas que otros usan |
| 4 | Funcionalidades con lógica propia y alcance claro |
| 3 | Funcionalidades pequeñas, cableado de integraciones, correcciones con análisis |
| 2 | Configuración, subidas de versión, ajustes de manifiestos, correcciones de una línea |
| 1 | Nada más allá de plantillas, copias o cambios sin contenido |

### D3. Calidad

Qué tan correcto y limpio es lo que entregó. Usa la lista de problemas de `references/classification.md`.

| Nota | Ancla |
|---|---|
| 5 | Sin defectos encontrados, commits limpios, pruebas reales, nada que otros tuvieran que corregir |
| 4 | Problemas menores (estilo, mensajes de commit pobres, algo de código comentado) |
| 3 | Algún defecto real que la misma persona corrigió, o varios problemas menores |
| 2 | Defectos que otras personas tuvieron que corregir, archivos basura en git, ensayo y error en PRs, configuración contradictoria |
| 1 | Defectos graves (seguridad, pérdida de datos, comportamiento roto en producción), secretos en git, o defectos repetidos en la mayoría de su código propio |

### D4. Durabilidad

Cuánto de su trabajo propio sigue en pie y si otros tuvieron que rehacerlo.

**Métrica:** trabajo propio vigente / trabajo propio agregado (`d4` en `summary.md`, con la mediana del equipo y la nota sugerida), y el destino de su código (`references/classification.md`).

| Nota | Ancla |
|---|---|
| 5 | ≥ 70% vigente y sin reescrituras por defectos |
| 4 | Del 50% al 69%, o reescrito solo por cambios de requisitos o refactors generales |
| 3 | Del 30% al 49% |
| 2 | Del 10% al 29%, o la mayor parte reescrita o borrada por otras personas por defectos |
| 1 | < 10% vigente |

Un repositorio con mucho cambio de requisitos tiene poca durabilidad para todos. Si el equipo también tiene una durabilidad baja, dilo y sube una nota como máximo.

### D5. Pruebas

Si escribió pruebas que verifican el comportamiento de su código.

| Nota | Ancla |
|---|---|
| 5 | Pruebas con aserciones reales que cubren la lógica que escribió, incluidos los casos de error |
| 4 | Pruebas reales para la mayor parte de su lógica |
| 3 | Algunas pruebas reales, con huecos importantes |
| 2 | Pruebas mínimas o que verifican muy poco |
| 1 | Sin pruebas, o solo pruebas de plantilla |

**No aplica** si la persona no escribió lógica que se pueda probar (por ejemplo, un perfil de DevOps sin scripts con lógica). En ese caso, reparte su peso entre las demás dimensiones de forma proporcional y dilo.

### D6. Constancia

Si aportó de forma sostenida durante el tiempo en que debía hacerlo.

**Métrica:** semanas con al menos un commit, frente a las semanas del periodo en que el repositorio tuvo actividad mientras la persona estaba asignada (por defecto, desde su primer commit hasta el último commit del repositorio en el periodo). Está en `d6` en `summary.md`, con los días sin commits al final y la nota sugerida, que ya aplica el tope de abajo.

| Nota | Ancla |
|---|---|
| 5 | ≥ 80% de las semanas |
| 4 | Del 60% al 79% |
| 3 | Del 40% al 59% |
| 2 | Del 20% al 39% |
| 1 | < 20% |

Si lleva más de 4 semanas sin commits mientras el repositorio sigue activo, la nota máxima es 2, salvo que el usuario confirme que la persona estaba asignada a otra cosa (vacaciones, otro proyecto, baja). En ese caso, recalcula con el periodo real de asignación.

## Pesos según el rol

| Dimensión | Desarrollador | DevOps o plataforma | QA o automatización | Líder técnico |
|---|---|---|---|---|
| D1 Volumen de trabajo propio | 25 | 25 | 25 | 15 |
| D2 Complejidad y valor | 20 | 25 | 20 | 30 |
| D3 Calidad | 20 | 25 | 20 | 25 |
| D4 Durabilidad | 15 | 15 | 15 | 15 |
| D5 Pruebas | 10 | 0 | 10 | 5 |
| D6 Constancia | 10 | 10 | 10 | 10 |

Practicante o junior: usa los pesos de desarrollador. Puedes comentar en el informe qué se espera del nivel, pero no cambies las notas.

Para un líder técnico, las revisiones de PR y las decisiones de diseño pesan mucho y casi nunca están en git. Consulta las revisiones con `--platform`; si no pudiste, la confianza es Baja.

## Nota final

```text
nota = Σ peso_i × (nota_i − 1) / 4
```

El resultado va de 0 a 100. Redondéalo a un entero. Escribe la tabla con cada dimensión, su peso, su nota, su aporte a la nota final y la evidencia.

| Nota | Nivel |
|---|---|
| 85 – 100 | **Sobresaliente**: aporte propio alto, de calidad y sostenido |
| 70 – 84 | **Sólido**: aporte propio claro, con problemas menores |
| 50 – 69 | **Aceptable con brechas**: aporta, pero con huecos importantes en volumen, calidad o constancia |
| 30 – 49 | **Bajo**: poco trabajo propio o con problemas serios |
| 0 – 29 | **Muy bajo**: casi sin trabajo propio vigente, o con defectos graves |

## Confianza

| Confianza | Cuándo |
|---|---|
| **Alta** | Todas sus identidades confirmadas, periodo completo, revisiones de PR consultadas o irrelevantes para el rol, y nada importante fuera de git |
| **Media** | Faltan datos de fuera de git (revisiones de PR, tareas asignadas) que podrían cambiar una nota en un punto |
| **Baja** | Faltan datos que pueden cambiar la conclusión: rol de líder sin revisiones, trabajo conocido en otros repositorios, periodo corto (menos de 4 semanas) o identidades dudosas |

Di siempre qué subiría la confianza.

## Reglas

- Cada nota cita sus métricas o sus commits. "D3 = 2: el único código propio (`a1b2c3d4`) dejó un timeout fijo de 1500 s, y otro compañero lo reescribió completo" es una justificación; "D3 = 2: calidad mejorable" no lo es.
- No promedies a ojo. Calcula la nota con la fórmula.
- Si la rúbrica no encaja con un caso (por ejemplo, un repositorio de solo documentación), dilo y explica cómo lo calificaste.
- La nota describe el aporte en este repositorio y en este periodo, no el valor de la persona como profesional. Escríbelo así en el informe.
