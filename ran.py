#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║              GHOST — OSINT & Reconnaissance Toolkit              ║
║         Ethical Use Only | Educational Purpose | v5.0            ║
║                    Developer: FORHAD                             ║
╚══════════════════════════════════════════════════════════════════╝

⚠  LEGAL DISCLAIMER:
   This tool is for authorized security research and educational use ONLY.
   Unauthorized scanning or reconnaissance may violate:
     • Computer Fraud and Abuse Act (CFAA)
     • Computer Misuse Act (CMA)
     • ISP Terms of Service & Local/National Laws
   Only use on systems you OWN or have EXPLICIT WRITTEN PERMISSION to test.
   The developer assumes NO liability for misuse of this tool.
"""

import os, sys, json, time, socket, hashlib, ssl, re, shutil, getpass
import threading, subprocess, ipaddress, random, html as html_lib
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
import http.client
from concurrent.futures import ThreadPoolExecutor

# ══════════════════════════════════════════════
# GLOBAL CONFIG
# ══════════════════════════════════════════════
DEFAULT_TIMEOUT  = 8
MAX_THREADS      = min(50, (os.cpu_count() or 4) * 4)
LOG_FILE         = "ghost_log.txt"
RESULTS          = {}
VERSION          = "5.0"
DEVELOPER        = "FORHAD"
GITHUB_TOKEN     = ""          # Optional: set for higher GitHub rate limit
CONFIG_FILE      = "config.json"

# Load config.json if present
def load_config():
    global DEFAULT_TIMEOUT, MAX_THREADS, GITHUB_TOKEN
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                cfg = json.load(f)
            DEFAULT_TIMEOUT = cfg.get("timeout",    DEFAULT_TIMEOUT)
            MAX_THREADS     = cfg.get("threads",    MAX_THREADS)
            GITHUB_TOKEN    = cfg.get("github_token", "")
        except Exception:
            pass

load_config()

# ══════════════════════════════════════════════
# COLORS
# ══════════════════════════════════════════════
class C:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RESET   = '\033[0m'

def c(color, text):  return f"{color}{text}{C.RESET}"
def ok(m):           print(f"  {c(C.GREEN,  '✔')} {m}")
def fail(m):         print(f"  {c(C.RED,    '✘')} {m}")
def info(m):         print(f"  {c(C.BLUE,   '›')} {m}")
def warn(m):         print(f"  {c(C.YELLOW, '!')} {m}")
def sep():           print(c(C.DIM, "  " + "─" * 58))
def section(t):
    print(); print(c(C.BOLD, c(C.MAGENTA, f"  ┌─[ {t} ]"))); sep()

def status(label, value, color=C.WHITE):
    """Consistent key→value print helper."""
    info(f"{label:<22} → {c(color, str(value)[:70])}")

def get_input(p):
    return input(f"\n  {c(C.CYAN,'❯❯❯❯')} {p}: ").strip()

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def rate_sleep():
    time.sleep(random.uniform(0.4, 1.0))

def progress_bar(label, total=28, delay=0.035):
    for i in range(total):
        filled = '█'*(i+1); empty = '░'*(total-i-1)
        pct = int((i+1)/total*100)
        print(f"\r  {c(C.DIM,label)} [{c(C.CYAN,filled)}{c(C.DIM,empty)}] {pct}%",
              end="", flush=True)
        time.sleep(delay)
    print(f"\r  {c(C.GREEN,'✔')} {label} {c(C.GREEN,'[100%]')}              ")

# ══════════════════════════════════════════════
# HTTP FETCH HELPER  (replaces repeated pattern)
# ══════════════════════════════════════════════
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

def _random_ua():
    return random.choice(_USER_AGENTS)

def fetch(url, extra_headers=None, timeout=None):
    """Simple fetch helper. Returns (response_object, body_bytes)."""
    hdrs = {"User-Agent": _random_ua()}
    if extra_headers:
        hdrs.update(extra_headers)
    req  = Request(url, headers=hdrs)
    resp = urlopen(req, timeout=timeout or DEFAULT_TIMEOUT)
    body = resp.read()
    return resp, body

# ══════════════════════════════════════════════
# TOOL AVAILABILITY CHECK
# ══════════════════════════════════════════════
def require_tool(name, install_hint=""):
    if not shutil.which(name):
        fail(f"'{name}' not found on this system.")
        if install_hint:
            info(f"Install: {install_hint}")
        return False
    return True

# ══════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════
def banner():
    os.system('clear')
    ghost = (
        "  \u2800\u2800\u2800\u2800\u2800\u2800\u28c0\u2842\u2810\u2810\u2810\u2810\u2810\u2810\u2810\u2810\u2810\u2810\u28d0\u2842\u2801\u2801\u2806\u2800\u2800\u2800\u2800\u2800\u2800\n"
        "  \u2800\u2800\u2800\u2800\u28c0\u2897\u2803\u2800\u2801\u2840\u2806\u280d\u2801\u2812\u2812\u2802\u2800\u282c\u2810\u2810\u282c\u280d\u2809\u281d\u2832\u2841\u2806\u2800\u2800\n"
        "  \u2800\u2800\u2800\u28c0\u2897\u2881\u2800\u2800\u280a\u2815\u2815\u2808\u2801\u2801\u2806\u2808\u2800\u2800\u2800\u288d\u2801\u2800\u2800\u2801\u2808\u2802\u2800\u2808\u2843\u2800\u2800\n"
        "  \u2800\u2800\u2821\u28be\u2825\u2800\u2800\u2821\u28a0\u284e\u28bf\u28bf\u28bf\u2849\u2833\u2841\u2800\u2800\u28c0\u2842\u28f6\u28f6\u28f6\u2846\u2800\u2800\u2818\u28a6\u2806\n"
        "  \u28c0\u2897\u2885\u2821\u289e\u28cb\u28db\u2836\u2810\u2842\u2834\u289a\u2800\u2808\u2819\u2801\u2800\u2800\u28b9\u288f\u2801\u2800\u2801\u28a0\u2830\u28d0\u2815\u2831\u28b7\n"
        "  \u2818\u2887\u2807\u28af\u2830\u28be\u2899\u2832\u28d0\u2841\u2806\u2830\u2800\u28b2\u2896\u28d0\u2801\u2800\u2800\u28d9\u28be\u28a4\u2808\u2809\u2828\u2806\u2800\u2821\u28bf\n"
        "  \u2800\u2839\u2843\u281a\u2800\u2808\u28b7\u28a6\u282c\u284f\u2809\u281b\u2832\u28a4\u2842\u2801\u2801\u2806\u2816\u2814\u28c0\u2801\u282c\u2816\u283f\u2845\u2809\u2897\u2801\n"
        "  \u2800\u2800\u2808\u28b7\u2806\u2800\u2800\u2833\u2843\u289f\u281b\u281d\u2896\u28a7\u2801\u2801\u2849\u2849\u2849\u28bf\u28c9\u2849\u2847\u2842\u28f6\u28bf\u2800\u2885\u2800\n"
        "  \u2800\u2800\u2800\u2808\u28b3\u2846\u2800\u2800\u2818\u2831\u28a4\u2806\u2897\u2808\u2809\u281b\u2899\u283f\u283e\u289f\u283f\u28bf\u28fe\u28bf\u28bf\u2887\u2806\u2800\u2887\u2800\n"
        "  \u2800\u2800\u2800\u2800\u2800\u2819\u28a6\u2815\u2830\u2812\u280c\u2899\u281b\u2836\u2810\u2842\u28a7\u2801\u2848\u2847\u2842\u28a7\u283e\u283e\u280b\u2800\u2800\u2887\u2800\n"
        "  \u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2808\u2819\u2836\u282d\u2812\u2829\u2816\u28a0\u2844\u2834\u2800\u2800\u2800\u2800\u2800\u2830\u2814\u2801\u2860\u2800\u28a7\u2800\n"
        "  \u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2809\u281b\u2832\u28d0\u2841\u2801\u2809\u2809\u2800\u2800\u2800\u2800\u2800\u2801\u2800\u2821\u280f\u2800\n"
        "  \u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2808\u2809\u2809\u281b\u2812\u2832\u2836\u2810\u2834\u2812\u281a\u2801\u2800\u2800"
    )
    print(c(C.CYAN, C.BOLD + ghost))
    print(c(C.CYAN, C.BOLD + "        ─────────────────────────────────────────"))
    print(c(C.CYAN, C.BOLD + "           👻  G H O S T  —  O S I N T  T O O L  👻"))
    print(c(C.DIM,            f"              OSINT & Reconnaissance Toolkit v{VERSION}"))
    print(c(C.YELLOW,         "           ⚡ Ethical Use Only | Authorized Targets ⚡"))
    print(c(C.DIM,  "           Developer: ") + c(C.CYAN, C.BOLD + DEVELOPER))
    print(c(C.CYAN, C.BOLD + "        ─────────────────────────────────────────\n"))

# ══════════════════════════════════════════════
# 01 — USERNAME RECON
# ══════════════════════════════════════════════
def user_forhad():
    section("01 — USER RECON")
    warn("Only check usernames for legitimate OSINT/research purposes.")
    username = get_input("Enter username")
    if not username: fail("Username cannot be empty."); return

    sites = {
        "GitHub":     (f"https://github.com/{username}",
                       ["Not Found","This is not the web page"]),
        "Twitter/X":  (f"https://twitter.com/{username}",
                       ["This account doesn't exist","account doesn't exist"]),
        "Instagram":  (f"https://www.instagram.com/{username}/",
                       ["Sorry, this page","Page Not Found","page isn't available"]),
        "Reddit":     (f"https://www.reddit.com/user/{username}",
                       ["nobody on Reddit goes by that name","page not found"]),
        "TikTok":     (f"https://www.tiktok.com/@{username}",
                       ["Couldn't find this account","couldn't find"]),
        "Pinterest":  (f"https://www.pinterest.com/{username}/",
                       ["Sorry! We couldn't find","not found"]),
        "LinkedIn":   (f"https://www.linkedin.com/in/{username}",
                       ["Page not found","profile not found"]),
        "Telegram":   (f"https://t.me/{username}",
                       ["If you have Telegram, you can contact"]),
        "Medium":     (f"https://medium.com/@{username}",
                       ["Page not found","404"]),
        "Dev.to":     (f"https://dev.to/{username}",
                       ["404","page not found"]),
        "Pastebin":   (f"https://pastebin.com/u/{username}",
                       ["Not Found (#404)"]),
        "Twitch":     (f"https://www.twitch.tv/{username}",
                       ["Sorry. Unless you've got a time machine"]),
        "HackerNews": (f"https://news.ycombinator.com/user?id={username}",
                       ["No such user."]),
        "Keybase":    (f"https://keybase.io/{username}",
                       ["isn't a Keybase user","Page not found"]),
        "GitLab":     (f"https://gitlab.com/{username}",
                       ["404","User not found"]),
        "Replit":     (f"https://replit.com/@{username}",
                       ["We couldn't find","404"]),
        "Steam":      (f"https://steamcommunity.com/id/{username}",
                       ["The specified profile could not be found"]),
        "Snapchat":   (f"https://www.snapchat.com/add/{username}",
                       ["Sorry, we couldn't find","404"]),
        "Flickr":     (f"https://www.flickr.com/people/{username}",
                       ["page not found","404"]),
        "Vimeo":      (f"https://vimeo.com/{username}",
                       ["Page not found","404"]),
        "Behance":    (f"https://www.behance.net/{username}",
                       ["Page not found"]),
        "SoundCloud": (f"https://soundcloud.com/{username}",
                       ["404","page not found"]),
        "GitLab":     (f"https://gitlab.com/{username}",
                       ["404","User not found"]),
    }

    found, not_found = [], []
    print()
    for site, (url, false_pos) in sites.items():
        try:
            resp, body_bytes = fetch(url)
            body = body_bytes.decode('utf-8', errors='ignore')
            # Strong false-positive check: require NO false positive strings
            if resp.status == 200 and not any(
                    fp.lower() in body.lower() for fp in false_pos if fp):
                ok(f"{site:<18} {c(C.GREEN,'FOUND')}  → {c(C.DIM,url)}")
                found.append({"site": site, "url": url})
                log(f"USER RECON FOUND: {username} @ {site}")
            else:
                fail(f"{site:<18} {c(C.RED,'NOT FOUND')}")
                not_found.append(site)
        except HTTPError as e:
            if e.code == 404:
                fail(f"{site:<18} {c(C.RED,'NOT FOUND')}")
            else:
                warn(f"{site:<18} {c(C.YELLOW,f'HTTP {e.code}')}")
            not_found.append(site)
        except Exception:
            warn(f"{site:<18} {c(C.DIM,'TIMEOUT/ERROR')}")
        rate_sleep()

    sep()
    info(f"Found on {c(C.GREEN,str(len(found)))} sites | "
         f"Not found on {c(C.RED,str(len(not_found)))} sites")
    RESULTS["user_recon"] = {
        "username": username, "found": found, "count": len(found)
    }

# ══════════════════════════════════════════════
# 02 — PHONE INFO
# ══════════════════════════════════════════════
def phone_info():
    section("02 — PHONE INFO")
    warn("Public format validation and carrier lookup only.")
    phone = get_input("Enter phone number with country code (e.g. +8801XXXXXXXXX)")
    if not phone: fail("Phone cannot be empty."); return

    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    print()

    if not re.match(r'^\+?[1-9]\d{6,14}$', phone_clean):
        fail("Invalid phone number format."); return
    ok(f"Format       → {c(C.GREEN,'VALID')}")
    info(f"Cleaned      → {c(C.CYAN, phone_clean)}")
    info(f"Length       → {c(C.WHITE, str(len(phone_clean.lstrip('+'))))} digits")

    country_codes = {
        '+880':'Bangladesh',    '+1':'USA / Canada',    '+44':'United Kingdom',
        '+91':'India',          '+86':'China',          '+81':'Japan',
        '+49':'Germany',        '+33':'France',         '+7':'Russia',
        '+55':'Brazil',         '+61':'Australia',      '+971':'UAE',
        '+966':'Saudi Arabia',  '+92':'Pakistan',       '+234':'Nigeria',
        '+20':'Egypt',          '+27':'South Africa',   '+62':'Indonesia',
        '+82':'South Korea',    '+39':'Italy',          '+34':'Spain',
        '+90':'Turkey',         '+31':'Netherlands',    '+46':'Sweden',
        '+47':'Norway',         '+45':'Denmark',        '+358':'Finland',
        '+41':'Switzerland',    '+43':'Austria',        '+32':'Belgium',
        '+351':'Portugal',      '+48':'Poland',         '+36':'Hungary',
        '+420':'Czech Republic','+40':'Romania',        '+380':'Ukraine',
        '+375':'Belarus',       '+994':'Azerbaijan',    '+995':'Georgia',
        '+998':'Uzbekistan',    '+212':'Morocco',       '+213':'Algeria',
        '+216':'Tunisia',       '+60':'Malaysia',       '+65':'Singapore',
        '+66':'Thailand',       '+84':'Vietnam',        '+63':'Philippines',
        '+94':'Sri Lanka',      '+977':'Nepal',         '+95':'Myanmar',
        '+855':'Cambodia',
    }

    detected = None
    for code, country in sorted(country_codes.items(), key=lambda x: -len(x[0])):
        if phone_clean.startswith(code):
            detected = (code, country); break

    if detected:
        ok(f"Country Code → {c(C.GREEN, detected[0])}")
        ok(f"Country      → {c(C.CYAN,  detected[1])}")
        local = phone_clean[len(detected[0]):]
        info(f"Local Number → {c(C.WHITE, local)}")
    else:
        warn("Country code not recognized in database.")

    num_len = len(phone_clean.lstrip('+'))
    if num_len == 10:
        info(f"Number Type  → {c(C.CYAN,'10-digit (likely mobile/landline)')}")
    elif num_len >= 11:
        info(f"Number Type  → {c(C.CYAN,'International format')}")

    if phone_clean.startswith('+880') or phone_clean.startswith('880'):
        local_bd = phone_clean.lstrip('+').lstrip('880').lstrip('0')
        prefix   = local_bd[:2] if len(local_bd) >= 2 else ''
        bd_carriers = {
            '17':'Grameenphone', '13':'Grameenphone',
            '19':'Banglalink',   '14':'Banglalink',
            '18':'Robi',         '16':'Robi (Airtel)',
            '15':'Teletalk',     '12':'Teletalk',
            '11':'Skitto (GP)',  '10':'Robi',
        }
        carrier = bd_carriers.get(prefix, 'Unknown BD Carrier')
        sep()
        info(f"BD Carrier   → {c(C.YELLOW, carrier)}")
        info(f"BD Prefix    → {c(C.WHITE, '+880' + prefix + 'XXXXXXXX')}")
        if len(local_bd) == 10:
            ok(f"BD Format    → {c(C.GREEN,'Valid 10-digit Bangladesh number')}")
        else:
            warn(f"BD Format    → {c(C.YELLOW,'Unusual length for BD number')}")

    sep()
    info(f"Note: {c(C.DIM,'For full carrier lookup, use numverify or abstract API.')}")
    RESULTS["phone_info"] = {
        "phone": phone_clean,
        "country": detected[1] if detected else "Unknown"
    }
    log(f"PHONE INFO: {phone_clean}")

# ══════════════════════════════════════════════
# 03 — MAIL FINDER
# ══════════════════════════════════════════════
def mail_finder():
    section("03 — MAIL FINDER")
    warn("Searches publicly available sources only (ethical OSINT).")
    domain = get_input("Enter company domain (e.g. example.com)")
    if not domain: fail("Domain cannot be empty."); return

    first = get_input("Enter person's first name (optional, Enter to skip)")
    last  = get_input("Enter person's last name  (optional, Enter to skip)")
    print()

    progress_bar("Generating email pattern predictions")
    print()

    patterns = []
    if first and last:
        f, l = first.lower(), last.lower()
        patterns = [
            f"{f}@{domain}",        f"{l}@{domain}",
            f"{f}.{l}@{domain}",    f"{f}{l}@{domain}",
            f"{l}.{f}@{domain}",    f"{l}{f}@{domain}",
            f"{f[0]}{l}@{domain}",  f"{f}{l[0]}@{domain}",
            f"{f[0]}.{l}@{domain}", f"{f}_{l}@{domain}",
            f"{l}_{f}@{domain}",    f"{f[0]}_{l}@{domain}",
        ]
        info(f"Generated {c(C.GREEN,str(len(patterns)))} patterns "
             f"for {c(C.CYAN,f'{first} {last}')}:")
        print()
        for i, p in enumerate(patterns, 1):
            print(f"    {c(C.DIM,f'[{i:>2}]')} {c(C.CYAN,p)}")
    else:
        generic = [
            f"info@{domain}",     f"contact@{domain}", f"admin@{domain}",
            f"support@{domain}",  f"hello@{domain}",   f"sales@{domain}",
            f"hr@{domain}",       f"careers@{domain}", f"security@{domain}",
            f"abuse@{domain}",    f"webmaster@{domain}",f"noreply@{domain}",
            f"team@{domain}",     f"office@{domain}",  f"press@{domain}",
        ]
        info(f"Common email addresses for {c(C.CYAN,domain)}:")
        print()
        for p in generic:
            print(f"    {c(C.DIM,'•')} {c(C.CYAN,p)}")
        patterns = generic

    sep()
    # MX check — prefer nslookup, fallback to socket
    if require_tool("nslookup", "pkg install dnsutils"):
        try:
            result = subprocess.run(
                ['nslookup','-type=MX', domain],
                capture_output=True, text=True, timeout=DEFAULT_TIMEOUT)
            if 'mail exchanger' in result.stdout.lower():
                ok(f"MX Record    → {c(C.GREEN,'EXISTS')} (domain accepts email)")
            else:
                warn(f"MX Record    → {c(C.YELLOW,'NOT FOUND')}")
        except Exception:
            warn("MX check failed.")
    else:
        try:
            socket.getaddrinfo(domain, None, socket.AF_INET)
            ok(f"MX Record    → {c(C.DIM,'(basic DNS OK, nslookup unavailable)')}")
        except Exception:
            warn("MX check failed.")

    sep()
    info("Checking SMTP banner (port 25)...")
    try:
        mx_host = domain
        s = socket.socket(); s.settimeout(4)   # short timeout — port 25 often blocked
        s.connect((mx_host, 25))
        banner_data = s.recv(512).decode('utf-8', errors='ignore').strip()
        ok(f"SMTP Banner  → {c(C.CYAN, banner_data[:80])}")
        s.close()
    except Exception:
        info(f"SMTP probe   → {c(C.DIM,'No direct SMTP access (normal for ISP blocks)')}")

    sep()
    info(f"Tip: {c(C.DIM,'Verify with Hunter.io or Skrapp.io.')}")
    RESULTS["mail_finder"] = {"domain": domain, "patterns": patterns}
    log(f"MAIL FINDER: {domain} — {first} {last}")

# ══════════════════════════════════════════════
# 04 — IP LOCATION  (HTTPS API)
# ══════════════════════════════════════════════
def ip_location():
    section("04 — IP LOCATION")
    target = get_input("Enter IP address or domain")
    if not target: fail("Input cannot be empty."); return

    progress_bar("Fetching geolocation data")
    print()

    try:
        ip = socket.gethostbyname(target)
        if ip != target:
            info(f"Resolved     → {c(C.CYAN,ip)}")

        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            warn(f"IP Type      → {c(C.YELLOW,'PRIVATE / LOCAL')} (no geo data)"); return

        # Use HTTPS endpoint (ipwho.is) instead of HTTP ip-api.com
        url  = f"https://ipwho.is/{ip}"
        resp, body = fetch(url)
        data = json.loads(body.decode())

        if data.get("success"):
            lat = data.get("latitude",  "N/A")
            lon = data.get("longitude", "N/A")
            rows = [
                ("IP Address",   data.get("ip",         "N/A")),
                ("Country",      data.get("country",     "N/A")),
                ("Region",       data.get("region",      "N/A")),
                ("City",         data.get("city",        "N/A")),
                ("Postal Code",  data.get("postal",      "N/A")),
                ("Latitude",     str(lat)),
                ("Longitude",    str(lon)),
                ("Timezone",     data.get("timezone",{}).get("id","N/A")),
                ("ISP",          data.get("connection",{}).get("isp","N/A")),
                ("Organization", data.get("connection",{}).get("org","N/A")),
                ("AS Number",    data.get("connection",{}).get("asn","N/A")),
                ("Type",         data.get("type",        "N/A")),
            ]
            for label, value in rows:
                info(f"{label:<14} → {c(C.WHITE, str(value))}")

            # GeoIP Map Link
            if lat not in ("N/A", None) and lon not in ("N/A", None):
                map_link = f"https://maps.google.com/?q={lat},{lon}"
                sep()
                info(f"Map Link     → {c(C.CYAN, map_link)}")

            RESULTS["ip_location"] = dict(rows)
            log(f"IP LOCATION: {ip} → {data.get('city')}, {data.get('country')}")
        else:
            fail(f"API Error: {data.get('message','Unknown')}")

    except socket.gaierror:
        fail("Could not resolve hostname.")
    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 05 — SUBDOMAIN SCAN
# ══════════════════════════════════════════════
def subdomain_scan():
    section("05 — SUBDOMAIN SCAN")
    domain = get_input("Enter base domain (e.g. example.com)")
    if not domain: fail("Domain cannot be empty."); return

    subdomains = [
        'www','mail','ftp','smtp','pop','imap','webmail','admin','portal','api',
        'app','dev','staging','test','beta','shop','store','blog','forum','wiki',
        'vpn','remote','secure','cloud','cdn','static','assets','media','img',
        'images','files','docs','support','help','status','monitor','dashboard',
        'panel','cpanel','whm','ns1','ns2','mx','mx1','mx2','git','gitlab',
        'jenkins','jira','confluence','db','database','mysql','postgres','redis',
        'elasticsearch','kibana','grafana','prometheus','backup','old','new','v2',
        'v1','m','mobile','api2','stage','uat','qa','internal','intranet',
        'extranet','office','mail2','exchange','autodiscover','sso','auth',
        'login','account','accounts','billing','pay','payment','video','stream',
        'live','chat','news','events','careers','jobs','promo','ads','track',
        'smtp2','pop3','imap4','webdisk','ftp2','upload','download','data',
        'analytics','stats','report','reports','search','maps','map',
        'gw','gateway','proxy','lb','node','server','wp','phpmyadmin',
    ]

    print(f"\n  {c(C.DIM,f'Scanning {len(subdomains)} common subdomains...')}\n")
    found = []; lock = threading.Lock()

    def check(sub):
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            with lock:
                ok(f"{target:<48} → {c(C.GREEN,ip)}")
                found.append({"subdomain": target, "ip": ip})
                log(f"SUBDOMAIN: {target} → {ip}")
        except socket.gaierror:
            pass

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as exe:
        exe.map(check, subdomains)

    sep()
    if found:
        info(f"Discovered {c(C.GREEN,str(len(found)))} subdomains "
             f"out of {len(subdomains)} checked")
    else:
        warn("No subdomains found from wordlist.")

    # Robots.txt parser
    sep()
    info("Checking robots.txt for hidden paths...")
    try:
        resp, body = fetch(f"https://{domain}/robots.txt")
        if resp.status == 200:
            text = body.decode('utf-8', errors='ignore')
            ok(f"robots.txt   → {c(C.GREEN,'FOUND')}")
            disallowed = [l.split(':',1)[1].strip()
                          for l in text.splitlines()
                          if l.lower().startswith('disallow:') and len(l) > 12]
            if disallowed:
                info(f"Disallowed paths ({len(disallowed)}):")
                for p in disallowed[:15]:
                    print(f"    {c(C.DIM,'•')} {c(C.YELLOW,p)}")
    except Exception:
        info(f"robots.txt   → {c(C.DIM,'Not accessible')}")

    RESULTS["subdomains"] = {
        "domain": domain, "found": found, "count": len(found)
    }

# ══════════════════════════════════════════════
# 06 — PORT SCANNER
# ══════════════════════════════════════════════
def port_scanner():
    section("06 — PORT SCANNER")
    print()
    print(c(C.RED, C.BOLD+"  ⚠  LEGAL WARNING:"))
    print(c(C.YELLOW,"     Unauthorized port scanning may violate laws."))
    print(c(C.YELLOW,"     Use ONLY on systems you OWN or have written permission."))
    print()
    confirm = get_input("Type 'yes' to confirm you have authorization")
    if confirm.lower() != 'yes':
        warn("Scan cancelled."); return

    target = get_input("Enter IP or hostname")
    if not target: fail("Target cannot be empty."); return

    # Optional: restrict to private/local IPs only
    private_only_input = get_input("Restrict to private/local IPs only? (y/N)")
    private_only = private_only_input.lower() == 'y'

    print(f"\n  {c(C.BOLD,'Scan Mode:')}")
    print(f"  {c(C.CYAN,'[1]')} Quick    — Top 25 common ports")
    print(f"  {c(C.CYAN,'[2]')} Standard — Top 100 ports")
    print(f"  {c(C.CYAN,'[3]')} Full     — Common 1000 ports")
    print(f"  {c(C.CYAN,'[4]')} Custom   — Enter port range")
    mode = get_input("Choose mode"); print()

    top25   = [21,22,23,25,53,80,110,111,135,139,143,443,445,
               993,995,1723,3306,3389,5900,8080,8443,8888,9090,27017]
    top100  = list(range(1,101)) + [443,445,993,995,1433,1521,
               3306,3389,5432,5900,6379,8080,8443,27017,27018]
    top1000 = list(range(1,1001))

    if mode == '4':
        try:
            rng = get_input("Enter port range (e.g. 1-1024)")
            s_p, e_p = map(int, rng.split('-'))
            ports = list(range(s_p, e_p+1))
        except Exception:
            fail("Invalid range."); return
    elif mode == '2': ports = sorted(set(top100))
    elif mode == '3': ports = top1000
    else:             ports = top25

    open_ports = []; closed = 0; lock = threading.Lock()

    try:
        ip = socket.gethostbyname(target)
        ip_obj = ipaddress.ip_address(ip)

        if private_only and not ip_obj.is_private:
            fail("Target is not a private IP. Scan cancelled (private-only mode).")
            return

        info(f"Target IP    → {c(C.CYAN,ip)}")
        try:
            rdns = socket.gethostbyaddr(ip)[0]
            info(f"Reverse DNS  → {c(C.CYAN,rdns)}")
        except Exception: pass
    except Exception:
        fail("Could not resolve host."); return

    info(f"Scanning {c(C.YELLOW,str(len(ports)))} ports "
         f"with {MAX_THREADS} threads...\n")

    def scan(port):
        nonlocal closed
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            r = s.connect_ex((ip, port))
            banner_str = ''
            if r == 0:
                try:
                    s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner_str = s.recv(256).decode(
                        'utf-8', errors='ignore').split('\n')[0][:50].strip()
                except Exception: pass
            s.close()
            if r == 0:
                try:    svc = socket.getservbyport(port)
                except: svc = "unknown"
                with lock:
                    bd = f"  {c(C.DIM,banner_str)}" if banner_str else ""
                    ok(f"Port {str(port):<6} → {c(C.GREEN,'OPEN')}  "
                       f"[{c(C.CYAN,svc)}]{bd}")
                    open_ports.append({"port":port,"service":svc,"banner":banner_str})
            else:
                with lock: closed += 1
        except Exception: pass

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as exe:
        exe.map(scan, ports)

    sep()
    info(f"Open: {c(C.GREEN,str(len(open_ports)))} | "
         f"Closed/Filtered: {c(C.RED,str(closed))}")
    RESULTS["port_scanner"] = {"target": ip, "open": open_ports}
    log(f"PORT SCAN: {ip} — {len(open_ports)} open ports")

# ══════════════════════════════════════════════
# 07 — DNS RECON
# ══════════════════════════════════════════════
def dns_forhad():
    section("07 — DNS RECON")
    domain = get_input("Enter domain name")
    if not domain: fail("Domain cannot be empty."); return

    if not require_tool("nslookup", "pkg install dnsutils"):
        warn("Falling back to basic socket DNS resolution.")

    print()
    record_types = ['A','AAAA','MX','NS','TXT','CNAME','SOA','PTR','CAA','SRV']
    dns_records  = {}

    for rtype in record_types:
        if shutil.which("nslookup"):
            try:
                result = subprocess.run(
                    ['nslookup', f'-type={rtype}', domain],
                    capture_output=True, text=True, timeout=DEFAULT_TIMEOUT)
                lines = [
                    l.strip() for l in result.stdout.splitlines()
                    if (l.strip()
                        and 'Server'    not in l
                        and 'Address'   not in l
                        and (domain.lower()  in l.lower()
                             or 'mail'       in l.lower()
                             or 'name'       in l.lower()
                             or 'canonical'  in l.lower()
                             or 'text'       in l.lower()))
                ]
                if lines:
                    info(f"{rtype:<8} → {c(C.CYAN,lines[0][:65])}")
                    dns_records[rtype] = lines
                else:
                    print(f"  {c(C.DIM,'·')} {rtype:<8} → {c(C.DIM,'No record')}")
            except Exception:
                print(f"  {c(C.DIM,'·')} {rtype:<8} → {c(C.DIM,'Error')}")
        else:
            print(f"  {c(C.DIM,'·')} {rtype:<8} → {c(C.DIM,'nslookup unavailable')}")

    sep()
    try:
        ip   = socket.gethostbyname(domain)
        ok(f"A Record IP  → {c(C.GREEN,ip)}")
        try:
            rdns = socket.gethostbyaddr(ip)[0]
            ok(f"Reverse DNS  → {c(C.CYAN,rdns)}")
        except Exception:
            info(f"Reverse DNS  → {c(C.DIM,'N/A')}")
    except Exception:
        fail("Could not resolve domain.")

    sep()
    # Robots.txt parser
    info("Checking robots.txt for hidden paths...")
    try:
        resp, body = fetch(f"https://{domain}/robots.txt")
        if resp.status == 200:
            text = body.decode('utf-8', errors='ignore')
            ok(f"/robots.txt  → {c(C.GREEN,'FOUND')}")
            disallowed = [l.split(':',1)[1].strip()
                          for l in text.splitlines()
                          if l.lower().startswith('disallow:') and len(l) > 12]
            if disallowed:
                info(f"Disallowed paths ({len(disallowed)}):")
                for p in disallowed[:10]:
                    print(f"    {c(C.DIM,'•')} {c(C.YELLOW,p)}")
    except Exception:
        info(f"/robots.txt  → {c(C.DIM,'Not accessible')}")

    sep()
    # Wayback Machine lookup
    info("Checking Wayback Machine for archived snapshots...")
    try:
        wb_url = f"https://archive.org/wayback/available?url={domain}"
        resp, body = fetch(wb_url)
        wb_data = json.loads(body.decode())
        snap = wb_data.get("archived_snapshots",{}).get("closest",{})
        if snap.get("available"):
            ok(f"Wayback Snap → {c(C.CYAN, snap.get('url','N/A'))}")
            info(f"Snapshot     → {c(C.WHITE, snap.get('timestamp','N/A'))}")
        else:
            info(f"Wayback      → {c(C.DIM,'No snapshot found')}")
    except Exception:
        info(f"Wayback      → {c(C.DIM,'Unavailable')}")

    sep()
    for chk in ['/security.txt','/.well-known/security.txt','/sitemap.xml']:
        try:
            resp, body = fetch(f"https://{domain}{chk}")
            if resp.status == 200:
                ok(f"{chk:<36} → {c(C.GREEN,'FOUND')}")
        except Exception:
            info(f"{chk:<36} → {c(C.DIM,'Not found')}")

    sep()
    info("DNS Brute Force (mini wordlist):")
    brute_list = ['www','mail','ftp','api','dev','staging',
                  'admin','vpn','ns1','ns2','remote','portal',
                  'shop','app','test','beta','cloud','git']
    for sub in brute_list:
        tgt = f"{sub}.{domain}"
        try:
            ip_bf = socket.gethostbyname(tgt)
            ok(f"  {tgt:<42} → {c(C.GREEN,ip_bf)}")
        except socket.gaierror:
            print(f"  {c(C.DIM,'·')}  {tgt:<42} → {c(C.DIM,'NX')}")

    RESULTS["dns_recon"] = {"domain": domain, "records": dns_records}
    log(f"DNS RECON: {domain}")

# ══════════════════════════════════════════════
# 08 — WHOIS LOOKUP
# ══════════════════════════════════════════════
def whois_lookup():
    section("08 — WHOIS LOOKUP")
    domain = get_input("Enter domain or IP")
    if not domain: fail("Input cannot be empty."); return

    if not require_tool("whois", "pkg install whois"):
        return

    progress_bar("Querying WHOIS server")
    print()

    try:
        result = subprocess.run(
            ['whois', domain],
            capture_output=True, text=True, timeout=15)
        output = result.stdout

        fields = {
            'Registrar':          r'Registrar:\s*(.+)',
            'Creation Date':      r'Creation Date:\s*(.+)',
            'Expiry Date':        r'Registry Expiry Date:\s*(.+)|Expiration Date:\s*(.+)',
            'Updated Date':       r'Updated Date:\s*(.+)',
            'Domain Status':      r'Domain Status:\s*(.+)',
            'Name Servers':       r'Name Server:\s*(.+)',
            'Registrant Org':     r'Registrant Organization:\s*(.+)',
            'Registrant Country': r'Registrant Country:\s*(.+)',
            'Registrant Email':   r'Registrant Email:\s*(.+)',
            'Admin Email':        r'Admin Email:\s*(.+)',
            'Tech Email':         r'Tech Email:\s*(.+)',
            'DNSSEC':             r'DNSSEC:\s*(.+)',
        }

        found_any = False
        for label, pattern in fields.items():
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                val = next((g for g in match.groups() if g), '').strip()[:80]
                if val:
                    info(f"{label:<22} → {c(C.WHITE,val)}")
                    found_any = True

        if not found_any:
            warn("Could not parse WHOIS. Raw output:")
            for line in output.splitlines()[:25]:
                if line.strip():
                    print(f"    {c(C.DIM,line.strip())}")

        RESULTS["whois"] = {"domain": domain}
        log(f"WHOIS: {domain}")

    except subprocess.TimeoutExpired:
        fail("WHOIS query timed out.")
    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 09 — SSL CHECKER  (timezone-aware)
# ══════════════════════════════════════════════
def ssl_checker():
    section("09 — SSL CHECKER")
    domain = get_input("Enter domain (without https://)")
    if not domain: fail("Domain cannot be empty."); return

    progress_bar("Fetching SSL certificate")
    print()

    try:
        ctx  = ssl.create_default_context()
        conn = ctx.wrap_socket(socket.socket(), server_hostname=domain)
        conn.settimeout(DEFAULT_TIMEOUT)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        tls_version = conn.version() if hasattr(conn, 'version') else 'N/A'
        conn.close()

        subject    = dict(x[0] for x in cert.get('subject', []))
        issuer     = dict(x[0] for x in cert.get('issuer',  []))
        not_after  = cert.get('notAfter',  '')
        not_before = cert.get('notBefore', '')

        try:
            # Use timezone-aware datetime to avoid DeprecationWarning in Python 3.12+
            expiry    = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            expiry    = expiry.replace(tzinfo=timezone.utc)
            now_utc   = datetime.now(timezone.utc)
            days_left = (expiry - now_utc).days
            exp_str   = expiry.strftime("%Y-%m-%d")
            if days_left > 30:
                exp_disp = c(C.GREEN,  f"{exp_str} ({days_left} days left ✔)")
            elif days_left > 0:
                exp_disp = c(C.YELLOW, f"{exp_str} (⚠ only {days_left} days left!)")
            else:
                exp_disp = c(C.RED,    f"{exp_str} (EXPIRED {abs(days_left)} days ago!)")
        except Exception:
            exp_disp = not_after

        sans = cert.get('subjectAltName', [])
        rows = [
            ("Common Name",  subject.get('commonName',       'N/A')),
            ("Organization", subject.get('organizationName', 'N/A')),
            ("Country",      subject.get('countryName',      'N/A')),
            ("Issuer Org",   issuer.get('organizationName',  'N/A')),
            ("Issuer CN",    issuer.get('commonName',        'N/A')),
            ("Valid From",   not_before),
            ("TLS Version",  tls_version),
            ("SANs Count",   f"{len(sans)} entries"),
        ]
        for label, val in rows:
            info(f"{label:<14} → {c(C.WHITE,str(val)[:65])}")
        print(f"  {c(C.BLUE,'›')} {'Expires':<14} → {exp_disp}")

        if sans:
            sep()
            info(f"Subject Alt Names ({len(sans)}):")
            for _, name in sans[:10]:
                print(f"    {c(C.DIM,'•')} {c(C.CYAN,name)}")
            if len(sans) > 10:
                print(f"    {c(C.DIM,f'... and {len(sans)-10} more')}")

        RESULTS["ssl"] = {
            "domain": domain,
            "issuer": issuer.get('organizationName','?'),
            "tls":    tls_version
        }
        log(f"SSL: {domain} TLS:{tls_version}")

    except ssl.SSLError as e:       fail(f"SSL Error: {e}")
    except socket.gaierror:         fail("Could not resolve domain.")
    except ConnectionRefusedError:  fail("Port 443 closed — no HTTPS.")
    except Exception as e:          fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 10 — HEADER ANALYZER
# ══════════════════════════════════════════════
def header_analyzer():
    section("10 — HEADER ANALYZER")
    url = get_input("Enter URL (e.g. https://example.com)")
    if not url: fail("URL cannot be empty."); return
    if not url.startswith('http'): url = 'https://' + url

    progress_bar("Fetching HTTP headers")
    print()

    try:
        resp, _ = fetch(url, extra_headers={"User-Agent": f"Ghost-OSINT/{VERSION}"})
        hdrs    = dict(resp.headers)

        info(f"Status Code  → {c(C.GREEN,str(resp.status))}")
        info(f"Final URL    → {c(C.CYAN,resp.url[:65])}")
        sep()

        sec_hdrs = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy':   'CSP',
            'X-Frame-Options':           'Clickjacking Protection',
            'X-Content-Type-Options':    'MIME Sniffing Protection',
            'X-XSS-Protection':          'XSS Protection',
            'Referrer-Policy':           'Referrer Policy',
            'Permissions-Policy':        'Permissions Policy',
            'Cross-Origin-Opener-Policy':'COOP',
        }
        score = 0
        print(f"\n  {c(C.BOLD,'Security Headers:')}")
        for h, label in sec_hdrs.items():
            val = hdrs.get(h) or hdrs.get(h.lower())
            if val:
                ok(f"{label:<30} → {c(C.GREEN,'PRESENT')} ({val[:40]})")
                score += 1
            else:
                fail(f"{label:<30} → {c(C.RED,'MISSING')}")

        sep()
        grade_map = {8:('A+',C.GREEN),6:('A',C.GREEN),
                     4:('B',C.YELLOW),2:('C',C.YELLOW),0:('D',C.RED)}
        grade, clr = next(
            (v for k,v in sorted(grade_map.items(), reverse=True) if score >= k),
            ('F', C.RED))
        info(f"Security Score → {c(clr,f'{score}/8  Grade: {grade}')}")

        print(f"\n  {c(C.BOLD,'Server Info:')}")
        for h in ['Server','X-Powered-By','Via','Content-Type',
                  'Cache-Control','X-Cache','Age']:
            val = hdrs.get(h) or hdrs.get(h.lower())
            if val: info(f"{h:<24} → {c(C.CYAN,val[:65])}")

        sep()
        print(f"\n  {c(C.BOLD,'HTTP Method Testing:')}")
        parsed = urlparse(url)
        host   = parsed.netloc
        path   = parsed.path or '/'
        for method in ['OPTIONS','DELETE','PUT','TRACE','PATCH']:
            try:
                co = http.client.HTTPSConnection(host, timeout=DEFAULT_TIMEOUT)
                co.request(method, path); r = co.getresponse(); co.close()
                if r.status in [200,204]:
                    warn(f"{method:<10} → {c(C.YELLOW,f'ALLOWED ({r.status})')}")
                else:
                    info(f"{method:<10} → {c(C.DIM,str(r.status))}")
            except Exception:
                info(f"{method:<10} → {c(C.DIM,'N/A')}")

        RESULTS["headers"] = {"url":url,"score":score,"grade":grade}
        log(f"HEADERS: {url} Score:{score}/8")

    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 11 — GITHUB RECON  (optional token support)
# ══════════════════════════════════════════════
def github_forhad():
    section("11 — GITHUB RECON")
    warn("Uses GitHub public API — add token to config.json for higher rate limit.")
    username = get_input("Enter GitHub username")
    if not username: fail("Username cannot be empty."); return

    progress_bar("Fetching GitHub public data")
    print()

    gh_headers = {
        "User-Agent": f"Ghost-OSINT/{VERSION}",
        "Accept":     "application/vnd.github.v3+json",
    }
    if GITHUB_TOKEN:
        gh_headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        resp, body = fetch(
            f"https://api.github.com/users/{username}",
            extra_headers=gh_headers)
        user = json.loads(body.decode())

        if user.get('message') == 'Not Found':
            fail("GitHub user not found."); return

        profile_fields = [
            ("Name",         user.get('name',             'N/A')),
            ("Bio",          user.get('bio',              'N/A')),
            ("Company",      user.get('company',          'N/A')),
            ("Location",     user.get('location',         'N/A')),
            ("Email",        user.get('email',            'N/A')),
            ("Blog/Website", user.get('blog',             'N/A')),
            ("Twitter",      user.get('twitter_username', 'N/A')),
            ("Public Repos", str(user.get('public_repos', 0))),
            ("Followers",    str(user.get('followers',    0))),
            ("Following",    str(user.get('following',    0))),
            ("Gists",        str(user.get('public_gists', 0))),
            ("Account Type", user.get('type',             'N/A')),
            ("Created At",   user.get('created_at',       'N/A')[:10]),
            ("Updated At",   user.get('updated_at',       'N/A')[:10]),
            ("Profile URL",  user.get('html_url',         'N/A')),
        ]
        for label, val in profile_fields:
            if val and val not in ('N/A','None','null',''):
                info(f"{label:<16} → {c(C.WHITE, str(val)[:70])}")

        sep(); info("Public Repositories (latest 10):")
        repos = []
        try:
            resp2, body2 = fetch(
                f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10",
                extra_headers=gh_headers)
            repos = json.loads(body2.decode())
            print()
            for repo in repos:
                lang  = repo.get('language') or 'N/A'
                stars = repo.get('stargazers_count', 0)
                forks = repo.get('forks_count',      0)
                desc  = (repo.get('description') or '')[:45]
                ok(f"{repo['name']:<35} ⭐{stars:<4} 🍴{forks:<4} "
                   f"[{lang}]  {c(C.DIM,desc)}")
        except Exception:
            warn("Could not fetch repositories.")

        sep()
        try:
            resp3, body3 = fetch(
                f"https://api.github.com/users/{username}/orgs",
                extra_headers=gh_headers)
            orgs = json.loads(body3.decode())
            if orgs:
                info(f"Organizations ({len(orgs)}):")
                for org in orgs:
                    print(f"    {c(C.DIM,'•')} {c(C.CYAN,org.get('login','?'))}")
        except Exception: pass

        sep()
        try:
            resp4, body4 = fetch(
                f"https://api.github.com/users/{username}/events/public?per_page=5",
                extra_headers=gh_headers)
            events = json.loads(body4.decode())
            if events:
                info(f"Recent Activity (last {len(events)} events):")
                for ev in events:
                    etype     = ev.get('type','?')
                    repo_name = ev.get('repo',{}).get('name','?')
                    created   = ev.get('created_at','')[:10]
                    print(f"    {c(C.DIM,'•')} {c(C.YELLOW,etype):<35} "
                          f"→ {c(C.CYAN,repo_name)}  {c(C.DIM,created)}")
        except Exception: pass

        RESULTS["github_recon"] = {
            "username": username, "repos": len(repos)
        }
        log(f"GITHUB RECON: {username}")

    except HTTPError as e:
        if e.code == 404:   fail("GitHub user not found.")
        elif e.code == 403: warn("Rate limited by GitHub API. Add token to config.json.")
        else:               fail(f"HTTP Error: {e.code}")
    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 12 — BREACH CHECKER
# ══════════════════════════════════════════════
def breach_checker():
    section("12 — BREACH CHECKER")
    warn("Checks against public breach databases (informational only).")
    email = get_input("Enter email address to check")
    if not email: fail("Email cannot be empty."); return

    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        fail("Invalid email format."); return

    progress_bar("Checking breach databases")
    print()

    sha1 = hashlib.sha1(email.encode()).hexdigest().upper()
    info(f"Email SHA1   → {c(C.DIM,sha1[:20]+'...')}")
    info(f"Domain       → {c(C.CYAN,email.split('@')[1])}")

    known_breached = {
        'linkedin.com': '2016 LinkedIn breach — 117M accounts',
        'adobe.com':    '2013 Adobe breach — 153M accounts',
        'yahoo.com':    '2013-2016 Yahoo — 3B accounts affected',
        'hotmail.com':  'Microsoft/Hotmail breach exposure',
        'myspace.com':  '2013 Myspace breach — 359M accounts',
        'tumblr.com':   '2013 Tumblr breach — 65M accounts',
        'dropbox.com':  '2012 Dropbox breach — 68M accounts',
        'twitter.com':  '2022 Twitter breach — 200M emails',
        'twitch.tv':    '2021 Twitch source code leak',
        'facebook.com': '2019 Facebook scraping — 533M records',
        'canva.com':    '2019 Canva breach — 137M accounts',
        'quora.com':    '2018 Quora breach — 100M accounts',
        'chegg.com':    '2018 Chegg breach — 40M accounts',
        'dubsmash.com': '2018 Dubsmash — 162M accounts',
    }

    user_domain = email.split('@')[1].lower()
    sep()

    if user_domain in known_breached:
        warn(f"Domain Risk  → {c(C.RED,'HIGH')}")
        warn(f"Known Breach → {c(C.YELLOW,known_breached[user_domain])}")
    else:
        ok(f"Domain Risk  → {c(C.GREEN,'Not in known high-risk list')}")

    sep()
    info("For full breach check, visit:")
    print(f"    {c(C.CYAN,'• https://haveibeenpwned.com/')}")
    print(f"    {c(C.CYAN,'• https://dehashed.com/')}")
    print(f"    {c(C.CYAN,'• https://intelx.io/')}")

    # k-anonymity password check — use getpass so it's not visible in terminal
    sep()
    try:
        pwd = getpass.getpass(f"\n  {c(C.CYAN,'❯❯❯❯')} Check a password? (hidden input, Enter to skip): ")
    except Exception:
        pwd = ''

    if pwd:
        sha1_pwd = hashlib.sha1(pwd.encode()).hexdigest().upper()
        prefix_p, suffix_p = sha1_pwd[:5], sha1_pwd[5:]
        try:
            resp, body = fetch(
                f"https://api.pwnedpasswords.com/range/{prefix_p}",
                extra_headers={"Add-Padding":"true"})
            hashes = body.decode('utf-8')
            found_count = 0
            for line in hashes.splitlines():
                h, cnt = line.split(':')
                if h == suffix_p:
                    found_count = int(cnt); break
            if found_count:
                fail(f"Password found in "
                     f"{c(C.RED,f'{found_count:,}')} breaches! Change it immediately.")
            else:
                ok(f"Password NOT found in any known breach ✔")
        except Exception:
            warn("Could not reach HIBP password API.")

    RESULTS["breach"] = {"email": email}
    log(f"BREACH CHECK: {email}")

# ══════════════════════════════════════════════
# 13 — TECH DETECTOR
# ══════════════════════════════════════════════
def tech_detector():
    section("13 — TECH DETECTOR")
    url = get_input("Enter URL (e.g. https://example.com)")
    if not url: fail("URL cannot be empty."); return
    if not url.startswith('http'): url = 'https://' + url

    progress_bar("Analyzing technology stack")
    print()

    try:
        resp, body_bytes = fetch(url)
        body  = body_bytes.decode('utf-8', errors='ignore')
        hdrs  = dict(resp.headers)
        detected = {}

        cms = {
            'WordPress':   ['/wp-content/','/wp-includes/','wp-json','wp-embed'],
            'Joomla':      ['/components/com_','Joomla!','/templates/joomla'],
            'Drupal':      ['Drupal.settings','/sites/default/','X-Generator: Drupal'],
            'Magento':     ['Mage.Cookies','/skin/frontend/','magento'],
            'Shopify':     ['cdn.shopify.com','Shopify.theme','/cdn/shop/'],
            'Wix':         ['static.wixstatic.com','_wix_','X-Wix-'],
            'Squarespace': ['squarespace.com','sqsp.net'],
            'Ghost CMS':   ['ghost.io','/ghost/api/'],
            'PrestaShop':  ['prestashop','/modules/blockcart/'],
            'OpenCart':    ['opencart','route=common'],
            'Webflow':     ['webflow.com','wf-form'],
            'HubSpot CMS': ['hs-scripts.com','hubspot'],
        }
        frameworks = {
            'Laravel':       ['laravel_session','XSRF-TOKEN','Laravel'],
            'Django':        ['csrfmiddlewaretoken','django','DJANGO'],
            'Ruby on Rails': ['Phusion Passenger','_rails_session'],
            'ASP.NET':       ['__VIEWSTATE','ASP.NET','X-AspNet-Version'],
            'Spring Boot':   ['X-Application-Context','spring'],
            'Express.js':    ['X-Powered-By: Express'],
            'FastAPI':       ['fastapi','openapi.json'],
            'CodeIgniter':   ['ci_session','CodeIgniter'],
            'Symfony':       ['symfony','sf_redirect'],
        }
        frontend = {
            'React':       ['__react','data-reactroot','react-dom'],
            'Vue.js':      ['__vue','v-app','data-v-','vue.min.js'],
            'Angular':     ['ng-version','ng-app','_nghost'],
            'Next.js':     ['__NEXT_DATA__','/_next/'],
            'Nuxt.js':     ['__nuxt','/_nuxt/'],
            'jQuery':      ['jquery.min.js','jQuery','jquery-'],
            'Bootstrap':   ['bootstrap.min.css','bootstrap.min.js'],
            'Tailwind CSS':['tailwind','cdn.tailwindcss.com'],
            'Svelte':      ['__svelte','svelte'],
        }
        analytics = {
            'Google Analytics':   ['gtag','UA-','G-','google-analytics.com'],
            'Google Tag Manager': ['googletagmanager.com','GTM-'],
            'Facebook Pixel':     ['fbevents.js','connect.facebook.net'],
            'HotJar':             ['hotjar.com','hjid'],
            'Mixpanel':           ['mixpanel.com','mixpanel.init'],
            'Segment':            ['segment.com','analytics.js'],
            'Intercom':           ['intercom.io','intercomSettings'],
            'Zendesk':            ['zendesk.com','zdassets.com'],
            'Crisp Chat':         ['crisp.chat','CRISP_WEBSITE_ID'],
        }
        cdn_waf = {
            'Cloudflare':       ['cf-ray','cloudflare','cf-cache-status'],
            'AWS CloudFront':   ['cloudfront','x-amz-cf-id'],
            'Akamai':           ['akamai','AkamaiGHost'],
            'Fastly':           ['fastly','x-fastly','x-served-by'],
            'Sucuri WAF':       ['sucuri','x-sucuri-id'],
            'Imperva Incapsula':['incap_ses','visid_incap','x-iinfo'],
            'Varnish Cache':    ['via: varnish','x-varnish'],
            'Nginx':            ['nginx'],
            'Apache':           ['apache'],
            'LiteSpeed':        ['litespeed','x-litespeed'],
            'IIS':              ['microsoft-iis','x-aspnet-version'],
        }

        combined = body + str(hdrs)
        comb_low = combined.lower()

        for category, tech_dict, label in [
            (cms,       'CMS',       'CMS Detection'),
            (frameworks,'Framework', 'Backend Framework'),
            (frontend,  'Frontend',  'Frontend Framework'),
            (analytics, 'Analytics', 'Analytics / Marketing'),
        ]:
            print(f"\n  {c(C.BOLD,label+':')}")
            for tech, pats in category.items():
                if any(p in combined for p in pats):
                    ok(f"{tech:<24} → {c(C.GREEN,'DETECTED')}")
                    detected[tech] = label

        sep()
        print(f"\n  {c(C.BOLD,'CDN / WAF Fingerprinting:')}")
        cdn_found = False
        for cdn, pats in cdn_waf.items():
            if any(p.lower() in comb_low for p in pats):
                ok(f"{cdn:<24} → {c(C.YELLOW,'DETECTED')}")
                detected[cdn] = 'CDN/WAF'; cdn_found = True
        if not cdn_found:
            info(f"CDN/WAF      → {c(C.DIM,'None identified')}")

        sep()
        info(f"Total technologies detected: {c(C.GREEN,str(len(detected)))}")
        RESULTS["tech"] = {"url": url, "detected": list(detected.keys())}
        log(f"TECH DETECT: {url} — {list(detected.keys())}")

    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 14 — REVERSE IP  (with fallback)
# ══════════════════════════════════════════════
def reverse_ip():
    section("14 — REVERSE IP")
    warn("Finds other domains hosted on the same server.")
    target = get_input("Enter IP address or domain")
    if not target: fail("Input cannot be empty."); return

    print(); progress_bar("Performing reverse IP lookup"); print()

    try:
        ip = socket.gethostbyname(target)
        if ip != target:
            info(f"Resolved     → {c(C.CYAN,ip)}")
        info(f"IP Address   → {c(C.WHITE,ip)}")

        try:
            rdns = socket.gethostbyaddr(ip)
            ok(f"PTR Record   → {c(C.GREEN,rdns[0])}")
            if rdns[1]:
                info(f"Aliases      → {c(C.CYAN,', '.join(rdns[1]))}")
        except socket.herror:
            warn(f"PTR Record   → {c(C.DIM,'No PTR record found')}")

        sep()
        # Use HTTPS geo endpoint
        geo_url = f"https://ipwho.is/{ip}"
        try:
            resp, body = fetch(geo_url)
            geo = json.loads(body.decode())
            if geo.get('success'):
                conn = geo.get('connection', {})
                info(f"ISP          → {c(C.WHITE,conn.get('isp','N/A'))}")
                info(f"Organization → {c(C.WHITE,conn.get('org','N/A'))}")
                info(f"AS Number    → {c(C.WHITE,conn.get('asn','N/A'))}")
                info(f"Location     → "
                     f"{c(C.WHITE,geo.get('city','?')+', '+geo.get('country','?'))}")
        except Exception:
            warn("Geo lookup failed.")

        sep()
        info("Checking shared hosting (HackerTarget API)...")
        ht_success = False
        try:
            ht_url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
            resp2, body2 = fetch(ht_url, timeout=15)
            raw = body2.decode('utf-8', errors='ignore').strip()

            if 'error' in raw.lower() or 'API count' in raw:
                warn("HackerTarget API limit reached.")
            elif raw:
                domain_list = [d.strip() for d in raw.splitlines() if d.strip()]
                ok(f"Shared Domains → {c(C.GREEN,str(len(domain_list)))} found:")
                print()
                for d in domain_list[:20]:
                    print(f"    {c(C.DIM,'•')} {c(C.CYAN,d)}")
                if len(domain_list) > 20:
                    info(f"... and {len(domain_list)-20} more")
                RESULTS["reverse_ip"] = {"ip":ip,"domains":domain_list}
                ht_success = True
        except Exception:
            pass

        if not ht_success:
            warn("HackerTarget API unavailable. Fallback options:")
            info(f"  → {c(C.CYAN,f'https://viewdns.info/reverseip/?host={ip}')}")
            info(f"  → Bing search: {c(C.CYAN,f'ip:{ip}')}")

        log(f"REVERSE IP: {ip}")

    except socket.gaierror:
        fail("Could not resolve hostname.")
    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 15 — ASN LOOKUP  (new module)
# ══════════════════════════════════════════════
def asn_lookup():
    section("15 — ASN LOOKUP")
    target = get_input("Enter IP address or ASN (e.g. AS15169)")
    if not target: fail("Input cannot be empty."); return

    progress_bar("Querying ASN data")
    print()

    try:
        if target.upper().startswith("AS"):
            url = f"https://ipwho.is/{target}"
        else:
            url = f"https://ipwho.is/{target}"
        resp, body = fetch(url)
        data = json.loads(body.decode())

        conn = data.get("connection", {})
        if conn:
            info(f"ASN          → {c(C.WHITE, str(conn.get('asn','N/A')))}")
            info(f"Organization → {c(C.WHITE, conn.get('org','N/A'))}")
            info(f"ISP          → {c(C.WHITE, conn.get('isp','N/A'))}")
            info(f"Domain       → {c(C.CYAN,  conn.get('domain','N/A'))}")
        if data.get("country"):
            info(f"Country      → {c(C.WHITE, data.get('country','N/A'))}")

        RESULTS["asn_lookup"] = {"target": target, "data": conn}
        log(f"ASN LOOKUP: {target}")
    except Exception as e:
        fail(f"Error: {e}")

# ══════════════════════════════════════════════
# 16 — EXPORT RESULTS
# ══════════════════════════════════════════════
def export_results():
    section("EXPORT RESULTS")
    if not RESULTS:
        warn("No results yet. Run some modules first."); return

    print(f"\n  {c(C.BOLD,'Format:')}")
    print(f"  {c(C.CYAN,'[1]')} JSON")
    print(f"  {c(C.CYAN,'[2]')} TXT Report")
    print(f"  {c(C.CYAN,'[3]')} HTML Report (Dark Mode)")
    choice = get_input("Choose")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == '1':
        fname = f"ghost_{ts}.json"
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(RESULTS, f, indent=2, default=str)
        ok(f"Saved → {c(C.CYAN,fname)}")

    elif choice == '2':
        fname = f"ghost_{ts}.txt"
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(f"GHOST — OSINT Toolkit v{VERSION}\n")
            f.write(f"Developer: {DEVELOPER}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*60+"\n\n")
            for key, val in RESULTS.items():
                f.write(f"[{key.upper()}]\n")
                f.write(json.dumps(val, indent=2, default=str))
                f.write("\n\n")
        ok(f"Saved → {c(C.CYAN,fname)}")

    elif choice == '3':
        fname = f"ghost_{ts}.html"
        cards = ""
        for key, val in RESULTS.items():
            safe  = html_lib.escape(json.dumps(val, indent=2, default=str))
            title = html_lib.escape(key.replace("_"," ").upper())
            cards += (f'<div class="card"><h2>{title}</h2>'
                      f'<pre>{safe}</pre></div>\n')

        html_doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ghost OSINT Report — {DEVELOPER}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#06060e;color:#ccc;font-family:'Courier New',monospace;padding:24px;
      background-image:radial-gradient(ellipse at 20% 20%,#0d0d2a 0%,#06060e 70%)}}
h1{{color:#00fff7;text-align:center;letter-spacing:5px;margin:16px 0 4px;
    text-shadow:0 0 20px #00fff7aa}}
.sub{{text-align:center;color:#555;font-size:13px;margin-bottom:24px}}
.dev{{text-align:center;color:#7f7fff;font-size:15px;margin-bottom:20px;letter-spacing:3px}}
h2{{color:#7f7fff;border-bottom:1px solid #1e1e30;padding-bottom:6px;margin-bottom:12px;
    letter-spacing:2px}}
.card{{background:#0c0c1a;border:1px solid #1e1e35;border-radius:10px;
       padding:18px;margin:14px 0;box-shadow:0 0 12px #00fff710}}
pre{{color:#9898c0;white-space:pre-wrap;word-break:break-all;font-size:13px;
     line-height:1.6}}
.badge{{display:inline-block;background:#00fff715;color:#00fff7;border:1px solid #00fff730;
        padding:2px 8px;border-radius:4px;font-size:11px;margin-left:8px}}
.footer{{text-align:center;color:#333;margin-top:30px;font-size:12px;
         padding:12px;border-top:1px solid #1a1a2e}}
.stats{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;justify-content:center}}
.stat{{background:#0c0c1a;border:1px solid #1e1e35;border-radius:8px;
       padding:10px 18px;text-align:center;min-width:100px}}
.stat-num{{font-size:22px;color:#00fff7;font-weight:bold}}
.stat-lbl{{font-size:11px;color:#555;margin-top:4px}}
</style></head><body>
<h1>👻 GHOST — OSINT REPORT</h1>
<p class="dev">Developer: {DEVELOPER}</p>
<p class="sub">Generated: {html_lib.escape(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
 &nbsp;|&nbsp; Ghost OSINT Toolkit v{VERSION}</p>
<div class="stats">
  <div class="stat"><div class="stat-num">{len(RESULTS)}</div>
    <div class="stat-lbl">Modules Run</div></div>
</div>
{cards}
<div class="footer">Ghost OSINT Toolkit v{VERSION} &nbsp;|&nbsp; Developer: {DEVELOPER}
<br>⚠ Authorized Use Only — Unauthorized scanning may violate laws.</div>
</body></html>"""
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        ok(f"Saved → {c(C.CYAN,fname)}")

