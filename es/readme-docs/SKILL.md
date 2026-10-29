---
name: readme-docs
description: Crea o actualiza el README.md de un proyecto de software (backend, frontend, móvil, librería, CLI o cualquier otro) siguiendo un estándar de documentación con apartados obligatorios, condicionales y opcionales. Úsala cuando el usuario pida documentar un proyecto, crear o mejorar el README, o actualizar la documentación después de hacer cambios en el código.
---

# readme-docs

Genera y mantiene el `README.md` de un proyecto siguiendo el estándar de `references/standard.md`. Sirve para cualquier tecnología y lenguaje.

Tiene dos modos:

- **Crear:** el proyecto no tiene README o tiene uno mínimo (solo el título o el texto que genera una plantilla). Se escribe completo.
- **Actualizar:** ya existe un README con contenido real. Solo se modifican los apartados afectados por los cambios del código.

Si el usuario indica el modo (`/readme-docs crear` o `/readme-docs actualizar`), úsalo. Si no, elige según el estado del README.

## Principios

- **Todo sale del proyecto.** Cada dato del README tiene que poder rastrearse a un archivo, comando o respuesta del usuario. Nunca inventes versiones, comandos, endpoints, responsables ni reglas de negocio.
- **Lo que el código no dice, se pregunta.** Hay datos que solo conoce el equipo (estado del proyecto, responsables, el porqué de una decisión). Reúnelos y pregúntalos todos juntos en un solo mensaje. Lo que quede sin respuesta se marca como pendiente (ver más abajo), nunca se rellena con una suposición.
- **Proporcional al proyecto.** Una librería pequeña no necesita los ocho bloques del estándar. Incluye los `[M]`, los `[C]` que apliquen y solo los `[O]` que aporten algo real.
- **El README es la puerta de entrada.** El contenido extenso (referencia completa de una API, modelo de datos detallado, procedimientos operativos largos) va en archivos dentro de `docs/` y se enlaza desde el README (ver "Archivos de `docs/`"). Si existe una fuente de verdad (OpenAPI, esquema de base de datos, CHANGELOG), enlázala en vez de copiarla.
- **Nunca secretos.** No copies valores de `.env`, credenciales, tokens ni URLs internas con credenciales. Documenta el nombre de la variable, para qué sirve y un valor de ejemplo ficticio.
- **Fácil de leer.** Lenguaje sencillo en los apartados para cualquier lector y técnico donde el apartado lo requiere, Markdown limpio y diagramas Mermaid claros y con color cuando ayude. Sigue `references/style.md` en todo lo que escribas.
- **Respeta el idioma del README.** Si ya existe, mantén su idioma. Si es nuevo, usa el idioma en el que te habla el usuario, salvo que pida otro.

## Modo crear

1. **Analiza el proyecto.** Recorre la estructura de carpetas, los manifiestos de dependencias, los scripts, la configuración, Docker o infraestructura, CI, las pruebas y los puntos de entrada. Usa `references/evidence-map.md` para saber qué apartados activa cada evidencia.
2. **Decide qué apartados aplican.** Recorre `references/standard.md`:
   - `[M]`: siempre se incluyen.
   - `[C]`: se incluyen si encontraste evidencia de que aplican.
   - `[O]`: se incluyen solo si aportan valor para este proyecto (por ejemplo, un diagrama Mermaid cuando hay varios servicios, o una tabla de contenido cuando el README es largo).
   - Los apartados que no aplican se omiten, sin poner "No aplica".
3. **Pregunta lo que falta.** Junta en un solo mensaje todas las preguntas sobre los datos que no pudiste deducir. Ofrece una propuesta cuando la tengas (por ejemplo: "Estado: ¿activo?"). Si el usuario no responde algo, sigue y márcalo como pendiente.
4. **Escribe el README.** Sigue el orden de los bloques del estándar, pero usa títulos naturales y agrupa apartados pequeños. El estándar define qué se documenta, no obliga a tener un título por cada punto. Aplica `references/style.md` para la redacción, el formato y los diagramas.
5. **Verifica.**
   - Comprueba que cada comando documentado existe (en `package.json`, `Makefile`, scripts, etc.), que las rutas y archivos mencionados existen y que los enlaces internos funcionan. No ejecutes comandos que instalen dependencias, desplieguen o modifiquen datos.
   - Revisa el Markdown y los diagramas con la lista de `references/style.md`. Si `markdownlint` o `mmdc` ya están instalados en el proyecto o en el sistema, úsalos; no los instales sin preguntar.
6. **Añade la marca de sincronización** al final del README (ver más abajo).
7. **Informa** al usuario de lo que creaste: los apartados incluidos, los archivos de `docs/` generados y la lista de pendientes.

## Modo actualizar

