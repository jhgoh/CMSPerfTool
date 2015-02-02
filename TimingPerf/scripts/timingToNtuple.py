#!/usr/bin/env python

import sys, os

d = sys.argv[1].rstrip('/')
if not os.path.isdir(d):
    print "Cannot open directory", d

timing = {}
for f in os.listdir(d):
    if not f.startswith("detailedInfo"): continue
    print "Readling file", f

    for l in open("%s/%s" % (d, f)).readlines():
        l = l.strip()
        if not l.startswith('TimeModule>'): continue
        event, run, instance, typeName, cpuTime = l.split()[1:]
        bName = "%s_%s" % (typeName, instance)

        if bName not in timing: timing[bName] = []
        timing[bName].append(float(cpuTime))

import ctypes
bInput = {}
for bName in timing: bInput[bName] = ctypes.c_float()
bInput["total"] = ctypes.c_float()

from ROOT import *
f = TFile("timing_%s.root" % d, "RECREATE")
f.cd()
tree = TTree("timing", "timing")
tree.Branch("total", bInput["total"], "total/F")
for bName in timing:
    print "Booking branch", bName
    tree.Branch(bName, bInput[bName], "%s/F" % bName)

nEvent = len(timing[bInput.keys()[0]])
print "Filling", nEvent, "Events"
for entry in xrange(nEvent):
    total = 0.
    for bName in timing:
        t = timing[bName][entry]
        bInput[bName].value = t
        total += t
    bInput["total"].value = total
    tree.Fill()
tree.Write()
f.Write()
