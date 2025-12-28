# Target Store Maps Scraper - Setup Guide

Complete step-by-step guide to set up your environment for capturing Target store maps.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Android Studio & Emulator Setup](#android-studio--emulator-setup)
3. [mitmproxy Setup](#mitmproxy-setup)
4. [Target App Installation](#target-app-installation)
5. [GPS Spoofing Configuration](#gps-spoofing-configuration)
6. [SSL Pinning Bypass (if needed)](#ssl-pinning-bypass)
7. [Verification](#verification)

---

## Prerequisites

### System Requirements

- **OS**: macOS (you're on darwin 25.0.0) ✓
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Internet**: Stable connection

### Software to Install

- [ ] Android Studio
- [ ] Python 3.8+
- [ ] Homebrew (for macOS dependencies)

---

## Android Studio & Emulator Setup

### Step 1: Install Android Studio

```bash
# Download from: https://developer.android.com/studio
# Or install via Homebrew:
brew install --cask android-studio
```

### Step 2: Install Android SDK Command Line Tools

1. Open Android Studio
2. Go to **Preferences → Appearance & Behavior → System Settings → Android SDK**
3. Select **SDK Tools** tab
4. Check:
   - Android SDK Build-Tools
   - Android Emulator
   - Android SDK Platform-Tools
5. Click **Apply** to install

### Step 3: Add Android Tools to PATH

```bash
# Add to your ~/.zshrc
echo 'export ANDROID_HOME=$HOME/Library/Android/sdk' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/emulator' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.zshrc
source ~/.zshrc

# Verify installation
adb --version
emulator -version
```

### Step 4: Create Android Virtual Device (AVD)

```bash
# Open AVD Manager
android-studio → Tools → Device Manager

# Or from command line:
# avdmanager create avd -n target_scraper -k "system-images;android-33;google_apis;x86_64" -d pixel_5
```

**Recommended Settings:**
- **Device**: Pixel 5
- **System Image**: Android 13 (API 33) - Google APIs (NOT Google Play)
  - ⚠️ Important: Choose "Google APIs" for root access
- **Storage**: 2048 MB internal storage
- **RAM**: 2048 MB
- **Graphics**: Hardware - GLES 2.0

### Step 5: Launch Emulator

```bash
# List available AVDs
emulator -list-avds

# Start emulator with writable system (for SSL cert installation)
emulator -avd target_scraper -writable-system &

# Wait for emulator to boot (check with):
adb devices
```

Expected output:
```
List of devices attached
emulator-5554	device
```

---

## mitmproxy Setup

### Step 1: Install mitmproxy

```bash
# Install via Homebrew
brew install mitmproxy

# Verify installation
mitmproxy --version
```

### Step 2: Start mitmproxy Web Interface

```bash
# Start mitmweb (web UI for easier viewing)
mitmweb --listen-port 8080 --web-port 8081

# This starts:
# - Proxy on port 8080 (for emulator)
# - Web interface on http://localhost:8081 (for you)
```

Keep this terminal window open!

### Step 3: Configure Emulator Proxy

In the Android emulator:

1. Open **Settings**
2. Go to **Network & Internet → Internet → AndroidWiFi**
3. Long press **AndroidWiFi** → **Modify network**
4. Expand **Advanced options**
5. Set **Proxy** to **Manual**
6. Configure:
   - **Proxy hostname**: `10.0.2.2` (special IP for host machine)
   - **Proxy port**: `8080`
   - **Bypass proxy for**: (leave empty)
7. **Save**

### Step 4: Install mitmproxy CA Certificate

In the emulator's Chrome browser:

1. Navigate to: `http://mitm.it`
2. Click **Android** icon
3. Download certificate (will prompt to save)
4. Go to **Settings → Security → Encryption & credentials**
5. Tap **Install a certificate → CA certificate**
6. Tap **Install Anyway** (warning)
7. Select the downloaded certificate file
8. Name it "mitmproxy"

### Step 5: Verify Proxy is Working

In emulator's Chrome:

1. Visit: `http://example.com`
2. Check mitmweb interface at `http://localhost:8081`
3. You should see the HTTP request appear

✅ If you see traffic, proxy is working!

---

## Target App Installation

### Option 1: Download APK

```bash
# Download Target APK from APKPure or APKMirror
# Example URL: https://www.apkpure.com/target/com.target.ui

# Install via adb
adb install target-app.apk
```

### Option 2: Use Google Play Store (if available)

1. Set up Google Account in emulator
2. Open Play Store
3. Search for "Target"
4. Install app (com.target.ui)

### Verify Installation

```bash
# List installed packages
adb shell pm list packages | grep target

# Expected output:
# package:com.target.ui
```

---

## GPS Spoofing Configuration

### Step 1: Enable Location in Emulator

1. In emulator: **Settings → Location**
2. Toggle **Use location** to ON
3. Grant location permission to Target app when prompted

### Step 2: Set GPS Location via Extended Controls

1. In emulator window, click **⋮** (three dots) at bottom
2. Select **Location**
3. Enter coordinates for a Target store:

**Example Target Store Locations:**

```
Target Minneapolis Downtown
Latitude: 44.9778
Longitude: -93.2650

Target Brooklyn Park, MN
Latitude: 45.1089
Longitude: -93.3566

Target Brooklyn Center, MN
Latitude: 45.0690
Longitude: -93.3267
```

4. Click **Send**

### Step 3: Verify Location

Open Google Maps in emulator to confirm your spoofed location shows correctly.

---

## SSL Pinning Bypass

⚠️ **Only if Target app blocks proxy traffic**

If you configure everything correctly but see no Target app traffic in mitmproxy, Target is likely using SSL certificate pinning.

### Install Frida

```bash
# Install Frida tools
pip install frida-tools objection

# Download Frida server for Android
# Visit: https://github.com/frida/frida/releases
# Download: frida-server-XX.XX.XX-android-x86_64.xz (match your Frida version)

# Extract and push to emulator
unxz frida-server-XX.XX.XX-android-x86_64.xz
adb root
adb push frida-server-XX.XX.XX-android-x86_64 /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"
```

### Bypass SSL Pinning

```bash
# Use objection to disable SSL pinning
objection -g com.target.ui explore --startup-command "android sslpinning disable"

# Then launch Target app
# Traffic should now appear in mitmproxy
```

---

## Verification

### Run Verification Script

```bash
cd "/Users/jordan.cheung/Documents/GitHub/Store maps scraping"
python scripts/verify_setup.py
```

This will check:
- ✓ Android emulator is running
- ✓ adb is accessible
- ✓ mitmproxy is running
- ✓ Target app is installed
- ✓ Proxy configuration is correct

### Manual Verification Checklist

- [ ] Emulator launches successfully
- [ ] `adb devices` shows emulator
- [ ] mitmproxy web interface accessible at http://localhost:8081
- [ ] Emulator proxy set to 10.0.2.2:8080
- [ ] mitmproxy certificate installed
- [ ] Target app installed and launches
- [ ] GPS location spoofed to Target store
- [ ] HTTP/HTTPS traffic visible in mitmproxy

---

## Troubleshooting

### Emulator won't start
```bash
# Check for conflicts
ps aux | grep emulator
# Kill any existing instances
pkill -9 emulator

# Start with more verbose output
emulator -avd target_scraper -verbose
```

### Can't see HTTPS traffic
- Ensure mitmproxy certificate is installed as **CA certificate**
- Verify proxy settings: `10.0.2.2:8080`
- Try SSL pinning bypass with Frida

### Target app crashes on location
- Ensure "Google APIs" system image (not Google Play)
- Grant all permissions to Target app
- Try different GPS coordinates

### adb not found
```bash
# Verify PATH
echo $ANDROID_HOME
ls $ANDROID_HOME/platform-tools

# Re-source your shell config
source ~/.zshrc
```

---

## Next Steps

Once setup is complete:

1. Launch emulator with GPS spoofed to Target store
2. Start mitmproxy to capture traffic
3. Open Target app and trigger Store Mode
4. Run `capture_api_traffic.py` to save session
5. Analyze captured traffic for map endpoints

See main README.md for workflow details.






