# Guia de Infraestructura VPS — Kha0sys

Referencia completa para conectar, desplegar y configurar nuevas estrategias en el VPS.

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

### Conectarse desde Python (winrm)

```python
import winrm

session = winrm.Session(
    'https://85.239.230.215:5986/wsman',
    auth=('Administrator', 'Violetica906'),
    transport='basic',
    server_cert_validation='ignore'
)
result = session.run_ps('Get-Date')
print(result.std_out.decode())
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

- **Config activa:** `C:\Proyectos\Kha0sys\config\broker.yaml`
- **Template:** `C:\Proyectos\Kha0sys\config\broker.yaml.template`

```yaml
# broker.yaml (live)
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

- **Config activa:** `C:\Proyectos\Kha0sys\config\telegram.yaml`

```yaml
token: "8268613194:AAF1Dt15QXwUGAA4M_A8xrDqNMoSiYbpoyk"
chat_id: "778542603"
group_chat_id: "-5170985767"
```

### Como modificar el bot de Telegram

1. **Cambiar el token/chat_id:** Editar `config/telegram.yaml` en local y desplegar con `deploy/_deploy_changes.py`
2. **Modificar mensajes/alertas:** Editar `src/monitoring/telegram_pro.py`
3. **Agregar nuevo grupo:** Agregar `group_chat_id` en `telegram.yaml`, el bot manda mirror a ambos (personal + grupo)
4. **Comandos admin:** Solo responde en chat personal (778542603), el grupo es solo lectura

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

```
MetaTrader5>=5.0.45
polars>=1.0           # <-- SI esta instalado
pyarrow>=15.0
duckdb>=0.10
numpy>=1.26
scipy>=1.12
scikit-learn>=1.4
hmmlearn>=0.3
filterpy>=1.4
riskfolio-lib>=6.0
optuna>=3.5
python-telegram-bot>=21.0
streamlit>=1.30
plotly>=5.18
pyyaml>=6.0
psutil>=5.9
requests
```

### Comando de instalacion de paquetes

```powershell
python -m pip install polars pyarrow duckdb numpy scipy scikit-learn hmmlearn filterpy riskfolio-lib optuna streamlit plotly pyyaml psutil requests MetaTrader5
```

Para instalar paquetes adicionales para una nueva estrategia:

```python
# Desde local via WinRM
session.run_ps('C:\\Python312\\python.exe -m pip install <paquete_nuevo>')
```

---

## 5. Servicios NSSM (Auto-start)

### Kha0sysBot (Bot de Trading Principal)

| Campo             | Valor                                                    |
|-------------------|----------------------------------------------------------|
| Service Name      | `Kha0sysBot`                                             |
| Executable        | `C:\Python312\python.exe`                                |
| Arguments         | `-u C:\Proyectos\Kha0sys\scripts\run_bot_supervisor.py`  |
| Working Dir       | `C:\Proyectos\Kha0sys`                                   |
| Startup           | AUTO_START                                               |
| Restart Delay     | 10,000 ms (10s)                                          |
| Stdout Log        | `C:\Proyectos\Kha0sys\logs\bot_stdout.log`               |
| Stderr Log        | `C:\Proyectos\Kha0sys\logs\bot_stderr.log`               |
| Log Rotation      | Habilitado (10MB max)                                    |

### Kha0sysWatchdog (Monitoreo)

| Campo             | Valor                                                                                          |
|-------------------|------------------------------------------------------------------------------------------------|
| Service Name      | `Kha0sysWatchdog`                                                                              |
| Executable        | `C:\Python312\python.exe`                                                                      |
| Arguments         | `-u C:\Proyectos\Kha0sys\scripts\watchdog.py --db C:\Proyectos\Kha0sys\data\live_state\kha0sys_live.db` |
| Working Dir       | `C:\Proyectos\Kha0sys`                                                                        |
| Startup           | AUTO_START                                                                                     |
| Restart Delay     | 5,000 ms (5s)                                                                                  |
| Stdout Log        | `C:\Proyectos\Kha0sys\logs\watchdog_stdout.log`                                               |
| Stderr Log        | `C:\Proyectos\Kha0sys\logs\watchdog_stderr.log`                                               |

