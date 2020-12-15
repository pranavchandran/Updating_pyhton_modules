#to in docker machine
docker-machine ssh manager1
docker-machine ssh worker1
docker-machine ssh worker2

#To show the manager is active or not

#it will not work in workers

docker node ls 

#to add a worker to swarm
#after this command it will prompt the token

docker swarm join-token worker

#after check the node

docker node ls

#this command help to learn more

docker swarm

#docker initializing
docker swarm init --advertise-addr 192.168.99.100 

docker service create --replicas 3 -p 80:80 --name web1 nginx

docker service ls

docker service ps web1

#creating more nodes
docker service scale web1=4

docker node inspect worker1

docker node inspect self

docker service update --image nginx:1.14.0 web1 

#docker set to drain status
docker node update --availability drain worker1 

#remove service
docker service rm servicename

#Mongo database installation
sudo docker run --name mongo -d mongo

#processes that are running in the specified container
docker top mongo

#processes in the system
ps aux

#filter with grep from preocesses
ps aux | grep mongo

#start a mysql container
sudo docker container run -d -p 3306:3306 --name db -e MYSQL_RANDOM_ROOT_PASSWORD=yes mysql

sudo docker container logs --details db 

#start a apache container
sudo docker container run -d --name webserver -p 8084:80 httpd

#start a nginx container
sudo docker container run -d --name proxy -p 82:80 nginx

#old container ls command
sudo docker container ls

#testing apache is working
curl localhost:8084

#container stop command
sudo docker container stop 2a2e 51da 7c59

#Details of container
sudo docker container inspect mysql

#live straming data about containers
sudo docker container stats

#container remove command
sudo docker container rm -f  2a2e7 6ff89 21ce6f

#work inside a container?
sudo docker container run -it --name proxy nginx bash

#exit inside from the shell
exit

#start ubuntu image and work inside init
sudo docker container run -it --name ubuntu ubuntu
apt-get update
apt-get install -y curl

#go inside a existing container and work
sudo docker container start -ai ubuntu

#alpine pulling
sudo docker pull alpine

#docker container sh
docker container run -it alpine sh

sudo docker container exec -it db2 bash

#! very important to find log-password
sudo docker container logs --details db2

#checking the port
docker container port webhost

#finding the ipaddress of docker container
docker container inspect --format '{{ .NetworkSettings.IPAddress}}' webhost

#all the networks would be created
docker network ls

#get containers attached to the network
docker network inspect bridge

#create docker virtual network
docker network create my_app_net

#container to the my_app_net network
docker container run -d --name new_nginx --network my_app_net nginx

#inspecting my_app_net network
docker network inspect my_app_net

docker network connect 688af3f83edd 8412476063be 

docker network disconnect 688af3f83edd 8412476063be 

#To start an existing docker
docker start [containername]

#making and connecting to my network
docker container run -d --name my_nginx --network my_app_net nginx

#to solve the ping error
step -1 sudo service docker restart

Step -2 docker container exec -it mynginx bash

Step-3 apt-get update

Step-4 apt-get install iputils-ping

Step -4 Exit()

Step-5 docker container exec -it mynginx ping newnginx

#docker communicate to same network
docker container exec -it my_nginx ping new_nginx


#Assignment cli-app testing

docker container run --rm -it centos:7 bash
docker container run --rm -it ubuntu:14.04 bash

#DNS Round RobinTest
docker network create dude

docker container run -d --net dude --net-alias search elasticsearch:2

docker container run --rm --net dude alpine nslookup search

docker container run --rm --net dude centos curl -s search:9200

docker container run --rm --net dude centos:7 curl -s search:9200

#docker container remove command
docker container rm -f [name]

#pull a docker image
docker pull nginx

specified version
docker pull nginx:1.11.9

#history looking
docker history nginx:latest

docker image inspect nginx

#download by tag
docker pull nginx:mainline

#docker login command
docker login

#docker push
docker image push bretfish/nginx

#how to push a docker image to your repository
https://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker

#docker image build
docker image build -t customnginx .

#docker container run from dockerfile
docker container run -p 80:80 --rm nginx

docker image build -t nginx-with-html .

docker image tag nginx-with-html:latest bretfisher/nginx-with-html:latest

#Assignment build your own image and push it to dockerhub

#Testing the build node
docker build -t testnode .

docker container run --rm -p 82:3000 testcase

docker build -t pranavchandran/redisimage .

#docker container mysql running command
docker container run -d --name -e MYSQL_ALLOW_EMPTY_PASSWORD=True mysql

docker volume ls

docker container stop mysql

docker container stop mysql2

#remove containers in one command

docker container rm mysql mysql2

#creating volume and identify 

docker container run -d --name mysql2 -e MYSQL_ALLOW_EMPTY_PASSWORD=True -v mysql-db:/var/lib/mysql mysql

#After docker volume ls u can see the volume
docker volume ls

docker volume inspect mysql-db

#check the volume where is (in mount)
docker container inspect mysql3

#run time moving command
docker container run -d --name nginx -p 84:80 -v $(pwd):/usr/share/nginx/html nginx