# ══════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════
def main_menu():
    left_col = [
        ("01", "User Recon",     user_forhad),
        ("02", "Phone Info",     phone_info),
        ("03", "Mail Finder",    mail_finder),
        ("04", "IP Location",    ip_location),
        ("05", "Subdomain Scan", subdomain_scan),
        ("06", "Port Scanner",   port_scanner),
        ("07", "DNS Recon",      dns_forhad),
        ("08", "WHOIS Lookup",   whois_lookup),
    ]
    right_col = [
        ("09", "SSL Checker",    ssl_checker),
        ("10", "Header Analyzer",header_analyzer),
        ("11", "GitHub Recon",   github_forhad),
        ("12", "Breach Checker", breach_checker),
        ("13", "Tech Detector",  tech_detector),
        ("14", "Reverse IP",     reverse_ip),
        ("15", "ASN Lookup",     asn_lookup),
        ("16", "Export Results", export_results),
    ]

    all_items = left_col + right_col

    while True:
        banner()

        line_top = c(C.DIM, "  ┌" + "─"*28 + "┬" + "─"*28 + "┐")
        line_mid = c(C.DIM, "  ├" + "─"*28 + "┼" + "─"*28 + "┤")
        line_bot = c(C.DIM, "  └" + "─"*28 + "┴" + "─"*28 + "┘")
        hdr_l = c(C.BOLD, c(C.MAGENTA, "          LEFT PANEL           "))
        hdr_r = c(C.BOLD, c(C.MAGENTA, "          RIGHT PANEL          "))

        print(line_top)
        print(c(C.DIM,"  │") + hdr_l + c(C.DIM,"│") + hdr_r + c(C.DIM,"│"))
        print(line_mid)

        for (nl, namel, _), (nr, namer, _) in zip(left_col, right_col):
            cell_l = (f" {c(C.CYAN,f'[{nl}]')} {c(C.WHITE, namel):<22}")
            cell_r = (f" {c(C.CYAN,f'[{nr}]')} {c(C.WHITE, namer):<22}")
            print(c(C.DIM,"  │") + cell_l + c(C.DIM,"│") + cell_r + c(C.DIM,"│"))

        print(line_mid)
        cell_exit = (f" {c(C.RED,'[00]')} {c(C.RED,'Exit'):<22}")
        cell_ver  = (f"  {c(C.DIM,f'Ghost v{VERSION} | Developer: {DEVELOPER}'):<28}")
        print(c(C.DIM,"  │") + cell_exit + c(C.DIM,"│") + cell_ver + c(C.DIM,"│"))
        print(line_bot)
        print()

        choice = get_input("Select module").strip().upper()

        if choice in ['0','00','EXIT','Q','QUIT']:
            print(f"\n  {c(C.CYAN,f'Ghost v{VERSION} — Stay ethical. Stay legal.')}")
            print(f"  {c(C.DIM,f'Developer: {DEVELOPER}')}\n")
            sys.exit(0)

        mapping = {}
        for num, _, func in all_items:
            mapping[num]                    = func
            mapping[num.lstrip('0') or '0'] = func

        func = mapping.get(choice) or mapping.get(choice.lstrip('0') or '0')
        if func:
            try:
                func()
            except KeyboardInterrupt:
                print(f"\n\n  {c(C.YELLOW,'Module interrupted.')}")
            input(f"\n  {c(C.DIM,'Press Enter to return to menu...')}")
        else:
            warn("Invalid option. Try again.")
            time.sleep(0.8)

# ══════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {c(C.CYAN,f'Goodbye — {DEVELOPER}')}\n")
