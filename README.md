# ekn_stack
Elasticsearch, Kibana and NGINX stack installation

Ansible playbooks for creating an Elasticsearch cluster with Kibana, using an nginx load balancer and http authenticator

This has been tested on:
* Debian 7
* RHEL 7
* Fedora 22
* Fedora 24

The latest versions of the available services are installed to ensure compatibility.
Ansible version 2.1.2.0 was used durig the test and in cases where the target 
machines are Fedora 24+ the python-dnf 
package is required.

## Usage

You must the location where you want to store the playbooks. In the same location you 
must also have the roles folder with all the required roles that used. You may choose 
to either fetch them there directly or create links to their original locations.

There are three roles you must acquire first.
* [elastic/ansible-elasticsearch](https://github.com/elastic/ansible-elasticsearch)
* [geerlingguy/ansible-role-kibana](https://github.com/geerlingguy/ansible-role-kibana)
* [jdauphant/ansible-role-nginx](https://github.com/jdauphant/ansible-role-nginx)

The playbooks assume you have renamed the roles to just the service they handle.
* elastic/ansible-elasticsearch is renamed to elasticsearch
* geerlingguy/ansible-role-kibana is renamed to kibana
* jdauphant/ansible-role-nginx is renamed to nginx


e.g. 
Acquiring the required roles and storing them under the same location.

```
cd ~/ansible/
git clone https://github.com/elastic/ansible-elasticsearch.git roles/elasticsearch
git clone https://github.com/geerlingguy/ansible-role-kibana.git roles/kibana
git clone https://github.com/jdauphant/ansible-role-nginx.git roles/nginx
git clone https://github.com/andreoua/ekn_stack.git
```
If you don't have python2-dnf installed and plan on deploying on Fedora 24 and later you will need the python2-dnf package.
```
pip install python2-dnf
```
You must now configure the hosts file. Since a network of 3 elastic nodes, 1 kibana and 1 nginx are assume 
the host file will contain three lists of hosts.
```
[elastic_servers]
10.10.80.10
10.10.80.11

[elastic_servers:vars]
ansible_user=root
ansible_private_key_file=~/ansible/keys/simpleit.pri

[kibana_server]
10.10.80.12

[kibana_server:vars]
ansible_user=root
ansible_private_key_file=~/ansible/keys/simpleit.pri

[web_servers]
10.10.80.100

[web_servers:vars]
ansible_user=root
ansible_private_key_file=~/ansible/keys/simpleit.pri
```
You can use the supplied private key file for convenience or create your own. You will have to change the location and name.
```
ssh-keygen -t rsa
```
You should now be ready to execute the ansible playbook
```
ansible-playbook -i hosts cluster.yml
```
If all goes well you should see something like this.
```
PLAY RECAP *********************************************************************
10.181.27.73               : ok=47   changed=0    unreachable=0    failed=0   
10.181.28.177              : ok=47   changed=0    unreachable=0    failed=0   
10.181.30.73               : ok=54   changed=0    unreachable=0    failed=0
```

All operations are indempodent and any modification to a part of the playbook will modify
that setting and restart the corresponding service. The cluster.yml playbook will install 
Elasticsearch, Kibana and NGINX but if you want to install just one the three or modify the 
settings in the future you may execute just the corresponding playbook.

With supplied hosts file Kibana will be accessible through 10.10.80.12:5601.
The default username is `admin` and the password `secret`.

## Included roles

The three roles used in these playbooks offer a wealth of options. They are all fully supported and can be used here.
You should refer to the respective role documentation for a complete list of available settings.
The only case where an issue might occur is if the node OS is Fedore 24 or later. The elasticsearch role has been 
designed to use the yum package manager and Fedora uses dnf. In most cases dnf will interpret the command executed
using yum but only of the yum package is installed. If yum is not installed or you not sure you may include the 
supplied dnf.yml and main.yml files. These should be stored in the same directory as the elasticsearch role.

e.g.
```
mv dnf.yml ~/ansible/roles/elasticsearch/tasks/
mv main.yml ~/ansible/roles/elasticsearch/tasks/
```

### Role Documentation

* [elastic/ansible-elasticsearch](https://github.com/elastic/ansible-elasticsearch/blob/master/README.md)
* [geerlingguy/ansible-role-kibana](https://github.com/geerlingguy/ansible-role-kibana/blob/master/README.md)
* [jdauphant/ansible-role-nginx](https://github.com/jdauphant/ansible-role-nginx/blob/master/README.md)


## Vagrant Provisioning

You want to test the playbooks using Vagrant and not on actuall machines or instances.
Supplied are two Vagrantfile configuration files prepared for both a VirtualBox and Docker provider.

The configuration will 4 node cluster with 3 elasticsearch nodes, 1 kibana (hosted on an elasticsearch node) and 1 nginx.

In the case of VirtualBox the VM created are limited to 1 CPU and 512MB of memory.

#### Usage

In order to use the Vagrantfile configurations you must copy the corresponding Vagrantfile to a directory and provide
all the playbooks and roles in a subdirectory names `provisioning`.

e.g.
Provisioning for both VirtualBox and Docker
```
git clone https://github.com/andreoua/ekn_stack.git ~/simpleit/
```
For Docker
```
mkdir -p ~/vagrant/docker_cluster/provisioning
cp ~/simpleit/vagrant_docker/Vagrantfile ~/vagrant/docker_cluster/
cp ~/simpleit/keys/simpleit.* ~/vagrant/docker_cluster/
cd ~/vagrant/docker_cluster/provisioning
ln -s ~/simpleit/roles roles
vagrant up --provider docker
```
For VirtualBox
```
mkdir -p ~/vagrant/docker_vbox/provisioning
cp ~/simpleit/vagrant_vbox/Vagrantfile ~/vagrant/vbox_cluster/
cp ~/simpleit/keys/simpleit.* ~/vagrant/vbox_cluster/
cd ~/vagrant/vbox_cluster/provisioning
ln -s ~/simpleit/roles roles
vagrant up --provider virtualbox
```




# Python Health monitoring Script

A python script is also provided to monitor the health of the cluster and retrieve CPU and RAM statistic.

It requires the elasticsearch python library.
```
pip install elasticsearch
```

## Usage

Execution is simple. You just need to make the script executable and supply at least a host to connect to.
```
chmod +x elastic_health.py
./elastic_health.py -h 10.10.80.10 -u admin -pw secret
```

Python is assumed to be install under `/usr/bin/`. If Python is located elsewhere modify the first line.
```
#!/usr/bin/python
```
In case you don't know where python is located type the following copy the location.
```
which python
```

### Options

```
  -h, --help                         show this help message and exit
  -i HOSTS, --hosts HOSTS            host or hosts to connect to
  -u USERNAME, --username USERNAME   http_auth username
  -pw PASSWORD, --password PASSWORD  http_auth password
  -p PORT, --port PORT               elasticsearch node connection port

```

