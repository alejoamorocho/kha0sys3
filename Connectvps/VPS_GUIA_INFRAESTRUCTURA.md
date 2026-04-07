# Guia de Infraestructura VPS — Kha0sys3

Referencia completa para conectar, desplegar y operar el bot Kha0sys3 en el VPS.

---

## 1. Conexion al VPS

| Campo        | Valor                        |
|--------------|------------------------------|
| IP           | `85.239.230.215`             |
| Puerto       | `5986` (WinRM over HTTPS)    |
| Protocolo    | WinRM (Windows Remote Mgmt)  |
| Usuario      | `Administrator`              |
| Password     | `Violetica906`               |
| OS           | Windows Server               |

### Conectarse desde Python (modulo integrado)

```python
from deploy.vps_connection import VPSConnection

vps = VPSConnection()
if vps.test_connection():
    result = vps.run_ps("Get-Date")
    print(result["stdout"])
```

### Conectarse desde PowerShell (remoto)

```powershell
$cred = Get-Credential  # Administrator / Violetica906
$session = New-PSSession -ComputerName 85.239.230.215 -Port 5986 -UseSSL -Credential $cred -SessionOption (New-PSSessionOption -SkipCACheck -SkipCNCheck)
Enter-PSSession $session
```

---

## 2. Credenciales MT5

### Cuenta Live (ACTIVA)

| Campo    | Valor                             |
|----------|-----------------------------------|
| Login    | `23540222`                        |
| Password | `Frotas1429!`                     |
| Server   | `VantageInternational-Live 5`     |
| Broker   | Vantage International (ECN)       |
| Leverage | 1:500                             |

### Cuenta Demo

| Campo    | Valor                             |
|----------|-----------------------------------|
| Login    | `11877944`                        |
| Password | `Frotas1429.`                     |
| Server   | `VantageInternational-Demo`       |

### Archivos de configuracion

- **Config activa:** `C:\Proyectos\kha0sys3\config\broker.yaml`

```yaml
login: 23540222
password: "Frotas1429!"
server: "VantageInternational-Live 5"
```

### Variables de entorno en VPS

```
MT5_LOGIN=23540222
MT5_PASSWORD=Frotas1429!
MT5_SERVER=VantageInternational-Live 5
```

---

## 3. Credenciales Telegram Bot

| Campo          | Valor                                                  |
|----------------|--------------------------------------------------------|
| Bot Token      | `8268613194:AAF1Dt15QXwUGAA4M_A8xrDqNMoSiYbpoyk`     |
| Chat ID (personal) | `778542603`                                       |
| Group Chat ID  | `-5170985767`                                          |

### Archivo de configuracion

- **Config activa:** `C:\Proyectos\kha0sys3\config\telegram.yaml`

```yaml
token: "8268613194:AAF1Dt15QXwUGAA4M_A8xrDqNMoSiYbpoyk"
chat_id: "778542603"
group_chat_id: "-5170985767"
```

### Como modificar el bot de Telegram

1. **Cambiar el token/chat_id:** Editar `config/telegram.yaml` y hacer deploy con `deploy/pull_and_restart.py`
2. **Modificar mensajes/alertas:** Editar `src/monitoring/telegram_notifier.py`
3. **Agregar nuevo grupo:** Agregar `group_chat_id` en `telegram.yaml`, el bot manda mirror a ambos (personal + grupo)
4. **Comandos admin:** Solo responde en chat personal (778542603), el grupo es solo lectura

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
| Estado de cuenta | 📈 | Balance, Equity, Margen, Posiciones |
| Heartbeat | 💓 | Uptime, trades del dia |
| Error critico | ❌ | Contexto y mensaje del error |
| Limpieza ordenes | 🧹 | Ordenes huerfanas canceladas |

---

## 4. Software Instalado en el VPS

### Sistema Base

| Software       | Version/Path                    |
|----------------|---------------------------------|
| Python         | 3.12.7 en `C:\Python312`       |
| NSSM           | v2.24 en `C:\nssm\nssm.exe`    |
| Git            | v2.47.1                         |
| MetaTrader 5   | Instalado (terminal)            |

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

# Parar / Iniciar (NO usar restart, es poco confiable)
nssm stop Kha0sysBot3
nssm start Kha0sysBot3

