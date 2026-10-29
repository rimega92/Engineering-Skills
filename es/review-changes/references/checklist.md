# Checklist de revisión

Qué buscar en un cambio, por orden de prioridad, y cómo calificar cada hallazgo. Los puntos no dependen de ningún lenguaje: aplica cada uno con las convenciones del lenguaje y el framework del proyecto.

No todos los puntos aplican a todos los cambios. Úsalos como guía, no como un formulario que rellenar.

## Severidad

| Nivel | Significado | Ejemplos |
|---|---|---|
| 🔴 Crítico | Hay que corregirlo antes de integrar. Rompe el comportamiento, pierde o corrompe datos, o abre un agujero de seguridad. | Error de lógica en el flujo principal, inyección SQL, secreto en un commit, migración que borra datos |
| 🟠 Importante | Conviene corregirlo antes de integrar. Un problema real que todavía no es urgente: causará errores o hará el código difícil de cambiar. | Error sin manejar en un camino probable, lógica de negocio en la capa equivocada, lógica nueva sin pruebas, lógica duplicada que acabará divergiendo |
| 🟡 Menor | Vale la pena corregirlo, en este cambio o pronto. Legibilidad y mantenibilidad. | Nombres poco claros, función larga, número mágico, comentario engañoso |
| 💡 Sugerencia | Mejora o alternativa opcional. Decide el autor. | Una forma más simple de escribir algo, una función de una librería que ya lo hace |

**Veredicto** de la revisión:

- ✅ **Listo:** ningún hallazgo Crítico ni Importante.
- ⚠️ **Listo con cambios:** ningún hallazgo Crítico, pero hay Importantes que corregir antes.
- ❌ **Necesita trabajo:** al menos un hallazgo Crítico, o hay que replantear el enfoque.

## 1. Diseño y estructura

- **Responsabilidad única.** ¿Cada función, clase o módulo nuevo o cambiado hace una sola cosa? Las responsabilidades mezcladas (por ejemplo, validación, reglas de negocio y acceso a datos en la misma función) son un hallazgo.
- **El sitio correcto.** ¿El código está en la capa o el módulo donde el proyecto pone ese tipo de código? La lógica de negocio en controladores o vistas, o el acceso a datos en el dominio, rompen la arquitectura.
- **Dependencias en la dirección correcta.** ¿El cambio introduce una dependencia que va en contra de las capas del proyecto (por ejemplo, el dominio importando de la infraestructura) o una dependencia circular?
- **Acoplamiento.** ¿Accede a los detalles internos de otros módulos en lugar de usar su interfaz pública? ¿Un cambio aquí obliga a cambiar muchos sitios sin relación?
- **Nivel de abstracción.** ¿Falta una abstracción (la misma estructura repetida) o sobra una (una interfaz con una sola implementación sin motivo, capas que solo reenvían llamadas)?
- **Coherencia.** ¿Resuelve un problema que el proyecto ya resuelve de otra forma? Reutiliza la solución existente o justifica la nueva.
- **Interfaces públicas.** ¿Las APIs, firmas de funciones y tipos nuevos son fáciles de usar bien y difíciles de usar mal? ¿Los cambios incompatibles en interfaces existentes son intencionados y están gestionados?
- **Tamaño del cambio.** ¿Mezcla cambios sin relación (una funcionalidad, una refactorización y una pasada de formato) que serían más fáciles de revisar por separado?

## 2. Clean code

- **Nombres.** ¿Los nombres dicen qué es o qué hace cada cosa, con el vocabulario del proyecto? Evita nombres vagos (`data`, `info`, `manager`, `handle`), abreviaturas que nadie conoce y nombres que mienten sobre lo que hace el código.
- **Funciones.** Cortas, en un solo nivel de abstracción y con pocos parámetros. Los parámetros booleanos que cambian el comportamiento suelen esconder dos funciones.
- **Duplicación.** Lógica copiada que habrá que cambiar en varios sitios. Tres líneas parecidas no siempre son duplicación; la misma regla en dos sitios sí lo es.
- **Complejidad.** Anidamiento profundo, condicionales largos, flujo difícil de seguir. Pueden ayudar los retornos tempranos, extraer funciones o estructuras de datos más claras.
- **Valores mágicos.** Números o textos sin explicar que deberían ser constantes con nombre o configuración.
- **Código muerto.** Variables, funciones, imports o parámetros sin usar, código comentado y restos de depuración (`print`, `console.log`, puntos de interrupción).
- **Comentarios.** Deben explicar el porqué, no repetir el qué. Un comentario desactualizado o engañoso es peor que ninguno. Comentarios `TODO` sin contexto ni responsable.
- **Formato y estilo.** Solo lo que el formateador o el linter del proyecto no impone ya, y solo si es incoherente con el resto del código.

