# LAB01
Creating a simple webservers playbook

# Before you start
* Please ensure that you have setup your ansible controller. You can find the ansible workstation setup guide [here](../../WORKSTATION.md)
* You will need to manually create virtual machine in AWS
  * You have to copy the ip address of the created machine to your hosts file
  * You have to download the ssh key and store it in your profile ~/.ssh/ansible-demo.pem

# More about Ansible
Ansible is a simple open-source software for configuration management and orchestration. It is powerful and flexible platform which can configure both Windows and Unix-like systems. Almost everything in Ansible is described as human readable YAML (Ansible automation language). Another important fact about Ansible is its agentless nature. It relays on the native operating system services like SSH and Windows Remote Management (Winrm). The Ansible platform is a good solution for both administrators and developers and it can be used to automate many different tasks.

# Ansible Execution Modes
## Ad-Hoc mode
Execute ansible tasks direct from the command line. This is a good place to start to understand the basics of what Ansible can do prior to learning the playbooks language. Ad-Hoc commands can also be used to do quick things that you might not necessarily want to write a full playbook for.

## Playbook mode
Playbooks are automation documents that Ansible engine executes. When you want to automate an IT process, you define the required steps in a playbook and give this playbook to Ansible so it can do the required job for you.

# Ansible Components
## Playbooks
Playbooks define a set of plays which are executed on different groups of hosts in your organization. They are defined in YAML (plain text) format and they use the Ansible automation language. 

## Plays
You define one or many plays in your playbooks based on the complexity of the solution that you want to achieve. Each play is executed against a target group of systems. For example you may need to setup a software like 'nginx' on your web servers and then you may want to add those servers to your load balancer. So in order to do this setup you will need to create a playbook with two plays - play one is doing the installation on all of the web servers and then play two is adding those servers to your load balancer. 

## Inventory
The inventory defines the hosts and groups of hosts upon which ansible operate. You specify later those hosts or groups in your plays. Ansible supports multiple inventory methods. The most simple method is using a "hosts" file in "ini" format. However, ansible can use different file formats and not only files but it could also use a methods called dynamic inventory. Dynamic inventory can generate information for your infrastructure from different systems like cloud, active directory, database and even you can build a custom dynamic inventory script which is combining information from whatever different sources you have.

## Modules
Ansible Modules help you to install and configure your resources and to keep them in a desired state. Every module has a logic developed to do something with a specific system or component. For example you have modules which install operating system packages, execute APIs calls to external system, set configuration files and much more. There are a lot of built in modules in Ansible that are developed to automate many different tasks with variate of technologies. You can also find a lot of modules provided by vendors or community based modules. All these additional modules extend the Ansible capabilities to manage more technologies.

**Note:** In Ansible 2.10 and later, most modules are hosted in collections. This is a big change how modules were distributed and versioned.
  
* Example of modules
```
template – Template a file out to a remote server
package – Generic OS package manager (supports apt, yum, etc)
docker_container – manage docker containers
win_copy – Copies files to remote locations on windows hosts
win_environment – Modify environment variables on windows hosts
win_feature – Installs and uninstalls Windows Features on Windows Server
panos_loadcfg – load configuration on PAN-OS device
ec2_instance – Create & manage EC2 instances
```

## Tasks
Tasks are used within a play to call specific modules with parameters. They are executed in the defined order in your plays.

* Example of tasks
```
- name: Install nginx
  package:
    name: nginx
    state: present

- name: Install IIS (Web-Server only)
  win_feature:
    name: Web-Server
    state: present

- name: Template a file to /etc/file.conf
  template:
    src: /mytemplates/foo.j2
    dest: /etc/file.conf
    owner: bin
    group: wheel
    mode: '0644'
```

# Execute Ansible

## Ping our hosts 
This is a good example of ad-hoc command. You execute the ping module to all of the web servers defined in your inventory. 
```bash
user@computer$ ansible webservers -m ping
10.20.30.40 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

## Execute our playbook
This is an example of calling your webservers playbook
```bash
user@computer$ ansible-playbook webservers.yml -i hosts --key-file "~/.ssh/ansible-demo.pem"
```