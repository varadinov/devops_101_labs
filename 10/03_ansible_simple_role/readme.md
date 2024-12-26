# LAB02
In this lab you are going to refactor the playbook from LAB01 to use role.

# Before you start
* You can reuse the machine from LAB01

# Roles
Roles are key concept for code reusability in Ansible. The Ansible community recommend to keep your playbooks clean as much as possible and use only roles in your plays.

## Refactoring playbooks to use roles
It is a common practice to develop quick and dirty a cookbook to proof a concept of something. However, when you are ready with it, you have to refactor it to use roles. This way you can organize your code and resources in well structured project. Roles define a directory structure which you must follow and move all your peaces from the playbook to the correct directories.

## Role directory structure
```
tasks - contains the tasks that the role executes
handlers - contains the role handlers - special kind of tasks which are executed only on notify from another task.
defaults - default variables for the role. Defaults can be overridden by external variables
vars - local role variables. Cannot be overridden by external variables
files - any static files that role can use in the tasks
templates - any templates that the role use to generate dynamically files
meta - Role metadata information like, owner, role dependencies and etc.
```

## main.yml
By default Ansible looks in each directory within a role for a main.yml file for relevant content. You can add other YAML files in some directories. For example, you can place platform-specific tasks in separate files and refer to them in the tasks/main.yml file:

```yaml
- name: Install the correct web server for RHEL
  import_tasks: redhat.yml
  when: ansible_facts['os_family']|lower == 'redhat'

- name: Install the correct web server for Debian
  import_tasks: debian.yml
  when: ansible_facts['os_family']|lower == 'debian'
```