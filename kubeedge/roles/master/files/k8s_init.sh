#!/bin/bash

_HOME=$HOME
[ -n "$1" ] && _HOME=$1
export PATH=/home/$_HOME/.local/bin:$PATH

kubeadm reset -f
rm -rf $_HOME/.kube

set -e
swapoff -a
systemctl enable docker.service
kubeadm init --pod-network-cidr=192.168.0.0/16

mkdir -p $_HOME/.kube
cp -i /etc/kubernetes/admin.conf $_HOME/.kube/config
chmod 644 $_HOME/.kube/config