# Ver logs en tiempo real
Get-Content C:\Proyectos\kha0sys3\logs\bot_stdout.log -Tail 50
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
│   │   ├── risk_manager.py      # Calculo de riesgo/lotaje
│   │   └── bot_config.json      # Portfolio y parametros
│   ├── infrastructure\          # Config & Data loaders
│   ├── monitoring\
│   │   ├── telegram_bot.py      # Bot interactivo con comandos
│   │   ├── telegram_notifier.py # Notificaciones push (legacy)
│   │   ├── mt5_reporter.py      # Datos reales MT5 (PnL, posiciones)
│   │   └── system_health.py     # Salud del sistema (CPU, RAM, MT5)
│   └── optimize\                # Optuna runners
├── data\                        # Datos historicos CSV
├── reports\                     # Edge analysis & tearsheets
├── deploy\                      # Scripts de despliegue (LOCAL)
├── logs\                        # Logs de servicios
└── requirements.txt             # Dependencias Python
```

---

## 7. Scripts de Deploy (se ejecutan desde tu PC local)

| Script                        | Proposito                                             |
|-------------------------------|-------------------------------------------------------|
| `deploy/deploy_new_bot.py`   | Deploy completo: elimina bot viejo, clona repo, configura servicios |
| `deploy/check_bot.py`        | Verifica estado del bot remoto                         |
| `deploy/restart_bot.py`      | Reinicia los servicios del bot                         |
| `deploy/pull_and_restart.py` | Git pull + reinicio de servicios                       |
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

### Portfolio Activo (Trinity)

| Instrumento | MT5 Symbol | Magic Time | TP Opt | Riesgo/Trade |
|-------------|-----------|-----------|--------|--------------|
| USDJPY      | USDJPY+   | 00:00 UTC | 0.8x   | 3.5%         |
| GBPUSD      | GBPUSD+   | 07:00 UTC | 0.7x   | 3.5%         |
| NASDAQ100   | NAS100    | 13:30 UTC | 0.7x   | 3.5%         |

### Logica ORB (consistente con backtest)

1. A la hora `magic_time`, lee la vela M15 **CERRADA** anterior (no la que se esta formando)
2. Define Opening Range: High/Low de esa vela cerrada
3. **Filtro ATR14:** Calcula ATR(14) desde barras D1. Si `or_width / atr14` esta fuera de [0.1, 0.8], descarta
4. Coloca BUY_STOP en el High y SELL_STOP en el Low
5. SL = extremo opuesto del rango
6. TP = entry + (rango * tp_opt)
7. Lotaje calculado por DynamicRiskAllocator sobre **BALANCE** (no free_margin)
8. **Un trade por activo por dia** — si first_break_dir ya ocurrio, no re-entra
9. Al detectar fill de una pierna, **cancela la opuesta** (OCO en software)

### Filtros Defensivos

- **ATR14 Filter:** Rechaza si or_atr_ratio fuera de [0.1, 0.8] (consistente con backtest)
- **Spread Filter:** Rechaza si spread > 1.5x baseline (con piso minimo de 5 puntos)
- **One-Trade-Per-Day:** Un solo trade por activo por dia (first_break_dir)
- **Exposure Check:** No coloca ordenes si ya hay posiciones/ordenes en el simbolo
- **Volume Check:** Rechaza si lotaje < volume_min del broker
- **Expiracion Hardware:** ORDER_TIME_SPECIFIED a 8 horas (broker mata la orden si Python cae)
- **Limpieza Software:** wipe_stale_orders() cada hora (complementa hardware)
- **Magic Number:** 1337 (identifica ordenes del bot)

### Seguridad y Resiliencia

- **Reconexion MT5:** Automatica con backoff exponencial (3 intentos)
- **Error Isolation:** try/except por simbolo — un fallo no afecta otros
- **Thread Safety:** Lock en flags de control (_paused)
- **Watchdog:** Servicio NSSM independiente que reinicia el bot si cae
- **Supervisor:** Max 5 crashes con cooldown, NSSM reinicia el supervisor
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
| /stop       | Detener trading (posiciones siguen activas) |
| /resume     | Reanudar trading |

### Telegram — Notificaciones Automaticas

- **Cada 15 min:** Heartbeat con balance, equity, P&L del dia, estado MT5
- **Por evento:** ORB detectado, orden colocada/rechazada, trade cerrado (🦋/💥)
- **Alertas:** Spread alto, MT5 desconectado, CPU/RAM/disco critico, crash del bot

---

*Documento actualizado: 2026-04-06*
*Refactored: Consistencia backtest-live, ATR14 filter, OCO, balance sizing*
*Para Kha0sys3 ORB Bot corriendo en VPS 85.239.230.215*
