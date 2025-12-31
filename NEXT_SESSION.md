# Next Session Guide - Target Store Maps Scraper

**Last Session**: December 30, 2025  
**Status**: 90% Complete - Ready for Frida SSL Bypass  
**Time to Finish**: ~30 minutes

---

## 🎉 What We Accomplished Last Session

### ✅ Complete Android Development Environment
- Android Studio installed and configured
- Android 13 (API 33) SDK downloaded
- Android Virtual Device (AVD) created: `target_scraper`
- Emulator running successfully
- adb configured and working

### ✅ Network Interception Setup
- mitmproxy installed and running (port 8080)
- mitmweb UI accessible (port 8081 with token)
- Emulator proxy configured (10.0.2.2:8080)
- HTTP traffic confirmed working

### ✅ Target App
- APK downloaded (v2025.49.1)
- Split APKs installed successfully
- App launches: `com.target.ui/.activity.NavigationActivity`
- App runs but blocks HTTPS (SSL pinning active)

### ✅ Git & GitHub
- Repository initialized
- Committed all framework code
- Live at: https://github.com/jcheung611-byte/target-store-maps-scraper
- All documentation in place

### ✅ Frida Tools
- frida-tools installed (v17.5.2)
- frida-server downloaded for Android ARM64
- Ready to deploy to emulator

---

## 🎯 What We're Doing (The Big Picture)

### The Goal:
**Reverse engineer Target's Store Mode API to download store maps at scale**

### The Method:
1. **Intercept API calls** - Use mitmproxy as middleman
2. **Bypass SSL pinning** - Use Frida to disable Target's certificate checks
3. **Capture traffic** - See all API endpoints Target uses
4. **Discover endpoints** - Find store map API calls
5. **Replicate calls** - Write Python to call their API directly
6. **Scale** - Download all ~2000 Target stores automatically!

### Why This Works:
```
Target App → Makes API call → mitmproxy (captures it) → Target Servers
                                    ↓
                            We see everything:
                            - Endpoints
                            - Authentication
                            - Request/response format
                            
Then we write:
Python Script → Calls Target API directly → Downloads all store maps! 🎉
```

---

## 🚀 Next Session: Complete in 30 Minutes

### Step 1: Start Everything (5 min)

```bash
cd "/Users/jordan.cheung/Documents/GitHub/Store maps scraping"

# Start mitmproxy
pkill -9 mitmweb  # Kill any old instances
mitmweb --listen-port 8080 --web-port 8081 &

# Start emulator (if not running)
emulator -avd target_scraper -writable-system &

# Wait for boot, then set proxy
adb wait-for-device
adb shell settings put global http_proxy 10.0.2.2:8080
```

---

### Step 2: Install Frida Server on Emulator (5 min)

```bash
cd ~/Downloads

# Make sure frida-server is extracted
ls -la frida-server

# If you see frida-server.xz instead:
rm frida-server 2>/dev/null
unxz frida-server.xz
chmod +x frida-server

# Push to emulator
adb root
adb push frida-server /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"

# Start frida-server on emulator
adb shell "/data/local/tmp/frida-server &"
```

---

### Step 3: Verify Frida is Working (2 min)

```bash
# Check if Frida can see the emulator
frida-ps -U

# Should show list of running processes
# Look for "com.target.ui" if Target app is open
```

---

### Step 4: Bypass SSL Pinning (5 min)

**Option A: Using objection (easiest)**

```bash
# Install objection (if not already)
pip3 install objection

# Launch Target with SSL pinning disabled
objection -g com.target.ui explore --startup-command "android sslpinning disable"

# This will:
# - Attach to Target app
# - Disable SSL certificate pinning
# - Target app will work normally
# - ALL HTTPS traffic appears in mitmweb!
```

**Option B: Using Frida script directly**

```bash
# Create bypass script
cat > ssl_bypass.js << 'EOF'
Java.perform(function() {
    console.log("[*] SSL Pinning Bypass Started");
    
    // Bypass common SSL pinning implementations
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    
    // Hook checkServerTrusted
    X509TrustManager.checkServerTrusted.overload('[Ljava.security.cert.X509Certificate;', 'java.lang.String').implementation = function(chain, authType) {
        console.log("[*] Bypassing SSL pinning");
    };
    
    console.log("[*] SSL Pinning Bypass Complete");
});
EOF

# Run it
frida -U -f com.target.ui -l ssl_bypass.js --no-pause
```

---

### Step 5: Test & Capture! (10 min)

**In emulator Target app:**
1. Browse the app
2. Search for products
3. Try to trigger Store Mode:
   - May need to spoof GPS to Target store location
   - Look in menu/settings for "Store Mode" or "In-Store"

