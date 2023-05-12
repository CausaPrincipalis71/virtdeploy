source ~/vars.sh

function createEnvironmentFile {
cat > /etc/etcd.env <<EOF
${thisHostname}
${thisIp}
EOF
}

function createServiceFile {
cat > /lib/systemd/system/etcd.service <<EOF
[Unit]
Description=etcd
Documentation=https://github.com/coreos/etcd
Conflicts=etcd.service
Conflicts=etcd2.service

[Service]
EnvironmentFile=/etc/etcd.env
Type=notify
Restart=always
RestartSec=5s
LimitNOFILE=40000
TimeoutStartSec=0

ExecStart=/usr/sbin/etcd \\
  --name $thisHostname \\
  --listen-peer-urls http://$thisIp:2380 \\
  --listen-client-urls http://0.0.0.0:2379 \\
  --advertise-client-urls http://$thisIp:2379 \\
  --initial-cluster-token $etcdToken \\
  --initial-advertise-peer-urls http://$thisIp:2380 \\
  --initial-cluster {CLUSTER_REPLACE} \\
  --initial-cluster-state new

[Install]
WantedBy=multi-user.target
EOF
}

createEnvironmentFile
createServiceFile
systemctl enable --now etcd
