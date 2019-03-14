#!/usr/bin/python3

import shutil,os,sys

version = "0.0.1"

nms9000_dir="../nms9000"
nms_api_gateway_dir=nms9000_dir+"/nms-api-gateway"
adaptor_mts_dir=nms9000_dir+"/adaptor-mts"
nms_mts_dir=nms9000_dir+"/nms-mts"
nms_server_dir=nms9000_dir+"/nms-server"
mysql_dir=nms9000_dir+"/mysql56"
init_sql = "create_database.sql"


def init_nmsserver():
    shutil.copy("nms-server-"+version+".jar",nms_server_dir)
    f=open(nms_server_dir+"/Dockerfile","w+")
    f.writelines("FROM openjdk:8-jdk-alpine\n")
    f.writelines("ADD nms-server-"+version+".jar server.jar\n")
    f.writelines('ENTRYPOINT ["java","-jar","server.jar"]')
    f.writelines("\n")
    f.close()


def init_mysql():
    f=open(mysql_dir+"/"+init_sql,"w+")
    f.writelines("create database test\n")
    f.close()

    f=open(mysql_dir+"/Dockerfile","w+")
    f.writelines("FROM mysql:5.6\n")
    f.writelines("ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d\n")
    f.writelines("ENV INSTALL_DB_SQL "+init_sql+"\n")
    f.writelines('COPY ./$INSTALL_DB_SQL $AUTO_RUN_DIR'+"\n")
    f.writelines('RUN chmod a+x $AUTO_RUN_DIR/$INSTALL_DB_SQL'+"\n")
    f.close()





def init_gateway():
    shutil.copy("nms-api-gateway-"+version+".jar",nms_api_gateway_dir)
    f=open(nms_api_gateway_dir+"/Dockerfile","w+")
    f.writelines("FROM openjdk:8-jdk-alpine\n")
    f.writelines("ADD nms-api-gateway-"+version+".jar gateway.jar\n")
    f.writelines('ENTRYPOINT ["java","-jar","gateway.jar"]')
    f.writelines("\n")
    f.close()




def init_adaptor():
    shutil.copy("adaptor-middle-tie-service-"+version+".jar",adaptor_mts_dir)
    f=open(adaptor_mts_dir+"/Dockerfile","w+")
    f.writelines("FROM openjdk:8-jdk-alpine\n")
    f.writelines("ADD adaptor-middle-tie-service-"+version+".jar adaptor.jar\n")
    f.writelines('ENTRYPOINT ["java","-jar","adaptor.jar"]')
    f.writelines("\n")
    f.close()


def init_mts():
    shutil.copy("nms-middle-tie-service-"+version+".jar",nms_mts_dir)
    f=open(nms_mts_dir+"/Dockerfile","w+")
    f.writelines("FROM openjdk:8-jdk-alpine\n")
    f.writelines("ADD nms-middle-tie-service-"+version+".jar middletie.jar\n")
    f.writelines('ENTRYPOINT ["java","-jar","middletie.jar"]')
    f.writelines("\n")
    f.close()




def initdemo():
    if len(sys.argv) == 2:
        version = sys.argv[1]

    '''step1: delete nms9000 dir'''
    shutil.rmtree(nms9000_dir,True)
    '''step2: create nms9000 dirs'''
    os.makedirs(nms_api_gateway_dir)
    os.makedirs(adaptor_mts_dir)
    os.makedirs(nms_mts_dir)
    os.makedirs(nms_server_dir)
    os.makedirs(mysql_dir)
    '''step3:format nms9000 dir'''
    init_nmsserver()
    init_mysql()
    init_gateway()
    init_adaptor()
    init_mts()
    '''step4:Copy start.py stop.py'''
    shutil.copy("start.py",nms9000_dir)
    shutil.copy("stop.py",nms9000_dir)
    shutil.copy("reinitialize.py",nms9000_dir)



if __name__ == '__main__':
    initdemo()