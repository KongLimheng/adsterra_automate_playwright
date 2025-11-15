import random
import re
import pytz
import hashlib
from fake_useragent import UserAgent

ua = UserAgent()

# ===================================================
# BASE WEIGHTS
# ===================================================
PLATFORM_WEIGHTS = {
    "windows": 0.40,
    "mac_intel": 0.20,
    "mac_arm": 0.30,
    "linux": 0.10,
}

BROWSER_WEIGHTS = {
    "edge": 0.40,
    "safari": 0.40,
    "firefox": 0.15,
    "chrome": 0.05,
}

# ===================================================
# PLATFORM DEFINITIONS
# ===================================================
PLATFORM_DATA = {
    "windows": {
        "platform": "Win32",
        "cpu": "Intel x64",
        "architecture": "x86_64",
        "ua_platform": "(Windows NT 10.0; Win64; x64)",
        "screen_sizes": [(1920,1080), (1366,768), (2560,1440)],
        "gpus": [
            ("ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)", "Google Inc."),
            ("ANGLE (Intel UHD Graphics Direct3D11 vs_5_0 ps_5_0)", "Google Inc."),
        ]
    },
    "mac_intel": {
        "platform": "MacIntel",
        "cpu": "Intel",
        "architecture": "x86_64",
        "ua_platform": "(Macintosh; Intel Mac OS X 10_15_7)",
        "screen_sizes": [(2560,1600), (2880,1800), (1680,1050)],
        "gpus": [
            ("Intel Iris Plus Graphics", "Apple Inc."),
            ("AMD Radeon Pro 555", "AMD"),
        ]
    },
    "mac_arm": {
        "platform": "MacARM",
        "cpu": "Apple M2",
        "architecture": "arm64",
        "ua_platform": "(Macintosh; arm64; Mac OS X 14_0)",
        "screen_sizes": [(3024,1964), (2560,1600), (3456,2234)],
        "gpus": [
            ("Apple M1", "Apple Inc."),
            ("Apple M2", "Apple Inc."),
            ("Apple M3", "Apple Inc."),
        ]
    },
    "linux": {
        "platform": "Linux x86_64",
        "cpu": "Intel x64",
        "architecture": "x86_64",
        "ua_platform": "(X11; Linux x86_64)",
        "screen_sizes": [(1920,1080), (2560,1440)],
        "gpus": [
            ("NVIDIA GTX 1060", "NVIDIA Corporation"),
            ("llvmpipe (LLVM 11.0.0)", "Mesa/X.org"),
        ]
    },
}

LANGUAGES = [
    "en-US","en-GB","fr-FR","de-DE","es-ES",
    "pt-BR","ja-JP","ko-KR","zh-CN"
]

TIMEZONES = pytz.all_timezones


# ===================================================
# UTILITY FUNCTIONS
# ===================================================
def weighted_choice(d):
    return random.choices(list(d.keys()), weights=list(d.values()), k=1)[0]

def canvas_fingerprint():
    data = str(random.random()).encode()
    return hashlib.md5(data).hexdigest()

def audio_fingerprint():
    data = str(random.random() * 9999).encode()
    return hashlib.sha1(data).hexdigest()

# ===================================================
# FIREFOX SPECIAL BUILD
# ===================================================
def build_firefox_ua(platform_paren):
    raw = ua.firefox
    m = re.search(r"Firefox/([0-9\.]+)", raw)
    version = m.group(1) if m else "130.0"
    return f"Mozilla/5.0 {platform_paren} Gecko/20100101 Firefox/{version}"

# ===================================================
# SAFARI DESKTOP CLEANUP
# ===================================================
def clean_safari(ua_str):
    ua_str = re.sub(r"iPhone;[^)]*\)", "Macintosh)", ua_str)
    ua_str = re.sub(r"\sMobile\/[^\s)]+", "", ua_str)
    return ua_str

# ===================================================
# BUILD USER-AGENT
# ===================================================
def build_user_agent(browser, platform_key):
    plat = PLATFORM_DATA[platform_key]["ua_platform"]

    if browser == "firefox":
        return build_firefox_ua(plat)

    raw = getattr(ua, browser, ua.random)

    ua_string = re.sub(
        r'^Mozilla/5.0\s*\([^)]+\)',
        f"Mozilla/5.0 {plat}",
        raw, count=1
    )

    if browser == "safari":
        ua_string = clean_safari(ua_string)

    return ua_string


# ===================================================
# MAIN — ULTRA HIGH-FIDELITY PROFILE
# ===================================================
def generate_profile():

    # Choose platform + browser
    platform_key = weighted_choice(PLATFORM_WEIGHTS)
    browser = weighted_choice(BROWSER_WEIGHTS)

    # Force Safari on Mac only
    if browser == "safari" and not platform_key.startswith("mac"):
        platform_key = random.choice(["mac_intel", "mac_arm"])

    pdata = PLATFORM_DATA[platform_key]

    lang = random.choice(LANGUAGES)
    tz = random.choice(TIMEZONES)
    screen = random.choice(pdata["screen_sizes"])
    gpu_renderer, gpu_vendor = random.choice(pdata["gpus"])

    # Generate UA
    ua_string = build_user_agent(browser, platform_key)

    # Final profile
    return {
        "userAgent": ua_string,
        "browser": browser,
        "os": platform_key,
        "platform": pdata["platform"],
        "cpuArchitecture": pdata["architecture"],
        "deviceMemoryGB": random.choice([4,8,16,32]),
        "hardwareConcurrency": random.choice([4,6,8,10,12]),

        # Display
        "screen": {
            "width": screen[0],
            "height": screen[1],
            "colorDepth": 24,
            "pixelRatio": random.choice([1.0, 1.25, 1.5, 2.0]),
        },

        # System
        "timezone": tz,
        "locale": lang,
        "languages": [lang, lang.split("-")[0]],
        "touchSupport": random.choice([0, 0, 0, 1]),

        # WebGL & GPU
        "webgl": {
            "vendor": gpu_vendor,
            "renderer": gpu_renderer,
        },

        # Fingerprints
        "canvasFingerprint": canvas_fingerprint(),
        "audioFingerprint": audio_fingerprint(),

        # Permissions
        "permissions": {
            "geolocation": random.choice(["prompt", "denied"]),
            "notifications": random.choice(["granted","denied","prompt"]),
            "camera": "prompt",
            "microphone": "prompt",
            "clipboard": "granted",
        },

        # Battery API
        "battery": {
            "charging": random.choice([True, False]),
            "level": round(random.uniform(0.1, 1.0), 2),
        },

        # Media Devices
        "mediaDevices": {
            "audioInputs": random.randint(1, 3),
            "audioOutputs": random.randint(1, 3),
            "videoInputs": random.randint(0, 2),
        },

        # Fonts (simplified realistic set)
        "fonts": [
            "Arial", "Verdana", "Times New Roman", "Courier New",
            "Helvetica", "Tahoma", "Noto Sans", "Segoe UI",
        ],

        # Color gamuts
        "colorGamut": random.choice(["srgb", "p3", "rec2020"]),

        # Speech synthesis
        "voices": [
            {"name": "Google US English", "lang": "en-US"},
            {"name": "Google UK English", "lang": "en-GB"},
        ]
    }


# Test
for _ in range(3):
    print(generate_profile())
    print("=" * 80)
