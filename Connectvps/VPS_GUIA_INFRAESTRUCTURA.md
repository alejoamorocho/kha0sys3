# Guia de Infraestructura VPS — Kha0sys3

Referencia completa para conectar, desplegar y operar el bot Kha0sys3 en el VPS.

---

> **Nota de seguridad:** todos los valores sensibles (IP, usuarios, passwords,
> tokens) viven en `.env` (gitignored). Esta guia describe **estructura**, no
> credenciales. Plantilla en `.env.example` en la raiz del repo.

## 1. Conexion al VPS

| Campo        | Origen                        |
|--------------|-------------------------------|
| IP           | `$VPS_IP` (.env)              |
| Puerto       | `$VPS_PORT` (default 5986)    |
| Protocolo    | WinRM (HTTPS)                 |
| Usuario      | `$VPS_USER` (.env)            |
| Password     | `$VPS_PASS` (.env)            |
| OS           | Windows Server                |

### Conectarse desde Python (modulo integrado)

```python
from deploy.vps_connection import VPSConnection  # lee .env automaticamente

vps = VPSConnection()
if vps.test_connection():
    result = vps.run_ps("Get-Date")
    print(result["stdout"])
```

### Conectarse desde PowerShell (remoto)

```powershell
# Credenciales se piden interactivamente — nunca se hardcodean.
$cred = Get-Credential
$session = New-PSSession -ComputerName $env:VPS_IP -Port 5986 -UseSSL `
    -Credential $cred -SessionOption (New-PSSessionOption -SkipCACheck -SkipCNCheck)
