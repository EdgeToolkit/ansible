# ansible

## KubeEdge 环境部署
   为便于部署建议将所有机器添加相同账号 如
```bash
epm@epm:~$ sudo adduser k8s
Adding user `k8s' ...
Adding new group `k8s' (1001) ...
Adding new user `k8s' (1001) with group `k8s' ...
Creating home directory `/home/k8s' ...
Copying files from `/etc/skel' ...
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
Changing the user information for k8s
Enter the new value, or press ENTER for the default
	Full Name []: Kubernetes
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] y

epm@epm:~$ sudo usermod -a -G  sudo k8s
epm@epm:~$ sudo usermod -a -G  adm  k8s
epm@epm:~$ id k8s
uid=1001(k8s) gid=1001(k8s) groups=1001(k8s),4(adm),27(sudo)


```

   * 安装软件 `ansible-playbook -i ./hosts  installyml`
   * 部署k8s master `ansible-playbook -i ./hosts  k8s_master.yml`
   * 部署KubeEdge clould `ansible-playbook -i ./hosts  clodecore.yml`
   * 部署k8s node `ansible-playbook -i ./hosts  k8s_nodes.yml`
   * 启动KubeEdge Cloud `sudo ~/.local/bin/cloud.sh`
   * 启动KubeEdge Edge `sudo ~/.local/bin/edged.sh`

testnode
https://segmentfault.com/a/1190000038233991
