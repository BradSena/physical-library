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

* [x] SQLite database
* [x] FastAPI backend
* [x] Basic web UI
* [x] Barcode recognition
* [x] DVDfr provider
* [x] Automatic title extraction
* [x] Automatic year extraction
* [x] Automatic media type detection
* [x] Direct scan workflow
* [x] Automatic insertion into database

### Phase 2 – Collection Management

* [ ] Duplicate detection
* [ ] Automatic storage locations
* [ ] Shelf sessions
* [ ] Manual metadata editing
* [ ] Bulk scanning workflow
* [ ] Loan management

### Phase 3 – Metadata Enrichment

* [ ] Multi-provider recognition engine
* [ ] Metadata aggregation
* [ ] Audio formats
* [ ] Video formats
* [ ] HDR metadata
* [ ] Dolby Vision detection
* [ ] Dolby Atmos detection
* [ ] DTS:X detection
* [ ] Language information
* [ ] Aspect ratio

### Phase 4 – Kodi Integration

* [ ] STRM export
* [ ] Kodi plugin
* [ ] Physical disc launcher
* [ ] Library synchronization

### Phase 5 – Home Cinema Automation

* [ ] Home Assistant add-on
* [ ] Blu-ray drive control
* [ ] Cinema mode automation
* [ ] AVR integration
* [ ] Projector integration

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