Enter-PSSession $session
```

---

## 2. Credenciales MT5

Las credenciales reales viven en `.env` (`MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER`)
o en `config/broker.yaml` (gitignored). Este documento solo describe el formato.

### Estructura `config/broker.yaml`

```yaml
login: <numero de cuenta MT5>
password: "<password>"
server: "<nombre del servidor MT5, p.ej. VantageInternational-Demo>"
```

### Estructura `.env`

```
MT5_LOGIN=<numero>
MT5_PASSWORD=<password>
MT5_SERVER=<server>
```

`MT5Client.connect()` lee `config/broker.yaml` y fuerza login con esas
credenciales, validando que `account_info().login` coincida.

---

## 3. Credenciales Telegram Bot

| Campo          | Origen                                |
|----------------|---------------------------------------|
| Bot Token      | `$TELEGRAM_TOKEN` (.env)              |
| Chat ID        | `$TELEGRAM_CHAT_ID` (.env)            |
| Group Chat ID  | `$TELEGRAM_GROUP_CHAT_ID` (.env)      |

### Estructura `config/telegram.yaml` (legacy, gitignored)

```yaml
token: "<bot token>"
chat_id: "<personal chat id>"
group_chat_id: "<group chat id>"
```

`TelegramNotifier` y `TelegramCommandBot` priorizan variables de entorno y
solo caen al yaml si las env vars no estan definidas.

### Como modificar el bot de Telegram

1. **Cambiar el token/chat_id:** Editar `config/telegram.yaml` y hacer deploy con `deploy/pull_and_restart.py`
2. **Modificar mensajes/alertas:** Editar `src/monitoring/telegram_bot.py` (interactivo) o `src/monitoring/telegram_notifier.py` (push legacy)
3. **Agregar nuevo grupo:** Agregar `group_chat_id` en `telegram.yaml`, el bot manda mirror a ambos (personal + grupo)
4. **Comandos admin:** Solo responde en el chat personal del admin (`$TELEGRAM_CHAT_ID`), el grupo es solo lectura

### Notificaciones que envia el bot

| Evento | Emoji | Descripcion |
|--------|-------|-------------|
| Bot iniciado | 🚀 | Portfolio activo, riesgo/trade, hora |
| Bot detenido | 🛑 | Razon del stop |
| ORB detectado | 📊 | High, Low, Width del rango |
| Orden colocada | 🟢/🔴 | Entry, SL, TP, Lotes |
| Orden rechazada | ⚠️ | Razon del rechazo |
| Spread alto | ⚠️ | Spread actual vs promedio |
| Exposicion bloqueada | 🛡️ | Ya hay posiciones abiertas |
| Trade cerrado | 🦋/💥 | Win/Loss, PnL, comision |
| Heartbeat | 💓 | Balance, equity, PnL dia (cada 15min) |
| Salud sistema | 🚨 | CPU/RAM/disco critico, MT5 offline |
| Limpieza ordenes | 🧹 | Ordenes huerfanas canceladas |

---

## 4. Software Instalado en el VPS

### Sistema Base

| Software       | Version/Path                    |
|----------------|---------------------------------|
| Python         | 3.12.7 en `C:\Python312`       |
| NSSM           | v2.24 en `C:\nssm\nssm.exe`    |
| Git            | v2.47.1                         |
| MetaTrader 5   | Instalado (terminal + paquete Python 5.0.5735) |

### Paquetes Python Instalados

Ver `requirements.txt` en la raiz del proyecto.

---

## 5. Servicios NSSM (Auto-start)

### Kha0sysBot3 (Bot de Trading Principal)

| Campo             | Valor                                                      |
|-------------------|------------------------------------------------------------|
| Service Name      | `Kha0sysBot3`                                              |
| Executable        | `C:\Python312\python.exe`                                  |
| Arguments         | `-u C:\Proyectos\kha0sys3\scripts\run_bot_supervisor.py`   |
| Working Dir       | `C:\Proyectos\kha0sys3`                                    |
| Startup           | AUTO_START                                                 |
| Restart Delay     | 10,000 ms (10s)                                            |
| Stdout Log        | `C:\Proyectos\kha0sys3\logs\bot_stdout.log`                |
| Stderr Log        | `C:\Proyectos\kha0sys3\logs\bot_stderr.log`                |
| Log Rotation      | Habilitado (10MB max)                                      |

### Kha0sysWatchdog3 (Monitoreo)

| Campo             | Valor                                                      |
|-------------------|------------------------------------------------------------|
| Service Name      | `Kha0sysWatchdog3`                                         |
| Executable        | `C:\Python312\python.exe`                                  |
| Arguments         | `-u C:\Proyectos\kha0sys3\scripts\watchdog.py`             |
| Working Dir       | `C:\Proyectos\kha0sys3`                                    |
| Startup           | AUTO_START                                                 |
| Restart Delay     | 5,000 ms (5s)                                              |
| Stdout Log        | `C:\Proyectos\kha0sys3\logs\watchdog_stdout.log`           |
| Stderr Log        | `C:\Proyectos\kha0sys3\logs\watchdog_stderr.log`           |

### Kha0sysMathBot (MATH parallel runner, magic 1338)

| Campo             | Valor                                                      |
|-------------------|------------------------------------------------------------|
| Service Name      | `Kha0sysMathBot`                                           |
| Executable        | `C:\Python312\python.exe`                                  |
| Arguments         | `-u C:\Proyectos\kha0sys3\scripts\run_math_bot_supervisor.py --live` (o `--dry-run`) |
| Working Dir       | `C:\Proyectos\kha0sys3`                                    |
| Magic Number      | 1338 (aislado del FADE bot magic 1337)                     |
| Startup           | AUTO_START                                                 |
| Restart Delay     | 10,000 ms (10s)                                            |
| Stdout Log        | `C:\ProgramData\Kha0sysMath\logs\math_bot.log`             |
| Stderr Log        | `C:\ProgramData\Kha0sysMath\logs\math_bot_err.log`         |
| Log Rotation      | Habilitado (10MB max)                                      |
| Config            | `src/execution/bot_config_math.json`                       |
| Mode flip         | `nssm stop` → `nssm set Kha0sysMathBot AppParameters "..."` → `nssm start` (ver footer de `deploy/deploy_math_bot.py`) |

**Importante:** `deploy/pull_and_restart.py` cubre los 3 servicios y NO toca
`AppParameters`, por lo que preserva el modo `--live`/`--dry-run` actual.
`deploy/deploy_math_bot.py` SI reinstala el servicio y resetea a `--dry-run`
— úsalo solo para instalación inicial o si necesitas resetear configuración.

### Tarea Programada

| Campo        | Valor                                |
|--------------|--------------------------------------|
| Nombre       | `Kha0sys3WeeklyRestart`              |
| Horario      | Domingos 20:00 UTC                   |
| Accion       | Reinicia Kha0sysBot3 + Kha0sysWatchdog3 |

### Comandos NSSM utiles

```powershell
# Ver estado de servicios
nssm status Kha0sysBot3
nssm status Kha0sysWatchdog3
nssm status Kha0sysMathBot

# Parar / Iniciar (NO usar restart, es poco confiable)
nssm stop Kha0sysBot3
nssm start Kha0sysBot3
nssm stop Kha0sysMathBot
nssm start Kha0sysMathBot

