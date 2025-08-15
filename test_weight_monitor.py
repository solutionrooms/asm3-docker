#!/usr/bin/env python3
"""
Test script for the ASM3 Weight Monitor

This script can be used to:
1. Test database connectivity
2. Verify the weight_monitor.py script works
3. Check the animal_weight_history table structure

Usage:
    python3 test_weight_monitor.py
"""

from weight_monitor import WeightMonitor, WeightMonitorConfig
import sys

def test_config():
    """Test configuration loading."""
    print("Testing configuration loading...")
    config = WeightMonitorConfig()
    
    db_host = config.get_string("db_host", "localhost")
    db_name = config.get_string("db_name", "asm")
    db_user = config.get_string("db_username", "asm3")
    
    print(f"Database host: {db_host}")
    print(f"Database name: {db_name}")
    print(f"Database user: {db_user}")
    print("✓ Configuration loaded successfully\n")

def test_database_connection():
    """Test database connectivity."""
    print("Testing database connection...")
    monitor = WeightMonitor()
    
    try:
        monitor.connect_database()
        print("✓ Database connection successful")
        
        # Test a simple query
        cursor = monitor.db_conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM animal")
        result = cursor.fetchone()
        print(f"✓ Found {result['count']} animals in database")
        cursor.close()
        
        monitor.db_conn.close()
        print("✓ Database connection closed\n")
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}\n")
        return False
    
    return True

def test_weight_history_table():
    """Test weight history table creation."""
    print("Testing weight history table...")
    monitor = WeightMonitor()
    
    try:
        monitor.connect_database()
        monitor.create_weight_history_table()
        
        # Check table exists and structure
        cursor = monitor.db_conn.cursor()
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'animal_weight_history'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("✓ animal_weight_history table structure:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']}")
        
        cursor.close()
        monitor.db_conn.close()
        print("✓ Weight history table test completed\n")
        
    except Exception as e:
        print(f"✗ Weight history table test failed: {e}\n")
        return False
    
    return True

def test_audit_query():
    """Test the audit trail query."""
    print("Testing audit trail query...")
    monitor = WeightMonitor()
    
    try:
        monitor.connect_database()
        
        # Test audit query with a very old date to see all results
        weight_updates = monitor.get_weight_updates_from_audit("1900-01-01 00:00:00")
        print(f"✓ Found {len(weight_updates)} historical weight updates")
        
        if weight_updates:
            print("✓ Sample weight update:")
            sample = weight_updates[0]
            print(f"  - Animal ID: {sample['animalid']}")
            print(f"  - Date: {sample['auditdate']}")
            print(f"  - User: {sample['username']}")
            print(f"  - Weight: {sample['weight']}")
        
        monitor.db_conn.close()
        print("✓ Audit trail query test completed\n")
        
    except Exception as e:
        print(f"✗ Audit trail query test failed: {e}\n")
        return False
    
    return True

def main():
    """Run all tests."""
    print("ASM3 Weight Monitor Test Suite")
    print("=" * 40)
    
    tests = [
        ("Configuration", test_config),
        ("Database Connection", test_database_connection),
        ("Weight History Table", test_weight_history_table),
        ("Audit Trail Query", test_audit_query)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}\n")
    
    print(f"Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n✓ All tests passed! Weight monitor is ready to use.")
        print("\nTo run the weight monitor:")
        print("  - Once: python3 weight_monitor.py --once")
        print("  - Continuous: python3 weight_monitor.py")
    else:
        print(f"\n✗ {len(tests) - passed} tests failed. Please check configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()