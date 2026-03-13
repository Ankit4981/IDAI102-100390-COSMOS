<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════╗
║  🚀  COSMOS MISSION CONTROL DASHBOARD  ·  v7.0.0                      ║
╚══════════════════════════════════════════════════════════════════════════╝
```

# 🚀 COSMOS Mission Control Dashboard

### *A production-grade aerospace analytics platform built with Streamlit*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75?style=flat-square&logo=plotly)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📋 Overview

**COSMOS Mission Control Dashboard** is a full-stack data analytics application that replicates the visual language and operational structure of real aerospace mission control systems used by **NASA**, **SpaceX**, **ESA**, and **ISRO**.

It combines **196 verified real historical space missions** (1966–2025) with an interactive **rocket physics simulation engine**, delivering an immersive mission control experience through a dark futuristic UI with a live animated space background.

---

## 📸 Screenshots

### 🔐 Mission Auth Terminal — Login Screen

![Login Terminal](screenshot_login.png)
*SHA-256 secured auth terminal with operator role selection and live system telemetry chips.*

---

### 🖥️ Mission Control Overview

![Mission Control Overview](screenshot_overview.png)
*Fleet KPIs, dual-axis annual launch trends, mission type donut chart, and vehicle performance analysis.*

---

### 📊 Mission Data Analytics

![Mission Data Analytics](screenshot_analytics.png)
*Five interactive Plotly charts — payload vs fuel scatter, cost analysis, duration vs distance, crew analysis, and scientific yield.*

---

### 🚀 Rocket Launch Simulation

![Rocket Launch Simulation](screenshot_simulation.png)
*Real-time physics engine (Newton's 2nd Law + exponential atmosphere), altitude/velocity telemetry, GO/NO-GO checklist, and altitude gauge.*

---

### 🔬 Scientific Insights

![Scientific Insights](screenshot_insights.png)
*Yield analysis with LOWESS trendlines, key analytical insight cards, violin distributions, and target performance comparison.*

---

<!-- ============================================================ -->
<!--   📸 DATASET EXPLORER SCREENSHOT — Add your image below      -->
<!-- ============================================================ -->
### 🗃️ Dataset Explorer

![Dataset Explorer](screenshots/dataset_explorer.png)
<!-- Drop screenshot here → screenshots/dataset_explorer.png      -->
<!-- Recommended size: 1200×700 px                                -->
<!-- ============================================================ -->

---

<!-- ============================================================ -->
<!--     📸 ANIMATED BACKGROUND GIF — Add your GIF below          -->
<!-- ============================================================ -->
### 🌌 Live Space Background Animation

![Space Background Animation](screenshots/background_animation.gif)
<!-- Drop an animated GIF here → screenshots/background_animation.gif -->
<!-- Recommended size: 1280×720 px                                -->
<!-- ============================================================ -->

---

## ✨ Features

### 🖥️ Aerospace-Grade UI
- **Dark space theme** with neon cyan / rocket orange accent colors
- **Live animated background** — Hubble Deep Field canvas animation with moving galaxies, twinkling stars, shooting stars, and a rocket flying across the screen
- **NASA / SpaceX-inspired** visual design with Orbitron, Share Tech Mono, and Exo 2 fonts
- **Fully responsive** layout with glassmorphism panels

### 🔐 Authentication System
- SHA-256 hashed credential verification
- **Mission Auth Terminal** login screen with live telemetry chips
- Operator role selection (Mission Analyst, Flight Engineer, Payload Specialist, Systems Commander)
- Animated boot-sequence loading screen on successful login

### 📊 Six Dashboard Screens

| Screen | Description |
|--------|-------------|
| **Mission Control Overview** | Fleet KPIs, annual launch trends (dual-axis), mission type donut chart, vehicle performance bar, destination bubble chart, Pearson correlation heatmap |
| **Mission Data Analytics** | 5 interactive Plotly charts — payload vs fuel scatter, cost analysis, duration vs distance, crew analysis, scientific yield |
| **Rocket Launch Simulation** | Real-time physics engine (Newton's 2nd Law + exponential atmosphere), 4 telemetry charts, altitude gauge, mission console log |
| **Scientific Insights** | Yield analysis with lowess trendlines, violin distributions, target performance with error bars, insight cards |
| **Dataset Explorer** | Full searchable/sortable data table, CSV export, descriptive statistics, column distributions |
| **About Project** | Mathematical model, tech stack, architecture docs, installation guide |

---

## 🚀 Physics Simulation Engine

Real-time Euler integration of the rocket equation:

```
F_net = F_thrust − m·g − F_drag
a     = F_net / m_total
ρ(h)  = 1.225 · exp(−h / 8500)   [kg/m³]
F_drag = ½ · ρ · Cᵈ · A · v²    [N]
m(t)  = m_dry + m_payload + m_fuel(t)
```

**Adjustable Parameters:**

| Parameter | Range | Default |
|-----------|-------|---------|
| Thrust | 500 – 12,000 kN | 4,200 kN |
| Dry Mass | 5,000 – 120,000 kg | 28,000 kg |
| Payload | 500 – 60,000 kg | 12,000 kg |
| Fuel | 5,000 – 600,000 kg | 180,000 kg |
| Drag Coefficient | 0.10 – 1.60 | 0.38 |
| Burn Rate | 50 – 2,500 kg/s | 480 kg/s |
| Time Step | 0.10 – 2.00 s | 0.50 s |

---

## 🛰️ Real Mission Data

**196 verified historical missions** from major space agencies:

```
Total Missions  : 196
Success Rate    : 93.4%
Date Range      : 1966 – 2025
Launch Vehicles : 36 unique
Destinations    : 11 (LEO, ISS, Moon, Mars, GEO, Jupiter, L2, Venus, Saturn, Mercury, MEO)
Mission Types   : Science · Crewed · Commercial · Tech Demo · Defense · Exploration
Crewed Missions : 65
Robotic Missions: 131
```

Agencies covered: **NASA · SpaceX · ESA · ISRO · CNSA · Roscosmos · JAXA · Blue Origin**

Notable missions: Apollo 11, Voyager 1 & 2, Hubble Space Telescope, ISS Expeditions, Mars Curiosity & Perseverance, JWST, Starship IFT series, Artemis I, Chandrayaan-3, and more.

---

## 🗂️ Project Structure

```
cosmos_app.py          ← Main application (single-file Streamlit app)
requirements.txt       ← Python dependencies
README.md              ← This file
screenshots/           ← Place additional screenshots here
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone or download the project
git clone https://github.com/yourusername/cosmos-mission-control.git
cd cosmos-mission-control

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run cosmos_app.py
```

### Custom Port / Theme
```bash
streamlit run cosmos_app.py --server.port 8080 --theme.base dark
```

The app will open at **http://localhost:8501** (default).

---

## 🔑 Demo Credentials

| Username   | Password   | Role                  |
|------------|------------|-----------------------|
| `admin`    | `rocket123`| Full access           |
| `engineer` | `nasa2024` | Engineering access    |
| `guest`    | `guest`    | Read-only access      |

---

## 🛠️ Tech Stack

| Library       | Version  | Purpose                                          |
|---------------|----------|--------------------------------------------------|
| `streamlit`   | ≥ 1.32   | Web app framework, UI components, state management |
| `pandas`      | ≥ 2.0    | Data manipulation, filtering, aggregation        |
| `numpy`       | ≥ 1.26   | Numerical computing, physics simulation          |
| `plotly`      | ≥ 5.20   | Interactive charts (Express + Graph Objects)     |
| `matplotlib`  | ≥ 3.8    | Seaborn integration, heatmap rendering           |
| `seaborn`     | ≥ 0.13   | Pearson correlation heatmap                      |
| `hashlib`     | stdlib   | SHA-256 password hashing                         |

**Frontend:** Custom CSS (Orbitron · Share Tech Mono · Exo 2 fonts)  
**Background:** HTML5 Canvas JavaScript animation (6-layer Hubble Deep Field)

---

## 🎨 Color System

```css
--bg:       #0b0f1a   /* Deep Space Blue        */
--panel:    #0f172a   /* Dark Panel Blue         */
--panel2:   #141a2e   /* Secondary Panel         */
--cyan:     #00e5ff   /* Neon Cyan (primary)     */
--orange:   #ff6b00   /* Rocket Orange (action)  */
--green:    #00ff9c   /* Success Green           */
--red:      #ff4b4b   /* Alert Red               */
--purple:   #7c8cff   /* Accent Purple           */
--text:     #ffffff   /* Primary Text            */
--text2:    #b8c1ec   /* Secondary Text          */
```

---

## 🌌 Background Animation Layers

| Layer | Elements | Description |
|-------|----------|-------------|
| 0 | Nebula clouds | 5 faint radial gradient blobs |
| 1 | Deep stars | 400 tiny drifting + twinkling stars |
| 2 | Mid stars | 120 medium stars with 12% cyan tint |
| 3 | Bright sparklers | 30 large stars, 35% with diffraction cross |
| 4 | Shooting stars | Up to 3 concurrent with gradient trail + head glow |
| 5 | Rocket | Procedurally drawn rocket with flickering flame, trail, cockpit |
| 6 | Galaxy field | 120 procedural Hubble-style galaxies (7 morphological types) |
| Post | Vignette | Radial darkening overlay for edge contrast |

---

## 🏗️ Application Architecture

```
Entry Point
│
├── inject_space_background()    ← Canvas animation (runs on all pages)
│
├── show_login()                 ← SHA-256 auth, role select, telemetry
├── show_loading()               ← Boot sequence animation
├── show_landing()               ← Cinematic stats entry page
│
└── show_dashboard()
    ├── Sidebar filters + nav
    ├── Page 1: Mission Control Overview
    ├── Page 2: Mission Data Analytics
    ├── Page 3: Rocket Launch Simulation  ← run_simulation()
    ├── Page 4: Scientific Insights
    ├── Page 5: Dataset Explorer
    └── Page 6: About Project