1. **Detecta qué cambió.**
   - Busca la marca de sincronización al final del README. Si existe y el proyecto usa git, revisa `git diff <commit>..HEAD` más los cambios sin confirmar (`git diff HEAD`) y los archivos nuevos sin seguimiento.
   - Si no hay marca, pregunta al usuario desde cuándo revisar (un commit, una rama base o una fecha). Si no lo sabe, compara el README entero con el estado actual del proyecto.
   - Si el usuario te dice qué cambió, empieza por ahí, pero confírmalo con el código.
   - Ignora los cambios en el propio README y en los archivos de `docs/`: son el resultado de la documentación, no la causa.
2. **Relaciona cambios con apartados.** Usa `references/evidence-map.md` para saber qué apartados afecta cada archivo modificado. Un cambio puede activar un apartado `[C]` que antes no aplicaba (por ejemplo, se añadió una cola de mensajes) o dejar obsoleto uno existente. Un apartado puede estar en el README, en un archivo de `docs/` o en ambos (resumen en el README y detalle en `docs/`); revisa los dos lugares.
3. **Edita solo lo afectado.** Modifica únicamente los apartados afectados, tanto en el README como en los archivos de `docs/` que mantiene la skill. Si cambias el detalle en `docs/`, comprueba que el resumen del README siga siendo correcto, y al revés. No reescribas ni cambies el estilo del resto. El texto escrito por personas se conserva tal cual, salvo que contradiga el código actual; en ese caso, corrígelo y menciónalo en el informe. Si un cambio afecta a lo que muestra un diagrama (un servicio nuevo, una relación que ya no existe), actualiza también el diagrama. Lo que escribas nuevo sigue `references/style.md`, aunque el resto del README tenga otro estilo.
4. **No borres sin avisar.** Si un apartado completo parece obsoleto (por ejemplo, documenta un servicio que ya no existe), propón eliminarlo y espera confirmación.
5. **Revisa los `[M]`.** Si al README le falta algún apartado obligatorio, añádelo aunque no esté relacionado con los cambios.
6. **Verifica, actualiza la marca e informa**, igual que en los pasos 5 a 7 del modo crear. En el informe, lista los apartados modificados y el cambio de código que motivó cada modificación.

## Pendientes

Cuando falta un dato que solo el equipo conoce, deja un marcador visible en su lugar:

```markdown
> **Pendiente:** indicar el equipo responsable y el canal de soporte.
```

En el modo actualizar, revisa los pendientes existentes, en el README y en `docs/`, y resuelve los que ya puedas completar.

## Archivos de `docs/`

Cuando un apartado ocupa más de una pantalla, muévelo a un archivo dentro de `docs/` y deja en el README un resumen corto con el enlace. Usa estos nombres:

| Archivo | Contenido |
|---|---|
| `docs/architecture.md` | Arquitectura, componentes y módulos, diagramas, decisiones arquitectónicas |
| `docs/api.md` | Endpoints, contratos de integración, autenticación, mensajería, ejemplos de consumo |
| `docs/data-model.md` | Entidades, relaciones, base de datos y migraciones |
| `docs/configuration.md` | Variables de entorno, configuración por ambientes |
| `docs/deployment.md` | Despliegue, infraestructura, CI/CD |
| `docs/operations.md` | Logs y observabilidad, monitoreo, procedimientos operativos, solución de problemas |
| `docs/development.md` | Estrategia de pruebas, estándares de código, contribución, depuración |

Crea solo los archivos que hagan falta. Cada archivo:

- Empieza con un título `#` y un enlace de vuelta al README.
- Sigue `references/style.md`.
- Termina con la marca de sincronización. La marca indica que el archivo lo mantiene la skill.

Los archivos de `docs/` sin marca los escribieron personas. Enlázalos desde el README, pero no los modifiques. Si contradicen el código, avísalo en el informe. Si uno de ellos cubre lo mismo que un archivo de la tabla, pregunta al usuario si la skill puede mantenerlo; si acepta, añade la marca y úsalo en lugar de crear uno nuevo.

## Marca de sincronización

Al terminar, deja (o reemplaza) esta línea como última línea del README y de cada archivo de `docs/` que hayas creado o modificado:

```markdown
<!-- readme-docs:sync commit=<sha corto de HEAD> date=<AAAA-MM-DD> -->
```

Si el proyecto no usa git, omite `commit=` y deja solo la fecha. La marca no se ve al renderizar el Markdown. La del README le dice a la próxima actualización desde dónde revisar cambios; la de los archivos de `docs/` indica cuáles mantiene la skill.

## Monorepos

Si el repositorio contiene varios paquetes o servicios, el README raíz da la visión general (propósito, arquitectura, cómo levantar el conjunto) y enlaza al README de cada paquete. Cada README de paquete sigue el mismo estándar, con su propia marca de sincronización. Pregunta al usuario si quiere documentar todos los paquetes o solo algunos.
