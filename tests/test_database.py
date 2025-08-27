import pymysql
import configparser
import os

def test_database_connection():
    """Test database connection independently"""
    try:
        # Load config from the correct path
        config = configparser.ConfigParser()
        
        # Try different possible paths
        possible_paths = [
            'database/config.ini',
            '../database/config.ini',
            os.path.join('..', 'config', 'db_config.ini'),
            os.path.join(os.path.dirname(__file__), '..', 'database', 'config.ini')
        ]
        
        config_found = False
        for config_path in possible_paths:
            if os.path.exists(config_path):
                config.read(config_path)
                config_found = True
                print(f"✓ Found config file at: {config_path}")
                break
        
        if not config_found:
            print("❌ config.ini file not found!")
            print("Please create database/config.ini with your database credentials")
            return False
        
        # Check if pymysql section exists
        if not config.has_section('pymysql'):
            print("❌ 'pymysql' section not found in config.ini")
            print("Available sections:", config.sections())
            return False
        
        print("📋 Testing database connection...")
        print(f"Host: {config.get('pymysql', 'host')}")
        print(f"Database: {config.get('pymysql', 'database')}")
        print(f"User: {config.get('pymysql', 'user')}")
        
        # Test connection
        connection = pymysql.connect(
            host=config.get("pymysql", "host"),
            user=config.get("pymysql", "user"), 
            password=config.get("pymysql", "password"),
            database=config.get("pymysql", "database"),
            port=int(config.get("pymysql", "port", fallback="3306")),
            charset='utf8mb4'
        )
        
        print("✓ Database connection successful!")
        
        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✓ Query test successful: {result}")
        
        # Check for staff table
        cursor.execute("SHOW TABLES LIKE 'staff'")
        staff_table = cursor.fetchone()
        
        if staff_table:
            print("✓ Staff table found!")
            cursor.execute("SELECT COUNT(*) FROM staff")
            count = cursor.fetchone()[0]
            print(f"Staff records: {count}")
        else:
            print("❌ Staff table not found!")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Available tables:")
            for table in tables:
                print(f"  - {table[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
