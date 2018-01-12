#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/18 13:35
# @Author  : Gustav
# @File    : gVariable.py

nginxAccess = 0
nginxDynamicAccess = 0
nginxStaticAccess = 0
nginxRejectAccess = 0
nginxBlackAccess = 0
nginxRejectRatio = 0
nginxIpTotal = 0

nginxIpAccess = {}
nginxIpReject = {}
nginxUri = {}

nginxHourAccess = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
nginxHourDynamic = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
nginxHourReject = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

nginxDfpTotal = 0
nginxDfpAccess = {}
nginxDfpReject = {}

# nginxLogPath = "/home/antispider-1.2.1/logs/nginx/"
nginxLogPath = "./"
