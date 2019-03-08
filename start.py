#!/usr/bin/python3

import os,sys


forceFlag = 0

if len(sys.argv) == 2:
    if sys.argv[1] == "-f":
        forceFlag = 1

print(forceFlag)

def getEchoValue(cmd):
    "获取命令的返回值，可能为空"
    val = os.popen(cmd).readlines()
    if len(val) == 0:
        return ""
    else:
        return val[0]


def execCmd(cmd):
    "执行命令"
    os.system(cmd)


'''
    if 镜像存在：
        if 容器存在
            关闭容器
            删除容器
        删除镜像
    生成镜像
    运行容器
'''
def forceStartContainer(*args):
    if args[0] != "":
        if args[1] != "":
            execCmd(args[2])
            execCmd(args[3])
        execCmd(args[4])
    execCmd(args[5])
    execCmd(args[6])



'''
    if 容器存在：
        关闭容器
        启动容器
    else 容器不存在：
        if 镜像不存在：
            下载镜像
        运行容器
    
'''
def startContainer(*args):
    if args[0] != "":
        execCmd(args[1])
        execCmd(args[2])
    else:
        if args[3] == "":
            execCmd(args[4])
        execCmd(args[5])





# ntpdate cn.pool.ntp.org    同步时间

# 启动nms_server容器
nms_server_image_exists = "docker images | grep nms_server"
nms_server_container_exists="docker ps -a | grep nms_server"
nms_server_stop_container="docker stop nms_server"
nms_server_start_container="docker start nms_server"
nms_server_remove_container="docker rm nms_server"
nms_server_remove_image="docker rmi nms_server:v1"
nms_server_add_image="docker build -t nms_server:v1 ./nms-server"
nms_server_add_container="docker run --name nms_server -d -p 8888:8888 nms_server:v1"
nms_server_image_exists_value = getEchoValue(nms_server_image_exists)
nms_server_container_exists_value = getEchoValue(nms_server_container_exists)
if forceFlag == 1:
    forceStartContainer(nms_server_image_exists_value,nms_server_container_exists_value,nms_server_stop_container,nms_server_remove_container,nms_server_remove_image,nms_server_add_image,nms_server_add_container)
else:
    startContainer(nms_server_container_exists_value,nms_server_stop_container,nms_server_start_container,nms_server_image_exists_value,nms_server_add_image,nms_server_add_container)


# 启动Mysql数据库

mysql_image_exist = "docker images | grep nms_mysql"
mysql_container_exist = "docker ps -a | grep nms_mysql"
mysql_stop_container = "docker stop nms_mysql"
mysql_start_container = "docker start nms_mysql"
mysql_remove_container = "docker rm nms_mysql"
mysql_add_image = "docker build -t nms_mysql:v1 ./mysql56"
mysql_add_container = "docker run --name nms_mysql -v /mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d nms_mysql:v1"
mysql_image_exist_value = getEchoValue(mysql_image_exist)
mysql_container_exist_value = getEchoValue(mysql_container_exist)
startContainer(mysql_container_exist_value,mysql_stop_container,mysql_start_container,mysql_image_exist_value,mysql_add_image,mysql_add_container)


# 获取mysql数据库地址和nms_server地址
mysql_IPAddress_value = ""
nms_server_IPAddress_value=""


mysql_IPAddress= getEchoValue("docker inspect nms_mysql | grep -w \"IPAddress\"")
mysql_IPAddress_value = mysql_IPAddress[ mysql_IPAddress.index(':') + 3:mysql_IPAddress.index(",") -1]

nms_server_IPAddress=getEchoValue("docker inspect nms_server | grep -w \"IPAddress\"")
nms_server_IPAddress_value = nms_server_IPAddress[nms_server_IPAddress.index(':')+3:nms_server_IPAddress.index(",") -1]


# 启动nms-gateway容器
nms_gateway_image_exist = "docker images | grep nms_gateway"
nms_gateway_container_exist = "docker ps -a | grep nms_gateway"
nms_gateway_image_exist_value = getEchoValue(nms_gateway_image_exist)
nms_gateway_container_exist_value = getEchoValue(nms_gateway_container_exist)
nms_gateway_stop_container="docker stop nms_gateway"
nms_gateway_start_container = "docker start nms_gateway"
nms_gateway_remove_container = "docker rm nms_gateway"
nms_gateway_remove_image = "docker rmi nms_gateway:v1"
nms_gateway_add_image = "docker build -t nms_gateway:v1 ./nms-api-gateway"
nms_gateway_add_container = "docker run --name nms_gateway  -p 9999:9999 -d nms_gateway:v1 --spring.datasource.url=jdbc:mysql://"+mysql_IPAddress_value+"/test --spring.cloud.client.ipAddress="+nms_server_IPAddress_value

