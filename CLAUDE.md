# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

**Development & Testing:**
- `make test` - Start development server on port 5000
- `make tests` - Run the full unittest suite
- `make deps` - Install all required dependencies on Debian/Ubuntu systems

**Code Quality:**
- `make compile` - Run code quality checks (Python flake8 + JavaScript jshint)
- `make compilepy` - Run Python linting with flake8
- `make compilejs` - Run JavaScript linting with jshint
- `npm run jshint` - Run JavaScript linting only

**Build & Packaging:**
- `make rollup` - Generate JavaScript bundles for production
- `make compat` - Generate browser-compatible JavaScript versions
- `make clean` - Clean build artifacts and cache files
- `make all` - Full build: clean, compile, tags, rollup, schema

**Database:**
- `python3 cron.py all` - Run daily maintenance tasks (age calculations, publishing, etc.)
- Database setup requires visiting `/database` endpoint after initial startup

**Docker Development:**
- `docker compose up -d` - Start all services (PostgreSQL + ASM3 + Memcached)
- `docker compose down -v` - Stop all services and remove volumes
- `docker compose logs -f asm3` - View ASM3 application logs
- `docker compose exec asm3 sh -c "cd /app/src && python3 cron.py all"` - Run maintenance tasks in container
- Copy `.env.example` to `.env` and customize before first run
- Access ASM3 at http://localhost:8090 (default port)

## Architecture Overview

ASM3 is a Python web application for animal shelter management with the following key architectural components:

**Core Framework:**
- Built on web062 (custom web framework based on web.py)
- WSGI-compatible application in `src/main.py`
- Supports MySQL, PostgreSQL, and SQLite databases

**Module Structure:**
- `src/asm3/` - Core business logic modules
  - `animal.py` - Animal management and records
  - `person.py` - Person/adopter management  
  - `movement.py` - Animal movements (adoptions, fosters, etc.)
  - `medical.py` - Medical records and treatments
  - `financial.py` - Payment and donation tracking
  - `service.py` - External API services
  - `publish.py` - Data publishing to external sites
- `src/asm3/publishers/` - External service integrations (Petfinder, etc.)
- `src/asm3/paymentprocessor/` - Payment gateway integrations
- `src/asm3/dbms/` - Database abstraction layer

**Key Data Models:**
- Animals - Core shelter animal records with intake/outcome tracking
- People - Adopters, fosterers, volunteers, staff with role-based access
- Movements - Track animal location changes (intake, adoption, foster, transfer)
- Medical - Vaccinations, treatments, tests with scheduling
- Financial - Donations, payments, costs with account tracking

**Configuration:**
- Primary config file: `/etc/asm3.conf` (use `scripts/asm3.conf.example` as template)
- Database connection settings required before first run
- Supports multi-site deployments with site-specific databases

**Frontend:**
- Static assets in `src/static/`
- JavaScript bundling via custom rollup scripts
- Template system with multi-language support in `src/asm3/locales/`

**Daily Operations:**
- `cron.py` handles automated tasks (age calculation, publishing, email notifications)
- Database schema updates managed in `src/asm3/dbupdates/`
- Media files stored via `dbfs.py` (database or filesystem)

The application follows a traditional MVC pattern with business logic separated into focused modules for each major functional area of shelter operations.