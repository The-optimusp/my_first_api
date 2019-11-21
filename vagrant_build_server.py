# upload new centos7 on VirtualBox with Vagrant

import os
from time import sleep

## Start creating vagrant env for centos 7 vm
def create_vagrant_project(vagrant_dir):
    print('create_vagrant_project')
    # vagrant_home_dir = vagrant_dir
    if not os.path.exists(vagrant_dir):
        os.mkdir(vagrant_dir)
    os.chdir(vagrant_dir)
    print('perform vagrant init cmd')
    vagrant_init_cmd = '/usr/local/bin/vagrant init centos/7 > /dev/null'
    os.system(vagrant_init_cmd)

## Edit vagrantfile for rest_api centos7 vm
def edit_vagrant_file(vagrant_dir, vagrantfile):
    print('edit_vagrant_file')
    os.chdir(vagrant_dir)
    line_to_check = '  # config.vm.provider "virtualbox" do |vb|'
    line_to_check2 = '  config.vm.box = "centos/7"'
    lines_to_add = '\n\n\tconfig.vm.provider "virtualbox" do |vb|\n\t\tvb.name = "docker"\n\t\tvb.memory = 2048\n\t\tvb.cpus = 2\n\tend'
    lines_to_add2 = '\n  config.vm.provision :shell, path: "bootstrap.sh"\n'
    with open(vagrantfile, 'r+') as vagrantfile_edit:
        lines = vagrantfile_edit.readlines()
        vagrantfile_edit.seek(0)
        vagrantfile_edit.truncate()
        for line in lines:
            if line.startswith(line_to_check):
                line = line.rstrip("\n") + lines_to_add + '\n'
            if line.startswith(line_to_check2):
                line = line.rstrip("\n") + lines_to_add2 + '\n'
            vagrantfile_edit.write(line)
    sleep(5)

# create bootstrap file to install Docker and update system
def create_bootstrap_file(vagrant_dir, boot_file):
    print('create_bootstrap_file')
    os.chdir(vagrant_dir)
    with open(boot_file, 'w+') as bootstrap_edit:
        bootstrap_edit.write('#!/bin/bash\n')
        bootstrap_edit.write('\nyum install -y yum-utils device-mapper-persistent-data lvm2\n')
        bootstrap_edit.write('\nyum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo\n')
        bootstrap_edit.write('\nyum install -y docker-ce docker-ce-cli containerd.io\n')
        bootstrap_edit.write('\nsystemctl start docker\n')
        bootstrap_edit.write('\nsystemctl enable docker\n')
        bootstrap_edit.write('\ngroupadd docker\n')
        bootstrap_edit.write('\nusermod -aG docker vagrant\n')
        bootstrap_edit.write('\nhostnamectl --transient --pretty --static set-hostname docker\n')
        bootstrap_edit.write('\nyum update -y\n')

def import_centos7_vm():
    print('import_centos7_vm')
    vagrant_import_cmd = 'echo "3" | /usr/local/bin/vagrant box add centos/7'
    os.system(vagrant_import_cmd)
    sleep(10)
    vagrant_up = '/usr/local/bin/vagrant up'
    os.system(vagrant_up)


def main():
    print('main')
    rest_api_vm_dir = '/Users/orenlalush/vagrant_rest_api_vm'
    rest_api_vagrantfile = '/Users/orenlalush/vagrant_rest_api_vm/Vagrantfile'
    bootstrap_file = '/Users/orenlalush/vagrant_rest_api_vm/bootstrap.sh'
    create_vagrant_project(rest_api_vm_dir)
    edit_vagrant_file(rest_api_vm_dir, rest_api_vagrantfile)
    create_bootstrap_file(rest_api_vm_dir, bootstrap_file)
    import_centos7_vm()

if __name__ == '__main__':
    main()