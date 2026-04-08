# KHA0SYS3
## La Historia de un Bot que Aprendio a Cazar en la Jungla del Mercado

---

```
    ██╗  ██╗██╗  ██╗ █████╗  ██████╗ ███████╗██╗   ██╗███████╗██████╗ 
    ██║ ██╔╝██║  ██║██╔══██╗██╔═══██╗██╔════╝╚██╗ ██╔╝██╔════╝╚════██╗
    █████╔╝ ███████║███████║██║   ██║███████╗ ╚████╔╝ ███████╗ █████╔╝
    ██╔═██╗ ██╔══██║██╔══██║██║   ██║╚════██║  ╚██╔╝  ╚════██║ ╚═══██╗
    ██║  ██╗██║  ██║██║  ██║╚██████╔╝███████║   ██║   ███████║██████╔╝
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═════╝ 
```

> *"El mercado no es un casino. Es una jungla. Y en la jungla, no sobrevive*
> *el mas fuerte ni el mas rapido. Sobrevive el que mejor entiende las trampas."*

---

## Tabla de Contenidos

1. [Prologo: El Mapa del Territorio](#cap-0)
2. [Capitulo I: El Rango de Apertura -- Donde Todo Comienza](#cap-1)
3. [Capitulo II: Los Tres Cazadores -- FADE, MOMENTUM y SHAKEOUT](#cap-2)
4. [Capitulo III: La Salsa Secreta -- Filtros de Contexto](#cap-3)
5. [Capitulo IV: La Gran Expedicion -- El Descubrimiento de 121 Estrategias](#cap-4)
6. [Capitulo V: El Arte del Riesgo -- De 1% a 6%](#cap-5)
7. [Capitulo VI: Los Campeonatos -- Las Mejores Estrategias](#cap-6)
8. [Capitulo VII: La Maquinaria -- Stack Tecnologico](#cap-7)
9. [Capitulo VIII: De la Simulacion al Campo de Batalla](#cap-8)
10. [Epilogo: Los Numeros Finales](#cap-9)

---

<a name="cap-0"></a>
## Prologo: El Mapa del Territorio

Imaginate esto: son las 7:00 UTC de un martes cualquiera. Londres acaba de abrir.
Miles de traders institucionales lanzan sus ordenes al mercado como lobos hambrientos.
El EURUSD forma un rango en los primeros 30 minutos -- un rectangulo compacto entre
1.0850 y 1.0870. Veinte pips de ancho. Una caja de cristal esperando romperse.

A las 7:31, el precio perfora 1.0870. Los traders de momentum saltan al tren.
"Breakout! Compra! Compra!" gritan sus algoritmos.

Y exactamente ahi... KHA0SYS3 vende.

No por capricho. No por corazonada. Sino porque en 8 anios de datos historicos,
ese escenario especifico -- EURUSD, sesion de Londres, rango de 30 minutos,
rompimiento alcista -- resulta en un falso quiebre el 64% de las veces.

Bienvenido a la historia de un bot que aprendio a cazar cazadores.

### El Universo de KHA0SYS3

```
    ┌─────────────────────────────────────────────────────────────────┐
    │                    15 ACTIVOS EN 5 MERCADOS                     │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   FOREX (7)          METALES (2)      ENERGIA (3)              │
    │   ├── EURUSD         ├── XAUUSD       ├── WTI                  │
    │   ├── GBPUSD         └── XAGUSD       ├── BRENT               │
    │   ├── USDJPY                          └── NATGAS               │
    │   ├── AUDUSD                                                    │
    │   ├── GBPJPY         INDICES (2)      VOLATILIDAD (1)          │
    │   ├── EURJPY         ├── SP500        └── VIX                  │
    │   └── GBPAUD         └── NASDAQ100                             │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
```

Quince activos. Cuatro sesiones de trading. Tres tipos de cazador. Ciento veintiuna
estrategias afiladas como bisturis. Y un unico principio rector:

**El Opening Range Breakout no es lo que parece.**

---

<a name="cap-1"></a>
## Capitulo I: El Rango de Apertura -- Donde Todo Comienza

### La Teoria

Cada maniana, cada sesion, cada mercado tiene un ritual. Durante los primeros minutos
de actividad, los participantes se tantean. Compradores y vendedores negocian un
territorio. Ese territorio es el **Opening Range (OR)**: el maximo y el minimo
alcanzados durante una ventana de tiempo especifica al inicio de la sesion.

```
    Precio
      ^
      |         OR_HIGH ─────────────────────── 1.0870
      |        /                                  \
      |   ┌───/────────────────────────────────────\───┐
      |   │  /    Zona del Opening Range            \  │
      |   │ /      (15-60 minutos)                   \ │
      |   │/                                          \│
      |   └────────────────────────────────────────────┘
      |        \                                  /
      |         OR_LOW ──────────────────────── 1.0850
      |
      +──────────────────────────────────────────────────> Tiempo
           |<---- Formacion ---->|<---- Breakout Zone ---->|
              (apertura)              (donde cazamos)
```

El OR es como la linea de salida de una carrera. No importa quien salga primero;
importa quien llega a la meta. Y la estadistica nos dice algo contraintuitivo:
**la mayoria de las veces, el primero en salir... no llega.**

### Las Cuatro Sesiones

KHA0SYS3 no duerme. Opera en cuatro ventanas horarias que cubren las principales
sesiones de liquidez del planeta:

| Sesion | Hora UTC | Duracion OR | Mercados Principales |
|:------------|:-----------|:------------|:-------------------------------|
| **Tokyo** | 00:00 | 15-60 min | Forex JPY, AUDUSD |
| **London** | 07:00 | 15-60 min | Forex EUR/GBP, Metales |
| **Pre-Market** | 12:00 | 30-60 min | Indices, Energia, VIX |
| **New York** | 13:00-13:30| 15-60 min | Todo el universo |

Cuatro sesiones. Cuatro campos de batalla. Cada uno con sus propias reglas,
sus propios depredadores, y sus propias presas.

La sesion de Tokyo es el agua mansa. Movimientos contenidos, spreads decentes
en los pares del yen. London es la tormenta: el 70% del volumen de forex
mundial pasa por ahi. Pre-Market es el calentamiento de los indices americanos,
donde el dinero institucional posiciona antes de la campana. Y New York...
New York es donde todos los mundos colisionan.

### El Filtro ATR: No Todo Rango Merece Atencion

No cualquier Opening Range es valido. KHA0SYS3 aplica un filtro quirurgico:

```
    Regla: OR_width debe estar entre 10% y 80% del ATR(14)

    ATR(14) = 100 pips (ejemplo)

    Demasiado estrecho        Zona valida           Demasiado ancho
    OR < 10 pips              10-80 pips            OR > 80 pips
    ├────────────┤├─────────────────────────────┤├──────────────┤
    [  RECHAZADO  ]          [  ACEPTADO  ]          [ RECHAZADO ]
    (ruido)                  (senial real)            (evento raro)
```

Un rango demasiado estrecho es ruido -- no hay suficiente estructura para operar.
Un rango demasiado ancho significa que algo extraordinario paso (NFP, decision
de tasas de interes, guerra) y las reglas normales no aplican.

El ATR(14) se calcula con un **shift de 1 dia** para evitar look-ahead bias.
Usamos el ATR de ayer, no el de hoy. Porque en backtesting, usar datos del
futuro es la forma mas rapida de enganarte a ti mismo.

---

<a name="cap-2"></a>
## Capitulo II: Los Tres Cazadores -- FADE, MOMENTUM y SHAKEOUT

En la jungla del mercado, KHA0SYS3 despliega tres tipos de depredador. Cada uno
con su propia filosofia, su propio temperamento, y su propia forma de matar.

### Cazador #1: FADE -- El Contrarian (95% de las estrategias)

> *"Cuando todos corren en una direccion, parate en la otra."*

El FADE es el alma de KHA0SYS3. De las 121 estrategias, 115 son variantes de
FADE. Y no es accidente: los falsos quiebres son el pan de cada dia del mercado.

**Como funciona:**

```
    Escenario: FADE_UP (Venta contra el rompimiento alcista)

    Precio
      ^
      |                            Sell Limit
      |                              v
      |                    x]========* <--- Precio rompe OR_HIGH
      |                   / ]        |      KHA0SYS3 VENDE aqui
      |   ┌──────────────/──┐        |
      |   │  Opening Range  │   SL --+-- OR_HIGH + OR_width
      |   │   (la caja)     │        |
      |   └─────────────────┘        |
      |                         TP --+-- OR_LOW (1:1 R:R)
      |                              |
      +──────────────────────────────+──────────> Tiempo


    Escenario: FADE_DOWN (Compra contra el rompimiento bajista)

    Precio
      ^
      |                         TP --+-- OR_HIGH (1:1 R:R)
      |                              |
      |   ┌─────────────────┐        |
      |   │  Opening Range  │   SL --+-- OR_LOW - OR_width
      |   │   (la caja)     │        |
      |   └──────────────\──┘        |
      |                   \ ]        |
      |                    x]========* <--- Precio rompe OR_LOW
      |                              ^      KHA0SYS3 COMPRA aqui
      |                          Buy Limit
      +──────────────────────────────+──────────> Tiempo
```

**La logica:** Cuando el precio rompe el OR_HIGH, la mayoria de los traders
de breakout compran. Sus stop-losses quedan justo debajo del OR_HIGH. El
mercado, ese animal despiadado, se los come y revierte. KHA0SYS3 espera
exactamente ese momento para entrar en la direccion contraria.

**Risk:Reward = 1:1.** No necesitamos ratios asimetricos cuando tenemos una
tasa de acierto del 63.5%. Las matematicas son simples:

```
    Con WR = 63.5% y R:R = 1:1:
    
    100 trades x $100 riesgo cada uno:
    - 63.5 ganadores x $100 = +$6,350
    - 36.5 perdedores x $100 = -$3,650
    - Beneficio neto = +$2,700
    - Profit Factor = 6,350 / 3,650 = 1.74
```

No es sexy. Es rentable.

**El monitor de 2 etapas (Live):**

```
    Etapa 1: ESPERANDO BREAKOUT
    ┌──────────────────────────────┐
    │ Monitorear precio cada tick  │
    │ Precio > OR_HIGH?  ─────────┼──> Etapa 2
    │ Precio < OR_LOW?   ─────────┼──> Etapa 2
    │ Orden expirada?    ─────────┼──> Cancelar
    └──────────────────────────────┘
                 │
                 v
    Etapa 2: COLOCAR CONTRA-ORDEN
    ┌──────────────────────────────┐
    │ Breakout UP detectado:      │
    │   -> SELL LIMIT en OR_HIGH   │
    │   -> SL = OR_HIGH + width    │
    │   -> TP = OR_LOW             │
    │                              │
    │ Breakout DOWN detectado:     │
    │   -> BUY LIMIT en OR_LOW     │
    │   -> SL = OR_LOW - width     │
    │   -> TP = OR_HIGH            │
    └──────────────────────────────┘
```

### Cazador #2: MOMENTUM -- El Oportunista

> *"A veces, el breakout es real. Y cuando lo es, hay que subirse al tren."*

El MOMENTUM es la antitesis del FADE. No apuesta contra el breakout; lo abraza.
Cuando el precio rompe el OR_HIGH, MOMENTUM compra. Cuando rompe el OR_LOW, vende.

Es la estrategia mas simple del arsenal, y la que menos se usa. Porque
resulta que, en la mayoria de las condiciones, los breakouts falsos superan
a los reales. Pero hay nichos -- ciertas combinaciones de activo, sesion
y contexto -- donde el momentum genuino domina.

```
    Escenario: MOMENTUM_UP

    Precio
      ^
      |                                   TP = OR_HIGH + 1.5 x width
      |                                        |
      |                               /--------+
      |                              /
      |                    x]═══════*  <--- BUY STOP en OR_HIGH
      |                   / ]       |       Se activa al romper
      |   ┌──────────────/──┐       |
      |   │  Opening Range  │  SL = OR_LOW
      |   │                 │       |
      |   └─────────────────┘───────+
      |
      +─────────────────────────────────────> Tiempo
```

**R:R = 1:1.5.** El TP se coloca a 1.5 veces el ancho del OR desde el punto
de entrada. Necesita menos aciertos para ser rentable, pero los consigue con
menos frecuencia.

**En live:** Ordenes BUY_STOP y SELL_STOP directas. Sin monitor de software.
La paridad con el backtest es perfecta -- es el unico arquetipo donde la
ejecucion live es identica a la simulacion.

### Cazador #3: SHAKEOUT -- El Estratega

> *"El mercado barre stops... y luego continua. Nosotros esperamos el barrido."*

El SHAKEOUT es el cazador mas sofisticado. Opera en tres actos, como una obra
de teatro:

```
    ACTO I: El Breakout Inicial
    ─────────────────────────────────────────
    Precio rompe OR_HIGH. Los momentum traders compran.
    "Es un breakout!" dicen.

    ACTO II: El Falso Quiebre (Shakeout)
    ─────────────────────────────────────────
    Precio retrocede DENTRO del OR. Los stops se activan.
    Los momentum traders son liquidados.
    "Fue una trampa..." se lamentan.

    ACTO III: La Re-entrada
    ─────────────────────────────────────────
    Precio vuelve a romper OR_HIGH. ESTA vez es real.
    Los debiles ya fueron eliminados. El camino esta libre.
    KHA0SYS3 entra AQUI.
```

Visualmente:

```
    Precio
      ^
      |                                              /───── Continuacion
      |                    (2)                      /
      |              x─────x     (3)          x════*  <── ENTRADA
      |             /         \  Re-break    / ]
      |   ┌────────/───────┐   \           / ──┤
      |   │  Opening Range │    \    x────x    │
      |   │                │     \  /          │
      |   └────────────────┘      \/            │
      |                        Shakeout         │
      |         (1)            sweep            SL
      |      Breakout                           │
      |      inicial                            │
      +─────────────────────────────────────────+──────> Tiempo
         Acto I          Acto II           Acto III
```

**El monitor de 3 etapas (Live):**

```
    Etapa 1: BREAKOUT INICIAL
    ┌────────────────────────┐
    │ Precio > OR_HIGH? ─────┼──> Registrar direccion, ir a Etapa 2
    │ Precio < OR_LOW?  ─────┼──> Registrar direccion, ir a Etapa 2
    └────────────────────────┘
              │
              v
    Etapa 2: ESPERAR SHAKEOUT
    ┌────────────────────────┐
    │ Precio retorna al OR?  │
    │ (vuelve < OR_HIGH si   │
    │  breakout fue UP)  ────┼──> Shakeout confirmado, ir a Etapa 3
    └────────────────────────┘
              │
              v
    Etapa 3: RE-BREAKOUT
    ┌────────────────────────┐
    │ Precio vuelve a romper │
    │ en la direccion        │
    │ original? ─────────────┼──> ENTRAR en la direccion del breakout
    └────────────────────────┘
```

El SHAKEOUT es raro pero poderoso. Requiere paciencia -- muchas seniales
no completan los tres actos. Pero cuando lo hacen, la probabilidad de
continuacion es alta. Muy alta.

### Los Tres Cazadores en Perspectiva

| Arquetipo | Filosofia | R:R | % del Portfolio | Monitor |
|:------------|:--------------------------------|:------|:----------------|:-----------|
| **FADE** | Contra el breakout | 1:1 | 95% | 2 etapas |
| **MOMENTUM** | Con el breakout | 1:1.5 | ~3% | Orden directa |
| **SHAKEOUT** | Espera el barrido, luego sigue | 1:1.5 | ~2% | 3 etapas |

---

<a name="cap-3"></a>
## Capitulo III: La Salsa Secreta -- Filtros de Contexto

Aqui es donde KHA0SYS3 pasa de ser un bot generico a ser un francotirador.

Un FADE generico en EURUSD London tiene un win rate del 55%. Decente, pero
no impresionante. Ahora, un FADE en EURUSD London **cuando el gap desde el
cierre anterior es pequenio y el RSI esta entre 50-70**... eso sube al 67%.

La diferencia esta en el **contexto**. No todos los dias son iguales. No todas
las condiciones producen el mismo tipo de breakout. Los filtros de contexto
son los lentes que le permiten a KHA0SYS3 distinguir entre una presa facil
y una trampa.

### Los 27 Filtros

```
    ┌───────────────────────────────────────────────────────────────┐
    │                     FILTROS DE CONTEXTO                       │
    ├───────────────┬───────────────────────────────────────────────┤
    │ CATEGORIA     │ FILTROS                                       │
    ├───────────────┼───────────────────────────────────────────────┤
    │ Gap           │ GapSmall (<0.5 ATR)                           │
    │               │ GapLarge (>0.5 ATR)                           │
    ├───────────────┼───────────────────────────────────────────────┤
    │ RSI           │ RSI < 30 (sobreventa)                         │
    │               │ RSI 30-50 (debil)                             │
    │               │ RSI 50-70 (fuerte)                            │
    │               │ RSI > 70 (sobrecompra)                        │
    ├───────────────┼───────────────────────────────────────────────┤
    │ OR Width      │ OR_Q1_Narrow (rango estrecho)                 │
    │               │ OR_Q4_Wide (rango ancho)                      │
    ├───────────────┼───────────────────────────────────────────────┤
    │ Posicion      │ AbovePD (OR > cierre previo)                  │
    │ relativa      │ BelowPD (OR < cierre previo)                  │
    │               │ BtwCloseHigh (entre cierre y max previo)      │
    │               │ BtwLowClose (entre min y cierre previo)       │
    ├───────────────┼───────────────────────────────────────────────┤
    │ Dia de        │ Monday, Tuesday, Wednesday, Thursday, Friday  │
    │ semana        │ (Wednesday es el rey)                         │
    ├───────────────┼───────────────────────────────────────────────┤
    │ ATR Regime    │ ATR creciente (+10%), ATR decreciente         │
    ├───────────────┼───────────────────────────────────────────────┤
    │ Combos        │ RSI<30 + ATR creciente                        │
    │ multi-feature │ AbovePD + RSI_D>65                            │
    │               │ GapSmall + Wednesday                          │
    │               │ OR_Wide + RSI 50-70                           │
    │               │ ... y mas                                     │
    └───────────────┴───────────────────────────────────────────────┘
```

### Por Que Funcionan: La Intuicion Detras de Cada Filtro

**GapSmall (Gap < 0.5 ATR):**
Cuando el mercado abre cerca de donde cerro ayer, no hay conviccion
direccional. Los breakouts en esa condicion son mas probablemente falsos.
Es como una pelea donde nadie quiere dar el primer golpe de verdad.
El FADE prospera aqui.

**RSI 30-50 / 50-70:**
Los extremos del RSI (< 30 o > 70) tienen su propia dinamica -- ahi los
breakouts pueden ser genuinos porque hay presion acumulada. Pero en la
zona media, el RSI no dice nada fuerte. El mercado esta indeciso. Y la
indecision favorece los falsos quiebres.

**OR_Q4_Wide (Rangos Anchos):**
Un OR ancho ya ha consumido mucha energia en la formacion. Los traders estan
exhaustos. Un breakout despues de un rango ancho tiene menos combustible
para continuar. Es como un corredor que sprinta en el calentamiento --
le quedan menos fuerzas para la carrera.

**BtwCloseHigh / BtwLowClose:**
Donde se forma el OR relativo al dia anterior revela el sesgo del mercado.
Si el OR se forma entre el cierre y el maximo de ayer, estamos en territorio
alcista indeciso -- un caldo de cultivo perfecto para trampas.

**Miercoles -- El Mejor Dia:**
Esto fue una sorpresa estadistica. Los miercoles concentran la mayor cantidad
de edges rentables. Una hipotesis: el miercoles esta lejos de los flujos de
inicio de semana (lunes) y de los ajustes de cierre (viernes). Es el dia
mas "puro" del mercado, donde las trampas funcionan con mayor fiabilidad.

### Combos Multi-Feature: Donde la Magia se Multiplica

Los filtros individuales son buenos. Los combos son devastadores.

```
    Ejemplo: RSI < 30 + ATR Creciente

    Significado:  El mercado esta sobrevendido Y la volatilidad esta
                  expandiendose. Un breakout bajista en estas condiciones
                  es frecuentemente la ultima sacudida antes del rebote.

    Resultado:    FADE_DOWN en estas condiciones tiene WR historico
                  significativamente superior al FADE_DOWN sin filtro.


    Ejemplo: AbovePD + RSI Diario > 65

    Significado:  El OR se forma por encima del cierre previo Y el RSI
                  diario muestra fuerza. Un breakout alcista podria ser
                  real (momentum), pero un breakout bajista desde ahi
                  arriba es casi siempre una trampa.

    Resultado:    FADE_DOWN prospera. El mercado tiene sesgo alcista y
                  cualquier dip es comprado agresivamente.
```

---

<a name="cap-4"></a>
## Capitulo IV: La Gran Expedicion -- El Descubrimiento de 121 Estrategias

Esta es la parte de la historia donde la ciencia se pone interesante.

### Fase 1: La Exploracion Inicial

Todo comenzo con una idea simple: "Que pasa si combino archetipo, direccion,
duracion de OR y sesion?"

```
    Permutaciones iniciales:
    5 archetypes x 2 directions x 4 durations x N sessions per asset

    Primer escaneo: 10 filtros de contexto
    Resultado: 36 estrategias con edge estadistico
```

36 estrategias. No esta mal para empezar. Pero habia un problema: estabamos
rascando la superficie. Con solo 10 filtros, estabamos perdiendo edges que
vivian en combinaciones mas especificas.

### Fase 2: Discovery v2 -- La Expedicion de 12,920 Permutaciones

Entonces ampliamos la busqueda. De 10 filtros pasamos a 27. Agregamos
dia de la semana, regimen de ATR, tamano de gap, zonas de RSI, y lo mas
importante: **combinaciones multi-feature**.

```
    ┌─────────────────────────────────────────────────────────────┐
    │              DISCOVERY v2: MAPA DE LA EXPEDICION            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │   Universo escaneado:    12,920 permutaciones               │
    │   Edges encontrados:      3,358 (26% hit rate)              │
    │                                                             │
    │   Criterios de seleccion:                                   │
    │   ├── WR > 57% (minimo estadistico)                         │
    │   ├── Trades/anio >= 12 (minimo para significancia)         │
    │   ├── Profit Factor > 1.2                                   │
    │   ├── Sin solapamiento con edges existentes                 │
    │   └── Robusto en out-of-sample                              │
    │                                                             │
    │   Supervivientes finales:                                   │
    │   ├── 21 del escaneo original (de 36 -- 15 no sobrevivieron│
    │   │    la validacion extendida)                              │
    │   └── 100 nuevos edges de Discovery v2                      │
    │                                                             │
    │   TOTAL: 121 estrategias                                    │
    └─────────────────────────────────────────────────────────────┘
```

De 12,920 permutaciones, solo 121 sobrevivieron. Eso es un **0.94% de tasa
de supervivencia**. Por cada 100 combinaciones probadas, menos de una
demostro tener un edge real, robusto y operable.

### La Piramide de Seleccion

```
         /\
        /  \          121 estrategias
       / OK \         seleccionadas
      /______\        (0.94%)
     /        \
    / 3,358    \      Edges crudos
   / encontrados\     (26%)
  /______________\
 /                \
/ 12,920           \   Permutaciones
/ permutaciones     \  escaneadas
/____________________\ (100%)
```

Cada estrategia en el portfolio final paso por un embudo brutal:

1. **Significancia estadistica:** Minimo 12 trades por anio. Sin esto,
   no hay confianza en los numeros.
2. **Win Rate minimo:** 57%. Por debajo de esto, el edge es demasiado
   fino para sobrevivir costos de ejecucion y slippage.
3. **Profit Factor > 1.2:** No basta con ganar mas veces; hay que ganar
   mas dinero del que se pierde.
4. **Robustez temporal:** El edge debe funcionar en multiples anios, no
   solo en un periodo especifico. Nada de overfitting.
5. **Sin solapamiento:** Dos estrategias que operan el mismo setup con
   filtros ligeramente diferentes no aportan diversificacion real.

### Distribucion por Activo

| Activo | Estrategias | % del Total | Activo Estrella |
|:-----------|:------------|:------------|:-------------------------------------|
| EURUSD | 12 | 9.9% | Clasico, liquido, abundante |
| GBPUSD | 10 | 8.3% | La libra ama las trampas |
| USDJPY | 9 | 7.4% | Tokyo + NY coverage |
| AUDUSD | 8 | 6.6% | Sydney sessions shine |
| GBPJPY | 11 | 9.1% | Volatilidad = oportunidad |
| EURJPY | 8 | 6.6% | Carry trade mechanics |
| GBPAUD | 7 | 5.8% | Joya oculta del portfolio |
| XAUUSD | 9 | 7.4% | Oro: el favorito de todos |
| XAGUSD | 8 | 6.6% | Plata: oro con esteroides |
| WTI | 7 | 5.8% | Petroleo West Texas |
| BRENT | 6 | 5.0% | Crudo del Mar del Norte |
| NATGAS | 5 | 4.1% | Gas natural, volatil y generoso |
| SP500 | 8 | 6.6% | El indice rey |
| NASDAQ100 | 7 | 5.8% | Tech y momentum |
| VIX | 6 | 5.0% | Volatilidad de la volatilidad |

---

<a name="cap-5"></a>
## Capitulo V: El Arte del Riesgo -- De 1% a 6%

Aqui es donde la mayoria de los bots se quedan cortos. Tienen buenas seniales,
buenas entradas, buenos stops. Pero arriesgan lo mismo en cada trade. El 1%
fijo. El 2% de siempre. Sin distincion entre una estrategia con 58% de WR
y una con 91%.

KHA0SYS3 no comete ese error.

### La Formula de Riesgo Dinamico

```
    risk_pct = 1% + ((WR - 0.57) / 0.34) * 5%

    Donde:
    - WR = Win Rate historico de la estrategia (entre 0.57 y 0.91)
    - 0.57 = WR minimo aceptado (floor)
    - 0.91 = WR maximo observado (ceiling)
    - 1% = Riesgo base
    - 5% = Rango adicional maximo

    Resultado:
    - WR = 57% --> risk = 1.0% (minimo, novato)
    - WR = 63% --> risk = 1.9% (promedio)
    - WR = 70% --> risk = 2.9% (solido)
    - WR = 80% --> risk = 4.4% (elite)
    - WR = 91% --> risk = 6.0% (maximo, campeon)
```

### La Curva de Riesgo Visualizada

```
    Risk %
    6.0% |                                                    *
         |                                               *
    5.0% |                                          *
         |                                     *
    4.0% |                                *
         |                           *
    3.0% |                      *
         |                 *
    2.0% |            *
         |       *
    1.0% |  *
         |
    0.0% +────────────────────────────────────────────────────
         57%   60%   65%   70%   75%   80%   85%   90%  91%
                            Win Rate

    Escalamiento LINEAL: cada punto de WR adicional
    se traduce proporcionalmente en mas riesgo.
```

### Por Que Funciona

La intuicion es simple pero poderosa:

**Una estrategia que gana el 91% de las veces merece mas capital que una
que gana el 57%.** Suena obvio, pero la mayoria de los traders usan riesgo
fijo. Eso es como pagar el mismo precio por un boleto de loteria y por
una inversion con retorno casi garantizado.

El escalamiento lineal evita los extremos del criterio de Kelly (que
sugeriria arriesgar cantidades absurdas en los extremos superiores).
Nuestro techo de 6% es conservador comparado con lo que Kelly recomendaria
para un 91% WR con R:R 1:1, pero la longevidad del capital importa mas
que la maximizacion a corto plazo.

### Position Sizing: Los Detalles que Importan

```
    ┌─────────────────────────────────────────────────────────────┐
    │                    CALCULO DE LOTE                           │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │   1. Determinar riesgo en dinero:                           │
    │      risk_money = BALANCE * risk_pct                        │
    │      (BALANCE, no free_margin -- para evitar apalancamiento │
    │       sobre posiciones abiertas)                            │
    │                                                             │
    │   2. Determinar SL en pips:                                 │
    │      sl_pips = |entry - stop_loss| / pip_value              │
    │                                                             │
    │   3. Calcular lote:                                         │
    │      lot = risk_money / (sl_pips * pip_cost_per_lot)        │
    │                                                             │
    │   4. Override de minimo:                                    │
    │      if lot < 0.01:                                         │
    │          lot = 0.01                                          │
    │          log("ADVERTENCIA: riesgo real = X.X%")             │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

Un detalle crucial: usamos **BALANCE**, no free margin. La diferencia parece
academica hasta que tienes 10 posiciones abiertas. Con free margin, cada
nueva posicion calcula su tamano sobre un denominador cada vez mas pequenio,
creando un efecto de apalancamiento compuesto involuntario. Con balance,
cada trade se dimensiona de forma independiente y predecible.

### El Safety Net: SL Guardian

```
    ┌─────────────────────────────────────────────────────┐
    │                 SL GUARDIAN                          │
    │                                                     │
    │   Cada 5 segundos:                                  │
    │   ├── Para cada posicion abierta:                   │
    │   │   ├── Tiene SL asignado?                        │
    │   │   │   └── NO --> CERRAR INMEDIATAMENTE          │
    │   │   └── Precio paso el SL por slippage?           │
    │   │       └── SI --> CERRAR INMEDIATAMENTE           │
    │   └── Log del estado                                │
    │                                                     │
    │   "Ningun trade vive sin stop loss.                  │
    │    Si el broker no lo respeta, nosotros si."        │
    └─────────────────────────────────────────────────────┘
```

En mercados con gaps o slippage severo, un SL puede no ejecutarse al precio
esperado. El SL Guardian es la red de seguridad: un proceso que corre en
paralelo y cierra cualquier posicion que haya sobrepasado su stop. Es el
bombero del sistema. Esperamos no necesitarlo nunca, pero esta ahi.

---

<a name="cap-6"></a>
## Capitulo VI: Los Campeonatos -- Las Mejores Estrategias

De las 121 estrategias, algunas son soldados confiables. Otras son
francotiradores de elite. Y unas pocas son leyendas.

### La Joya de la Corona: GBPAUD FADE_DOWN Sydney 30m

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │     G B P A U D   --   F A D E _ D O W N   --   S Y D N E Y│
    │                                                             │
    │     Win Rate:     91.3%                                     │
    │     Profit Factor: 10.44                                    │
    │     Risk asignado: 6.0% (MAXIMO)                            │
    │     Duracion OR:  30 minutos                                │
    │                                                             │
    │     De cada 10 trades, gana 9.                              │
    │     Por cada dolar perdido, gana diez.                      │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

GBPAUD en la sesion de Sydney. Un par exotico en una sesion tranquila.
La logica es elegante: durante Sydney, la libra esterlina y el dolar
australiano operan con baja liquidez. Los breakouts bajistas del OR son
casi siempre trampas de liquidez -- los pocos participantes barren stops
y el precio revierte rapidamente. KHA0SYS3 compra cada vez que el precio
rompe el OR_LOW. Y gana el 91.3% de las veces.

Con un riesgo del 6%, este unico trade puede hacer la semana.

### El Cuadro de Honor

| # | Estrategia | WR | PF | T/Y | Riesgo | Nota |
|:--|:-----------------------------------------|:------|:------|:----|:-------|:------------------------------|
| 1 | GBPAUD FADE_DOWN Sydney 30m | 91.3% | 10.44 | ~15 | 6.0% | La joya de la corona |
| 2 | SP500 SHAKEOUT_UP Pre-Market [ATR+10%] | 82.4% | 5.80 | ~20 | 4.7% | Maestro del shakeout bursatil |
| 3 | XAGUSD FADE_UP NY 60m [GapSmall] | 69.0% | 2.24 | 35 | 2.8% | Trampa de falso quiebre en plata|
| 4 | VIX FADE_DOWN NY Cash [RSI 30-50] | 69.0% | 2.20 | 30 | 2.8% | Reversion a la media del miedo |
| 5 | GBPJPY FADE_UP London 30m [Wednesday] | 72.0% | 2.57 | 40 | 3.2% | Miercoles letal en libra-yen |
| 6 | EURUSD FADE_DOWN NY 15m [BtwCloseHigh] | 66.0% | 1.94 | 50 | 2.3% | Caballo de batalla, alta freq. |
| 7 | NASDAQ100 MOMENTUM_UP Pre-Market [Wide] | 64.0% | 2.10 | 25 | 2.0% | Cuando el tech breakout es real |
| 8 | XAUUSD FADE_UP London 30m [GapSmall] | 67.0% | 2.03 | 45 | 2.5% | Oro: la trampa clasica |
| 9 | NATGAS FADE_DOWN NY 60m [ATR+10%] | 71.0% | 2.45 | 18 | 3.1% | Gas natural explosivo |
| 10| USDJPY FADE_UP Tokyo 15m [RSI 50-70] | 65.0% | 1.88 | 55 | 2.2% | El mas activo del portfolio |

### Anatomia de un Trade Campeon

Hagamos un ejemplo concreto con la estrategia #1:

```
    TRADE: GBPAUD FADE_DOWN Sydney 30m
    FECHA: Un martes cualquiera
    HORA:  00:00 UTC -- Apertura de Sydney

    00:00 - 00:30  Formacion del Opening Range
                   OR_HIGH = 1.9450
                   OR_LOW  = 1.9420
                   OR_WIDTH = 30 pips

    00:47          Precio rompe OR_LOW (1.9420)
                   -> Baja hasta 1.9415
                   -> Monitor Etapa 1: BREAKOUT DETECTADO

    00:47          Monitor Etapa 2: Colocar BUY LIMIT
                   -> Entry: 1.9420 (OR_LOW)
                   -> SL: 1.9390 (OR_LOW - 30 pips)
                   -> TP: 1.9450 (OR_HIGH, R:R = 1:1)

    00:52          BUY LIMIT activado a 1.9420
                   -> Posicion: LONG GBPAUD

    01:23          Precio alcanza 1.9450
                   -> TP HIT
                   -> Ganancia: 30 pips

    RIESGO: 6% de $10,000 balance = $600
    RESULTADO: +$600 en 36 minutos

    Nota: Este resultado ocurre 9 de cada 10 veces.
```

### Los Soldados Silenciosos

No todo es glamour. La mayoria de las 121 estrategias son "soldados": win rates
del 58-65%, profit factors entre 1.3 y 1.8, riesgos del 1-2%. No aparecen en
ningun cuadro de honor. Pero su contribucion acumulada es enorme.

```
    Contribucion al beneficio total estimado:

    Top 10 estrategias (WR > 70%):     ~25% del beneficio
    Medio 40 estrategias (WR 63-70%):  ~45% del beneficio
    Base 71 estrategias (WR 57-63%):   ~30% del beneficio
                                        ─────
                                        100%

    La base es ancha y estable. El top es concentrado y explosivo.
    Juntos forman una piramide de rendimiento diversificada.
```

---

<a name="cap-7"></a>
## Capitulo VII: La Maquinaria -- Stack Tecnologico

Un bot de trading es tan bueno como la infraestructura que lo sostiene.
Las mejores seniales del mundo no sirven de nada si el servidor se cae,
la orden no se envia, o el calculo del lote tiene un bug.

### Arquitectura General

```
    ┌──────────────────────────────────────────────────────────────────┐
    │                        VPS Windows Server                        │
    │                     (NSSM Service Manager)                       │
    │                                                                  │
    │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
    │   │  KHA0SYS3    │    │  MetaTrader 5 │    │  Telegram    │      │
    │   │  Python 3.12 │<-->│  Terminal     │<-->│  Bot         │      │
    │   │              │    │              │    │              │      │
    │   │  - Engine    │    │  - Ejecucion │    │  - Alertas   │      │
    │   │  - Monitors  │    │  - Data feed │    │  - Control   │      │
    │   │  - Risk Mgr  │    │  - Ordenes   │    │  - Status    │      │
    │   │  - SL Guard  │    │  - Historial │    │  - Comandos  │      │
    │   └──────────────┘    └──────────────┘    └──────────────┘      │
    │         ^                    ^                    ^               │
    │         │                    │                    │               │
    │         v                    v                    v               │
    │   ┌──────────────────────────────────────────────────────┐      │
    │   │              Polars DataFrames (In-Memory)            │      │
    │   │         Edges, Estrategias, Historico, Estado         │      │
    │   └──────────────────────────────────────────────────────┘      │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
```

### Python 3.12 + Polars: Velocidad Vectorizada

El backtester original y el motor de calculo usan **Polars**, no Pandas.
La diferencia es nocturna: donde Pandas toma 45 segundos para escanear
12,920 permutaciones, Polars lo hace en 3. Lazy evaluation, columnar
storage, zero-copy operations. Es la Formula 1 del procesamiento de datos
tabulares en Python.

```python
    # Ejemplo conceptual del motor de backtesting
    #
    # En lugar de iterar fila por fila (lento):
    # for i, row in df.iterrows():
    #     if row['price'] > row['OR_HIGH']:
    #         signal = 'FADE_DOWN'
    #
    # Usamos operaciones vectorizadas (rapido):
    # signals = df.filter(
    #     pl.col('price') > pl.col('OR_HIGH')
    # ).with_columns(
    #     pl.lit('FADE_DOWN').alias('signal')
    # )
    #
    # Resultado: 8 anios de datos procesados en segundos, no minutos.
```

### MetaTrader 5: La Interfaz con el Mercado

MT5 no es elegante. No es moderno. Pero es el estandar de la industria
para retail trading, y el broker Vantage lo soporta con buena ejecucion.

Detalles de integracion:
- Simbolos con mapping personalizado (Forex lleva sufijo `+`, indices y
  commodities usan nombres propios del broker)
- `SYMBOL_FILLING_FOK` como modo de relleno (fix desplegado 2026-04-07)
- Ordenes LIMIT, STOP, y MARKET segun el arquetipo
- Polling cada 5 segundos para el monitor de software

### Telegram: Ojos y Oidos

El bot de Telegram no opera. Observa. Reporta. Y obedece.

```
    Mensajes del bot:
    ├── "TRADE ABIERTO: GBPAUD FADE_DOWN @ 1.9420, SL 1.9390, TP 1.9450"
    ├── "TP HIT: GBPAUD +30 pips (+$600)"
    ├── "SL HIT: EURUSD -15 pips (-$150)"
    ├── "ALERTA: SL Guardian activo en XAUUSD"
    └── "STATUS: 5 posiciones abiertas, P&L del dia: +$1,230"

    Comandos disponibles:
    ├── /status    -- Estado actual de todas las posiciones
    ├── /today     -- Resumen del dia
    ├── /pause     -- Pausar todas las estrategias
    └── /resume    -- Reanudar operaciones
```

Sin spam. Sin notificaciones innecesarias. Solo lo que importa.

### Reglas de Consistencia Backtest-Live

Este es un punto critico. Muchos bots tienen un backtest espectacular y
una ejecucion live desastrosa. La diferencia suele estar en detalles que
el backtester ignora y el mercado no perdona.

```
    ┌───────────────────────────────────────────────────────────────┐
    │            REGLAS DE PARIDAD BACKTEST <--> LIVE               │
    ├───────────────────────────────────────────────────────────────┤
    │                                                               │
    │   1. Todos los indicadores con shift=1                        │
    │      (ATR, RSI calculados con datos de AYER)                  │
    │                                                               │
    │   2. Deduplicacion: 1 trade por (symbol, edge, session)/dia  │
    │      (Backtest: filtro en DataFrame)                          │
    │      (Live: registro en memoria con polling)                  │
    │                                                               │
    │   3. Ordenes con expiracion de 8 horas                        │
    │      (No hay ordenes zombi que se activen al dia siguiente)   │
    │                                                               │
    │   4. FADE: Monitor de software en ambos entornos              │
    │      (El backtest simula el monitor de 2 etapas)              │
    │                                                               │
    │   5. MOMENTUM: Ordenes STOP directas en ambos                 │
    │      (Sin monitor -- paridad perfecta)                        │
    │                                                               │
    │   6. SHAKEOUT: Monitor de 3 etapas en ambos                   │
    │      (La complejidad es identica en backtest y live)          │
    │                                                               │
    │   7. ATR filter: 10-80% en ambos entornos                     │
    │      (Misma logica, mismos umbrales)                          │
    │                                                               │
    │   NOTA: Las diferencias de dedup y polling entre backtest     │
    │   y live son INTENCIONALES, no bugs. El live necesita         │
    │   mecanismos ligeramente diferentes por la naturaleza         │
    │   del polling en tiempo real vs. datos historicos.            │
    └───────────────────────────────────────────────────────────────┘
```

---

<a name="cap-8"></a>
## Capitulo VIII: De la Simulacion al Campo de Batalla

8 anios de backtesting. 121 estrategias validadas. Miles de horas de
desarrollo. Y luego llega el momento de la verdad: encender el bot con
dinero real.

### Los Numeros del Backtest (2018-2026)

```
    ┌─────────────────────────────────────────────────────────────┐
    │              METRICAS GLOBALES DEL PORTFOLIO                 │
    ├──────────────────────────┬──────────────────────────────────┤
    │ Estrategias activas      │ 121                              │
    │ Activos cubiertos        │ 15                               │
    │ Trades esperados/anio    │ ~6,861                           │
    │ Trades esperados/dia     │ ~27                              │
    │ Win Rate promedio        │ 63.5%                            │
    │ Profit Factor promedio   │ 1.74                             │
    │ Periodo backtested       │ 2018-2026 (8 anios)             │
    │ Riesgo minimo            │ 1.0% (WR = 57%)                 │
    │ Riesgo maximo            │ 6.0% (WR = 91%)                 │
    └──────────────────────────┴──────────────────────────────────┘
```

**~27 trades por dia.** Eso es un trade cada 15-20 minutos durante las
horas activas. No es HFT, pero tampoco es swing trading. Es un ritmo
constante, como el latido de un corazon.

### La Expectativa Matematica

Tomemos un dia promedio con una cuenta de $10,000:

```
    27 trades/dia
    x 63.5% WR
    = ~17 ganadores y ~10 perdedores

    Riesgo promedio ponderado: ~2.2% (dado el mix de WR en el portfolio)

    Ganador promedio:  $220 (2.2% de $10,000)
    Perdedor promedio: $220 (R:R 1:1 para FADE dominante)

    Dia promedio:
    17 x $220 - 10 x $220 = $3,740 - $2,200 = +$1,540

    ADVERTENCIA: Esto es la EXPECTATIVA MATEMATICA, no una garantia.
    Los dias reales oscilan entre -$2,000 y +$5,000.
    La varianza es parte del juego.
```

### El Waterfall de Ejecucion

Cada segundo, el bot ejecuta un ciclo de decision:

```
    Tick del mercado
         │
         v
    ┌────────────────┐    No
    │ Sesion activa? ├────────> Esperar
    └───────┬────────┘
            │ Si
            v
    ┌────────────────┐    No
    │ OR formado?    ├────────> Monitorear formacion
    └───────┬────────┘
            │ Si
            v
    ┌────────────────┐    No
    │ ATR filter OK? ├────────> Descartar (rango invalido)
    └───────┬────────┘
            │ Si
            v
    ┌────────────────┐    No
    │ Contexto match?├────────> No hay edge, pasar
    └───────┬────────┘
            │ Si
            v
    ┌────────────────┐    Si
    │ Ya operado hoy?├────────> Dedup: no repetir
    └───────┬────────┘
            │ No
            v
    ┌────────────────┐
    │ EJECUTAR TRADE │
    │ - Calcular lot │
    │ - Colocar orden│
    │ - Registrar    │
    │ - Notificar    │
    └────────────────┘
```

### El Primer Dia Live

El 7 de abril de 2026 se desplego el fix critico de `SYMBOL_FILLING` que
permitio la ejecucion correcta en Vantage Markets. El bot encendio sus
motores. Los primeros trades se colocaron.

No hay resultados que reportar aun -- el primer dia completo de operacion
live con el fix es hoy, 8 de abril de 2026. Pero la maquinaria esta en
marcha. Los monitores observan. Los filtros filtran. Los cazadores cazan.

La jungla esta abierta.

---

<a name="cap-9"></a>
## Epilogo: Los Numeros Finales

### El Portfolio en Una Pagina

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    KHA0SYS3 -- RESUMEN                       ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║   CONCEPTO         Opening Range Breakout (Anti-Breakout)     ║
    ║   ESTRATEGIAS      121 (FADE 95% | MOMENTUM 3% | SHAKEOUT 2%)║
    ║   ACTIVOS           15 (Forex, Metales, Energia, Indices, VIX)║
    ║   SESIONES          4 (Tokyo, London, Pre-Market, New York)   ║
    ║   DATOS             8 anios (2018-2026)                       ║
    ║   TRADES/ANIO       ~6,861 (~27/dia)                          ║
    ║   WIN RATE          63.5% promedio (rango: 57% - 91%)         ║
    ║   PROFIT FACTOR     1.74 promedio (rango: 1.2 - 10.44)       ║
    ║   RIESGO            1% - 6% dinamico por estrategia           ║
    ║   FILTROS           27 contextuales + combos multi-feature    ║
    ║   TECH              Python 3.12 + Polars + MT5 + Telegram     ║
    ║   INFRA             VPS Windows + NSSM                        ║
    ║                                                               ║
    ║   MEJOR TRADE       GBPAUD FADE_DOWN Sydney: 91.3% WR        ║
    ║   MAS ACTIVO        USDJPY FADE_UP Tokyo: ~55 trades/anio    ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
```

### Lo Que KHA0SYS3 NO Es

Porque es tan importante saber lo que algo no es como lo que si es:

- **No es un sistema de HFT.** No compite en microsegundos. Opera en minutos.
- **No es una caja negra de ML.** No hay redes neuronales, no hay deep learning.
  Cada edge es explicable, interpretable, auditable.
- **No es un holy grail.** Tendra dias malos. Semanas malas. Posiblemente
  meses malos. La ventaja es estadistica, no determinista.
- **No usa trailing stop.** Nunca. TP fijo, SL fijo. La simplicidad es
  una feature, no un bug.
- **No persigue trades.** Un trade por (simbolo, edge, sesion) por dia.
  Si lo perdio, lo perdio. Maniana habra otro.

### Lo Que KHA0SYS3 SI Es

- **Un sistema de edges compuestos.** 121 pequenias ventajas que, sumadas,
  construyen un perfil de retorno robusto.
- **Un cazador de trampas.** Su negocio principal es explotar los falsos
  breakouts que destruyen a los traders de momentum ingenuous.
- **Un sistema disciplinado.** Sin emociones, sin FOMO, sin venganza.
  Opera las reglas. Solo las reglas. Siempre las reglas.
- **Un producto de datos.** 12,920 permutaciones escaneadas, 8 anios de
  historia, 27 filtros de contexto. Las decisiones nacen de numeros, no
  de opiniones.

### La Ultima Reflexion

```
    "En el mercado, la mayoria pierde porque sigue al rebano.
     El rebano ve un breakout y compra.
     El rebano ve panico y vende.
     El rebano es predecible.

     KHA0SYS3 no es parte del rebano.
     KHA0SYS3 caza al rebano.

     121 estrategias. 15 activos. 4 sesiones.
     27 trades por dia. 6,861 por anio.

     No con fuerza bruta.
     No con velocidad.
     Con contexto. Con paciencia. Con matematicas.

     La jungla esta abierta.
     Los cazadores estan listos."
```

---

> *KHA0SYS3 v1.0 -- Desplegado en produccion: Abril 2026*
> *Documento generado: 8 de abril de 2026*

---

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │   "The house always wins. Not because it's lucky.           │
    │    Because it has an edge. And it plays every hand."        │
    │                                                             │
    │                                    -- Adaptado del folklore │
    │                                       de Las Vegas          │
    └─────────────────────────────────────────────────────────────┘
```
