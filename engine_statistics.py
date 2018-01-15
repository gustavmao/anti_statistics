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
import gVariable_engine

def getDate():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

def getFileName():
    a1 = str(getDate())
    cmd = "ls " + gVariable_engine.engineLogPath + " |grep " + a1
    a2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    a3 = a2.communicate()
    # print a3
    a4 = a3[0].strip().split("\n")
    a5 = []
    for i in a4:
        a5.append(gVariable_engine.engineLogPath + i)
    return a5

def logParse(fileName):
    fileHandle = gzip.open(fileName, 'rb')
    for i in fileHandle:
        myTime = int(i[:2])
        try:
            # all access
            if re.search("ScheduledAgent\s-\s\d+\sobjs\sload", i):
                a1 = int(re.search("ScheduledAgent\s-\s(\d+)\sobjs\sload", i).group(1))
                gVariable_engine.engineHourAccess[myTime] += a1
                gVariable_engine.engineTotalAccess += a1

            # dynamic access
            if "cn.com.bsfit.frms.obj.AuditObject" in i:
                gVariable_engine.engineHourDynamic[myTime] += 1
                gVariable_engine.engineDynamicAccess += 1
                m5 = re.search(",\suri=(.*),\sip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}),", i)
                try:
                    m2 = m5.group(2)  #ip
                    m3 = m5.group(1)  #uri

                    if m2 in gVariable_engine.engineIpAccess:
                        gVariable_engine.engineIpAccess[m2] += 1
                    else:
                        gVariable_engine.engineIpAccess[m2] = 1

                    if m3 in gVariable_engine.engineUri:
                        gVariable_engine.engineUri[m3] += 1
                    else:
                        gVariable_engine.engineUri[m3] = 1
                except AttributeError:
                    pass
                try:
                    m6 = re.search("dfp=(.*), url=", i).group(1)
                    if m6 in gVariable_engine.engineDfpAccess:
                        gVariable_engine.engineDfpAccess[m6] += 1
                    else:
                        gVariable_engine.engineDfpAccess[m6] = 1
                except AttributeError:
                    pass
        except Exception:
            pass

        # reject access
        if "AsPublishHandlerImpl" in i:
            m4 = i.split("客户端IP:")[1].strip()
            gVariable_engine.engineHourReject[myTime] += 1
            gVariable_engine.engineRejectAccess += 1
            try:
                m7 = re.search("指纹:(.*),统计", i).group(1)
                if m7 in gVariable_engine.engineDfpReject:
                    gVariable_engine.engineDfpReject[m7] += 1
                else:
                    gVariable_engine.engineDfpReject[m7] = 1
            except AttributeError:
                pass

            m1 = re.search("触发的规则:(.*),规则分值", i).group(1).split("|")
            for j in m1:
                if j in gVariable_engine.engineRule:
                    gVariable_engine.engineRule[j] += 1
                else:
                    gVariable_engine.engineRule[j] = 1

            if "IP在黑名单中" in i:
                gVariable_engine.engineHourDynamic[myTime] += 1
                gVariable_engine.engineDynamicAccess += 1
                gVariable_engine.engineBlackAccess += 1
                if m4 in gVariable_engine.engineIpReject:
                    gVariable_engine.engineIpAccess[m4] += 1
                else:
                    gVariable_engine.engineIpAccess[m4] = 1
                try:
                    m7 = re.search("指纹:(.*),统计", i).group(1)
                    if m7 in gVariable_engine.engineDfpAccess:
                        gVariable_engine.engineDfpAccess[m7] += 1
                    else:
                        gVariable_engine.engineDfpAccess[m7] = 1
                except AttributeError:
                    pass

            if m4 in gVariable_engine.engineIpReject:
                gVariable_engine.engineIpReject[m4] += 1
            else:
                gVariable_engine.engineIpReject[m4] = 1

def run():
    logFiles = getFileName()
    for i in logFiles:
        print i
        logParse(i)
        t = time.localtime()
        print "%d:%d:%d" % (t.tm_hour, t.tm_min, t.tm_sec)

    gVariable_engine.engineStaticAccess = gVariable_engine.engineTotalAccess - gVariable_engine.engineDynamicAccess
    gVariable_engine.engineRejectRatio = (float(gVariable_engine.engineRejectAccess) / float(gVariable_engine.engineDynamicAccess)) * 100
    gVariable_engine.engineIpTotal = len(gVariable_engine.engineIpAccess)
    gVariable_engine.engineDfpTotal = len(gVariable_engine.engineDfpAccess)

    print "\n********************************************************************"
    print "total:%-10d  static:%-10d  dynamic:%-10d  reject:%d" % \
          (gVariable_engine.engineTotalAccess, gVariable_engine.engineStaticAccess, gVariable_engine.engineDynamicAccess,
           gVariable_engine.engineRejectAccess)

    print "blacklist:%-10d  iptotal:%-10d  rejectratio:%.2f%%" % \
          (gVariable_engine.engineBlackAccess, gVariable_engine.engineIpTotal, gVariable_engine.engineRejectRatio)

    print "**************************************************************************"
    print "Hour total access, hour total dynamic and hour total reject"
    print gVariable_engine.engineHourAccess
    print gVariable_engine.engineHourDynamic
    print gVariable_engine.engineHourReject
    print "**************************************************************************"

    a2 = sorted(gVariable_engine.engineRule.iteritems(), key=lambda x: x[1], reverse=True)
    for i in range(len(a2)):
        print a2[i][0], a2[i][1]
    print "**************************************************************************"

    a1 = sorted(gVariable_engine.engineIpAccess.iteritems(), key=lambda x: x[1], reverse=True)
    if len(gVariable_engine.engineIpAccess) > 300:
        k1 = 300
    else:
        k1= len(gVariable_engine.engineIpAccess)
    for i in range(k1):
        try:
            print "ip:%-19s access:%-10s hit:%-10s" % (a1[i][0], a1[i][1], gVariable_engine.engineIpReject[a1[i][0]])
        except KeyError:
            print "ip:%-19s access:%-10s **********" % (a1[i][0], a1[i][1])
            pass
    print "**************************************************************************"

    a4 = sorted(gVariable_engine.engineDfpAccess.iteritems(), key=lambda x: x[1], reverse=True)
    if len(gVariable_engine.engineDfpAccess) > 300:
        k2 = 300
    else:
        k2 = len(gVariable_engine.engineDfpAccess)
    for i in range(k2):
        try:
            print "dfp:%-37s access:%-8s hit:%-8s" % (a4[i][0], a4[i][1], gVariable_engine.engineDfpReject[a4[i][0]])
        except KeyError:
            print "dfp:%-37s access:%-8s ********" % (a4[i][0], a4[i][1])
    print "**************************************************************************"

    a3 = sorted(gVariable_engine.engineUri.iteritems(), key=lambda x: x[1], reverse=True)
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
