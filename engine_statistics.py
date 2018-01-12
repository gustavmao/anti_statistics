#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/17 17:23
# @Author  : Gustav
# @File    : engineCount.py

import gzip
import re
import datetime
import time
import subprocess
import gVariable

def getDate():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

def getFileName():
    a1 = str(getDate())
    cmd = "ls " + gVariable.engineLogPath + " |grep " + a1
    a2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    a3 = a2.communicate()
    # print a3
    a4 = a3[0].strip().split("\n")
    a5 = []
    for i in a4:
        a5.append(gVariable.engineLogPath + i)
    return a5

def logParse(fileName):
    fileHandle = gzip.open(fileName, 'rb')
    for i in fileHandle:
        myTime = int(i[:2])
        try:
            # all access
            if re.search("ScheduledAgent\s-\s\d+\sobjs\sload", i):
                a1 = int(re.search("ScheduledAgent\s-\s(\d+)\sobjs\sload", i).group(1))
                gVariable.engineHourAccess[myTime] += a1
                gVariable.engineTotalAccess += a1

            # dynamic access
            if "cn.com.bsfit.frms.obj.AuditObject" in i:
                gVariable.engineHourDynamic[myTime] += 1
                gVariable.engineDynamicAccess += 1
                m5 = re.search(",\suri=(.*),\sip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}),", i)
                try:
                    m2 = m5.group(2)
                    m3 = m5.group(1)

                    if m2 in gVariable.engineIpAccess:
                        gVariable.engineIpAccess[m2] += 1
                    else:
                        gVariable.engineIpAccess[m2] = 1

                    if m3 in gVariable.engineUri:
                        gVariable.engineUri[m3] += 1
                    else:
                        gVariable.engineUri[m3] = 1
                except AttributeError:
                    pass
                try:
                    m6 = re.search("dfp=(.*), url=", i).group(1)
                    if m6 in gVariable.engineDfpAccess:
                        gVariable.engineDfpAccess[m6] += 1
                    else:
                        gVariable.engineDfpAccess[m6] = 1
                except AttributeError:
                    pass
        except Exception:
            pass

        # reject access
        if "AsPublishHandlerImpl" in i:
            m4 = i.split("客户端IP:")[1].strip()
            gVariable.engineHourReject[myTime] += 1
            gVariable.engineRejectAccess += 1
            m1 = re.search("触发的规则:(.*),规则分值", i).group(1).split("|")
            for j in m1:
                if j in gVariable.engineRule:
                    gVariable.engineRule[j] += 1
                else:
                    gVariable.engineRule[j] = 1

            if "IP在黑名单中" in i:
                gVariable.engineHourDynamic[myTime] += 1
                gVariable.engineDynamicAccess += 1
                gVariable.engineBlackAccess += 1

            if m4 in gVariable.engineIpReject:
                gVariable.engineIpReject[m4] += 1
                gVariable.engineIpAccess[m4] += 1
            else:
                gVariable.engineIpReject[m4] = 1
                gVariable.engineIpAccess[m4] = 1

            try:
                m7 = re.search("指纹:(.*),统计", i).group(1)
                if m7 in gVariable.engineDfpReject:
                    gVariable.engineDfpReject[m7] += 1
                else:
                    gVariable.engineDfpReject[m7] = 1
            except AttributeError:
                pass

def run():
    logFiles = getFileName()
    for i in logFiles:
        print i
        logParse(i)
        t = time.localtime()
        print "%d:%d:%d" % (t.tm_hour, t.tm_min, t.tm_sec)

    gVariable.engineStaticAccess = gVariable.engineTotalAccess - gVariable.engineDynamicAccess
    gVariable.engineRejectRatio = (float(gVariable.engineRejectAccess) / float(gVariable.engineDynamicAccess)) * 100
    gVariable.engineIpTotal = len(gVariable.engineIpAccess)
    gVariable.engineDfpTotal = len(gVariable.engineDfpAccess)

    print "\n********************************************************************"
    print "total:%-10d  static:%-10d  dynamic:%-10d  reject:%d" % \
          (gVariable.engineTotalAccess, gVariable.engineStaticAccess, gVariable.engineDynamicAccess, gVariable.engineRejectAccess)

    print "blacklist:%-10d  iptotal:%-10d  rejectratio:%.2f%%" % \
          (gVariable.engineBlackAccess, gVariable.engineIpTotal, gVariable.engineRejectRatio)

    print "**************************************************************************"
    print "Hour total access, hour total dynamic and hour total reject"
    print gVariable.engineHourAccess
    print gVariable.engineHourDynamic
    print gVariable.engineHourReject
    print "**************************************************************************"

    a2 = sorted(gVariable.engineRule.iteritems(), key=lambda x: x[1], reverse=True)
    for i in range(len(a2)):
        print a2[i][0], a2[i][1]
    print "**************************************************************************"

    a1 = sorted(gVariable.engineIpAccess.iteritems(), key=lambda x: x[1], reverse=True)
    if len(gVariable.engineIpAccess) > 300:
        k1 = 300
    else:
        k1= len(gVariable.engineIpAccess)
    for i in range(k1):
        try:
            print "ip:%-19s access:%-10s hit:%-10s" % (a1[i][0], a1[i][1], gVariable.engineIpReject[a1[i][0]])
        except KeyError:
            print "ip:%-19s access:%-10s **********" % (a1[i][0], a1[i][1])
            pass
    print "**************************************************************************"

    a4 = sorted(gVariable.engineDfpAccess.iteritems(), key=lambda x: x[1], reverse=True)
    if len(gVariable.engineDfpAccess) > 300:
        k2 = 300
    else:
        k2 = len(gVariable.engineDfpAccess)
    for i in range(k2):
        try:
            print "dfp:%-37s access:%-8s hit:%-8s" % (a4[i][0], a4[i][1], gVariable.engineDfpReject[a4[i][0]])
        except KeyError:
            print "dfp:%-37s access:%-8s ********" % (a4[i][0], a4[i][1])
    print "**************************************************************************"

    a3 = sorted(gVariable.engineUri.iteritems(), key=lambda x: x[1], reverse=True)
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
