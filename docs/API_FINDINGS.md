# API Findings - Target Store Maps

This document tracks discovered API endpoints and data formats for Target's Store Mode feature.

## Status: 🔍 Discovery Phase

**Last Updated**: November 12, 2025

---

## Discovered Endpoints

### Store Locator API
```
Endpoint: TBD
Method: TBD
Purpose: Find store by coordinates or store ID
```

**Example Request:**
```json
{
  "pending": "Capture API traffic to populate"
}
```

**Example Response:**
```json
{
  "pending": "Capture API traffic to populate"
}
```

---

### Store Map/Layout API
```
Endpoint: TBD
Method: TBD
Purpose: Retrieve store floor plan and layout
```

**Example Request:**
```json
{
  "pending": "Capture API traffic to populate"
}
```

**Example Response:**
```json
{
  "pending": "Capture API traffic to populate"
}
```

---

### Product Location API
```
Endpoint: TBD
Method: TBD
Purpose: Get aisle/section location for specific products
```

**Example Request:**
```json
{
  "pending": "Capture API traffic to populate"
}
```

**Example Response:**
```json
{
  "pending": "Capture API traffic to populate"
}
```

---

## Authentication

**Type:** TBD (Bearer token, API key, session-based?)

**Headers Required:**
```
TBD - Extract from captured traffic
```

---

## Data Formats

### Map Format
- **Type**: Unknown (GeoJSON, SVG, vector tiles, proprietary?)
- **Structure**: TBD

### Coordinate System
- **Type**: TBD (lat/lng, local coordinates, grid-based?)
- **Origin**: TBD

---

## Rate Limiting

- **Limits**: Unknown
- **Headers**: TBD

---

## Notes & Observations

### Capture Session 1
- **Date**: TBD
- **Findings**: 
  - [ ] Capture initial traffic
  - [ ] Document API patterns
  - [ ] Extract authentication

### Capture Session 2
- **Date**: TBD
- **Findings**: TBD

---

## Next Steps

1. [ ] Complete first traffic capture session
2. [ ] Identify base API domain(s)
3. [ ] Extract authentication mechanism
4. [ ] Document request/response formats
5. [ ] Test API endpoints independently
6. [ ] Build working downloader script

---

## Questions to Answer

- [ ] What is the base API URL?
- [ ] What authentication is required?
- [ ] What format is the map data in?
- [ ] Are there separate endpoints for different floors?
- [ ] How are product locations encoded?
- [ ] Can we access maps without being at the store?
- [ ] What are the rate limits?






