# Android Studio Setup - Next Steps

## ✅ What's Already Done

- ✓ Android Studio installed via Homebrew
- ✓ PATH configured in `~/.zshrc`
- ✓ ANDROID_HOME set to `$HOME/Library/Android/sdk`

## 🎯 What You Need to Do Now

### Step 1: Launch Android Studio (First Time Setup)

```bash
open -a "Android Studio"
```

**What will happen:**
1. Android Studio will show a welcome wizard
2. Choose **"Standard"** installation
3. It will download and install:
   - Android SDK
   - Android SDK Platform-Tools
   - Android Emulator
   - (~2-3GB download)
4. Click through until you see the welcome screen

**Time estimate:** 10-15 minutes (depends on download speed)

---

### Step 2: Install Android 13 (API 33) SDK

Once Android Studio is open:

1. Click **"More Actions"** → **"SDK Manager"**
   - Or: **Android Studio** → **Preferences** → **Appearance & Behavior** → **System Settings** → **Android SDK**

2. In **"SDK Platforms"** tab:
   - ✓ Check **"Android 13.0 (Tiramisu)"** - API Level 33
   - ⚠️ **IMPORTANT**: Expand the row and select **"Google APIs"** (NOT "Google Play")
     - Google APIs gives us root access needed for mitmproxy certificate

3. In **"SDK Tools"** tab, ensure these are checked:
   - ✓ Android SDK Build-Tools
   - ✓ Android SDK Platform-Tools
   - ✓ Android Emulator
   - ✓ Android SDK Command-line Tools

4. Click **"Apply"** → **"OK"**
   - This will download ~2-3GB
   - Wait for completion

---

### Step 3: Create Android Virtual Device (AVD)

1. In Android Studio, click **"More Actions"** → **"Device Manager"**
   - Or: **Tools** → **Device Manager**

2. Click **"Create Device"** button

3. **Select Hardware:**
   - Category: **Phone**
   - Device: **Pixel 5** (recommended)
   - Click **"Next"**

4. **System Image:**
   - Release Name: **Tiramisu** (API 33)
   - Target: **"Google APIs"** (x86_64 or ARM depending on your Mac)
   - ⚠️ **DO NOT select "Google Play"** - we need root access
   - If not downloaded, click **"Download"** next to it
   - Click **"Next"**

5. **AVD Configuration:**
   - AVD Name: `target_scraper` (or any name you like)
   - Startup orientation: Portrait
   - Click **"Show Advanced Settings"**:
     - RAM: 2048 MB (2GB)
     - Internal Storage: 2048 MB (2GB)
     - SD card: (leave default or set to 512 MB)
   - Click **"Finish"**

---

### Step 4: Test Your Setup

After AVD is created:

```bash
# In terminal, verify adb is now available
adb --version

# Should see something like:
# Android Debug Bridge version 1.0.41

# Check emulator command
emulator -version

# Should see:
# Android emulator version X.X.X
```

**Start the emulator:**

```bash
# List available AVDs
emulator -list-avds

# Should show: target_scraper (or your AVD name)

# Launch it
emulator -avd target_scraper -writable-system &
```

**Wait 1-2 minutes for emulator to boot**, then:

```bash
# Verify emulator is running
adb devices

# Should show:
# List of devices attached
# emulator-5554	device
```

---

### Step 5: Run Verification Script

```bash
cd "/Users/jordan.cheung/Documents/GitHub/Store maps scraping"
python3 scripts/verify_setup.py
```

**Expected results:**
- ✓ adb installed
- ✓ Emulator running
- ✗ Target app (not yet installed - that's next!)
- ✓ mitmproxy installed
- ✗ mitmproxy not running (that's fine for now)
- And more...

---

## 🎉 Once Complete

You'll be ready to:
1. Download Target APK
2. Configure proxy in emulator
3. Capture API traffic
4. Discover store map endpoints!

---

## 🚨 Troubleshooting

### "adb: command not found" after Android Studio setup

```bash
# Reload your shell
source ~/.zshrc

# Or open a new terminal window
```

### Emulator won't start

```bash
# Check for conflicts
ps aux | grep emulator

# Kill any hanging processes
pkill -9 emulator

# Try launching with verbose output
emulator -avd target_scraper -verbose
```

### Can't find "Google APIs" system image

- Make sure you're looking at **API 33 (Tiramisu)**
- Expand the API 33 row to see variants
- "Google APIs" should be listed there
- If not visible, update SDK Manager

---

## 📝 Next Steps After Android Setup

1. **Download Target APK**
   - Visit: https://www.apkpure.com/target/com.target.ui
   - Download latest version
   - Install: `adb install target-app.apk`

2. **Configure Emulator Proxy**
   - See SETUP_GUIDE.md section: "mitmproxy Setup"

3. **Start Traffic Capture**
   - Run capture script
   - Trigger Store Mode in app
   - Analyze captured data

---

## ⏱️ Time Estimates

- **Android Studio first launch**: 10-15 min
- **SDK download**: 10-15 min (depends on internet)
- **AVD creation**: 5 min
- **First emulator boot**: 2-3 min

**Total**: ~30-40 minutes

Good luck! 🚀

