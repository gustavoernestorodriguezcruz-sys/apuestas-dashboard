# 🏆 Apuestas Dashboard - Mundial 2026

Dashboard interactivo para análisis de apuestas deportivas de la Copa del Mundo 2026 con predicciones de probabilidades y Expected Value (EV).

## 📋 Descripción

Este proyecto automatiza la recopilación de:
- **Partidos programados** desde [Football-Data.org](https://www.football-data.org/)
- **Cuotas de apuestas** desde [The Odds API](https://the-odds-api.com/)
- **Predicciones** basadas en probabilidades implícitas y EV

El workflow ejecuta cada minuto actualizando `dashboard.json` con datos en tiempo real.

## 🚀 Características

✅ Actualización automática cada minuto  
✅ Filtrado por estado: En Vivo, Próximos, Finalizados  
✅ Cálculo de probabilidades implícitas  
✅ Análisis de Expected Value (EV)  
✅ Visualización gráfica de distribuciones  
✅ Cálculo de ganancias potenciales  

## 📦 Instalación Local

### Requisitos
- Python 3.10+
- pip

### Pasos

1. **Clonar repositorio**
```bash
git clone https://github.com/gustavoernestorodriguezcruz-sys/apuestas-dashboard.git
cd apuestas-dashboard
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
export FOOTBALL_DATA_KEY="tu_clave_football_data"
export ODDS_API_KEY="tu_clave_odds_api"
```

O crear archivo `.env`:
```
FOOTBALL_DATA_KEY=tu_clave_aqui
ODDS_API_KEY=tu_clave_aqui
```

5. **Ejecutar scripts manualmente**
```bash
python script.py     # Obtener partidos y cuotas
python predict.py    # Generar predicciones
```

## 🔑 Configuración de Secretos (GitHub Actions)

Para que el workflow automatizado funcione, debes configurar los siguientes secretos en GitHub:

### Paso 1: Ir a Configuración del Repositorio
```
https://github.com/tu-usuario/apuestas-dashboard/settings/secrets/actions
```

### Paso 2: Crear Secretos

#### 🔹 `FOOTBALL_DATA_KEY`
1. Ir a https://www.football-data.org/
2. Registrarse o iniciar sesión
3. Copiar tu API Key
4. En GitHub: Click en "New repository secret"
5. Name: `FOOTBALL_DATA_KEY`
6. Value: *tu_clave*
7. Click "Add secret"

#### 🔹 `ODDS_API_KEY`
1. Ir a https://the-odds-api.com/
2. Registrarse o iniciar sesión
3. Copiar tu API Key
4. En GitHub: Click en "New repository secret"
5. Name: `ODDS_API_KEY`
6. Value: *tu_clave*
7. Click "Add secret"

#### 🔹 `GH_TOKEN`
1. Ir a https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Asignar permisos: `repo` (acceso completo)
4. Copiar el token
5. En GitHub (repositorio): Click en "New repository secret"
6. Name: `GH_TOKEN`
7. Value: *tu_token*
8. Click "Add secret"

### Paso 3: Verificar Configuración
```
https://github.com/tu-usuario/apuestas-dashboard/settings/secrets/actions
```

Deberías ver 3 secretos listados:
- ✅ FOOTBALL_DATA_KEY
- ✅ ODDS_API_KEY
- ✅ GH_TOKEN

## 📁 Estructura del Proyecto

```
apuestas-dashboard/
├── index.html              # Frontend HTML
├── style.css               # Estilos CSS
├── extras.js               # Funciones JavaScript (gráficos)
├── config.json             # Configuración (saldo inicial)
├── dashboard.json          # Datos generados (auto-actualizado)
│
├── script.py               # Backend: Obtener partidos y cuotas
├── predict.py              # Backend: Generar predicciones
├── requirements.txt        # Dependencias Python
│
├── .github/workflows/
│   └── update.yml          # Workflow de GitHub Actions
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## 📊 Estructura de `dashboard.json`

```json
[
  {
    "home": "Canada",
    "away": "Qatar",
    "fecha": "2026-06-18T22:00:00Z",
    "estado": "inplay",
    "odds": {
      "home_win": 1.0,
      "draw": 56.0,
      "away_win": 201.0,
      "bookmakers": [...],
      "over_under": [...],
      "handicap": [...]
    },
    "prediction": {
      "prob_home": 0.98,
      "prob_draw": 0.02,
      "prob_away": 0.0,
      "ev_home": 0.98,
      "ev_draw": 1.12,
      "ev_away": 0.0,
      "recommendation": "draw",
      "best_ev": 1.12
    }
  }
]
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `home` | string | Nombre equipo local |
| `away` | string | Nombre equipo visitante |
| `fecha` | ISO datetime | Fecha y hora UTC |
| `estado` | string | `scheduled`, `inplay`, `finished` |
| `odds.home_win` | float | Cuota victoria local (H2H) |
| `odds.draw` | float | Cuota empate (H2H) |
| `odds.away_win` | float | Cuota victoria visitante (H2H) |
| `prediction.prob_home` | float | Probabilidad implícita local (0-1) |
| `prediction.prob_draw` | float | Probabilidad implícita empate (0-1) |
| `prediction.prob_away` | float | Probabilidad implícita visitante (0-1) |
| `prediction.recommendation` | string | `home`, `draw`, `away`, o `PASS` |
| `prediction.best_ev` | float | Mejor Expected Value encontrado |

### Estados

- **scheduled**: Partido programado (próximo)
- **inplay**: Partido en juego (en vivo)
- **finished**: Partido finalizado

## 🧮 Lógica de Predicciones

### Probabilidades Implícitas
Se calculan invertiendo las cuotas:
```
P(resultado) = (1/cuota) / Σ(1/cuota_i)
```

### Expected Value (EV)
```
EV = Probabilidad × Cuota
```

### Recomendación
- Si **EV > 1.0**: Apuesta favorable (home/draw/away)
- Si **EV ≤ 1.0**: **PASS** (sin valor positivo)

## 🔄 Workflow Automatizado

El workflow `.github/workflows/update.yml` ejecuta cada minuto:

1. **Checkout** del código
2. **Setup Python** 3.10
3. **Install dependencies** desde `requirements.txt`
4. **Run script.py**: Obtiene partidos y cuotas
5. **Run predict.py**: Genera predicciones
6. **Commit & push**: Actualiza `dashboard.json`

### Monitoreo

Ir a: `https://github.com/tu-usuario/apuestas-dashboard/actions`

Verás los últimos runs del workflow con logs en tiempo real.

## 📈 Frontend

Abre `index.html` en un navegador. El dashboard:
- Carga datos desde `dashboard.json`
- Filtra por pestaña (En Vivo, Próximos, Finalizados)
- Muestra predicciones y ganancias potenciales
- Visualiza distribuciones de probabilidades con Chart.js

## 🐛 Troubleshooting

### ❌ Workflow falla con error de API

**Solución**: Verifica que los secretos están configurados correctamente:
```bash
# En Actions > Workflow > Logs, busca:
# ✓ script.py ejecutó exitosamente
# ✓ predict.py añadió predicciones
```

### ❌ `dashboard.json` no se actualiza

**Solución**: Revisa si `GH_TOKEN` tiene permisos de escritura:
```bash
# En GitHub: Settings > Developer settings > Personal access tokens
# Verifica: repo (Full control of private repositories) ✅
```

### ❌ Estados JSON no filtran en frontend

**Solución**: Verifica que `script.py` normaliza estados:
```bash
# Busca en dashboard.json:
# "estado": "inplay"    ✅ (minúsculas, sin guion)
# "estado": "IN_PLAY"   ❌ (no coincide)
```

### ❌ Sin predicciones en algunos partidos

**Solución**: El script reporta cuáles partidos faltan odds:
```bash
# Logs de workflow:
# ⚠️ X partidos SIN odds:
#    - Team A - Team B
```

## 📝 Licencia

Este proyecto es de uso educativo/personal.

## 🤝 Soporte

Para reportar bugs o sugerencias, abre un issue en:
```
https://github.com/gustavoernestorodriguezcruz-sys/apuestas-dashboard/issues
```

---

**Última actualización:** 2026-06-18  
**Versión:** 1.0.0
