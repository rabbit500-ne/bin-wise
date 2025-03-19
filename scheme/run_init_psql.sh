#!/bin/bash

# Database connection details
DB_NAME="your_database_name"
DB_USER="your_database_user"
DB_HOST="your_database_host"
DB_PORT="your_database_port"

# Path to the SQL file
SQL_FILE="/home/rag451/BinWize/bin-wise/scheme/init.sql"

# Execute the SQL file
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $SQL_FILE