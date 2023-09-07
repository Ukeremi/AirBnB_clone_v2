# Puppet script for setting up web_static
# Author: Alexander Udeogaranya
# Description: This Puppet script sets up web servers for the deployment
#              of web_static on an Ubuntu system with Nginx.
#              It performs the following tasks:
#              - Installs Nginx if not already installed
#              - Allows Nginx through the firewall
#              - Creates necessary directories for web_static
#              - Generates a fake HTML file for testing
#              - Sets up symbolic links for web_static
#              - Sets ownership to the ubuntu user and group recursively
#              - Updates Nginx configuration to serve web_static content
#              - Restarts Nginx to apply changes

# Nginx server configuration
$nginx_conf = "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://linktr.ee/firdaus_h_salim/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
"

# Install Nginx package
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

# Create necessary directories
-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

# Generate a fake HTML file for testing
-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "this webpage is found in data/web_static/releases/test/index.htm \n"
}

# Create or recreate the symbolic link to the test release
-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

# Set ownership to the ubuntu user and group recursively
-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Create directories for the default website
file { '/var/www':
  ensure => 'directory'
}

-> file { '/var/www/html':
  ensure => 'directory'
}

# Create an index.html file for the default website
-> file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "This is my first upload  in /var/www/index.html***\n"
}

# Create a custom 404.html error page
-> file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page - Error page\n"
}

# Update Nginx configuration with the custom server block
-> file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
}

# Restart Nginx to apply changes
-> exec { 'nginx restart':
  path => '/etc/init.d/'
}
