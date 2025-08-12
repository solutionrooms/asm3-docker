# Docker Setup for ASM3

This repository includes a complete Docker Compose setup for running ASM3 with PostgreSQL.

> **Note**: This documentation uses the modern `docker compose` command (Docker Compose V2). If you're using an older version of Docker, you may need to use `docker-compose` instead.

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file** with your preferred settings (especially passwords):
   ```bash
   nano .env
   ```

3. **Start the services:**
   ```bash
   docker compose up -d
   ```

4. **Access the application:**
   - Open http://localhost:5000 in your browser
   - Follow the initial setup wizard to create the database schema
   - The default admin login will be created during setup

5. **View logs:**
   ```bash
   docker compose logs -f asm3
   ```

## Services Included

- **postgres**: PostgreSQL 15 database with automatic ASM3 user/database creation
- **asm3**: Main ASM3 application server
- **memcached**: Session and object caching
- **asm3_cron**: Automated daily maintenance tasks

## Management Commands

**Start/Stop Services:**
```bash
docker compose up -d          # Start all services
docker compose down           # Stop all services
docker compose down -v        # Stop and remove volumes (deletes data!)
```

**View Logs:**
```bash
docker compose logs -f asm3   # Application logs
docker compose logs postgres  # Database logs
docker compose logs           # All service logs
```

**Execute Commands:**
```bash
# Run maintenance tasks manually
docker compose exec asm3 sh -c "cd /app/src && python3 cron.py all"

# Access database
docker compose exec postgres psql -U asm3 -d asm

# Shell access to ASM3 container
docker compose exec asm3 bash
```

**Backup/Restore:**
```bash
# Backup database
docker compose exec postgres pg_dump -U asm3 asm > backup.sql

# Restore database
docker compose exec -T postgres psql -U asm3 asm < backup.sql
```

## Configuration

### Environment Variables (.env)

Key settings in your `.env` file:

- `POSTGRES_PASSWORD`: PostgreSQL root password
- `ASM3_DB_PASSWORD`: ASM3 database user password  
- `ASM3_PORT`: Port to expose ASM3 (default: 5000)
- `ASM3_ADMIN_EMAIL`: Admin email for error notifications

### Application Configuration (asm3.conf)

The `asm3.conf` file contains ASM3-specific settings. Key Docker-optimized settings:

- Database connection points to `postgres` service
- Logging to stderr for Docker logs
- Caching enabled with `memcached` service
- File storage in database (not filesystem)

## Persistent Data

The following Docker volumes store persistent data:

- `postgres_data`: PostgreSQL database files
- `asm3_media`: Media files (if using filesystem storage)
- `asm3_cache`: Disk cache for performance

## Development

For development with hot reloading:

1. **Mount source code:**
   ```yaml
   # Add to asm3 service in compose.yml
   volumes:
     - ./src:/usr/lib/sheltermanager3/src
   ```

2. **Enable debug mode in asm3.conf:**
   ```
   log_debug = true
   email_errors = false
   ```

## Troubleshooting

**Database Connection Issues:**
- Ensure PostgreSQL service is healthy: `docker compose ps`
- Check database logs: `docker compose logs postgres`
- Verify credentials in `.env` and `asm3.conf` match

**Permission Issues:**
- The application runs as root in container by default
- For filesystem storage, ensure volumes have correct permissions

**Performance Issues:**
- Enable caching in `asm3.conf`: `cache_common_queries = true`
- Increase memcached memory: modify `command` in compose.yml
- Monitor with: `docker stats`

**Port Conflicts:**
- Change `ASM3_PORT` in `.env` if port 5000 is busy
- Update `base_url` in `asm3.conf` accordingly

## Production Deployment

For production use:

1. **Use strong passwords** in `.env`
2. **Enable TLS** with reverse proxy (nginx/traefik)
3. **Set up regular backups** of PostgreSQL
4. **Monitor logs** and set up log rotation
5. **Update** `base_url` and `service_url` in `asm3.conf`
6. **Enable email** error reporting in `asm3.conf`