#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# @version: v1.0
# @author: gustav
# @file: test
# @time: 18-1-11 上午11:45

import time
import datetime
def getDate():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

print getDate()



def getDate():
    temp = time.localtime()
    yy = temp.tm_year
    mm = temp.tm_mon
    dd = temp.tm_mday
    if dd == 1:
        if mm == 1:
            mm = 12
            yy -= 1
        else:
            mm -= 1
        if mm in (1, 3, 5, 7, 8, 10, 12):
            dd = 31
        elif mm in (4, 6, 9, 11):
            dd = 30
        elif mm == 2:
            if yy in (2020, 2024, 2028, 2032, 2036, 2040, 2044, 2048):
                dd = 29
            else:
                dd = 28
    else:
        dd -= 1
    y2 = str(yy)
    m2 = str(mm)
    d2 = str(dd)
    if len(m2) == 1:
        m2 = "0" + m2
    if len(d2) == 1:
        d2 = "0" + d2
    formDate = y2 + "-" + m2 + "-" + d2
    return formDate