# Ver logs en tiempo real
Get-Content C:\Proyectos\kha0sys3\logs\bot_stdout.log -Tail 50
Get-Content C:\ProgramData\Kha0sysMath\logs\math_bot.log -Tail 50
```

---

## 6. Estructura de Directorios en VPS

```
C:\Proyectos\kha0sys3\
├── config\
│   ├── broker.yaml              # Credenciales MT5
│   └── telegram.yaml            # Credenciales Telegram
├── scripts\
│   ├── run_bot_supervisor.py    # Supervisor que lanza LiveTraderEngine
│   └── watchdog.py              # Monitor independiente
├── src\
│   ├── application\             # Use Cases & Business Logic
│   ├── domain\                  # Domain Models & Interfaces
│   ├── engine\                  # Backtester & Optimization
│   ├── execution\               # Live Trading (MT5, Orders, Risk)
│   │   ├── live_trader.py       # LiveTraderEngine principal
│   │   ├── mt5_client.py        # Gateway MT5
│   │   ├── order_manager.py     # Ciclo de vida de ordenes
│   │   ├── risk_manager.py      # Calculo de riesgo/lotaje (DynamicRiskAllocator + SLGuardian)
│   │   └── bot_config.json      # Portfolio y parametros
│   ├── infrastructure\          # Config & Data loaders
│   ├── monitoring\
│   │   ├── telegram_bot.py      # Bot interactivo con comandos (async, python-telegram-bot)
│   │   ├── telegram_notifier.py # Notificaciones push (sync, requests — usado por supervisor/watchdog)
│   │   ├── mt5_reporter.py      # Datos reales MT5 (PnL, posiciones)
│   │   └── system_health.py     # Salud del sistema (CPU, RAM, MT5)
│   └── optimize\                # Optuna runners
├── data\
│   ├── live_state\              # Estado persistente (daily_trades.json)
│   └── *.csv                    # Datos historicos
├── reports\                     # Edge analysis & tearsheets
├── deploy\                      # Scripts de despliegue (LOCAL)
├── logs\                        # Logs de servicios + bot_heartbeat
└── requirements.txt             # Dependencias Python
```

---

## 7. Scripts de Deploy (se ejecutan desde tu PC local)

| Script                        | Proposito                                             |
|-------------------------------|-------------------------------------------------------|
| `deploy/deploy_new_bot.py`   | Deploy inicial FADE bot: elimina viejo, clona, configura NSSM |
| `deploy/deploy_math_bot.py`  | Deploy/reinstall MATH bot (RESETEA a --dry-run, usar solo para setup inicial) |
| `deploy/check_bot.py`        | Verifica estado del bot remoto                         |
| `deploy/restart_bot.py`      | Reinicia los servicios del bot                         |
| `deploy/pull_and_restart.py` | Git pull + reinicio de los 3 servicios (FADE + Watchdog + MATH). Preserva AppParameters (modo --live/--dry-run del MATH). |
| `deploy/vps_diagnose.py`     | Diagnostico completo del VPS                           |
| `deploy/vps_connection.py`   | Modulo de conexion WinRM (usado por los demas scripts) |

### Flujo tipico de operacion

```bash
# 1. Deploy inicial (primera vez)
python deploy/deploy_new_bot.py

# 2. Actualizar codigo (cambios futuros)
python deploy/pull_and_restart.py

# 3. Verificar estado
python deploy/check_bot.py

# 4. Diagnosticar problemas
python deploy/vps_diagnose.py

