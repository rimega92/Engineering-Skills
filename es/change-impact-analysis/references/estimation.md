# Valoración y estimación

Cómo valorar un cambio y estimar su esfuerzo. El estimado es un rango razonado, no un compromiso: sirve para comparar opciones, planificar y decidir qué revisar primero.

## Valoración

Tres ejes por separado, cada uno con una justificación corta. Mantenlos separados: un cambio puede ser fácil de escribir y muy arriesgado (una migración de datos), o difícil de escribir y de poco riesgo (un módulo nuevo y aislado).

### Complejidad: qué tan difícil es implementarlo

| Nivel | Señales |
|---|---|
| **Baja** | Un módulo, pocos archivos, un patrón conocido que ya se repite en el proyecto, sin contratos ni datos de por medio |
| **Media** | Varios archivos o módulos, algo de lógica nueva, un cambio de contrato compatible o una migración sencilla |
| **Alta** | Varios módulos o servicios, lógica nueva con muchos casos, un cambio de contrato incompatible, una migración con backfill |
| **Muy alta** | Cambio transversal (arquitectura, plataforma, modelo de datos), coordinación entre equipos, convivencia de versiones antigua y nueva |

### Riesgo: qué puede salir mal y cuánto dolería

| Nivel | Señales |
|---|---|
| **Bajo** | Cambio aislado, buena cobertura de pruebas, fácil de revertir, sin datos sensibles |
| **Medio** | Afecta a un flujo principal o tiene cobertura parcial, pero es reversible |
| **Alto** | Toca un área sensible, datos existentes, consumidores externos o código sin pruebas; difícil de revertir |
| **Muy alto** | Puede corromper o exponer datos, romper operaciones críticas o consumidores que no se ven, y no se puede revertir fácilmente |

### Confianza: qué tan seguro es el análisis

| Nivel | Señales |
|---|---|
| **Alta** | Se encontraron en el código todos los puntos de contacto, los consumidores son visibles y la zona tiene pruebas |
| **Media** | La mayor parte está confirmada, pero hay consumidores o comportamientos por confirmar |
| **Baja** | Partes clave están fuera del repositorio, el código es difícil de seguir (reflexión, configuración dinámica) o los requisitos siguen abiertos |

## Talla y estimado

El estimado es para **un desarrollador que conoce el código**, desde que empieza el trabajo hasta que el cambio está listo para integrar: implementación, pruebas, migraciones y correcciones de la revisión. No incluye tiempos de espera (otros equipos, colas de QA, aprobaciones, ventanas de despliegue); lístalos aparte como "no incluido".

| Talla | Rango típico | Forma típica |
|---|---|---|
| **XS** | Menos de 2 horas | Uno o dos archivos, sin pruebas nuevas o con una prueba sencilla |
| **S** | De 2 horas a 1 día | Pocos archivos en un módulo, con sus pruebas |
| **M** | De 1 a 3 días | Varios módulos, o un cambio compatible de contrato o de datos |
| **L** | De 3 a 10 días | Varios módulos y consumidores, una migración con backfill o un cambio de contrato incompatible |
| **XL** | Más de 2 semanas | Recomienda dividirlo en cambios más pequeños y estima cada uno |

## Cómo estimar

1. **Desglosa por actividad**, con un rango para cada una, solo las que apliquen:
   - Implementación (código de producción).
   - Pruebas (modificar las existentes y escribir nuevas; también las que se escriben primero donde falta cobertura).
   - Migraciones, scripts y backfill.
   - Contratos y consumidores (versionado, clientes generados, actualizar los consumidores del repositorio).
   - Configuración, infraestructura y observabilidad.
   - Documentación.
   - Revisión y correcciones.
2. **Suma los rangos** y redondea a un rango que suene a estimado real ("de 2 a 4 días", no "de 13,5 a 27 horas").
3. **Amplía el rango cuando baja la confianza:** con confianza Media, sube el límite superior en torno a la mitad; con Baja, duplícalo y di qué lo acotaría.
4. **Di qué lo hace crecer:** los hechos concretos que subirían el estimado (por ejemplo, "si la app móvil necesita el campo, suma de 1 a 2 días").
5. **Di qué no está incluido:** tiempos de espera, coordinación, QA, despliegue.

## Reglas

- Basa el estimado en el impacto encontrado, no en la descripción de la petición.
- Nunca des una única cifra exacta. Un rango y las razones que lo sostienen son más útiles.
- No infles el estimado por precaución; la confianza y la lista de "qué lo hace crecer" ya expresan la incertidumbre.
- Si hay un alcance mínimo y uno completo, estima los dos.
- Si el proyecto tiene su propia escala de estimación (story points, tallas), añádela al lado, pero mantén el rango.
