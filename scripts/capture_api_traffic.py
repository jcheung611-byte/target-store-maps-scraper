#!/usr/bin/env python3
"""
Capture API traffic from Target app through mitmproxy.

This script helps you:
1. Monitor traffic in real-time
2. Save captured requests to a file
3. Filter for relevant API calls
4. Export for later analysis

Usage:
    python capture_api_traffic.py [--output captured_session.json]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import box
import time
import subprocess

console = Console()


class TrafficMonitor:
    """Monitor and display captured API traffic."""
    
    def __init__(self, output_file=None):
        self.output_file = output_file
        self.captured_requests = []
        self.interesting_patterns = [
            "store",
            "map",
            "navigation",
            "layout",
            "location",
            "aisle",
            "product",
            "inventory"
        ]
    
    def is_interesting(self, url):
        """Check if URL contains interesting patterns."""
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in self.interesting_patterns)
    
    def save_capture(self):
        """Save captured requests to file."""
        if not self.output_file:
            return
        
        output_path = Path("data/captured") / self.output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        capture_data = {
            "capture_time": datetime.now().isoformat(),
            "total_requests": len(self.captured_requests),
            "requests": self.captured_requests
        }
        
        with open(output_path, 'w') as f:
            json.dump(capture_data, f, indent=2)
        
        console.print(f"\n[green]✓ Saved {len(self.captured_requests)} requests to {output_path}[/green]")


def generate_table(captured_count, interesting_count):
    """Generate status table for live display."""
    table = Table(title="Capturing Target App Traffic", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Requests", str(captured_count))
    table.add_row("Interesting Requests", str(interesting_count))
    table.add_row("Status", "🎯 Monitoring...")
    table.add_row("", "Press Ctrl+C to stop")
    
    return table


def check_mitmproxy_running():
    """Check if mitmproxy is running."""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(("localhost", 8080))
        sock.close()
        return result == 0
    except:
        return False


def parse_mitm_flow_file(flow_file):
    """Parse mitmproxy flow file (if using mitmdump)."""
    # This would parse the binary flow file
    # For now, we'll use manual instructions
    pass


def main():
    """Main capture function."""
    parser = argparse.ArgumentParser(description="Capture Target app API traffic")
    parser.add_argument(
        "--output",
        default=f"target_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        help="Output filename for captured traffic"
    )
    parser.add_argument(
        "--auto-save",
        action="store_true",
        help="Automatically save interesting requests"
    )
    
    args = parser.parse_args()
    
    console.print("\n[bold cyan]Target API Traffic Capture Tool[/bold cyan]\n")
    
    # Check if mitmproxy is running
    if not check_mitmproxy_running():
        console.print("[red]✗ mitmproxy is not running on port 8080[/red]")
        console.print("\nStart mitmproxy first:")
        console.print("[yellow]  mitmweb --listen-port 8080 --web-port 8081[/yellow]\n")
        return 1
    
    console.print("[green]✓ mitmproxy detected on port 8080[/green]\n")
    
    # Instructions for manual capture
    console.print("[cyan]📋 Manual Capture Instructions:[/cyan]\n")
    console.print("1. Open mitmweb UI: [link=http://localhost:8081]http://localhost:8081[/link]")
    console.print("2. In the Target app on emulator:")
    console.print("   - Navigate to a Target store location (GPS spoofed)")
    console.print("   - Trigger Store Mode feature")
    console.print("   - Browse products and aisles")
    console.print("   - Use navigation features")
    console.print("\n3. In mitmweb UI, look for API calls containing:")
    
    monitor = TrafficMonitor(args.output)
    for pattern in monitor.interesting_patterns:
        console.print(f"   • [yellow]{pattern}[/yellow]")
    
    console.print("\n4. In mitmweb, you can:")
    console.print("   • Click on requests to see details")
    console.print("   • Use 'f' to filter (e.g., '~u store' for URLs with 'store')")
    console.print("   • Right-click → Export → Save to file")
    console.print("\n5. Export captured traffic:")
    console.print("   • File → Save (in mitmweb)")
    console.print("   • Or use: File → Export → HAR format")
    
    console.print("\n[cyan]💡 What to look for:[/cyan]\n")
    console.print("API endpoints that might contain store map data:")
    console.print("  • [green]GET[/green] /api/stores/{id}/layout")
    console.print("  • [green]GET[/green] /api/stores/{id}/map")
    console.print("  • [green]GET[/green] /api/navigation/...")
    console.print("  • [green]POST[/green] /api/stores/nearby")
    console.print("  • Any endpoints with 'floor', 'aisle', 'section', 'zone'")
    
    console.print("\n[cyan]📁 Recommended export location:[/cyan]")
    output_path = Path("data/captured") / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    console.print(f"  {output_path.absolute()}")
    
    console.print("\n[yellow]Once you've captured traffic, analyze it with:[/yellow]")
    console.print(f"  python scripts/analyze_traffic.py data/captured/{args.output}")
    
    console.print("\n[dim]Press Ctrl+C when done capturing[/dim]\n")
    
    try:
        # Keep script running for convenience
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n\n[cyan]Capture session ended.[/cyan]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("1. Export captured traffic from mitmweb to data/captured/")
        console.print("2. Run analyze_traffic.py to find store map endpoints")
        console.print("3. Build download_store_map.py to extract the data\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())






