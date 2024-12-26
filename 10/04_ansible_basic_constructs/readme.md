# LAB04
In this lab you are going to understand how to use some basic constructs in Ansible

# Before you start
* You need to login to AWS either with a tool like aws-adfs or with IAM user credentials. You can find the ansible workstation setup guide [here](../../WORKSTATION.md)
* You will need to execute molecule create. Molecule will create two machines for you, so you can experiment on them.

```bash
user@computer$ molecule create
```

# Run the different playbooks
We have six playbooks which are showing some basic constructs in Ansible.
```
1_create_users.yml - Creating users. There is nothing special with this playbook, it just executes tasks
2_create_users_with_loop.yml - Creating users using the loop construct. This is the natural evolution of the first playbook. We are optimizing our code so we don't repeat our code.
3_condition_on_command.yml - Sometimes you may need to do something with Ansible based on a condition. This is a simple example of running task based on a command output.
4_condition_on_facts.yml - Simple example of condition based on facts. Ansible can collect some facts for the remote system and you can use those facts to have conditional logic in your playbooks.
5_blocks.yml - Blocks are just groups of tasks. Sometimes you need to do conditional execution of multiple tasks and that's the right moment ot use the blocks construct.
6_debug.yml - Debugging your playbook is a very import skill which can save you a lot of time struggling to find why and what is happening with your code.
```
## Run the ansible-playbook 
```bash
user@computer$ ansible-playbook <playbook_name> -i inventory/
```
**Note:** When we called the *molecule create* command, it generated a static inventory file (inventory/hosts.yml) for us. For this reason we are passing *-i inventory/* as parameter. Ansible will use the inventory fail and group variables from this directory.

# Clean up
Do not forget to clean your servers!
```bash
user@computer$ molecule destroy
```