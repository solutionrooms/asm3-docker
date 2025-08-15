#!/usr/bin/env python3
"""
ASM3 Weight Monitor
==================

A standalone process that monitors the audittrail table for weight updates
from online form processing and:
1. Updates the animal's weight in the animal table
2. Logs the weight change to an animal_weight_history table

This process runs every minute and only processes new audit entries since
the last run.

Usage:
    python3 weight_monitor.py

Configuration:
    Reads database configuration from asm3.conf (same as main ASM3 application)
    Or set environment variables: ASM3_CONF to point to config file
"""

import os
import sys
import time
import codecs
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Tuple, Optional

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Error: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)


class WeightMonitorConfig:
    """Configuration management for the weight monitor."""
    
    def __init__(self):
        self.cfg = None
        self.read_config_file()
    
    def read_config_file(self) -> None:
        """Load config file into cfg map, same logic as ASM3 sitedefs.py"""
        fname = ""
        insconf = os.path.dirname(os.path.abspath(__file__)) + os.sep + "asm3.conf"
        homeconf = os.path.expanduser("~") + os.sep + ".asm3.conf"
        
        if "ASM3_CONF" in os.environ and os.environ["ASM3_CONF"] != "":
            fname = os.environ["ASM3_CONF"]
        elif os.path.exists(insconf):
            fname = insconf
        elif os.path.exists(homeconf):
            fname = homeconf
        elif os.path.exists("/etc/asm3.conf"):
            fname = "/etc/asm3.conf"
        
        if fname == "":
            self.cfg = {}
            print("Warning: No config file found, using defaults")
        else:
            self.cfg = {}
            try:
                with codecs.open(fname, 'r', encoding='utf8') as f:
                    lines = f.readlines()
                for line in lines:
                    if line.find("#") != -1 and line.find("{") == -1:
                        line = line[0:line.find("#")]
                    if line.find("=") != -1:
                        k, v = line.split("=", 1)
                        self.cfg[k.strip()] = v.strip()
                print(f"Loaded config from: {fname}")
            except Exception as e:
                print(f"Error reading config file {fname}: {e}")
                self.cfg = {}
    
    def get_string(self, k: str, dv: str = "") -> str:
        if k not in self.cfg:
            return dv
        return self.cfg[k]
    
    def get_integer(self, k: str, dv: int = 0) -> int:
        v = self.get_string(k)
        if v == "":
            return dv
        return int(v)


