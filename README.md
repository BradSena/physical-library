# Avatra

> Digital avatars for your physical media.

Avatra is a self-hosted application designed for collectors who own Blu-rays, DVDs and UHD Blu-rays and want the convenience of a modern media library **without ripping hundreds of discs**.

Instead of storing movies on hard drives, Avatra lets Kodi display your physical collection exactly like a digital library while keeping every movie on its original disc.

---

## Why?

Most collection managers focus on cataloging.

Most media centers focus on digital files.

Avatra connects both worlds.

Browse your movies from Kodi.

Select a title.

The system tells you exactly which disc to insert and where to find it.

Optionally, Home Assistant can prepare your entire home cinema automatically.

---

## Features

### 📀 Physical media first

Supports:

* Blu-ray
* UHD Blu-ray
* DVD
* Steelbooks
* Collector editions

The project is built around **physical items**, not movie files.

---

### 📚 Fast collection management

* Barcode scanning
* Automatic title recognition
* Automatic year extraction
* Automatic media type detection
* Direct scan workflow
* Original storage locations
* Loan tracking
* Display collections

Designed to catalog **hundreds of discs quickly**.

---

### 🎬 Kodi integration

Avatra exports virtual movie entries.

Kodi remains responsible for:

* Posters
* Fanart
* Cast
* Synopsis
* Ratings
* Collections
* Movie browsing

Avatra only manages the physical media.

---

### 🏠 Home Assistant integration

Optional Home Assistant integration allows automations such as:

* Open Blu-ray drive tray
* Switch AVR input
* Power on projector
* Start cinema mode

Home Assistant coordinates the hardware.

Avatra owns the catalog.

---

## Design Philosophy

Avatra intentionally **does not replace Kodi**.

Instead, it complements Kodi by solving one specific problem:

Managing physical movie collections.

If Kodi already does something well, Avatra does not duplicate it.

---

## Vision

Kodi remains the source of truth for:

* Posters
* Artwork
* Collections
* Movie metadata
* Browsing experience

Avatra manages:

* Physical discs
* Storage locations
* Availability
* Loans
* Ownership
* Disc identification

Metadata providers are used only to identify discs and enrich technical information useful to home cinema enthusiasts.

---

## Current Status

🚧 Active development.

### Currently Working

* SQLite database
* FastAPI backend
* Web frontend
* Barcode scanning
* DVDfr recognition provider
* Automatic title extraction
* Automatic year extraction
* Automatic media type detection
* Direct scan-to-library workflow
* Automatic insertion into database

### Current Focus

* Duplicate detection
* Automatic storage locations
* Multi-provider recognition engine

---

## Recognition Flow

Barcode

↓

DVDfr Lookup

↓

Metadata Extraction

↓

Consensus Engine

↓

SQLite Database

↓

Web UI

Future versions will aggregate metadata from multiple providers and merge the most reliable information from each source.

---

## Roadmap

### Phase 1 – Inventory Foundation

#### Core platform

* [x] SQLite database
* [x] FastAPI backend
* [x] Basic web UI
* [x] Barcode scanning
* [x] Direct scan workflow
* [x] Automatic insertion into database

#### First recognition provider

* [x] DVDfr integration
* [x] Automatic title extraction
* [x] Automatic year extraction
* [x] Automatic media type detection

---

### Phase 2 – Recognition Engine

#### Multi-provider architecture

* [ ] Pluggable provider system
* [ ] DVDfr provider
* [ ] Blu-ray.com provider
* [ ] Additional community providers
* [ ] Provider health monitoring

#### Metadata aggregation

* [ ] Consensus engine
* [ ] Field-level confidence
* [ ] Metadata merging
* [ ] Conflict detection
* [ ] Manual conflict resolution

#### Technical metadata

* [ ] Audio formats
* [ ] Video formats
* [ ] HDR metadata
* [ ] Dolby Vision
* [ ] Dolby Atmos
* [ ] DTS:X
* [ ] Languages
* [ ] Subtitles
* [ ] Aspect ratio
* [ ] Runtime
* [ ] Edition identification

---

### Phase 3 – Collection Management

#### Inventory workflow

* [ ] Duplicate detection
* [ ] Duplicate confirmation dialog
* [ ] Manual metadata editing
* [ ] Bulk scanning workflow
* [ ] Shelf Sessions

#### Storage management

* [ ] Automatic storage locations
* [ ] Location editor
* [ ] Loan management
* [ ] Display collections
* [ ] Missing disc tracking

#### Shelf visualization

* [ ] Interactive shelf map
* [ ] Highlight disc location
* [ ] Empty slot visualization
* [ ] Drag & drop shelf reorganization
* [ ] Automatic renumbering after moves
* [ ] Multi-room support
* [ ] Shelf occupancy statistics

---

### Phase 4 – Kodi Integration

#### Library integration

* [ ] STRM export
* [ ] Automatic library synchronization
* [ ] Collection synchronization

#### Playback workflow

* [ ] Physical disc launcher
* [ ] "Disc required" dialog
* [ ] Display storage location
* [ ] Display graphical shelf map
* [ ] Open disc details
* [ ] Launch Home Assistant actions

---

### Phase 5 – Home Assistant Integration

#### Smart Home

* [ ] Official Home Assistant Add-on
* [ ] REST API
* [ ] Webhooks
* [ ] Cinema mode automation
* [ ] Blu-ray drive tray control
* [ ] AVR control
* [ ] Projector control
* [ ] Lighting scenes

---

### Phase 6 – Smart Library

#### LED-guided collection

* [ ] ESPHome integration
* [ ] Addressable LED support (WS2812 / SK6812)
* [ ] Locate selected disc
* [ ] Animated guidance
* [ ] Highlight search results
* [ ] Highlight an entire collection
* [ ] Highlight movies by director
* [ ] Highlight by audio format (Atmos, DTS:X...)
* [ ] Highlight by custom filters

#### Advanced visualization

* [ ] Interactive shelf map inside Kodi
* [ ] Display shelf map when selecting a movie
* [ ] Real-time shelf occupancy
* [ ] Shelf optimization suggestions
* [ ] Collection heat map

---

### Phase 7 – Ecosystem

* [ ] Backup & Restore
* [ ] CSV Import / Export
* [ ] Public REST API
* [ ] Plugin system
* [ ] Multi-user support
* [ ] Permissions
* [ ] Documentation


---

## Technical Stack

### Backend

* Python
* FastAPI
* SQLite
* httpx
* BeautifulSoup

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### Metadata Providers

Current:

* DVDfr

Planned:

* Blu-ray.com
* Additional community sources
* Technical metadata providers

---

## License

## License

License not finalized yet.

The project is intended to remain free for personal use.
Commercial use will require explicit permission.
