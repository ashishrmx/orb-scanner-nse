# 🚀 15-Min ORB Scanner (NSE F&O)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Demo](https://img.shields.io/badge/Live_Demo-Coming_Soon-brightgreen.svg)](https://vercel.com)

**Discretionary intuition generates alpha. Algorithmic execution generates infinite scale.**

I've fully automated my **battle-tested 15-Minute Opening Range Breakout** engine that I traded manually for years.

## 🔥 Live Terminal Demo
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0b8c0305-a4aa-4b44-ba86-2c84ac7ece7c" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/46585253-6f01-40c1-85a1-5e43ebdb0c84" />


## 🎯 Features
- **Scans 50+ NSE F&O stocks** in <5 seconds
- **Smart Filters**: Volume (>500K), Gap (>0.3%), Range (<5%)
- **Dynamic Scoring** (0-100): Vol-X × R:R × Gap Quality × Range × Signal
- **Deterministic Trade Plans**: Entry/Stop/Target with exact Risk:Reward
- **Pro Terminal UI** (Rich library) matching your screenshot
- **Bordered Score Bars** with clear 40/60/100 levels

## 🚀 Quick Start (Local)

```bash
git clone https://github.com/ashishrmx/orb-scanner-nse.git
cd orb-scanner-nse
pip install -r requirements.txt
python main.py

REQUIREMENTS: 
yfinance 0.2.36
pandas 2.0.0
numpy 1.24.0
rich 13.7.0
requests 2.31.0
pytz 2024.1

* Install these libraries on virtual environment 

🌐 Web Version (Coming Soon)

FastAPI dashboard → Live NSE scans → Vercel deployment

🏗️ Architecture

config.py → data_feed(yfinance) → scanner.py → scorer.py → display.py
                                                      ↓
                                              trade_plan.py
📊 Scoring Engine (0-100)
Factor	Weight	Perfect Score
R:R	30pts	≥4:1
Vol-X	25pts	≥2x average
Gap	20pts	0.5-2.0%
Range	15pts	≤0.75%
Signal	10pts	LONG/SHORT confirmed
Score Colors: 🟢80+ Elite | 🟡60-79 Strong | 🟡40-59 Watch | 🔴<40 Pass

📈 Sample Output

SYMBOL    PRICE    CHG%  GAP%  ORB-H   ORB-L  RANGE  SIGNAL  VOL    VOL-X  R:R   SCORE
TATASTEEL ₹152.30 +1.45 +0.85 ₹153.20 ₹148.20  3.4%  ▲LONG  12.5L  2.1x  3.2:1 ████│░░ 87
NTPC      ₹385.40 +0.92 +0.45 ₹387.10 ₹382.50  1.2%  ◆WATCH 8.2L   1.8x  2.1:1 ██│░░░│ 68

🔧 Tech Stack

Core: Python 3.10+ | yfinance | pandas | numpy
UI: Rich (Terminal) | FastAPI (Web - coming)
Scoring: Deterministic weighted algorithm
Data: NSE real-time 1min OHLCV

📁 Project Structure

orb-scanner-nse/
├── main.py          # Entry point (python main.py)
├── config.py        # Strategy parameters
├── scanner.py       # ORB detection + filtering
├── scorer.py        # 0-100 scoring engine
├── display.py       # Rich terminal UI
├── trade_plan.py    # Entry/Stop/Target generator
├── data_feed.py     # yfinance NSE data
├── requirements.txt
└── README.md

🚀 Roadmap

Terminal scanner + scoring (Live!)

 Pro UI with bordered score bars

🤝 Built By
Ashish
Quant Developer | Algorithmic Trading | Python | NSE F&O

📞 Let's Connect!
Quants/traders: What features would you add?
Brokers: API integration interest?

⭐ Star if useful! Fork for your strategies.

