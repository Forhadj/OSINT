<div align="center">

```
  ⠀⠀⠀⠀⠀⠀⣀⠂⠐⠐⠐⠐⠐⠐⠐⠐⠐⠐⣐⠂⠁⠁⠆⠀⠀⠀⠀⠀⠀
  ⠀⠀⠀⠀⣀⥷⠃⠀⠁⡀⠆⡍⠁⠒⠒⠂⠀⢬⠐⠐⢬⡍⠉⡝⠲⡁⠆⠀⠀
  ⠀⠀⠀⣀⥷⡁⠀⠀⠊⡕⡕⡈⠁⠁⠆⡈⠀⠀⠀⡍⠁⠀⠀⠁⡈⠂⠀⡈⣃⠀⠀
  ⠀⠀⡁⣾⡥⠀⠀⡡⠠⡎⣿⣿⣿⡉⠳⡁⠀⠀⣀⠂⣶⣶⣶⡆⠀⠀⡘⠦⠆
  ⣀⥷⡥⡡⡞⣋⣛⠶⠐⠂⠳⡊⠀⡈⡙⠁⠀⠀⣹⡏⠁⠀⠁⠠⠰⣐⡕⠱⣷
  ⠘⡷⡗⡯⠰⣾⡙⠲⣐⡁⠆⠰⠀⣲⡖⣐⠁⠀⠀⣙⣾⠤⡈⡉⡨⠆⠀⡡⣿
  ⠀⠹⣃⡚⠀⡈⣷⠦⢬⡏⡉⡛⠲⠤⡂⠁⠁⠆⡖⡔⣀⠁⢬⡖⡿⡅⡉⥷⠁
  ⠀⠀⡈⣷⠆⠀⠀⠳⣃⡟⡛⡝⡖⠧⠁⠁⡉⡉⡉⣿⣉⡉⡇⠂⣶⣿⠀⡥⠀
  ⠀⠀⠀⡈⣳⠦⠀⠀⡘⠱⠤⠆⥷⡈⡉⡛⡙⡿⡞⡟⡿⣿⣾⣿⣿⡷⠆⠀⡷⠀
  ⠀⠀⠀⠀⠀⡙⠦⡕⠰⠒⡌⡙⡛⠶⠐⠂⠧⠁⡈⡇⠂⠧⡞⡞⡋⠀⠀⡷⠀
  ⠀⠀⠀⠀⠀⠀⠀⡈⡙⠶⢭⠒⡩⡖⠠⡤⠴⠀⠀⠀⠀⠀⠰⡔⠁⡠⠀⠧⠀
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡉⡛⠲⣐⡁⠁⡉⡉⠀⠀⠀⠀⠀⠁⠀⡡⡏⠀
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⡉⡉⡛⠒⠲⠶⠐⠴⠒⡚⠁⠀⠀
```

# 👻 GHOST — OSINT Toolkit v5.0