### Tarea Programada

| Campo        | Valor                                |
|--------------|--------------------------------------|
| Nombre       | `Kha0sysWeeklyRestart`               |
| Horario      | Domingos 20:00 UTC                   |
| Accion       | Reinicia bot + watchdog              |

### Comandos NSSM utiles

```powershell
# Ver estado de servicios
nssm status Kha0sysBot
nssm status Kha0sysWatchdog

# Parar / Iniciar (NO usar restart, es poco confiable)
nssm stop Kha0sysBot
nssm start Kha0sysBot

# Ver logs en tiempo real
Get-Content C:\Proyectos\Kha0sys\logs\bot_stdout.log -Tail 50

# Registrar un nuevo servicio
nssm install NuevoServicio C:\Python312\python.exe "-u C:\Proyectos\Kha0sys\scripts\nuevo_script.py"
nssm set NuevoServicio AppDirectory C:\Proyectos\Kha0sys
nssm set NuevoServicio AppStdout C:\Proyectos\Kha0sys\logs\nuevo_stdout.log
nssm set NuevoServicio AppStderr C:\Proyectos\Kha0sys\logs\nuevo_stderr.log
nssm set NuevoServicio AppRestartDelay 10000
nssm start NuevoServicio
```

---

## 6. Estructura de Directorios en VPS

```
C:\Proyectos\Kha0sys\
├── config\
│   ├── broker.yaml          # Credenciales MT5
│   ├── telegram.yaml        # Credenciales Telegram
│   ├── risk_params.yaml     # Parametros de riesgo
│   ├── instruments.yaml     # 14 instrumentos (5 asset classes)
│   └── settings.yaml        # Timeframes y pesos MTF
├── scripts\
│   ├── run_demo_live.py     # Entry point del bot (V7.1)
│   ├── run_bot_supervisor.py # Supervisor que lanza run_demo_live
│   └── watchdog.py          # Monitor independiente
├── src\
│   ├── signals\
│   │   ├── signal_generator_v6.py    # Pipeline V6 Trend
│   │   └── signal_generator_v6_mr.py # Pipeline V6 MR
│   └── monitoring\
│       └── telegram_pro.py  # Notificaciones Telegram
├── data\
│   ├── live_state\          # Base de datos del estado live
│   ├── parquet\             # Datos historicos
│   └── optuna_v7_*_best.json # Params optimizados por instrumento
├── logs\
│   ├── bot_stdout.log
│   ├── bot_stderr.log
│   ├── watchdog_stdout.log
│   └── watchdog_stderr.log
└── deploy\                  # Scripts de despliegue (se ejecutan desde LOCAL)
```

---

## 7. Scripts de Deploy (se ejecutan desde tu PC local)

| Script                        | Proposito                                             |
|-------------------------------|-------------------------------------------------------|
| `_deploy_changes.py`         | Sube archivos modificados y reinicia bot               |
| `_check_bot.py`              | Verifica estado del bot remoto                         |
| `_restart.py`                | Reinicia el servicio del bot                           |
| `_nssm_start.py`             | Inicia servicios NSSM                                 |
| `_register_services.py`      | Registra nuevos servicios NSSM                         |
| `vps_diagnose.py`            | Diagnostico completo del VPS                           |
| `vps_verify.py`              | Verifica config MT5 y Telegram en VPS                  |
| `vps_setup_services.py`      | Configura servicios NSSM via WinRM                     |
| `vps_start.py`               | Inicia servicios y muestra logs                        |
| `fix_configs.py`             | Corrige archivos de config en VPS                      |
| `_pull_and_verify.py`        | Git pull + verificacion de config                      |
| `deploy_live.ps1`            | Setup completo del VPS desde cero                      |

