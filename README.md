# Target Store Maps Scraper

A tool to programmatically access and download Target store maps from their mobile app's Store Mode feature.

## Project Goal (v1)

Successfully capture and download the store map for one Target store location.

## Architecture Overview

```
Mobile App → API Calls → Proxy Interceptor → Parser → Store Map Data
```

## Approach

1. **Android Emulator Setup** - Run Target app in controlled environment
2. **Traffic Interception** - Use mitmproxy to capture API calls
3. **GPS Spoofing** - Simulate being inside a Target store
4. **API Analysis** - Identify endpoints that deliver map data
5. **Data Extraction** - Parse and save store map information

## Project Structure

```
Store maps scraping/
├── README.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup instructions
├── requirements.txt            # Python dependencies
├── config/
│   └── target_stores.json      # Target store locations for testing
├── scripts/
│   ├── verify_setup.py         # Verify emulator and proxy setup
│   ├── capture_api_traffic.py  # Monitor and save API calls
│   ├── analyze_traffic.py      # Parse captured traffic for map endpoints
│   └── download_store_map.py   # v1: Download store map for one store
├── data/
│   ├── captured/               # Raw mitmproxy captures
│   ├── analyzed/               # Parsed API endpoint info
│   └── maps/                   # Downloaded store maps
└── docs/
    └── API_FINDINGS.md         # Document discovered API endpoints

```

## Quick Start

### Prerequisites

- macOS (you're on darwin 25.0.0)
- Android Studio with emulator
- Python 3.8+
- Target mobile app APK

### Installation

```bash
cd "/Users/jordan.cheung/Documents/GitHub/Store maps scraping"

# Install Python dependencies
pip install -r requirements.txt

# Follow detailed setup guide
cat SETUP_GUIDE.md
```

### Workflow

1. **Setup Phase** (One-time)
   ```bash
   # Verify your environment
   python scripts/verify_setup.py
   ```

2. **Capture Phase**
   ```bash
   # Start mitmproxy and capture traffic
   python scripts/capture_api_traffic.py
   ```

3. **Analysis Phase**
   ```bash
   # Analyze captured traffic
   python scripts/analyze_traffic.py data/captured/target_session_1.har
   ```

4. **Download Phase** (v1 Goal)
   ```bash
   # Download store map for a specific store
   python scripts/download_store_map.py --store-id T-1234
   ```

## Current Status

- [ ] Emulator setup complete
- [ ] mitmproxy configured
- [ ] Target app installed
- [ ] GPS spoofing working
- [ ] API endpoints identified
- [ ] Store map downloaded (v1 goal)

## Legal & Ethical Notes

⚠️ **Important:**
- This is for educational/research purposes only
- Review Target's Terms of Service
- Store maps may be proprietary data
- Do not use for commercial purposes without permission
- Respect rate limits and don't overload Target's servers

## Next Steps

1. Complete emulator setup (see SETUP_GUIDE.md)
2. Capture first API session
3. Identify store map endpoints
4. Extract map data
5. Validate downloaded map

## Resources

- [Target Press Release on Store Mode](https://corporate.target.com/press/release/2025/11/target-launches-new-ai-powered-features-to-make-holiday-shopping-easier,-smarter-and-more-fun)
- [mitmproxy Documentation](https://docs.mitmproxy.org/)
- [Android Debug Bridge (adb)](https://developer.android.com/studio/command-line/adb)
- [Frida (SSL Pinning Bypass)](https://frida.re/)






