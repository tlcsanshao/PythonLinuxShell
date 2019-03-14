#!/usr/bin/python3

import os,sys

def execCmd(cmd):
    "执行命令"
    os.system(cmd)

execCmd("docker stop nms_server")
execCmd("docker stop nms_gateway")
execCmd("docker stop nms_adaptor")
execCmd("docker stop nms_mts")
execCmd("docker stop nms_mysql")

