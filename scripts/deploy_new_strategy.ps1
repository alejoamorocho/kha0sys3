# ============================================================
# Kha0sys3 — Deploy New Alpha Portfolio Strategy to VPS
# ============================================================
# Run this script on the VPS as Administrator
# It pulls the latest code and restarts the bot services
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Kha0sys3 — Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_DIR = "C:\Proyectos\kha0sys3"
$NSSM = "C:\nssm\nssm.exe"
$BOT_SERVICE = "Kha0sysBot3"
$WATCHDOG_SERVICE = "Kha0sysWatchdog3"

# 1. Stop services
Write-Host "[1/5] Deteniendo servicios..." -ForegroundColor Yellow
& $NSSM stop $BOT_SERVICE 2>$null
& $NSSM stop $WATCHDOG_SERVICE 2>$null
Start-Sleep -Seconds 3
Write-Host "  Servicios detenidos." -ForegroundColor Green

# 2. Pull latest code
Write-Host "[2/5] Actualizando codigo..." -ForegroundColor Yellow
Set-Location $PROJECT_DIR
git pull origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: git pull fallo!" -ForegroundColor Red
    exit 1
}
Write-Host "  Codigo actualizado." -ForegroundColor Green

# 3. Verify critical files exist
Write-Host "[3/5] Verificando archivos criticos..." -ForegroundColor Yellow
$critical_files = @(
    "src/execution/bot_config.json",
    "src/execution/live_trader.py",
    "src/execution/order_manager.py",
    "src/execution/mt5_client.py",
    "src/execution/risk_manager.py",
    "config/broker.yaml",
    "config/telegram.yaml"
)
foreach ($f in $critical_files) {
    $path = Join-Path $PROJECT_DIR $f
    if (-not (Test-Path $path)) {
        Write-Host "  FALTA: $f" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  Todos los archivos presentes." -ForegroundColor Green

# 4. Verify bot_config.json has new portfolio
Write-Host "[4/5] Verificando configuracion..." -ForegroundColor Yellow
$config = Get-Content (Join-Path $PROJECT_DIR "src/execution/bot_config.json") | ConvertFrom-Json
$portfolio = $config.portfolio
if ($null -eq $portfolio) {
    $portfolio = $config.trinity_portfolio
}
Write-Host "  Portfolio: $($portfolio.Count) setups" -ForegroundColor Green
Write-Host "  Risk: $($config.risk_percent_per_trade * 100)% per trade" -ForegroundColor Green
foreach ($s in $portfolio) {
    Write-Host "    $($s.sym) | $($s.edge) | $($s.magic_time) | dur=$($s.durations -join ',')" -ForegroundColor Gray
}

# 5. Verify symbol names in MT5
Write-Host ""
Write-Host "  IMPORTANTE: Verificar que estos simbolos existen en Vantage MT5:" -ForegroundColor Yellow
Write-Host "    - USDJPY+  (Forex con +)" -ForegroundColor Yellow
Write-Host "    - XAUUSD   (Gold)" -ForegroundColor Yellow
Write-Host "    - EURUSD+  (Forex con +)" -ForegroundColor Yellow
Write-Host "    - USOIL    (WTI — verificar nombre exacto en Market Watch)" -ForegroundColor Yellow
Write-Host "    - SP500    (verificar nombre exacto en Market Watch)" -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Simbolos verificados en MT5? (s/n)"
if ($confirm -ne "s") {
    Write-Host "  Actualiza bot_config.json con los nombres correctos y re-ejecuta." -ForegroundColor Red
    exit 1
}

# 6. Restart services
Write-Host "[5/5] Reiniciando servicios..." -ForegroundColor Yellow
& $NSSM start $WATCHDOG_SERVICE
Start-Sleep -Seconds 2
& $NSSM start $BOT_SERVICE
Start-Sleep -Seconds 5

# Check status
$botStatus = & $NSSM status $BOT_SERVICE 2>&1
$wdStatus = & $NSSM status $WATCHDOG_SERVICE 2>&1
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Estado Post-Deploy:" -ForegroundColor Cyan
Write-Host "  Bot:      $botStatus" -ForegroundColor $(if ($botStatus -match "RUNNING") {"Green"} else {"Red"})
Write-Host "  Watchdog: $wdStatus" -ForegroundColor $(if ($wdStatus -match "RUNNING") {"Green"} else {"Red"})
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verifica en Telegram que el bot envie el mensaje de inicio." -ForegroundColor Yellow
Write-Host "Usa /status en Telegram para confirmar que todo esta OK." -ForegroundColor Yellow
