#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/18 13:35
# @Author  : Gustav
# @File    : gVariable.py

engineTotalAccess = 0
engineDynamicAccess = 0
engineStaticAccess = 0
engineRejectAccess = 0
engineBlackAccess = 0
engineRejectRatio = 0
engineIpTotal = 0

engineIpAccess = {}
engineIpReject = {}
engineUri = {}
engineRule = {}

engineHourAccess = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
engineHourDynamic = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
engineHourReject = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

engineDfpTotal = 0
engineDfpAccess = {}
engineDfpReject = {}

# engineLogPath = "/home/antispider-1.2.1/antispider-engine/logs/engine-info/"
engineLogPath = "./"