class WeightMonitor:
    """Main weight monitoring class."""
    
    def __init__(self):
        self.config = WeightMonitorConfig()
        self.setup_logging()
        self.db_conn = None
        self.last_audit_date = None
        
    def setup_logging(self):
        """Setup logging configuration."""
        # In Docker, prefer stdout logging
        log_handlers = [logging.StreamHandler(sys.stdout)]
        
        # Try to add file logging to a writable location
        writable_paths = ['/tmp/weight_monitor.log', '/var/log/weight_monitor.log', './weight_monitor.log']
        
        for log_path in writable_paths:
            try:
                log_handlers.append(logging.FileHandler(log_path))
                break  # Success, use this path
            except (PermissionError, FileNotFoundError, OSError):
                continue  # Try next path
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - WeightMonitor - %(levelname)s - %(message)s',
            handlers=log_handlers
        )
        self.logger = logging.getLogger(__name__)
    
    def connect_database(self):
        """Connect to the PostgreSQL database using ASM3 configuration."""
        try:
            db_host = self.config.get_string("db_host", "localhost")
            db_port = self.config.get_integer("db_port", 5432)
            db_name = self.config.get_string("db_name", "asm")
            db_user = self.config.get_string("db_username", "asm3")
            db_pass = self.config.get_string("db_password", "asm3")
            
            self.logger.info(f"Connecting to database {db_name} at {db_host}:{db_port}")
            
            self.db_conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_pass,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            self.db_conn.autocommit = True
            self.logger.info("Database connection established")
            
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            raise
    
    def create_weight_history_table(self):
        """Create the animal_weight_history table if it doesn't exist."""
        try:
            cursor = self.db_conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'animal_weight_history'
                );
            """)
            
            exists = cursor.fetchone()[0]
            
            if not exists:
                self.logger.info("Creating animal_weight_history table")
                cursor.execute("""
                    CREATE TABLE animal_weight_history (
                        id SERIAL PRIMARY KEY,
                        animalid INTEGER NOT NULL,
                        weight_date TIMESTAMP NOT NULL,
                        username VARCHAR(255) NOT NULL,
                        weight REAL NOT NULL,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                cursor.execute("""
                    CREATE INDEX idx_animal_weight_history_animalid 
                    ON animal_weight_history (animalid);
                """)
                
                cursor.execute("""
                    CREATE INDEX idx_animal_weight_history_weight_date 
                    ON animal_weight_history (weight_date);
                """)
                
                self.logger.info("animal_weight_history table created successfully")
            else:
                self.logger.debug("animal_weight_history table already exists")
                
            cursor.close()
            
        except Exception as e:
            self.logger.error(f"Error creating weight history table: {e}")
            raise
    
    def get_last_processed_audit_date(self) -> Optional[str]:
        """Get the last audit date that was processed."""
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                SELECT MAX(weight_date) as last_date 
                FROM animal_weight_history
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['last_date']:
                return result['last_date']
            else:
                # If no records, start from 24 hours ago
                return "1900-01-01 00:00:00"
                
        except Exception as e:
            self.logger.error(f"Error getting last processed audit date: {e}")
            return "1900-01-01 00:00:00"
    
    def get_weight_updates_from_audit(self, last_audit_date: str) -> List[Dict]:
        """
        Query the audit trail for new weight-related entries.
        Returns list of dicts with keys: animalid, auditdate, username, weight
        """
        try:
            cursor = self.db_conn.cursor()
            
            sql = """
            WITH this_audittable AS (
                SELECT 
                    auditdate,
                    username,
                    REPLACE(SPLIT_PART(description, ' ', 3), ',', '') as animal_name,
                    REPLACE(SPLIT_PART(description, ' ', 5), ',', '') as animal_weight,
                    description
                FROM public.audittrail
                WHERE tablename = 'onlineformincoming'
                    AND description LIKE '%Weight%'
                    AND description LIKE '%=Processed=%'
                    AND auditdate > %s
            )
            SELECT 
                an.id as animalid,
                au.auditdate,
                au.username,
                au.animal_weight::REAL as weight
            FROM this_audittable au
            JOIN public.animal an ON au.animal_name = an.animalname
            WHERE au.animal_weight ~ '^[0-9.]+$'  -- Only valid numeric weights
            ORDER BY au.auditdate
            """
            
            cursor.execute(sql, (last_audit_date,))
            results = cursor.fetchall()
            cursor.close()
            
            self.logger.info(f"Found {len(results)} new weight updates since {last_audit_date}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error querying audit trail: {e}")
            return []
    
    def update_animal_weight(self, animal_id: int, weight: float, username: str, weight_date: str):
        """Update an animal's weight and log to history table."""
        try:
            cursor = self.db_conn.cursor()
            
            # Get current weight for comparison
            cursor.execute("SELECT weight FROM animal WHERE id = %s", (animal_id,))
            current_result = cursor.fetchone()
            current_weight = current_result['weight'] if current_result else 0.0
            
            # Update animal weight
            cursor.execute("""
                UPDATE animal 
                SET weight = %s 
                WHERE id = %s
            """, (weight, animal_id))
            
            # Log to weight history
            cursor.execute("""
                INSERT INTO animal_weight_history 
                (animalid, weight_date, username, weight)
                VALUES (%s, %s, %s, %s)
            """, (animal_id, weight_date, username, weight))
            
            cursor.close()
            
            self.logger.info(f"Updated animal {animal_id}: weight {current_weight} -> {weight} by {username}")
            
        except Exception as e:
            self.logger.error(f"Error updating animal {animal_id} weight: {e}")
            raise
    
    def process_weight_updates(self):
        """Main processing loop - check for weight updates and process them."""
        try:
            # Get last processed audit date
            last_audit_date = self.get_last_processed_audit_date()
            self.logger.info(f"Processing weight updates since: {last_audit_date}")
            
            # Get new weight updates from audit trail
            weight_updates = self.get_weight_updates_from_audit(last_audit_date)
            
            if not weight_updates:
                self.logger.debug("No new weight updates to process")
                return
            
            # Process each weight update
            processed_count = 0
            for update in weight_updates:
                try:
                    self.update_animal_weight(
                        animal_id=update['animalid'],
                        weight=update['weight'],
                        username=update['username'],
                        weight_date=update['auditdate']
                    )
                    processed_count += 1
                    
                except Exception as e:
                    self.logger.error(f"Error processing weight update for animal {update['animalid']}: {e}")
                    continue
            
            self.logger.info(f"Successfully processed {processed_count} of {len(weight_updates)} weight updates")
            
        except Exception as e:
            self.logger.error(f"Error in process_weight_updates: {e}")
            raise
    
    def run_once(self):
        """Run one iteration of the weight monitor."""
        try:
            self.connect_database()
            self.create_weight_history_table()
            self.process_weight_updates()
            
        except Exception as e:
            self.logger.error(f"Error in run_once: {e}")
            traceback.print_exc()
            
        finally:
            if self.db_conn:
                self.db_conn.close()
    
    def run_continuous(self):
        """Run the weight monitor continuously, checking every minute."""
        self.logger.info("Starting ASM3 Weight Monitor - checking every 60 seconds")
        
        while True:
            try:
                self.run_once()
                time.sleep(60)  # Wait 60 seconds before next check
                
            except KeyboardInterrupt:
                self.logger.info("Weight monitor stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in continuous mode: {e}")
                traceback.print_exc()
                time.sleep(60)  # Wait before retrying


def main():
    """Main entry point."""
    monitor = WeightMonitor()
    
    # Check command line args
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run once and exit (useful for cron)
        monitor.run_once()
    else:
        # Run continuously
        monitor.run_continuous()


if __name__ == "__main__":
    main()