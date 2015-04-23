#!/usr/bin/env python
import os, sys
from ROOT import *

gROOT.ProcessLine(".x rootlogon.C")
gStyle.SetMarkerSize(2)
gStyle.SetPaintTextFormat("5.1f")

interestedName = 'muons1stStep'

dirs = sys.argv[1:]

hModuleTime = TH1F("hModuleTime", "ModuleTime;;CPU time (ms)", len(dirs), 1, len(dirs)+1)
hOthersTime = TH1F("hOthersTime", "OthersTime;;CPU time (ms)", len(dirs), 1, len(dirs)+1)

modIndex = 1
for d in dirs:
    if not os.path.isdir(d): continue
    fName = '%s/log.txt' % d
    if not os.path.exists(fName): continue

    tReports = []
    for l in open(fName).readlines():
        l = l.strip()
        if tReports == []:
            if l == 'TimeReport ---------- Module Summary ---[sec]----':
                tReports.append(l)
        elif l[:len('TimeReport')] == 'TimeReport':
            tReports.append(l)

    timeTotal = 0.
    timeForModule = []
    for l in tReports[4:-2]: ## First 3 lines are headers, 2 lines are footers
        items = l[10:].split()
        modName = items[-1]
        times = [1000*float(xx) for xx in items[:-1]]

        # We keep CPU time per event only
        timeForModule.append((modName, times[0]))
        timeTotal += times[0]

    timeForModule.sort(key=lambda x: x[1], reverse=True)
    timeForModule = timeForModule[:10]

    maxFW = max([len(x[0]) for x in timeForModule])
    fmt   = "{:>3} {:<%d}{:>9} ms/evt ({:>5}%%)" % maxFW

    print "====== Time per Modules for %s ======" % d
    hModuleTime.GetXaxis().SetBinLabel(modIndex, d)
    hOthersTime.GetXaxis().SetBinLabel(modIndex, d)
    for i, (modName, time) in enumerate(timeForModule):
        percent = time/timeTotal*100
        BEGIN, END = '', ''
        if modName == interestedName:
            BEGIN, END = ('\033[91m', '\033[0m')
            hModuleTime.Fill(modIndex, time)
        else:
            hOthersTime.Fill(modIndex, time)
        print BEGIN, fmt.format(i+1, modName, ("%8.3f" % time), ("%3.2f" % percent)), END
    print "..."
    print ""
    modIndex += 1

hModuleTime.SetMaximum(1500)
hOthersTime.SetMaximum(1500)
hModuleTime.SetFillColor(kRed)
hOthersTime.SetFillColor(kBlue)
hStack = THStack("hstack", "hstack;;CPU time (ms)")
hStack.Add(hModuleTime)
hStack.Add(hOthersTime)
hStack.SetMaximum(1500)
c = TCanvas("c", "c", 500, 500)
hStack.Draw("texthist")


