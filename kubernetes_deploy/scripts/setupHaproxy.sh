#!/bin/bash

source ~/vars.sh

function configureHaproxy {
cat > /etc/haproxy/haproxy.cfg <<EOF
global
	log /dev/log	local0
	log /dev/log	local1 notice
	chroot /var/lib/haproxy
	stats socket /run/haproxy/admin.sock mode 660 level admin
	stats timeout 30s
	daemon

	# Default SSL material locations
	ca-base /etc/ssl/certs
	crt-base /etc/ssl/private

	# Default ciphers to use on SSL-enabled listening sockets.
	# For more information, see ciphers(1SSL). This list is from:
	#  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
	# An alternative list with additional directives can be obtained from
	#  https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=haproxy
	ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
	ssl-default-bind-options no-sslv3

defaults
	log	global
	mode	http
	option	httplog
	option	dontlognull
  timeout connect 5000
  timeout client  50000
  timeout server  50000

frontend k8s-api
	bind ${thisIp}:6443
	bind 127.0.0.1:6443
	mode tcp
	option tcplog
	default_backend k8s-api

backend k8s-api
	mode tcp
	option tcplog
	option tcp-check
	balance roundrobin
	default-server port 6443 inter 10s downinter 5s rise 2 fall 2 slowstart 60s maxconn 250 maxqueue 256 weight 100
        {CLUSTER_REPLACE_SERVER}
EOF
mkdir /run/haproxy
systemctl restart haproxy
}

function connectNodeToLocalHaproxy {
  # Заменить адрес мастер узла на локальный адрес узла Haproxy.
  sed -i --regexp-extended "s/(server: https:\/\/)[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}/\1127.0.0.1/g" /etc/kubernetes/kubelet.conf
  systemctl restart kubelet
}

configureHaproxy
connectNodeToLocalHaproxy
