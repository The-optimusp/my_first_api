#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

docker version || { 
	apt-get -y install apt-transport-https ca-certificates software-properties-common curl
	wget https://download.docker.com/linux/debian/gpg 
	apt-key add gpg
	unlink gpg
	add-apt-repository "deb https://download.docker.com/linux/debian stretch stable"
	apt-get -y update
	apt-get -y install docker-ce
	usermod -aG docker vagrant

	systemctl start docker
	systemctl enable docker

	docker version
}

cd /vagrant
docker pull python:3-stretch 2>&1
docker build -t my_first_app . 
docker run -i --rm my_first_app python3 app.py
