# OpenTofu or Terraform 
## Install tenv tool 
tenv is used to manage which version of OpenTofu is installed and active in the environment. tenv makes it easy to install, switch between, and manage multiple versions of the tofu CLI, similar to how other version managers work.
```bash
# Prereqs
sudo apt update -y
sudo apt install -y jq gnupg
LATEST_VERSION=$(curl --silent https://api.github.com/repos/tofuutils/tenv/releases/latest | jq -r .tag_name)
curl -O -L "https://github.com/tofuutils/tenv/releases/latest/download/tenv_${LATEST_VERSION}_amd64.deb"
sudo dpkg -i "tenv_${LATEST_VERSION}_amd64.deb"
```
## Install OpenTofu with tofuenv
```bash
tenv tofu install 1.10.6   
```
## Validate tofu is installed
```bash
tofu -v 
```

## Run 01_terraform_ec2
```bash
# Enter 01_terraform_ec2
cd 01_terraform_ec2
# Review ec2.tf file
cat ec2.tf
# Run tofu init
tofu init
# Run tofu apply
tofu apply
# Review the plan and approval
## yes
```
After the the apply you should see something like this:
```
webservers = [
  "ec2-3-133-153-44.us-east-2.compute.amazonaws.com",
  "ec2-3-133-142-155.us-east-2.compute.amazonaws.com",
  "ec2-52-14-224-63.us-east-2.compute.amazonaws.com",
]
```
Keep the list of the servers. We will use it later.

```bash
# Go back to parent dir
cd ..
```

# Ansible
## Install ansible
* Create python venv
```bash
python -m venv venv
```

* Activate venv
```bash
source venv/bin/activate
```

* Install ansible and molecule
```bash
pip3 install -r requirements.txt
```

## Run 02_ansible_simple_playbook
* Enter directory
```bash
cd 02_ansible_simple_playbook
```

* Update hosts file with the servers from terraform
```
editor hosts
```

* Test connection using ping module
```bash
export ANSIBLE_HOST_KEY_CHECKING=False
ansible webservers -m ping -i hosts -u ubuntu --private-key=$HOME/.ssh/id_rsa_tofu
```
 
* Apply playbook 
``` bash
ansible-playbook webservers.yml -i hosts --key-file ~/.ssh/id_rsa_tofu
```

* Enter parent directory
```bash
cd ..
```



## Run 03_ansible_simple_playbook
* Enter directory
```bash
cd 03_ansible_simple_role
```

* Update hosts file with the servers from terraform
```
editor hosts
```

* Apply playbook 
``` bash
ansible-playbook webservers.yml -i hosts --key-file ~/.ssh/id_rsa_tofu
```

* Enter parent directory
```bash
cd ..
```

## Run 04_ansible_basic_constructs
* Enter directory
```bash
cd 04_ansible_basic_constructs
```

* Update hosts file with the servers from terraform
```
editor hosts
```

* Run playbook
```bash
ansible-playbook 1_create_users.yml -i inventory --key-file ~/.ssh/id_rsa_tofu
ansible-playbook 2_create_users_with_loop.yml -i inventory --key-file ~/.ssh/id_rsa_tofu
ansible-playbook 3_condition_on_command.yml -i inventory --key-file ~/.ssh/id_rsa_tofu
ansible-playbook 4_condition_on_facts.yml -i inventory --key-file ~/.ssh/id_rsa_tofu
ansible-playbook 5_blocks.yml -i inventory --key-file ~/.ssh/id_rsa_tofu
ansible-playbook 6_debug.yml -i inventory --key-file ~/.ssh/id_rsa_tofu
```

* Enter parent directory
```bash
cd ..
```


## Run 05_ansible_dynamic_inventory
* Enter directory
```bash
cd 05_ansible_dynamic_inventory
```

```bash
ansible-playbook web_servers.yml -i dynamic_inventory/ --key-file ~/.ssh/id_rsa_tofu
```

* Enter parent directory
```bash
cd ..
```

## Run 06_ansible_molecule
This example uses molecule to create local environment in docker and converge it
* Enter directory
```bash
cd 06_ansible_molecule
```

* Execute molecule converge
```bash
molecule converge
```


* Login to one of the containers
```bash
molecule login --host web01 
```

* Destroy the molecule environment
```bash
molecule destroy
```


* Enter parent directory
```bash
cd ..
```

# Run 01_terraform_ec2 destroy
```bash
# Enter 01_terraform_ec2
cd 01_terraform_ec2
# Run tofu destroy
tofu destroy
## yes
```

