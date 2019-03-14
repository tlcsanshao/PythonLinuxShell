import os,shutil


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




def doReinitialize():
    execCmd("docker stop nms_server")
    execCmd("docker stop nms_gateway")
    execCmd("docker stop nms_mts")
    execCmd("docker stop nms_adaptor")
    execCmd("docker stop nms_mysql")
    execCmd("docker rm nms_server")
    execCmd("docker rm nms_gateway")
    execCmd("docker rm nms_mts")
    execCmd("docker rm nms_adaptor")
    execCmd("docker rm nms_mysql")
    execCmd("docker rmi nms_server:v1")
    execCmd("docker rmi nms_gateway:v1")
    execCmd("docker rmi nms_mts:v1")
    execCmd("docker rmi nms_adaptor:v1")
    execCmd("docker rmi nms_mysql:v1")
    shutil.rmtree("/Framework",True)
    shutil.rmtree("/mysqldata",True)


if __name__ == '__main__':
    doReinitialize()


