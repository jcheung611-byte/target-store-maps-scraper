#!/usr/bin/env python3
"""
Verify that all components are set up correctly for Target store map scraping.

This script checks:
- Android emulator is running
- adb is accessible
- mitmproxy is installed and running
- Target app is installed
- Proxy configuration
"""

import subprocess
import sys
import socket
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def check_command_exists(command):
    """Check if a command exists in PATH."""
    try:
        subprocess.run(
            [command, "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_adb_devices():
    """Check if emulator is running via adb."""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            check=True
        )
        devices = [line for line in result.stdout.split('\n') 
                   if 'emulator' in line or 'device' in line.split('\t')[-1]]
        return len(devices) > 1  # First line is header
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_emulator_name():
    """Get the name/ID of running emulator."""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'emulator' in line and '\tdevice' in line:
                return line.split('\t')[0]
        return None
    except:
        return None


def check_target_app_installed():
    """Check if Target app is installed on emulator."""
    try:
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages", "com.target"],
            capture_output=True,
            text=True,
            check=True
        )
        return "com.target.ui" in result.stdout
    except:
        return False


def check_port_open(host, port):
    """Check if a port is open (mitmproxy)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def check_emulator_proxy():
    """Check if emulator has proxy configured (best effort)."""
    try:
        # This is approximate - checking if global proxy is set
        result = subprocess.run(
            ["adb", "shell", "settings", "get", "global", "http_proxy"],
            capture_output=True,
            text=True,
            check=True
        )
        proxy = result.stdout.strip()
        return "10.0.2.2:8080" in proxy or proxy != "null"
    except:
        return None  # Unknown


def check_python_packages():
    """Check if required Python packages are installed."""
    required = ["mitmproxy", "requests", "pandas", "rich"]
    installed = []
    missing = []
    
    for package in required:
        try:
            __import__(package)
            installed.append(package)
        except ImportError:
            missing.append(package)
    
    return installed, missing


def main():
    """Run all verification checks."""
    console.print("\n[bold cyan]Target Store Maps Scraper - Setup Verification[/bold cyan]\n")
    
    # Create results table
    table = Table(title="Setup Status", box=box.ROUNDED)
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Details", style="white")
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: adb
    total_checks += 1
    if check_command_exists("adb"):
        table.add_row("adb", "✓ Installed", "Android Debug Bridge ready")
        checks_passed += 1
    else:
        table.add_row("adb", "✗ Not Found", "Install Android SDK platform-tools")
    
    # Check 2: Emulator running
    total_checks += 1
    emulator_name = get_emulator_name()
    if emulator_name:
        table.add_row("Emulator", "✓ Running", f"Device: {emulator_name}")
        checks_passed += 1
    else:
        table.add_row("Emulator", "✗ Not Running", "Start emulator with AVD Manager")
    
    # Check 3: Target app
    total_checks += 1
    if check_target_app_installed():
        table.add_row("Target App", "✓ Installed", "com.target.ui found")
        checks_passed += 1
    else:
        table.add_row("Target App", "✗ Not Installed", "Install Target APK on emulator")
    
    # Check 4: mitmproxy command
    total_checks += 1
    if check_command_exists("mitmproxy"):
        table.add_row("mitmproxy", "✓ Installed", "Proxy tool ready")
        checks_passed += 1
    else:
        table.add_row("mitmproxy", "✗ Not Found", "Install: brew install mitmproxy")
    
    # Check 5: mitmproxy running
    total_checks += 1
    if check_port_open("localhost", 8080):
        table.add_row("mitmproxy (port 8080)", "✓ Running", "Proxy listener active")
        checks_passed += 1
    else:
        table.add_row("mitmproxy (port 8080)", "✗ Not Running", "Start: mitmweb --listen-port 8080")
    
    # Check 6: mitmweb UI
    total_checks += 1
    if check_port_open("localhost", 8081):
        table.add_row("mitmweb UI (port 8081)", "✓ Running", "http://localhost:8081")
        checks_passed += 1
    else:
        table.add_row("mitmweb UI (port 8081)", "✗ Not Running", "Access UI after starting mitmweb")
    
    # Check 7: Emulator proxy
    total_checks += 1
    proxy_status = check_emulator_proxy()
    if proxy_status is True:
        table.add_row("Emulator Proxy", "✓ Configured", "Proxy settings detected")
        checks_passed += 1
    elif proxy_status is False:
        table.add_row("Emulator Proxy", "✗ Not Set", "Set proxy to 10.0.2.2:8080")
    else:
        table.add_row("Emulator Proxy", "? Unknown", "Verify manually in emulator WiFi settings")
    
    # Check 8: Python packages
    total_checks += 1
    installed, missing = check_python_packages()
    if not missing:
        table.add_row("Python Packages", "✓ Installed", f"{len(installed)} packages ready")
        checks_passed += 1
    else:
        table.add_row("Python Packages", "⚠ Incomplete", f"Missing: {', '.join(missing)}")
    
    console.print(table)
    console.print()
    
    # Summary
    if checks_passed == total_checks:
        console.print("[bold green]✓ All checks passed! Ready to capture API traffic.[/bold green]\n")
        console.print("[cyan]Next steps:[/cyan]")
        console.print("1. Open Target app in emulator")
        console.print("2. Spoof GPS to Target store location")
        console.print("3. Trigger Store Mode in app")
        console.print("4. Run: python scripts/capture_api_traffic.py\n")
        return 0
    else:
        console.print(f"[bold yellow]⚠ {checks_passed}/{total_checks} checks passed[/bold yellow]\n")
        console.print("[cyan]Action required:[/cyan]")
        console.print("Review the ✗ items above and complete setup.")
        console.print("See SETUP_GUIDE.md for detailed instructions.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())






