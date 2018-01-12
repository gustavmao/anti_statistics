#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 17:23
# @Author  : Gustav
# @File    : nginx.py

import gzip
import re
import datetime
import time
import subprocess
import gVariable_nginx

def getDate():
    today = datetime.date.today()
    today = str(today).replace('-','')
    return today

def getFileName():
    a1 = getDate()
    cmd = "ls " + gVariable_nginx.nginxLogPath + " |grep " + a1 + " |grep access.log"
    a2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    a3 = a2.communicate()
    # print a3
    a4 = a3[0].strip().split("\n")
    a5 = []
    for i in a4:
        a5.append(gVariable_nginx.nginxLogPath + i)
    return a5

def logParse(fileName):
    fileHandle = gzip.open(fileName, 'rb')
    for i in fileHandle:
        myTime = int(i.split(' +0800]')[0][-8:-6])
        ip = i.split()[0]
        uri = i.split()[6]
        try:
            # all access
            gVariable_nginx.nginxHourAccess[myTime] += 1
            gVariable_nginx.nginxAccess += 1

            if ip in gVariable_nginx.nginxIpAccess:
                gVariable_nginx.nginxIpAccess[ip] += 1
            else:
                gVariable_nginx.nginxIpAccess[ip] = 1

            if uri in gVariable_nginx.nginxUri:
                gVariable_nginx.nginxUri[uri] += 1
            else:
                gVariable_nginx.nginxUri[uri] = 1

            if re.search('png$|css$|js$|gif$|jpg$|map$|ico$|flv$|swf$|mp3$|tff$|woff$|woff2$', uri):
                gVariable_nginx.nginxStaticAccess += 1
            else:
                gVariable_nginx.nginxHourDynamic[myTime] += 1
                gVariable_nginx.nginxDynamicAccess += 1

            if "upstream[-]" in i:
                gVariable_nginx.nginxHourReject[myTime] += 1
                gVariable_nginx.nginxRejectAccess += 1
                if ip in gVariable_nginx.nginxIpReject:
                    gVariable_nginx.nginxIpReject[ip] += 1
                else:
                    gVariable_nginx.nginxIpReject[ip] = 1

            if "upstream[403]" in i:
                gVariable_nginx.nginxHourReject[myTime] += 1
                gVariable_nginx.nginxRejectAccess += 1
                gVariable_nginx.nginxBlackAccess += 1
                if ip in gVariable_nginx.nginxIpReject:
                    gVariable_nginx.nginxIpReject[ip] += 1
                else:
                    gVariable_nginx.nginxIpReject[ip] = 1

        except Exception:
            pass

def run():
    logFiles = getFileName()
    for i in logFiles:
        print i
        logParse(i)
        t = time.localtime()
        print "%d:%d:%d" % (t.tm_hour, t.tm_min, t.tm_sec)

    gVariable_nginx.nginxRejectRatio = (float(gVariable_nginx.nginxRejectAccess) / float(gVariable_nginx.nginxDynamicAccess)) * 100
    gVariable_nginx.nginxIpTotal = len(gVariable_nginx.nginxIpAccess)

    print "\n********************************************************************"
    print "total:%-10d  static:%-10d  dynamic:%-10d  reject:%d" % \
          (gVariable_nginx.nginxAccess, gVariable_nginx.nginxStaticAccess, 
           gVariable_nginx.nginxDynamicAccess, gVariable_nginx.nginxRejectAccess)

    print "blacklist:%-10d  iptotal:%-10d  rejectratio:%.2f%%" % \
          (gVariable_nginx.nginxBlackAccess, gVariable_nginx.nginxIpTotal, gVariable_nginx.nginxRejectRatio)

    print "**************************************************************************"
    print "Hour total access, hour total dynamic and hour total reject"
    print gVariable_nginx.nginxHourAccess
    print gVariable_nginx.nginxHourDynamic
    print gVariable_nginx.nginxHourReject
    print "**************************************************************************"

    a1 = sorted(gVariable_nginx.nginxIpAccess.iteritems(), key=lambda x: x[1], reverse=True)
    if len(gVariable_nginx.nginxIpAccess) > 300:
        k1 = 300
    else:
        k1= len(gVariable_nginx.nginxIpAccess)
    for i in range(k1):
        try:
            print "ip:%-19s access:%-10s hit:%-10s" % (a1[i][0], a1[i][1], gVariable_nginx.nginxIpReject[a1[i][0]])
        except KeyError:
            print "ip:%-19s access:%-10s **********" % (a1[i][0], a1[i][1])
            pass
    print "**************************************************************************"

    a3 = sorted(gVariable_nginx.nginxUri.iteritems(), key=lambda x: x[1], reverse=True)
    for i in range(len(a3)):
        if a3[i][1] >= 10:
            print a3[i][0], a3[i][1]
    print "**************************************************************************"

if __name__ == "__main__":
    t = time.localtime()
    print "%d:%d:%d" % (t.tm_hour, t.tm_min, t.tm_sec)
    run()
    t = time.localtime()
    print "%d:%d:%d" % (t.tm_hour, t.tm_min, t.tm_sec)
