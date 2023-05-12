#!/bin/bash

source ~/vars.sh

function createKubeadmConfig {
cat > kubeadm-init.yaml <<EOF
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "${thisIp}"
nodeRegistration:
  criSocket: "/var/run/crio/crio.sock"
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v${kubernetesVersion}
apiServer:
  certSANs:
  {CLUSTER_REPLACE_IP}
  - 127.0.0.1
controlPlaneEndpoint: ${thisIp}
etcd:
  external:
    endpoints:
    {CLUSTER_REPLACE_ETCD}
networking:
  podSubnet: "${podSubnet}"
  serviceSubnet: "${serviceSubnet}"
  dnsDomain: "cluster.local"
EOF
}

function initializeMasterNode {
  echo "#!/bin/bash" > ~/join-command.sh
  kubeadm init --config=kubeadm-init.yaml | grep 'kubeadm join' -A 1 -m 1 | sed 's|\\\\||' | xargs | tr -d '\n' >> ~/join-command.sh
}

function archiveCertificates {
  tar -zcvf certificates.tar.gz -C /etc/kubernetes/pki .
}

function extractCertificates {
  mkdir -p /etc/kubernetes/pki
  tar -xvf certificates.tar.gz -C /etc/kubernetes/pki
}

function installFlannel {
  export KUBECONFIG=/etc/kubernetes/admin.conf
  kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
}

createKubeadmConfig

if [[ $thisIp == $master0_IP ]]; then
  initializeMasterNode
  installFlannel
  archiveCertificates
fi

if [[ $thisIp != $master0_IP ]]; then
  extractCertificates
  initializeMasterNode
fi
