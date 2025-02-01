#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Execute the SQL file
sqlite3 $DB_FILE < $SQL_FILE