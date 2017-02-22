#!/bin/sh

echo "Install & setup apache"
sudo yum install httpd
sudo systemctl start httpd
sudo systemctl enable httpd
echo "Install php"
sudo yum install php php-mysql php-fpm
echo "Install & update mariadb"
sudo yum install mariadb
sudo yum update
echo "Download and setup wordpress"
sudo yum install wget
cd /var/www/html/
sudo wget http://wordpress.org/latest.tar.gz
sudo tar -zxvf latest.tar.gz

# Create & update wp-config.php file
cd wordpress
sudo cp wp-config-sample.php wp-config.php
sudo chown -R apache:apache wordpress/*
sudo systemctl restart httpd
## set DB host, username & password

# update selinux/config to be permissive
