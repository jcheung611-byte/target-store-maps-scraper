# Data Directory

This directory stores captured traffic, analysis results, and downloaded store maps.

## Directory Structure

```
data/
├── captured/    # Raw captured API traffic from mitmproxy
├── analyzed/    # Parsed analysis results from captured traffic
└── maps/        # Downloaded store map data
```

## File Naming Conventions

### captured/
- `target_session_YYYYMMDD_HHMMSS.har` - HAR format export from mitmweb
- `target_session_YYYYMMDD_HHMMSS.json` - Custom JSON format captures

### analyzed/
- `analysis_SESSIONNAME.json` - Analysis results for a capture session

### maps/
- `store_STOREID_YYYYMMDD_HHMMSS.json` - Downloaded map with timestamp
- `store_STOREID_latest.json` - Symlink to most recent map for this store

## Usage

1. **Capture traffic**: Export from mitmweb to `captured/`
2. **Analyze**: Run `analyze_traffic.py` → outputs to `analyzed/`
3. **Download**: Run `download_store_map.py` → saves to `maps/`

## Note

Files in these directories are .gitignored to avoid committing large/sensitive data.