**On Mac - Check mitmweb:**
- Open: http://127.0.0.1:8081/?token=<YOUR_TOKEN>
- You should now see Target API calls!
- Look for domains like:
  - `api.target.com`
  - `redsky.target.com`
  - `target.com/api/`

**What to look for:**
- Store location APIs
- Store map/layout endpoints
- Floor plan data
- Aisle information
- Navigation endpoints

---

### Step 6: Analyze & Document (5 min)

```bash
# Run analysis script
cd "/Users/jordan.cheung/Documents/GitHub/Store maps scraping"
python3 scripts/analyze_traffic.py

# Or manually in mitmweb:
# - Filter traffic: ~d target.com
# - Look at request/response
# - Document interesting endpoints in docs/API_FINDINGS.md
```

---

## 🎯 Success Criteria

You'll know it's working when:

1. ✅ Target app works normally (no SSL errors)
2. ✅ Can browse products, search, etc.
3. ✅ mitmweb shows Target's API calls with:
   - Full URLs
   - Request headers
   - Response bodies
   - Status codes (200 OK, not errors)
4. ✅ See domains like `api.target.com`, `redsky.target.com`

---

## 🔧 Troubleshooting

### If Frida won't connect:
```bash
# Kill and restart frida-server
adb shell "pkill frida-server"
adb shell "/data/local/tmp/frida-server &"

# Verify it's running
adb shell "ps | grep frida"
```

### If Target app crashes:
```bash
# Clear app data and restart
adb shell pm clear com.target.ui
adb shell am start -n com.target.ui/.activity.NavigationActivity
```

### If no traffic appears:
```bash
# Verify proxy is still set
adb shell settings get global http_proxy
# Should show: 10.0.2.2:8080

# If not, reset it:
adb shell settings put global http_proxy 10.0.2.2:8080
```

### If SSL pinning bypass fails:
- Try restarting Target app with objection attached from the start
- Make sure frida-server is running on emulator
- Check frida version matches: `frida --version` should be 17.5.2

---

## 📊 After Capturing APIs

### Document What You Find:

Update `docs/API_FINDINGS.md` with:
- Base API URL
- Authentication method (Bearer token? API key?)
- Store map endpoint structure
- Request parameters needed
- Response data format

### Then Build the Downloader:

Update `scripts/download_store_map.py` with:
- Real API endpoints discovered
- Proper authentication headers
- Request/response parsing
- Save map data

### Scale It:

```python
# Get all Target store IDs
stores = get_all_target_stores()  # ~2000 stores

# Download each one
for store in stores:
    print(f"Downloading store {store['id']}...")
    map_data = download_store_map(store['id'])
    save_map(map_data)
    time.sleep(1)  # Be respectful to their servers

print("✅ All Target store maps downloaded!")
```

---

## 🎉 After v1 is Complete

You'll have:
- ✅ Working Android reverse engineering environment
- ✅ Complete understanding of Target's Store Mode API
- ✅ Python scripts to download store maps
- ✅ Ability to scale to ALL Target stores
- ✅ Portfolio-worthy project on GitHub
- ✅ Skills for your fitness watch app!

---

## 💡 Skills You've Learned

This project taught you:
- Android emulator setup
- Mobile app reverse engineering
- Network traffic interception (mitmproxy)
- SSL pinning bypass (Frida)
- API discovery and replication
- Python automation
- Git workflow
- Technical documentation

**These skills transfer to:**
- Building your own mobile apps
- Security research
- Competitive analysis
- Backend API development
- Your fitness watch app project! 💪⌚

---

## 📁 Project Files Reference

**Main Scripts:**
- `scripts/verify_setup.py` - Check environment status
- `scripts/capture_api_traffic.py` - Monitor mitmproxy
- `scripts/analyze_traffic.py` - Parse captured traffic
- `scripts/download_store_map.py` - Download maps (needs API details)

**Documentation:**
- `README.md` - Project overview
- `SETUP_GUIDE.md` - Full setup instructions
- `TEST_RESULTS.md` - What's working
- `docs/API_FINDINGS.md` - Document discovered APIs
- `CURRENT_STATUS.md` - Session progress
- `NEXT_SESSION.md` - This file!

**Config:**
- `config/target_stores.json` - Sample store locations with GPS coordinates

---

## 🚀 You're So Close!

**30 minutes from now, you could have:**
- Target's API endpoints discovered
- Store map data downloading
- Project complete! 🎉

**Let's finish this!** 💪

---

**Last Updated**: December 30, 2025  
**Next Update**: After Frida bypass success!