# 5. Reiniciar si es necesario
python deploy/restart_bot.py
```

---

## 8. Parametros de Trading (ORB Strategy)

### Portfolio Activo (5 activos)

| Instrumento | MT5 Symbol | Magic Time (UTC) | Edge      | Duraciones | Riesgo/Trade |
|-------------|-----------|------------------|-----------|------------|--------------|
| USDJPY      | USDJPY+   | 00:00            | TREND_UP  | 15m, 30m   | 3.0%         |
| Oro (XAU)   | XAUUSD+   | 07:00            | TREND_UP  | 15m, 30m   | 3.0%         |
| EURUSD      | EURUSD+   | 07:00            | TREND_UP  | 15m, 30m   | 3.0%         |
| Petroleo    | USOUSD    | 07:00            | TREND_UP  | 15m, 30m   | 3.0%         |
| S&P 500     | SP500     | 12:00            | TREND_UP  | 15m, 30m   | 3.0%         |

### Logica ORB TREND_UP (consistente con backtest)

1. A la hora `magic_time + duration`, lee las barras M15 **CERRADAS** anteriores
2. Define Opening Range: High/Low de esas barras cerradas (1 barra para 15m, 2 para 30m)
3. **Filtro ATR14:** Calcula ATR(14) desde barras D1 (shifted, sin look-ahead). Si `or_width / atr14` esta fuera de [0.1, 0.8], descarta y avanza al siguiente duration (waterfall)
4. Coloca **BUY_STOP** en el OR High
5. SL = OR Low (extremo opuesto del rango)
6. TP = OR High + (rango * 1.5) = +1.5R
7. Lotaje calculado por DynamicRiskAllocator sobre **BALANCE** (no free_margin)
8. **Un trade por activo por dia** — si ya hay fill o cancellation, no re-entra
9. **Trend Monitor (Software OCO):** Si el precio toca OR Low primero, cancela el BUY_STOP

### Waterfall de Duraciones

Cada activo tiene duraciones [15m, 30m]. Si el ATR filter rechaza con 15m, el bot reintenta automaticamente con 30m en la siguiente ventana. Si ambas fallan, skip del dia para ese activo.

### Filtros Defensivos

- **ATR14 Filter:** Rechaza si or_atr_ratio fuera de [0.1, 0.8] (consistente con backtest)
- **Spread Filter:** Rechaza si spread > 1.5x baseline (con piso minimo de 5 puntos)
- **One-Trade-Per-Day:** Un solo trade por activo por edge por dia (persistido en disco)
- **Exposure Check:** No coloca ordenes si ya hay posiciones/ordenes en el simbolo
- **Volume Check:** Rechaza si lotaje < volume_min del broker
- **Expiracion Hardware:** ORDER_TIME_SPECIFIED a 8 horas (broker mata la orden si Python cae)
- **Limpieza Software:** wipe_stale_orders() cada hora (complementa hardware)
- **Magic Number:** 1337 (identifica ordenes del bot)

### SL Guardian (Proteccion de Emergencia)

Monitorea posiciones abiertas cada 10s. Si detecta que el precio cruzo el SL sin cerrar (gap/flash crash), cierra la posicion a mercado inmediatamente y notifica por Telegram.

### Seguridad y Resiliencia

- **Reconexion MT5:** Automatica con backoff exponencial (3 intentos)
- **Error Isolation:** try/except por simbolo — un fallo no afecta otros
- **Thread Safety:** Lock en flags de control (_paused)
- **Watchdog:** Servicio NSSM independiente que reinicia el bot si cae o si no hay heartbeat por 2min
- **Supervisor:** Max 5 crashes con cooldown de 30s, NSSM reinicia el supervisor
- **Estado Persistente:** daily_trades.json sobrevive reinicios, se resetea a medianoche UTC
- **Timezone:** Todo UTC via datetime.now(timezone.utc)

### Telegram — Comandos Admin

| Comando     | Descripcion |
|-------------|-------------|
| /start      | Panel de control |
| /status     | Estado completo (cuenta, posiciones, salud) |
| /balance    | Balance y equity en tiempo real |
| /pnl        | P&L realizado del dia |
| /weekly     | P&L semanal |
| /monthly    | P&L mensual |
| /positions  | Posiciones abiertas con detalle |
| /orders     | Ordenes pendientes |
| /health     | CPU, RAM, disco, estado MT5 |
| /stop       | Detener trading (cancela ordenes pendientes, posiciones siguen activas) |
| /resume     | Reanudar trading |

### Telegram — Notificaciones Automaticas

- **Cada 15 min:** Heartbeat con balance, equity, P&L del dia, estado MT5
- **Cada 5 min:** Check de salud del sistema (CPU, RAM, disco, MT5)
- **Por evento:** ORB detectado, orden colocada/rechazada, trade cerrado (🦋 win / 💥 loss)
- **Alertas:** Spread alto, MT5 desconectado, CPU/RAM/disco critico, crash del bot

### Intervalos del Loop Principal

| Funcion | Intervalo |
|---------|-----------|
| Process symbols | 10s (cada tick del loop) |
| Check positions & fills | 10s |
| MT5 reconnect check | 60s |
| System health check | 300s (5 min) |
| Heartbeat Telegram | 900s (15 min) |
| Stale order cleanup | 3600s (1 hora) |

---

*Documento actualizado: 2026-05-10 (agregada seccion Kha0sysMathBot / magic 1338)*
*FADE: portfolio K3-97, R:R individual por estrategia (ver `project_rr_optimization`), SL Guardian activo*
*MATH: portfolio multi-TF (M1/M15/H1/H4), Optuna 3-regime, inverted momentum, magic 1338*
*Cuenta activa post-migracion 2026-05-08: DEMO 25246666 @ VantageInternational-Demo*
*Para Kha0sys3 corriendo en VPS (`$VPS_IP`)*
