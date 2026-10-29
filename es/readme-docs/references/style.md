# Guía de estilo

Cómo escribir el README para que sea fácil de leer: redacción, formato Markdown y diagramas Mermaid.

## Redacción

### Tono y nivel técnico

- **Lenguaje sencillo por defecto.** Escribe como le explicarías el proyecto a una persona nueva en el equipo: frases cortas, voz activa y en segunda persona ("ejecuta", "configura").
- **Técnico donde hace falta.** El nivel depende del apartado:
  - **Para cualquier lector** (descripción, funcionalidad principal, alcance, estado): sin jerga. Alguien que no programa debería entender qué hace el proyecto y para qué sirve.
  - **Para quien va a ejecutar o modificar el proyecto** (inicio rápido, arquitectura, APIs, modelo de datos, operación, seguridad): usa la terminología técnica correcta, sin simplificar de más. Explica los términos propios del proyecto o del dominio, no los estándares de la industria.
- **Empieza por lo importante.** Cada apartado abre con una frase que dice qué cubre o para qué sirve. Después vienen los detalles.
- **Concreto antes que abstracto.** Un ejemplo, un comando o una tabla explican más que un párrafo genérico.
- **Siglas.** Defínelas la primera vez que aparecen, salvo las muy conocidas (API, URL, HTTP).
- **Terminología coherente.** Usa siempre el mismo nombre para la misma cosa. Si el código dice `order`, no alternes entre "pedido", "orden" y "compra".
- **Sin relleno.** Evita palabras como "simplemente", "fácilmente" u "obviamente", y frases que no aportan información ("Este apartado describe...").

### Párrafos y listas

- Párrafos de tres o cuatro frases como máximo.
- Listas numeradas para pasos que se siguen en orden. Un paso equivale a una acción, con su comando si lo tiene.
- Listas con viñetas para elementos sin orden.
- Tablas para información con la misma estructura repetida (variables de entorno, endpoints, comandos).

## Markdown

Sigue las reglas de [markdownlint](https://github.com/DavidAnson/markdownlint) y el formato de GitHub Flavored Markdown.

### Estructura

- Un solo título `#` (el nombre del proyecto), al principio del archivo.
- No te saltes niveles de título (`##` → `####`).
- Títulos con `#` (estilo ATX), sin punto final y sin repetir el mismo texto en dos títulos.
- Una línea en blanco antes y después de títulos, listas, tablas y bloques de código.
- Añade tabla de contenido cuando el README tenga más de cinco apartados de nivel `##`.

### Código y comandos

- Todo bloque de código lleva su lenguaje: `bash`, `json`, `yaml`, `http`, `sql`, `typescript`, etc. Usa `text` cuando no haya un lenguaje.
- Los comandos van sin el prompt (`$`), para que se puedan copiar y pegar.
- Un comando por línea. Si un paso necesita varios comandos, explica qué hace cada uno cuando no sea obvio.
- Los nombres de archivos, variables, comandos y valores van entre comillas invertidas: `` `.env` ``, `` `PORT` ``.

### Tablas

- Encabezados cortos y una sola idea por celda.
- Formato recomendado para variables de entorno:

  ```markdown
  | Variable | Obligatoria | Descripción | Ejemplo |
  |----------|-------------|-------------|---------|
  | `DATABASE_URL` | Sí | Cadena de conexión a PostgreSQL | `postgres://user:pass@localhost:5432/app` |
  ```

- Formato recomendado para endpoints:

  ```markdown
  | Método | Ruta | Descripción | Autenticación |
  |--------|------|-------------|---------------|
  | `GET` | `/api/orders/{id}` | Obtiene un pedido | Bearer token |
  ```

### Enlaces e imágenes

- Enlaces relativos para archivos del propio repositorio: `[guía de despliegue](docs/deployment.md)`.
- Texto de enlace descriptivo. Nunca "aquí" ni "este enlace".
- Toda imagen lleva texto alternativo que describa su contenido.

### Elementos de GitHub

- **Alertas** (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`): úsalas solo para información que el lector no debe pasar por alto, como mucho una o dos por apartado. Si el proyecto no está en GitHub, usa citas normales, porque otras plataformas muestran el texto `[!NOTE]` tal cual.
- **Bloques plegables** (`<details>` y `<summary>`): para contenido largo y secundario, como una salida de ejemplo extensa o la lista completa de opciones.
- **Badges:** solo si aportan información real (estado del CI, versión publicada, licencia). Nunca más de una línea de badges.

## Diagramas Mermaid

