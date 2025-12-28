#!/usr/bin/env python3
"""
Analyze captured API traffic to identify store map endpoints.

This script:
1. Parses captured mitmproxy traffic (HAR or JSON format)
2. Identifies API endpoints related to store maps
3. Extracts request/response patterns
4. Generates a report of findings

Usage:
    python analyze_traffic.py <capture_file.har>
    python analyze_traffic.py <capture_file.json>
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich import box
from rich.panel import Panel

console = Console()


class TrafficAnalyzer:
    """Analyze captured traffic for store map endpoints."""
    
    def __init__(self, capture_file):
        self.capture_file = Path(capture_file)
        self.requests = []
        self.interesting_endpoints = []
        
        # Patterns that might indicate store map data
        self.map_patterns = [
            "store",
            "map",
            "layout",
            "navigation",
            "floor",
            "aisle",
            "section",
            "zone",
            "location",
            "coordinates",
            "geometry",
            "geojson",
            "vector",
            "tile"
        ]
    
    def load_capture(self):
        """Load captured traffic from file."""
        if not self.capture_file.exists():
            console.print(f"[red]✗ File not found: {self.capture_file}[/red]")
            return False
        
        try:
            with open(self.capture_file, 'r') as f:
                data = json.load(f)
            
            # Handle HAR format
            if "log" in data and "entries" in data["log"]:
                self.requests = self._parse_har(data)
            # Handle custom JSON format
            elif "requests" in data:
                self.requests = data["requests"]
            else:
                console.print("[red]✗ Unknown capture file format[/red]")
                return False
            
            console.print(f"[green]✓ Loaded {len(self.requests)} requests[/green]")
            return True
            
        except json.JSONDecodeError as e:
            console.print(f"[red]✗ Invalid JSON: {e}[/red]")
            return False
    
    def _parse_har(self, har_data):
        """Parse HAR format to extract requests."""
        requests = []
        for entry in har_data["log"]["entries"]:
            request = entry["request"]
            response = entry.get("response", {})
            
            requests.append({
                "method": request["method"],
                "url": request["url"],
                "headers": request.get("headers", []),
                "status": response.get("status", 0),
                "response_size": response.get("bodySize", 0),
                "response_content": response.get("content", {})
            })
        return requests
    
    def analyze(self):
        """Analyze requests for store map endpoints."""
        console.print("\n[cyan]🔍 Analyzing traffic...[/cyan]\n")
        
        # Group by domain
        by_domain = defaultdict(list)
        for req in self.requests:
            parsed = urlparse(req["url"])
            domain = parsed.netloc
            by_domain[domain].append(req)
        
        # Find Target API domains
        target_domains = [d for d in by_domain.keys() if "target" in d.lower()]
        
        if not target_domains:
            console.print("[yellow]⚠ No Target API domains found in capture[/yellow]")
            console.print("Make sure you captured traffic while using the Target app.\n")
            return
        
        console.print(f"[green]Found {len(target_domains)} Target-related domains:[/green]")
        for domain in target_domains:
            console.print(f"  • {domain} ({len(by_domain[domain])} requests)")
        console.print()
        
        # Analyze each Target domain
        for domain in target_domains:
            self._analyze_domain(domain, by_domain[domain])
        
        # Generate summary
        self._generate_summary()
    
    def _analyze_domain(self, domain, requests):
        """Analyze requests for a specific domain."""
        console.print(f"[cyan]📊 Analyzing: {domain}[/cyan]\n")
        
        for req in requests:
            parsed = urlparse(req["url"])
            path = parsed.path
            
            # Check if path contains interesting patterns
            is_interesting = any(pattern in path.lower() for pattern in self.map_patterns)
            is_interesting = is_interesting or any(pattern in parsed.query.lower() for pattern in self.map_patterns)
            
            if is_interesting:
                self.interesting_endpoints.append({
                    "domain": domain,
                    "method": req["method"],
                    "url": req["url"],
                    "path": path,
                    "query": parsed.query,
                    "status": req.get("status", 0),
                    "response_size": req.get("response_size", 0),
                    "response_content": req.get("response_content", {})
                })
    
    def _generate_summary(self):
        """Generate analysis summary."""
        if not self.interesting_endpoints:
            console.print("[yellow]⚠ No store map-related endpoints found[/yellow]\n")
            console.print("This could mean:")
            console.print("  • Store Mode was not triggered in the app")
            console.print("  • Map data is loaded differently than expected")
            console.print("  • Need to capture more interactions\n")
            return
        
        console.print(f"\n[green]✓ Found {len(self.interesting_endpoints)} interesting endpoints[/green]\n")
        
        # Create table of findings
        table = Table(title="Potential Store Map Endpoints", box=box.ROUNDED)
        table.add_column("Method", style="cyan", no_wrap=True)
        table.add_column("Path", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Size", style="yellow")
        
        for endpoint in self.interesting_endpoints[:20]:  # Show first 20
            table.add_row(
                endpoint["method"],
                endpoint["path"][:60] + "..." if len(endpoint["path"]) > 60 else endpoint["path"],
                str(endpoint["status"]),
                f"{endpoint['response_size']} bytes"
            )
        
        console.print(table)
        console.print()
        
        # Save detailed findings
        self._save_findings()
        
        # Show example endpoint
        if self.interesting_endpoints:
            self._show_example_endpoint()
    
    def _save_findings(self):
        """Save analysis findings to file."""
        output_dir = Path("data/analyzed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"analysis_{self.capture_file.stem}.json"
        
        findings = {
            "analyzed_file": str(self.capture_file),
            "total_requests": len(self.requests),
            "interesting_endpoints": self.interesting_endpoints
        }
        
        with open(output_file, 'w') as f:
            json.dump(findings, f, indent=2)
        
        console.print(f"[green]✓ Detailed findings saved to: {output_file}[/green]\n")
    
    def _show_example_endpoint(self):
        """Show details of an example endpoint."""
        endpoint = self.interesting_endpoints[0]
        
        console.print("[cyan]📋 Example Endpoint Detail:[/cyan]\n")
        
        info = [
            f"URL: {endpoint['url']}",
            f"Method: {endpoint['method']}",
            f"Status: {endpoint['status']}",
            f"Response Size: {endpoint['response_size']} bytes"
        ]
        
        console.print(Panel("\n".join(info), title="Endpoint Info", border_style="cyan"))
        
        # Try to show response preview if available
        response_content = endpoint.get("response_content", {})
        if response_content.get("text"):
            console.print("\n[cyan]Response Preview:[/cyan]\n")
            text = response_content["text"][:500]
            
            # Try to parse as JSON for pretty printing
            try:
                json_data = json.loads(text)
                syntax = Syntax(json.dumps(json_data, indent=2)[:500], "json", theme="monokai")
                console.print(syntax)
            except:
                console.print(text)


def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(description="Analyze Target app API traffic")
    parser.add_argument("capture_file", help="Captured traffic file (HAR or JSON)")
    
    args = parser.parse_args()
    
    console.print("\n[bold cyan]Target API Traffic Analyzer[/bold cyan]\n")
    
    analyzer = TrafficAnalyzer(args.capture_file)
    
    if not analyzer.load_capture():
        return 1
    
    analyzer.analyze()
    
    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("1. Review identified endpoints in data/analyzed/")
    console.print("2. Test endpoints with authentication")
    console.print("3. Build download_store_map.py to extract map data\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())