### Flujo tipico para desplegar una nueva estrategia

```bash
# 1. Desarrollar y probar localmente

# 2. Subir cambios al VPS
python deploy/_deploy_changes.py

# 3. Verificar que todo esta bien
python deploy/vps_verify.py

# 4. Diagnosticar si hay problemas
python deploy/vps_diagnose.py

# 5. Reiniciar si es necesario
python deploy/_restart.py
```

---

## 8. Como Instalar una Nueva Estrategia

### Checklist rapido

1. **Verificar dependencias:** Si tu nueva estrategia usa paquetes no listados arriba, instalarlos via WinRM:
   ```python
   session.run_ps('C:\\Python312\\python.exe -m pip install <paquete>')
   ```

2. **Subir archivos:** Usar `_deploy_changes.py` como base, o crear un nuevo script de deploy que suba los archivos necesarios via base64 + WinRM.

3. **Configurar credenciales:** Reutilizar `config/broker.yaml` y `config/telegram.yaml` existentes, o crear configs nuevas para la estrategia.

4. **Registrar servicio NSSM:** Si la nueva estrategia corre como proceso independiente:
   ```powershell
   nssm install NuevaEstrategia C:\Python312\python.exe "-u C:\Proyectos\NuevaEstrategia\main.py"
   nssm set NuevaEstrategia AppDirectory C:\Proyectos\NuevaEstrategia
   nssm set NuevaEstrategia AppStdout C:\Proyectos\NuevaEstrategia\logs\stdout.log
   nssm set NuevaEstrategia AppStderr C:\Proyectos\NuevaEstrategia\logs\stderr.log
   nssm set NuevaEstrategia AppRestartDelay 10000
   nssm start NuevaEstrategia
   ```

5. **Telegram:** Reutilizar el mismo bot token y chat_id, solo importar `telegram_pro.py` o usar requests directamente.

6. **Verificar:** Revisar logs en `C:\Proyectos\...\logs\` y usar `vps_diagnose.py` adaptado.

---

## 9. Parametros de Riesgo Actuales (V7.1)

| Parametro           | Valor              |
|---------------------|---------------------|
| Base Risk/Trade     | 0.30% (global)      |
| ATR SL Multiplier   | 5.50 (global)       |
| Partial Close       | 80% @ 2.00R         |
| Trailing            | 20% restante         |
| Max Portfolio Heat  | 7%                  |
| Circuit Breakers    | Daily 6%, Weekly 10%, Monthly 20%, Max DD 25% |
| Cooldown            | 16 bars M15 (4h)    |
| Time Stop           | 12 bars M15 (3h)    |

**Nota:** V7.1 usa parametros PER-INSTRUMENT que sobreescriben estos globales. Ver archivos `data/optuna_v7_*_best.json`.

---

## 10. Instrumentos Activos

### V7.1 Live (7 combos en 5 simbolos)

| Instrumento   | Estrategia | Risk   | SL ATR | Partial       | Max Bars |
|---------------|-----------|--------|--------|---------------|----------|
| NASDAQ100     | Trend     | 0.25%  | 3.75   | 25% @ 4.0R    | 88       |
| NASDAQ100     | MR        | 0.60%  | 5.75   | 20% @ 1.7R    | 76       |
| SP500         | Trend     | 1.10%  | 3.75   | 15% @ 3.3R    | 64       |
| USDJPY        | Trend     | 0.35%  | 5.0    | 45% @ 1.8R    | 72       |
| USDJPY        | MR        | 1.10%  | 6.0    | 55% @ 1.6R    | 100      |
| EURUSD        | MR        | 0.25%  | 6.0    | 55% @ 2.2R    | 40       |
| WTI           | MR        | 0.60%  | 5.0    | 50% @ 2.0R    | 68       |

---

*Documento generado: 2026-04-06*
*Para la estrategia Kha0sys V7.1 corriendo en VPS 85.239.230.215*