GitHub, GitLab y la mayoría de editores renderizan Mermaid dentro de un bloque ` ```mermaid `.

### Cuándo usar un diagrama

- Cuando explica algo mejor que el texto: varios servicios conectados, un flujo con decisiones, una secuencia de llamadas entre componentes, un modelo de datos con relaciones.
- Nunca para algo que se entiende con una frase o una lista.
- Cada diagrama va precedido de una frase que dice qué muestra.

### Qué tipo usar

| Para mostrar | Tipo |
|---|---|
| Arquitectura, componentes, contexto, dependencias entre módulos | `flowchart` |
| Interacciones entre componentes a lo largo del tiempo | `sequenceDiagram` |
| Entidades de datos y sus relaciones | `erDiagram` |
| Estados por los que pasa una entidad | `stateDiagram-v2` |
| Estructura de clases o tipos | `classDiagram` |

Usa solo estos tipos. Los más nuevos (`architecture-beta`, `C4Context`, etc.) son experimentales y no siempre se renderizan en GitHub.

### Legibilidad

- **Como máximo unos 15 nodos por diagrama.** Si hay más, divídelo: uno de visión general y otros de detalle.
- **Dirección según la forma:** `LR` (izquierda a derecha) para flujos y cadenas de servicios, `TD` (arriba abajo) para jerarquías y capas.
- **IDs cortos y etiquetas claras:** `api["API de pedidos"]`. Pon las etiquetas entre comillas si llevan espacios, acentos, paréntesis u otros caracteres especiales.
- **Agrupa con `subgraph`** los componentes que pertenecen a la misma capa, servicio o frontera (por ejemplo, "Nube" frente a "Externo").
- **Etiqueta las flechas** cuando la relación no sea obvia: `api -->|"REST"| db`.
- **Formas con significado:** `[(...)]` para bases de datos, `([...])` para inicio y fin, `{...}` para decisiones, `[[...]]` para subprocesos.
- **En diagramas de secuencia,** usa `autonumber` y `participant` con alias cortos.
- **Sin directivas de tema** (`%%{init: ...}%%`): fuerzan un tema que puede no verse bien en modo claro u oscuro.

### Colores

Usa color cuando ayude a distinguir tipos de componentes, no como decoración. Define los colores con `classDef` y aplícalos con `:::clase` o `class`.

Esta paleta se lee bien en el modo claro y en el oscuro de GitHub: fondos claros, borde saturado y texto oscuro.

```text
classDef frontend fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
classDef backend  fill:#dcfce7,stroke:#16a34a,color:#14532d
classDef data     fill:#fef3c7,stroke:#d97706,color:#78350f
classDef external fill:#f3e8ff,stroke:#9333ea,color:#581c87
classDef async    fill:#ffe4e6,stroke:#e11d48,color:#881337
classDef infra    fill:#f1f5f9,stroke:#64748b,color:#0f172a
```

| Clase | Color | Para |
|---|---|---|
| `frontend` | Azul | Interfaces de usuario: web, móvil, escritorio |
| `backend` | Verde | Servicios, APIs, workers propios |
| `data` | Ámbar | Bases de datos, caché, almacenamiento |
| `external` | Morado | Sistemas y proveedores externos |
| `async` | Rosa | Colas, tópicos, eventos |
| `infra` | Gris | Infraestructura, gateways, balanceadores |

Reglas:

- Como máximo cinco o seis colores por diagrama, siempre con el mismo significado en todo el README.
- Si usas color, añade una leyenda debajo del diagrama (una línea de texto basta), porque el color solo no debe ser la única forma de transmitir información.
- No uses fondos oscuros ni texto claro.

Ejemplo:

```mermaid
flowchart LR
    user(["Usuario"])

    subgraph app["Aplicación"]
        web["Web (React)"]:::frontend
        api["API de pedidos"]:::backend
        worker["Worker de notificaciones"]:::backend
    end

    db[("PostgreSQL")]:::data
    queue["Cola de eventos"]:::async
    pay["Pasarela de pagos"]:::external

    user --> web
    web -->|"REST"| api
    api --> db
    api -->|"pedido.creado"| queue
    queue --> worker
    api -->|"HTTPS"| pay

    classDef frontend fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef backend  fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef data     fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef external fill:#f3e8ff,stroke:#9333ea,color:#581c87
    classDef async    fill:#ffe4e6,stroke:#e11d48,color:#881337
```

Leyenda: azul, interfaz de usuario; verde, servicios propios; ámbar, datos; rosa, mensajería; morado, sistemas externos.

### Validación

- Si `mmdc` (Mermaid CLI) está instalado, valida cada diagrama con él.
- Si no, revisa la sintaxis con cuidado: etiquetas con caracteres especiales entre comillas, cada `subgraph` cerrado con `end` y ninguna palabra reservada (`end`, `graph`, `class`) usada como ID de nodo.
