import sqlite3
from datetime import datetime

def migrate_database():
    conn = sqlite3.connect('patents.db')
    cursor = conn.cursor()
    
    # Create backup of existing table
    print("Creating backup...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Quantum_Computing_all_20241214_backup AS 
        SELECT * FROM Quantum_Computing_all_20241214_new
    """)
    
    # Create new tables
    print("Creating new schema...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patent_documents (
            document_no VARCHAR(20) PRIMARY KEY,
            title TEXT NOT NULL,
            country_code CHAR(2) NOT NULL,
            assignee TEXT,
            doc_type CHAR(1) CHECK (doc_type IN ('A', 'B')),
            doc_number INTEGER,
            doc_kind VARCHAR(5),
            status VARCHAR(50),
            file_date DATE,
            grant_date DATE,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(document_no)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patent_scores (
            document_no VARCHAR(20) PRIMARY KEY,
            pscore DECIMAL(5,2),
            cscore DECIMAL(5,2),
            lscore DECIMAL(5,2),
            tscore DECIMAL(5,2),
            prior_art_score DECIMAL(5,2),
            pendency INTEGER,
            category VARCHAR(50),
            FOREIGN KEY (document_no) REFERENCES patent_documents(document_no)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patent_classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_no VARCHAR(20),
            cpc_code VARCHAR(50),
            cpc_type VARCHAR(20),
            FOREIGN KEY (document_no) REFERENCES patent_documents(document_no)
        )
    """)
    
    # Migrate data to new structure
    print("Migrating data...")
    
    # Get distinct patent documents
    cursor.execute("""
        INSERT OR IGNORE INTO patent_documents (
            document_no,
            title,
            country_code,
            assignee,
            doc_type,
            doc_kind,
            status,
            file_date,
            grant_date
        )
        SELECT DISTINCT
            document_no,
            title,
            country_code,
            current_assignee,
            CASE 
                WHEN document_no LIKE '%B%' THEN 'B'
                ELSE 'A'
            END,
            SUBSTR(document_no, -2),
            document_status,
            date(file_date),
            date(grant_date)
        FROM Quantum_Computing_all_20241214_backup
    """)
    
    # Migrate scores
    print("Migrating scores...")
    cursor.execute("""
        INSERT OR IGNORE INTO patent_scores (
            document_no,
            pscore,
            cscore,
            lscore,
            tscore,
            prior_art_score,
            pendency,
            category
        )
        SELECT DISTINCT
            document_no,
            CAST(pscore AS DECIMAL(5,2)),
            CAST(cscore AS DECIMAL(5,2)),
            CAST(lscore AS DECIMAL(5,2)),
            CAST(tscore AS DECIMAL(5,2)),
            CAST(prior_art_score AS DECIMAL(5,2)),
            CAST(pendency AS INTEGER),
            category
        FROM Quantum_Computing_all_20241214_backup
    """)
    
    # Migrate CPC classifications
    print("Migrating CPC classifications...")
    cursor.execute("""
        INSERT INTO patent_classifications (document_no, cpc_code, cpc_type)
        SELECT DISTINCT
            document_no,
            cpc_first,
            'first'
        FROM Quantum_Computing_all_20241214_backup
        WHERE cpc_first IS NOT NULL AND cpc_first != ''
    """)
    
    cursor.execute("""
        INSERT INTO patent_classifications (document_no, cpc_code, cpc_type)
        SELECT DISTINCT
            document_no,
            cpc_inventive,
            'inventive'
        FROM Quantum_Computing_all_20241214_backup
        WHERE cpc_inventive IS NOT NULL AND cpc_inventive != ''
    """)
    
    # Verify migration
    print("\nVerifying migration...")
    cursor.execute("SELECT COUNT(*) FROM patent_documents")
    doc_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM patent_scores")
    score_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM patent_classifications")
    class_count = cursor.fetchone()[0]
    
    print(f"Patents migrated: {doc_count}")
    print(f"Scores migrated: {score_count}")
    print(f"Classifications migrated: {class_count}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("\nMigration completed successfully!")

if __name__ == '__main__':
    migrate_database()