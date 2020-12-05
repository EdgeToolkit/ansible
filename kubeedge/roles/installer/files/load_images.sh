#!/bin/bash
#images=$(kubeadm config images list | awk -F"/" 'if{ ($1=="k8s.gcr.io"){print "$2"} }')
rm -f /tmp/kubernetes_images.list
kubeadm config images list  >/tmp/kubernetes_images.list >&1
images=$(awk -F"/" '{print $2}' /tmp/kubernetes_images.list)
echo "${images[*]}"
for i in ${images[*]} ; do
  sudo docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/$i
  sudo docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/$i k8s.gcr.io/$i
  #sudo docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/$i
done
