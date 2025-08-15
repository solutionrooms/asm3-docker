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
from datetime import datetime, timezone
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
            level=logging.DEBUG,
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
            
            result = cursor.fetchone()
            exists = result['exists']
            
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
    
    def get_last_processed_audit_date(self) -> Optional[datetime]:
        """Get the last audit date that was processed."""
        try:
            cursor = self.db_conn.cursor()
            self.logger.debug("Querying for last processed audit date")
            cursor.execute("""
                SELECT MAX(weight_date) as last_date 
                FROM animal_weight_history
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['last_date']:
                self.logger.debug(f"Found last processed date: {result['last_date']}")
                return result['last_date']
            else:
                # If no records, start from a very early date
                default_date = datetime(1900, 1, 1, 0, 0, 0)
                self.logger.debug(f"No previous records found, starting from {default_date}")
                return default_date
                
        except Exception as e:
            self.logger.error(f"Error getting last processed audit date: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return datetime(1900, 1, 1, 0, 0, 0)
    
    def get_weight_updates_from_audit(self, last_audit_date: datetime) -> List[Dict]:
        """
        Query the audit trail for new weight-related entries.
        Returns list of dicts with keys: animalid, auditdate, username, weight
        """
        try:
            cursor = self.db_conn.cursor()
            
            self.logger.debug(f"Checking for audit entries since: {last_audit_date} (type: {type(last_audit_date)})")
            
            # Test basic connectivity first with a simple query
            cursor.execute("SELECT COUNT(*) as total_count FROM public.audittrail")
            total_result = cursor.fetchone()
            self.logger.debug(f"Total audit records: {total_result['total_count']}")
            
            # Simple count query to check our specific criteria
            count_sql = """
            SELECT COUNT(*) as count
            FROM public.audittrail
            WHERE tablename = 'onlineformincoming'
                AND description LIKE %s
                AND description LIKE %s
                AND auditdate > %s
            """
            
            self.logger.debug("Executing count query with parameters")
            cursor.execute(count_sql, ('%Weight%', '%=Processed=%', last_audit_date))
            debug_result = cursor.fetchone()
            self.logger.info(f"Found {debug_result['count']} potential audit entries to process")
            
            if debug_result['count'] == 0:
                cursor.close()
                self.logger.debug("No audit entries found, returning empty list")
                return []
            
            # Sample query to see what we're working with
            sample_sql = """
            SELECT auditdate, username, description
            FROM public.audittrail
            WHERE tablename = %s
                AND description LIKE %s
                AND description LIKE %s
                AND auditdate > %s
            ORDER BY auditdate DESC
            LIMIT 3
            """
            
            self.logger.debug("Getting sample audit entries")
            cursor.execute(sample_sql, ('onlineformincoming', '%Weight%', '%=Processed=%', last_audit_date))
            sample_results = cursor.fetchall()
            
            for i, sample in enumerate(sample_results):
                self.logger.debug(f"Sample {i+1}: {sample['auditdate']} - {sample['username']} - {sample['description'][:100]}...")
            
            # Now execute the full query to get weight updates
            main_sql = """
            WITH parsed_audit AS (
                SELECT 
                    auditdate,
                    username,
                    description,
                    -- Extract animal name: everything between "Animal: " and the next comma
                    TRIM(SUBSTRING(description FROM 'Animal: ([^,]+)')) as animal_name,
                    -- Extract weight: everything between "Weight: " and the next comma or end
                    TRIM(SUBSTRING(description FROM 'Weight: ([^,\\s]+)')) as animal_weight_text
                FROM public.audittrail
                WHERE tablename = %s
                    AND description LIKE %s
                    AND description LIKE %s
                    AND auditdate > %s
            )
            SELECT 
                an.id as animalid,
                pa.auditdate,
                pa.username,
                pa.animal_weight_text::REAL as weight,
                pa.description
            FROM parsed_audit pa
            JOIN public.animal an ON LOWER(pa.animal_name) = LOWER(an.animalname)
            WHERE pa.animal_weight_text ~ '^[0-9.]+$'  -- Only valid numeric weights
                AND pa.animal_weight_text::REAL > 0    -- Only positive weights
            ORDER BY pa.auditdate
            """
            
            self.logger.debug("Executing main weight processing query")
            cursor.execute(main_sql, ('onlineformincoming', '%Weight%', '%=Processed=%', last_audit_date))
            results = cursor.fetchall()
            cursor.close()
            
            self.logger.info(f"Successfully parsed {len(results)} weight updates from {debug_result['count']} audit entries")
            
            if results:
                for i, result in enumerate(results[:3]):  # Log first 3 results
                    self.logger.debug(f"Weight update {i+1}: Animal {result['animalid']} ({result['weight']}g) on {result['auditdate']}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error querying audit trail: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return []
    
    def update_animal_weight(self, animal_id: int, weight: float, username: str, weight_date: datetime):
        """Update an animal's weight and log to history table."""
        try:
            cursor = self.db_conn.cursor()
            
            self.logger.debug(f"Updating weight for animal {animal_id} to {weight} at {weight_date}")
            
            # Get current weight for comparison
            cursor.execute("SELECT weight FROM animal WHERE id = %s", (animal_id,))
            current_result = cursor.fetchone()
            current_weight = current_result['weight'] if current_result else 0.0
            
            # Convert weight to kilograms if entered in grams (weight > 10 assumed to be grams)
            weight_in_kg = weight / 1000 if weight > 10 else weight
            
            # Update animal weight (ASM3 stores in kilograms)
            cursor.execute("UPDATE animal SET weight = %s WHERE id = %s", (weight_in_kg, animal_id))
            
            # Log to weight history (store in kilograms)
            cursor.execute("""
                INSERT INTO animal_weight_history 
                (animalid, weight_date, username, weight)
                VALUES (%s, %s, %s, %s)
            """, (animal_id, weight_date, username, weight_in_kg))
            
            cursor.close()
            
            self.logger.info(f"Updated animal {animal_id}: weight {current_weight} -> {weight_in_kg}kg by {username}")
            
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
            self.logger.info("Starting weight monitor run")
            
            self.logger.debug("Step 1: Connecting to database")
            self.connect_database()
            
            self.logger.debug("Step 2: Creating weight history table if needed")
            self.create_weight_history_table()
            
            self.logger.debug("Step 3: Processing weight updates")
            self.process_weight_updates()
            
            self.logger.info("Weight monitor run completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in run_once: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            
        finally:
            if self.db_conn:
                self.logger.debug("Closing database connection")
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