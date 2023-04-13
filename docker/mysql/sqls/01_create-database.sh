#!/bin/bash
DB_NAME=financial_db
MYSQL=( mysql -u root -p${MYSQL_ROOT_PASSWORD} )

${MYSQL[@]} -e "CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` ;"
${MYSQL[@]} -e "GRANT ALL ON \`${DB_NAME}\`.* TO '"${MYSQL_USER}"'@'%' ;"
${MYSQL[@]} -e 'FLUSH PRIVILEGES ;'