## 3. Errores y lógica

- **¿Hace lo que pretende?** Compara el comportamiento con la intención de los mensajes de commit o del pull request.
- **Casos límite.** Colecciones vacías, valores nulos o ausentes, cero, números negativos, entradas muy grandes, duplicados, tipos inesperados, zonas horarias y fechas, codificación de texto.
- **Condiciones.** Errores de uno (off-by-one), condiciones invertidas, operadores equivocados, ramas `else` que faltan, casos de `switch` o `match` incompletos.
- **Estado.** Estado mutable compartido, valores modificados mientras se leen, objetos que quedan inconsistentes si algo falla.
- **Concurrencia.** Condiciones de carrera, bloqueos o `await` que faltan, operaciones que suponen un orden, llamadas asíncronas sin esperar.
- **Recursos.** Archivos, conexiones, suscripciones o listeners que se abren y nunca se cierran o liberan.
- **Cambios en los datos.** Migraciones que no se pueden revertir o que pierden datos; cambios en formatos guardados que rompen los datos existentes.

## 4. Manejo de errores

- **Los errores no se tragan.** Bloques `catch` vacíos, errores que se registran y se ignoran cuando quien llama necesitaba saberlo, valores de retorno que indican fallo y no se comprueban.
- **Los errores se manejan en el nivel correcto**, con contexto suficiente para diagnosticarlos y siguiendo la estrategia de errores del proyecto.
- **Un fallo deja todo consistente.** Escrituras a medias, transacciones que no se revierten, reintentos que duplican efectos.
- **El usuario ve un mensaje útil**, sin detalles internos ni trazas de pila.

## 5. Seguridad

- **Validación de entradas.** Los datos de usuarios, archivos, servicios externos o la red se validan antes de usarlos.
- **Inyección.** SQL, comandos, rutas, plantillas o consultas construidos concatenando entradas no confiables.
- **Secretos.** Credenciales, tokens o claves en el código, la configuración, las pruebas o los logs. Reporta la ubicación, nunca el valor.
- **Autenticación y autorización.** Endpoints o acciones nuevos sin control de acceso; controles hechos solo en el cliente.
- **Datos sensibles.** Datos personales o sensibles escritos en logs, expuestos en respuestas o guardados sin protección.
- **Dependencias.** Dependencias nuevas sin mantenimiento, innecesarias o de fuentes no confiables.

## 6. Pruebas

- **La lógica nueva tiene pruebas**, siguiendo las convenciones de pruebas del proyecto. Una corrección de un error idealmente trae una prueba que lo habría detectado.
- **Las pruebas comprueban comportamiento**, no detalles de implementación, y fallarían si el código se rompiera.
- **Los casos límite y los errores** del apartado 3 están cubiertos donde importan.
- **Las pruebas son fiables:** no dependen del orden, la hora, la red o el azar sin control.
- **El comportamiento cambiado** se refleja en las pruebas existentes, en lugar de esquivarlo borrándolas o debilitándolas.

## 7. Rendimiento

Solo problemas evidentes; no especules con microoptimizaciones.

- **Trabajo repetido:** consultas o llamadas dentro de bucles (N+1), el mismo cálculo costoso hecho varias veces.
- **Trabajo sin límite:** cargar tablas o archivos enteros en memoria, falta de paginación, colecciones o cachés que crecen sin límite.
- **Bloqueos:** operaciones lentas en el hilo principal o de la interfaz, llamadas síncronas donde el proyecto es asíncrono.
- **Estructuras ineficientes:** búsquedas lineales en caminos críticos donde un mapa o un conjunto serviría.