```

---

## 📊 Real Mission Data Sources

- **NASA Mission Pages** — mission.jpl.nasa.gov, nasa.gov
- **SpaceX Mission Database** — spacex.com/launches
- **ESA Mission Archive** — esa.int
- **Wikipedia Space Mission Articles** — cross-referenced for accuracy
- **NSSDC (NASA Space Science Data Center)** — nssdc.gsfc.nasa.gov
- **Gunter's Space Page** — space.skyrocket.de
- **Planet4589 Launch Log** — Jonathan McDowell's orbital database

---

## 🌐 Real-World Applications

- Mission planning and payload trade-off analysis
- Launch vehicle selection by payload mass and destination
- Fuel budget estimation for multi-stage rocket profiles
- Post-mission scientific yield attribution and benchmarking
- Fleet performance comparison across vehicle types
- Aerospace engineering education and training
- Interactive demonstration of rocket physics principles

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-page`)
3. Commit your changes (`git commit -m 'Add new analytics page'`)
4. Push to the branch (`git push origin feature/new-page`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with ❤️ for aerospace data enthusiasts and space mission analysts.

---

<div align="center">

**🚀 COSMOS MISSION CONTROL DASHBOARD v7.0.0**  
*Streamlit · Plotly · Pandas · NumPy · Seaborn · Matplotlib*

```
● SYS NOMINAL  ·  T-0 READY  ·  TELEMETRY LIVE
```

</div>

---
