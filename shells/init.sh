#!/bin/sh

nms9000_dir=../nms9000
rm $nms9000_dir -rf


nms_api_gateway_dir=$nms9000_dir/nms-api-gateway
adaptor_mts_dir=$nms9000_dir/adaptor-mts
nms_mts_dir=$nms9000_dir/nms-mts
nms_server_dir=$nms9000_dir/nms-server
mysql_dir=$nms9000_dir/mysql56
#framework_dir=$nms9000_dir/Framework
#log_dir=$framework_dir/logs

mkdir -p $nms_api_gateway_dir
mkdir -p $adaptor_mts_dir
mkdir -p $nms_mts_dir
mkdir -p $nms_server_dir
mkdir -p $mysql_dir
#mkdir -p $framework_dir
#mkdir -p $log_dir



cp nms-server-$1.jar $nms_server_dir
echo "FROM openjdk:8-jdk-alpine" > $nms_server_dir/Dockerfile
echo "ADD nms-server-$1.jar server.jar" >> $nms_server_dir/Dockerfile
echo 'ENTRYPOINT ["java","-jar","server.jar"]' >> $nms_server_dir/Dockerfile


echo "create database test" > $mysql_dir/create_database.sql

echo "FROM mysql:5.6" > $mysql_dir/Dockerfile
echo "ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d" >> $mysql_dir/Dockerfile
echo "ENV INSTALL_DB_SQL create_database.sql" >> $mysql_dir/Dockerfile
echo "COPY ./\$INSTALL_DB_SQL \$AUTO_RUN_DIR/" >> $mysql_dir/Dockerfile
echo "RUN chmod a+x \$AUTO_RUN_DIR/\$INSTALL_DB_SQL" >> $mysql_dir/Dockerfile




cp nms-api-gateway-$1.jar $nms_api_gateway_dir
echo "FROM openjdk:8-jdk-alpine" > $nms_api_gateway_dir/Dockerfile
echo "ADD nms-api-gateway-$1.jar gateway.jar" >> $nms_api_gateway_dir/Dockerfile
echo 'ENTRYPOINT ["java","-jar","gateway.jar"]' >> $nms_api_gateway_dir/Dockerfile




cp adaptor-middle-tie-service-$1.jar $adaptor_mts_dir
echo "FROM openjdk:8-jdk-alpine" > $adaptor_mts_dir/Dockerfile
echo "ADD adaptor-middle-tie-service-$1.jar adaptor.jar" >> $adaptor_mts_dir/Dockerfile
echo 'ENTRYPOINT ["java","-jar","adaptor.jar"]' >> $adaptor_mts_dir/Dockerfile



cp nms-middle-tie-service-$1.jar $nms_mts_dir
echo "FROM openjdk:8-jdk-alpine" > $nms_mts_dir/Dockerfile
echo "ADD nms-middle-tie-service-$1.jar middletie.jar" >> $nms_mts_dir/Dockerfile
echo 'ENTRYPOINT ["java","-jar","middletie.jar"]' >> $nms_mts_dir/Dockerfile

cp start.py $nms9000_dir
cp stop.py  $nms9000_dir