if forceFlag == 1:
    forceStartContainer(nms_gateway_image_exist_value,nms_gateway_container_exist_value,nms_gateway_stop_container,nms_gateway_remove_container,nms_gateway_remove_image,nms_gateway_add_image,nms_gateway_add_container)
else:
    startContainer(nms_gateway_container_exist_value,nms_gateway_stop_container,nms_gateway_start_container,nms_gateway_image_exist_value,nms_gateway_add_image,nms_gateway_add_container)



#启动adaptor_middle_tie
nms_adaptor_image_exist = "docker images | grep nms_adaptor"
nms_adaptor_container_exist = "docker ps -a | grep nms_adaptor"
nms_adaptor_image_exist_value = getEchoValue(nms_adaptor_image_exist)
nms_adaptor_container_exist_value = getEchoValue(nms_adaptor_container_exist)
nms_adaptor_stop_container = "docker stop nms_adaptor"
nms_adaptor_start_container = "docker start nms_adaptor"
nms_adaptor_remove_container = "docker rm nms_adaptor"
nms_adaptor_remove_image = "docker rmi nms_adaptor:v1"
nms_adaptor_add_image = "docker build -t nms_adaptor:v1 ./adaptor-mts"
nms_adaptor_add_container = "docker run --name nms_adaptor  -p 6666:6666 -d nms_adaptor:v1 --spring.datasource.url=jdbc:mysql://"+mysql_IPAddress_value+"/test --spring.cloud.client.ipAddress="+nms_server_IPAddress_value

if forceFlag == 1:
    forceStartContainer(nms_adaptor_image_exist_value,nms_adaptor_container_exist_value,nms_adaptor_stop_container,nms_adaptor_remove_container,nms_adaptor_remove_image,nms_adaptor_add_image,nms_adaptor_add_container)
else:
    startContainer(nms_adaptor_container_exist_value,nms_adaptor_stop_container,nms_adaptor_start_container,nms_adaptor_image_exist_value,nms_adaptor_add_image,nms_adaptor_add_container)



#启动nms_mts
nms_mts_image_exist = "docker images | grep nms_mts"
nms_mts_container_exist = "docker ps -a | grep nms_mts"
nms_mts_image_exist_value = getEchoValue(nms_mts_image_exist)
nms_mts_container_exist_value = getEchoValue(nms_mts_container_exist)
nms_mts_stop_container = "docker stop nms_mts"
nms_mts_start_container = "docker start nms_mts"
nms_mts_remove_container = "docker rm nms_mts"
nms_mts_remove_image = "docker rmi nms_mts:v1"
nms_mts_add_image = "docker build -t nms_mts:v1 ./nms-mts"
nms_mts_add_container = "docker run --name nms_mts -p 7777:7777  -d nms_mts:v1 --spring.datasource.url=jdbc:mysql://"+mysql_IPAddress_value+"/test --spring.cloud.client.ipAddress="+nms_server_IPAddress_value

if forceFlag == 1:
    forceStartContainer(nms_mts_image_exist_value,nms_mts_container_exist_value,nms_mts_stop_container,nms_mts_remove_container,nms_mts_remove_image,nms_mts_add_image,nms_mts_add_container)
else:
    startContainer(nms_mts_container_exist_value,nms_mts_stop_container,nms_mts_start_container,nms_mts_image_exist_value,nms_mts_add_image,nms_mts_add_container)





'''
mysql_image_exist = "docker images | grep docker.io/mysql"
mysql_container_exist = "docker ps -a | grep mysql56"
mysql_stop_container = "docker stop mysql56"
mysql_start_container = "docker start mysql56"
mysql_remove_container = "docker rm mysql56"
mysql_add_image = "docker pull mysql:5.6"
mysql_add_container = "docker run --name mysql56 -v /mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d docker.io/mysql:5.6"
mysql_image_exist_value = getEchoValue(mysql_image_exist)
mysql_container_exist_value = getEchoValue(mysql_container_exist)
startContainer(mysql_container_exist_value,mysql_stop_container,mysql_start_container,mysql_image_exist_value,mysql_add_image,mysql_add_container)
'''