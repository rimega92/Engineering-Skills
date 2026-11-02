# Arquitectura del proyecto generado

## Capas y módulos

| Capa | Carpeta | Qué contiene | Puede depender de |
| ---- | ------- | ------------ | ----------------- |
| Dominio | `domain/model` | Entidades y gateways (puertos, como interfaces) | Nada. En proyectos reactivos se permite Reactor |
| Dominio | `domain/usecase` | Lógica de aplicación, que orquesta los gateways | Solo `model` |
| Infraestructura | `infrastructure/driven-adapters/*` | Implementaciones de gateways: bases de datos, clientes REST, colas | `model`, librerías externas |
| Infraestructura | `infrastructure/entry-points/*` | Inicio de los flujos: REST, consumidores | `model`, `usecase`, librerías externas |
| Infraestructura | `infrastructure/helpers/*` | Utilidades compartidas por adaptadores y entry points | `model`, librerías externas |
| Aplicación | `applications/app-service` | `MainApplication`, configuración de beans, `application.yaml` | Ensambla todos los módulos |

Los módulos de infraestructura nunca deben depender de `app-service`. Un adaptador nunca llama a un entry point, y un caso de uso nunca nombra una tecnología.

## Un flujo, paso a paso

1. **Modelo:** `gm --name=Order` crea `model/order/Order.java` y `model/order/gateways/OrderRepository.java`. Añade campos a la entidad y métodos al gateway.
2. **Caso de uso:** `guc --name=CreateOrder` crea `usecase/createorder/CreateOrderUseCase.java`. Inyecta el gateway en un campo `final`.
3. **Adaptador:** genéralo con `gda`, implementa el gateway y anota la clase con `@Repository` o `@Component`. Convierte aquí entre los modelos de persistencia del adaptador y el modelo de dominio, nunca en el dominio.
4. **Entry point:** genéralo con `gep`, inyecta el caso de uso y llámalo.

Ejemplo de un caso de uso reactivo:

```java
@RequiredArgsConstructor
public class CreateOrderUseCase {
    private final OrderRepository orderRepository;

    public Mono<Order> create(String product) {
        return orderRepository.save(Order.builder().product(product).build());
    }
}
```

En proyectos imperativos, el mismo código devuelve `Order` directamente. En proyectos reactivos, no bloquees dentro de un flujo (`.block()`, clientes síncronos).

## Conexión automática

Lo hacen las convenciones del plugin. No lo hagas a mano:

- **Descubrimiento de módulos:** cualquier carpeta con un `build.gradle` bajo `applications`, `domain` o `infrastructure` es un módulo. `settings.gradle` no tiene líneas `include`.
- **Dependencias:** `usecase` recibe `model`; adaptadores y helpers reciben `model` y `spring-context`; entry points reciben `model`, `usecase` y `spring-context`; `app-service` recibe todos los módulos.
- **Las dependencias entre módulos de infraestructura no son automáticas:** añádelas en el `build.gradle` del módulo.
- **Librerías en todos los módulos:** el BOM de Spring Boot (así que las versiones de las librerías de Spring son opcionales), `spring-boot-starter-test`, Lombok si está activo y Reactor si es reactivo.
- **Beans de casos de uso:** `UseCasesConfig` escanea `<paquete>.usecase` con el patrón `^.+UseCase$`. Una clase que no termine en `UseCase` o que esté en otro sitio no será un bean.
- **Escaneo de componentes:** `MainApplication` escanea el paquete base, así que adaptadores y entry points deben estar debajo de él. En un módulo `generic`, que se genera sin archivos fuente, crea tú el paquete, sin guiones (`in-memory-orders` → `<paquete>.inmemory`).

## Regla de dependencias (`validateStructure`)

Corre en cada `compileJava`, así que una violación detiene la compilación:

| Violación | Mensaje |
| --------- | ------- |
| Una librería en `model` | `Model module is invalid` |
| Una librería distinta de `model` en `usecase` | `Use case module is invalid` |
| `app-service` como dependencia de infraestructura | `Infrastructure layer is invalid` |

Lo correcto ante una violación es mover el código a la capa que le corresponde, normalmente detrás de un gateway. Usa `whitelistedDependencies` solo para una librería que el usuario haya decidido permitir en el dominio.

## Reglas de ArchUnit

`validateStructure` escribe `ArchitectureTest.java` y `Utils.java` en los tests de `app-service`. Git los ignora porque contienen rutas absolutas. No los edites ni los subas.

| Regla | Qué comprueba | Efecto |
| ----- | ------------- | ------ |
| 1.5 | Los flujos reactivos usan clientes asíncronos de AWS | Aviso |
| 2.2 | Clases de dominio sin sufijos de tecnología (`Dto`, `Request`, `Response`) | Aviso |
| 2.4 | Clases de dominio sin nombres de tecnología | Aviso |
| 2.5 | Casos de uso solo con campos `final` | **Hace fallar el test** |
| 2.6 | Campos de dominio sin nombres de tecnología | Aviso |
| 2.7 | Beans solo con campos `final`, inyectados por constructor | Aviso |

Un aviso no rompe la compilación: se escribe en `build/issues.json`, para Sonar. Lee ese archivo y corrige lo que indique, en lugar de suponer que una compilación en verde significa que no hay violaciones.

La regla detrás de 2.5 y 2.7 importa para la corrección, no solo para el estilo: un bean se comparte entre peticiones concurrentes, así que los datos de una petición guardados en un campo se mezclan entre usuarios.

## Calidad y empaquetado

- **Cobertura:** `build/reports/jacocoMergedReport/`.
- **Mutación:** con Pitest declarado, `pitest` corre en cada módulo como parte de `jacocoTestReport`, y el agregado queda en `build/reports/pitest/`. Requiere que todos los tests pasen. Para omitirlo en una ejecución: `-x pitest`.
- **Sonar:** configurado en la raíz, lee los informes anteriores y `build/issues.json`. Los valores del proyecto van en un bloque `sonar {}` del `build.gradle` de la raíz.
- **Empaquetado:** `bootJar` produce `<proyecto>.jar` en `applications/app-service/build/libs/`. `deployment/Dockerfile` es un punto de partida: revísalo antes de confiar en él.
- **Caché de compilación:** en `build-cache/` en la raíz, ya ignorada por git.
- **README generado:** genérico y en español. Reemplázalo por uno que describa el proyecto real.
