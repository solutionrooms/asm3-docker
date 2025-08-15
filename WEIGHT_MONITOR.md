# ASM3 Weight Monitor

A standalone Python process that monitors the ASM3 audit trail for weight updates from online form processing and automatically:

1. Updates the animal's weight in the `animal` table
2. Creates a history record in the `animal_weight_history` table

## Features

- **Automatic Weight Updates**: Processes weight changes from online forms
- **Historical Tracking**: Maintains a complete history of weight changes
- **Incremental Processing**: Only processes new audit entries since last run
- **Error Handling**: Robust error handling with detailed logging
- **Flexible Deployment**: Can run once or continuously

## Requirements

- Python 3.6+
- psycopg2-binary (for PostgreSQL connectivity)
- Access to ASM3 configuration file (`asm3.conf`)

## Installation

1. Install Python dependencies:
   ```bash
   pip install psycopg2-binary
   ```

2. Ensure `asm3.conf` is accessible (same config used by main ASM3 application)

## Database Schema

The script automatically creates the `animal_weight_history` table:

```sql
CREATE TABLE animal_weight_history (
    id SERIAL PRIMARY KEY,
    animalid INTEGER NOT NULL,
    weight_date TIMESTAMP NOT NULL,
    username VARCHAR(255) NOT NULL,
    weight REAL NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage

### Test the Setup
```bash
python3 test_weight_monitor.py
```

### Run Once (for cron)
```bash
python3 weight_monitor.py --once
```

### Run Continuously (every 60 seconds)
```bash
python3 weight_monitor.py
```

## Deployment Options

### Option 1: Cron Job (Recommended)

Add to your crontab to run every minute:

```bash
# Edit crontab
crontab -e

# Add this line to run every minute
* * * * * cd /path/to/asm3-docker && python3 weight_monitor.py --once >> /var/log/weight_monitor_cron.log 2>&1
```

### Option 2: Docker Service

Add to your `docker-compose.yml`:

```yaml
  weight_monitor:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    environment:
      - ASM3_CONF=/etc/asm3.conf
    volumes:
      - ./asm3.conf:/app/asm3.conf:ro
      - ./src:/app/src:ro
    depends_on:
      - postgres
    networks:
      - asm3_network
    command: python3 /app/weight_monitor.py
```

### Option 3: Systemd Service

Create `/etc/systemd/system/asm3-weight-monitor.service`:

```ini
[Unit]
Description=ASM3 Weight Monitor
After=postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=asm3
Group=asm3
WorkingDirectory=/path/to/asm3-docker
ExecStart=/usr/bin/python3 weight_monitor.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable asm3-weight-monitor
sudo systemctl start asm3-weight-monitor
```

## Configuration

The weight monitor uses the same configuration as ASM3:

- Looks for config in standard ASM3 locations:
  1. `ASM3_CONF` environment variable
  2. `./asm3.conf` (next to script)
  3. `~/.asm3.conf`
  4. `/etc/asm3.conf`

Required config keys:
- `db_host` - Database hostname
- `db_port` - Database port (default: 5432)
- `db_name` - Database name
- `db_username` - Database username
- `db_password` - Database password

## Logging

Logs are written to:
- Console (stdout)
- `weight_monitor.log` file

Log levels:
- **INFO**: Normal operation, weight updates processed
- **ERROR**: Database errors, processing failures
- **DEBUG**: Detailed debugging information

## How It Works

1. **Query Audit Trail**: Searches for entries in `audittrail` table where:
   - `tablename = 'onlineformincoming'`
   - `description` contains 'Weight' and '=Processed='
   - `auditdate` > last processed date

2. **Extract Weight Data**: Parses the audit description to extract:
   - Animal name (3rd word after spaces)
   - Weight value (5th word after spaces)

3. **Match Animals**: Joins with `animal` table on `animalname`

4. **Update Records**: 
   - Updates `animal.weight` field
   - Inserts record into `animal_weight_history`

5. **Track Progress**: Uses the latest `weight_date` to avoid reprocessing

## Troubleshooting

### Common Issues

1. **"No config file found"**
   - Ensure `asm3.conf` exists and is readable
   - Set `ASM3_CONF` environment variable if needed

2. **Database connection fails**
   - Verify database credentials in config
   - Check database is running and accessible
   - Ensure PostgreSQL is accepting connections

3. **"No new weight updates"**
   - Check that online forms are creating audit entries
   - Verify audit entries match the expected format
   - Run with `--once` flag to see processing results

4. **Permission errors**
   - Ensure script has read access to config file
   - Ensure database user has INSERT/UPDATE permissions

### Testing Database Connectivity

```bash
# Test basic connectivity
python3 -c "
from weight_monitor import WeightMonitor
m = WeightMonitor()
m.connect_database()
print('Connection successful!')
"
```

### Checking Audit Trail Format

```sql
-- View recent audit entries for weight updates
SELECT auditdate, username, description 
FROM audittrail 
WHERE tablename = 'onlineformincoming' 
  AND description LIKE '%Weight%'
  AND description LIKE '%=Processed=%'
ORDER BY auditdate DESC 
LIMIT 10;
```

## License

This weight monitor is designed for use with ASM3 (Animal Shelter Manager) and follows the same usage terms.