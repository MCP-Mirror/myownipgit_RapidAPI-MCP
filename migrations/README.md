# Database Migrations

## Schema Update (01_schema_update.py)

This migration script updates the database schema to::

1. Split the single table into three normalized tables:
   - patent_documents: Core patent information
   - patent_scores: Patent scoring data
   - patent_classifications: CPC classification data

2. Adds proper constraints:
   - Primary keys
   - Foreign key relationships
   - Data type constraints

3. Improves data quality:
   - Removes duplicates
   - Properly formats dates
   - Adds document type classification

### Running the Migration

```bash
python migrations/01_schema_update.py
```

### Rollback

The original data is preserved in `Quantum_Computing_all_20241214_backup`.
To rollback, restore from this backup table.

### Verification

The migration script includes verification steps to ensure:
1. All unique patents are transferred
2. Score data is preserved
3. CPC classifications are properly split

After migration, the script prints counts of migrated records for verification.