#!/bin/bash
echo "SETTING UP DB"
mariadb -u root -e "CREATE DATABASE dmoj DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci"
mariadb -u root -e "GRANT ALL PRIVILEGES ON dmoj.* TO 'dmoj'@'%' IDENTIFIED BY '${MARIADB_PASSWORD}'" # mariadb -e "GRANT ALL PRIVILEGES ON dmoj.* TO 'dmoj'@'localhost' IDENTIFIED BY '<mariadb user password>'"
mariadb-tzinfo-to-sql /usr/share/zoneinfo | mariadb -u root mysql
echo "FINISH SETTING UP DB"
