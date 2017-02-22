#!/bin/sh

sudo yum install mariadb
sudo yum install mariadb-server
sudo yum update -y
sudo systemctl start mariadb
sudo systemctl stop mariadb
sudo systemctl start mariadb
#mysql_secure_installation interactive script
#mysql -u root -p setup database, user & privileges