**Professional Open Source Intelligence & Reconnaissance Framework**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20macOS-green?style=flat-square)](https://github.com/Forhadj/OSINT)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-5.0-purple?style=flat-square)](https://github.com/Forhadj/OSINT)
[![Developer](https://img.shields.io/badge/Developer-FORHAD-cyan?style=flat-square)](https://github.com/Forhadj)

*Built for authorized security research and educational purposes only.*

</div>

---

## ⚠️ Legal Disclaimer

> **This tool is strictly for authorized security research and educational use.**
> Unauthorized use may violate the Computer Fraud and Abuse Act (CFAA), Computer Misuse Act (CMA), your ISP's Terms of Service, and local/national laws.
> **Only use Ghost on systems you own or have explicit written permission to test.**
> The developer assumes NO liability for misuse.

---

## 📋 Features

Ghost is a modular, terminal-based OSINT toolkit with 16 recon modules built entirely on Python's standard library.

| # | Module | Description |
|---|--------|-------------|
| 01 | **User Recon** | Check username existence across 22+ platforms |
| 02 | **Phone Info** | Country detection, carrier lookup (BD), format validation |
| 03 | **Mail Finder** | Email pattern generation + MX/SMTP probe |
| 04 | **IP Location** | HTTPS geolocation with GeoIP map link |
| 05 | **Subdomain Scan** | Threaded enumeration of 80+ common subdomains + robots.txt parser |
| 06 | **Port Scanner** | Multi-threaded, 4 scan modes, service banner grabbing |
| 07 | **DNS Recon** | 10 record types + Wayback Machine + robots.txt parser |
| 08 | **WHOIS Lookup** | Structured WHOIS data extraction |
| 09 | **SSL Checker** | Certificate details, expiry, TLS version, SANs |
| 10 | **Header Analyzer** | Security header grading (A+ → F) + HTTP method testing |
| 11 | **GitHub Recon** | Profile, repos, orgs, recent events via public API |
| 12 | **Breach Checker** | Domain risk + k-anonymity HIBP password check |
| 13 | **Tech Detector** | CMS, framework, frontend, analytics, CDN/WAF fingerprinting |
| 14 | **Reverse IP** | PTR lookup + shared hosting enumeration |
| 15 | **ASN Lookup** | Autonomous System info for any IP |
| 16 | **Export Results** | JSON / TXT / HTML dark-mode report |

---

## 🚀 Installation

### Requirements
- Python 3.8+
- No third-party pip packages needed (pure standard library)

### Termux (Android)
```bash
# Update and install dependencies
pkg update && pkg upgrade
pkg install python git

# Optional (for WHOIS and nslookup modules)
pkg install whois dnsutils

# Clone the repository
git clone https://github.com/Forhadj/OSINT
cd OSINT

# Run
python ran.py
```

### Linux / macOS
```bash
# Install optional tools
sudo apt install whois dnsutils   # Debian/Ubuntu
# or
brew install whois               # macOS

# Clone the repository
git clone https://github.com/Forhadj/OSINT
cd OSINT

# Run
python3 ran.py
```

---

## ⚙️ Configuration

Edit `config.json` to customize behavior:

```json
{
  "timeout": 8,
  "threads": 20,
  "github_token": "ghp_your_token_here"
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `timeout` | `8` | HTTP/socket request timeout in seconds |
| `threads` | `20` | Thread count for parallel scans (10–50 recommended for Termux) |
| `github_token` | `""` | Optional GitHub Personal Access Token for higher API rate limits |

> **Note:** `config.json` is loaded automatically at startup. You do not need to restart to apply changes.

---

## 📸 Screenshots

```
        ─────────────────────────────────────────
           👻  G H O S T  —  O S I N T  T O O L  👻
              OSINT & Reconnaissance Toolkit v5.0
           ⚡ Ethical Use Only | Authorized Targets ⚡
           Developer: FORHAD
        ─────────────────────────────────────────

  ┌────────────────────────────┬────────────────────────────┐
  │          LEFT PANEL        │          RIGHT PANEL       │
  ├────────────────────────────┼────────────────────────────┤
  │ [01] User Recon            │ [09] SSL Checker           │
  │ [02] Phone Info            │ [10] Header Analyzer       │
  │ [03] Mail Finder           │ [11] GitHub Recon          │
  │ [04] IP Location           │ [12] Breach Checker        │
  │ [05] Subdomain Scan        │ [13] Tech Detector         │
  │ [06] Port Scanner          │ [14] Reverse IP            │
  │ [07] DNS Recon             │ [15] ASN Lookup            │
  │ [08] WHOIS Lookup          │ [16] Export Results        │
  ├────────────────────────────┼────────────────────────────┤
  │ [00] Exit                  │  Ghost v5.0 | FORHAD       │
  └────────────────────────────┴────────────────────────────┘
```

---

## 🔧 What Changed in v5.0 (Changelog)

### 🐛 Bug Fixes
- **Version mismatch fixed** — unified `VERSION = "5.0"` everywhere
- **SSL datetime bug** — now uses timezone-aware `datetime.now(timezone.utc)` to avoid Python 3.12+ deprecation
- **HTTP → HTTPS** — replaced `http://ip-api.com` with `https://ipwho.is` for secure geolocation
- **Password input hidden** — uses `getpass.getpass()` so passwords aren't visible in terminal
- **SMTP timeout** — port 25 probe now uses 4s timeout (ISP block-friendly) instead of full `DEFAULT_TIMEOUT`

### 🔒 Security & Reliability
- **Tool availability checks** — `shutil.which()` used before calling `whois`/`nslookup`; graceful fallback messages instead of crashes
- **GitHub rate limit** — optional `github_token` support in `config.json` with `Authorization: Bearer` header
- **Realistic User-Agent rotation** — randomized from a pool of real browser UAs to reduce blocking
- **Private-IP-only mode** — port scanner offers optional restriction to private/local IPs
- **False-positive hardening** — username checker requires stricter HTML pattern matching

### ✨ New Features
- **`config.json` system** — load timeout, threads, GitHub token from file
- **`fetch()` helper function** — replaces repeated `Request/urlopen` patterns
- **`status()` print helper** — consistent `label → value` formatting
- **robots.txt parser** — extracts and displays `Disallow:` paths (modules 05 & 07)
- **Wayback Machine lookup** — checks for archived snapshots in DNS Recon
- **GeoIP Map Link** — Google Maps link with lat/lon in IP Location module
- **ASN Lookup module** — new Module 15
- **Adaptive thread count** — `min(50, cpu_count * 4)` for Termux compatibility
- **Improved HTML report** — stats dashboard, better dark theme, version in footer

### 🏗️ Code Quality
- Eliminated all repeated `Request/urlopen` blocks → single `fetch()` helper
- Version string unified in banner, menus, reports, user-agent headers
- Modular loop for tech detector categories (removed duplicate code)

---

## 📁 File Structure

```
OSINT/
├── ghost_v5.py       # Main tool
├── config.json       # Configuration (timeout, threads, API key)
├── requirements.txt  # Dependency notes (stdlib only)
├── .gitignore        # Ignores output files and logs
└── README.md         # This file
```

---

## 🧠 How It Works

```
User Input
    │
    ▼
main_menu() ──► Module selected
                    │
                    ▼
              Module function
                    │
           ┌────────┴────────┐
           │                 │
      fetch() helper    subprocess
      (HTTP/HTTPS)      (whois/nslookup)
           │                 │
           └────────┬────────┘
                    │
              RESULTS dict
                    │
                    ▼
           export_results()
          JSON / TXT / HTML
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/new-module`)
3. Commit your changes (`git commit -m 'Add new module'`)
4. Push to branch (`git push origin feature/new-module`)
5. Open a Pull Request

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with 💀 by [FORHAD](https://github.com/Forhadj)**

*Ghost OSINT Toolkit — Stay Ethical. Stay Legal.*

[![GitHub](https://img.shields.io/badge/GitHub-Forhadj-black?style=flat-square&logo=github)](https://github.com/Forhadj)

</div>
