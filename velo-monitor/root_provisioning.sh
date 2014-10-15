#!/bin/sh

########################################
# Root provisioning
########################################
# Configure the VM for running the VELO web GUI.
#
# Updates the VM, installs ROOT dependencies, and then,
# after a reboot, configures AFS and runs the user provisions.
#
# Initialise the VM with provisioning
#   vagrant up --provision
# Reload the VM when prompted, provisioning a final time
#   vagrant reload --provision
# This restart is done to ensure any upgraded kernel is loaded.
########################################

echo "Beginning provisioning"

YUM=/usr/bin/yum

# Add the SLC6 XROOTD stable repository
# http://xrootd.org/binaries/xrootd-stable-slc6.repo
sudo cat > /etc/yum.repos.d/xrootd-stable-slc6.repo << EOF
[xrootd-stable]
name=XRootD Stable repository
baseurl=http://xrootd.org/binaries/stable/slc/6/\$basearch http://xrootd.cern.ch/sw/repos/stable/slc/6/\$basearch
gpgcheck=0
enabled=1
protect=0
EOF

# Add the RHEL6 nginx stable repo
sudo cat > /etc/yum.repos.d/nginx.repo << EOF
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/rhel/6/\$basearch/
gpgcheck=0
enabled=1
EOF

echo "Updating packages"
sudo $YUM -y update

echo "Installing required packages"
# The bare necessities:
#   vim and git
#   OpenAFS
#   ROOT dependencies
#   XROOTD
#   nginx
sudo $YUM install -y \
  vim git \
  kmod-openafs openafs openafs-client \
  libXpm \
  xrootd-client-devel xrootd-client xrootd-libs-devel xrootd-libs xrootd-server \
  nginx

PREPFILE=$HOME/.preparation

if [ ! -f $PREPFILE ]; then
  touch $PREPFILE
  echo "You now need to reboot the VM and rerun the provisioning."
  echo "To do this, run:"
  echo "  vagrant reload --provision"
  echo "I will then continue setting up the VM."
  exit
else
  rm -f $PREPFILE
  echo "Resuming provisioning"
fi

# Download, compile, and install the Redis server and CLI
echo "Installing Redis"
curl -O http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo cp src/redis-server src/redis-cli /usr/local/bin
# Provide default configuration
sudo mkdir -p /usr/local/etc
sudo cp redis.conf /usr/local/etc
cd -
rm -rf redis-stable
rm redis-stable.tar.gz
# Enable memory overcommit
# http://redis.io/topics/admin
sudo cat >> /etc/sysctl.conf << EOF

vm.overcommit_memory = 1
EOF


echo "Configuring AFS"
echo "cern.ch" > $HOME/ThisCell
sudo mv $HOME/ThisCell /usr/vice/etc/ThisCell
sudo /sbin/chkconfig --add afs
sudo /sbin/chkconfig afs on
sudo /sbin/service afs start

echo "Configuring nginx"
# Remove default configurations, replace with our own
sudo rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
sudo cat > /etc/nginx/nginx.conf << EOF
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
  worker_connections  1024;
}

http {
  include       /etc/nginx/mime.types;
  default_type  application/octet-stream;

  log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
  '\$status \$body_bytes_sent "\$http_referer" '
  '"\$http_user_agent" "\$http_x_forwarded_for"';

  access_log  /var/log/nginx/access.log  main;

  sendfile off;

  keepalive_timeout  65;

  # Enable gzip compression
  gzip  on;
  gzip_http_version 1.0;
  gzip_proxied      any;
  gzip_min_length   500;
  gzip_disable      "MSIE [1-6]\.";
  gzip_types        text/plain text/xml text/css
                    text/comma-separated-values
                    text/javascript
                    application/x-javascript
                    application/atom+xml
                    application/json;

  # List of application servers
  upstream uwsgicluster {
    server 127.0.0.1:5000;
    # server 127.0.0.1:5001;
    # ..
  }

  include /etc/nginx/conf.d/*.conf;
}
EOF
sudo cat > /etc/nginx/conf.d/velo-monitor.conf << EOF
server {
  listen 5000;

  #access_log  /var/log/nginx/log/host.access.log  main;

  location / {
    proxy_pass http://127.0.0.1:8000;

    proxy_redirect     off;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Host $server_name;
  }
}
EOF

# Run the user provision as the vagrant user
su vagrant -c '/vagrant/user_provisioning.sh'

echo "Provisioning complete! Reboot once more."
