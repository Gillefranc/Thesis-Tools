## Master node

- Install kubeadm
- Edit /etc/containerd/config.toml: set `SystemdCgroup = true`
  - If not present, run `containerd config default > /etc/containerd/config.toml`
- Run `kubeadm init --control-plane-endpoint 10.0.20.xxx --pod-network-cidr=10.245.0.0/16` (cidr 244 for KubeEdge and 245 for OpenYURT)
- Copy kubeconfig `cp /etc/kubernetes/admin.conf .kube/config`
- Install flannel: `kubectl apply -f kube-flannel.yml`
- Taint nodes:
  `kubectl taint nodes --all node-role.kubernetes.io/control-plane-`
- disable AppArmor for runc
  `sudo ln -s /etc/apparmor.d/runc /etc/apparmor.d/disable/
`sudo apparmor_parser -R /etc/apparmor.d/runc`
- OpenYURT: <https://openyurt.io/docs/installation/manually-setup>
- fix OpenYURT permissions bug:

  ```
  kubectl apply -f yurt-manager-admin-rolebinding.yaml
  kubectl apply -f yurt-manager-rolebinding.yaml
  ```

## Edge node

- Install Ubuntu Server 24(LTS) (used rpi-imager)

- Install containerd
  `sudo apt-get update && sudo apt-get upgrade`
  `sudo apt install containerd`

- Install CNI plugins:

  - wget [https://github.com/containernetworking/plugins/releases/download/v1.6.0/cni-plugins-linux-arm64-v1.6.0.tgz](https://github.com/containernetworking/plugins/releases/download/v1.6.0/cni-plugins-linux-arm64-v1.6.0.tgz)
  - tar -xzvf cni-plugins… -C /opt/cni/bin/

- Flannel fix:
  add file /run/flannel/subnet.env

```
FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.0.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
```

- Install Yurtadm binary on edge device: <https://openyurt.io/docs/developer-manuals/how-to-build-and-test/>
  Requirements: make, golang (1.17)

  - git clone [https://github.com/openyurtio/openyurt.git](https://github.com/openyurtio/openyurt.git)
  - cd openyurt
  - make build WHAT="yurtadm" ARCH="arm64" REGION=eu

- Install crictl

  - wget [https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.31.1/crictl-v1.31.1-linux-arm64.tar.gz](https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.31.1/crictl-v1.31.1-linux-arm64.tar.gz)
  - tar zxvf crictl-v1.31.1-linux-arm64.tar.gz
  - mv crictl /usr/local/bin/
  - vim /etc/crictl.yaml:

  ```Plain
  runtime-endpoint: unix:///run/containerd/containerd.sock
  image-endpoint: unix:///run/containerd/containerd.sock
  timeout: 10
  debug: true
  ```

- Join the node to the cluster:

```
yurtadm join 10.0.20.xxx:6443 --token=xx.xxx --node-type=edge --discovery-token-unsafe-skip-ca-verification --cri-socket=unix:///run/containerd/containerd.sock --v=5
```
