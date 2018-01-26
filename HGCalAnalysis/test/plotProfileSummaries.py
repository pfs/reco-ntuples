import os
import sys
import optparse
import ROOT
from array import array

def getDimensions(var,url,dims=['layer','ieta','thr']):
    """gets the unique list of layers,eta bins and thresholds"""

    dimensions={}
    for d in dims: dimensions[d]=[]

    fIn=ROOT.TFile.Open(url)
    tree=fIn.Get(var)
    for i in xrange(0,tree.GetEntriesFast()):
        tree.GetEntry(i)
        for d in dims: dimensions[d].append( getattr(tree,d) )
    fIn.Close()

    for d in dims: 
        dimensions[d]=sorted(set(dimensions[d]))
    return dimensions


def fillSummaryPlots(var,fileList):
    """parse the trees and make summary plots"""
    
    dimensions=getDimensions(var,fileList[0][0])
    nieta=len(dimensions['ieta'])
    nlay=len(dimensions['layer'])

    allH=[]
    for i in xrange(0,len(fileList)):

        url,title=fileList[i]

        h={}
        for thr in dimensions['thr']:
            h[thr]=ROOT.TH2F('layervsieta_%d_%d'%(i,thr),
                             title+';Layer;Pseudo-rapidity;',
                             nlay,1,nlay+1,nieta,1,nieta+1)
            h[thr].SetDirectory(0)
            
        #fill the histogram
        fIn=ROOT.TFile.Open(url)
        tree=fIn.Get(var)
        for i in xrange(0,tree.GetEntriesFast()):
            tree.GetEntry(i)
            xbin=h[tree.thr].GetXaxis().FindBin(tree.layer)
            ybin=h[tree.thr].GetYaxis().FindBin(tree.ieta)
            h[tree.thr].SetBinContent(xbin,ybin,tree.median)
            h[tree.thr].SetBinError(xbin,ybin,tree.medianUnc)
            h[tree.thr].GetXaxis().SetBinLabel(xbin,'%d'%tree.layer)
            h[tree.thr].GetYaxis().SetBinLabel(ybin,'%3.2f'%tree.eta)
        fIn.Close()
        
        allH.append(h)

    return allH

def showSummaryPlots(hcoll,var,outDir,bin,ytitle):
    """loops over the plot collection and shows the plots"""

    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    c=ROOT.TCanvas('c','c',500,500)
    c.SetTopMargin(0.06)
    c.SetLeftMargin(0.12)
    c.SetRightMargin(0.02)
    c.SetBottomMargin(0.12)

    for thr in hcoll[0]:
        
        nbins=getattr(hcoll[0][thr],'GetNbins%s'%bin)()
        projattr='X' if bin=='Y' else 'Y'
        for ibin in xrange(1,nbins):

            frame=getattr(hcoll[0][thr],'Projection'+projattr)('p'+projattr,ibin,ibin)
            frame.Reset('ICE')
            frame.GetYaxis().SetRangeUser(1e-3,1)
            frame.GetXaxis().SetLabelSize(0.05)
            frame.GetXaxis().SetTitleSize(0.05)
            frame.GetYaxis().SetLabelSize(0.04)
            frame.GetYaxis().SetTitleSize(0.05)
            frame.GetXaxis().SetTitle( getattr(hcoll[0][thr],'Get%saxis'%projattr)().GetTitle() )
            frame.GetYaxis().SetTitle(ytitle)
            frame.Draw()

            frameTitle=getattr(hcoll[0][thr],'Get%saxis'%bin)().GetTitle()
            frameVal=getattr(hcoll[0][thr],'Get%saxis'%bin)().GetBinLabel(ibin)

            leg=ROOT.TLegend(0.15,0.9,0.4,0.9-0.08*len(hcoll),'%s=%s'%(frameTitle,frameVal))
            leg.SetFillStyle(0)
            leg.SetTextFont(42)
            leg.SetTextSize(0.045)
            leg.SetBorderSize(0)

            allHx,allHxRatios=[],[]
            for ih in xrange(0,len(hcoll)):
                allHx.append( getattr(hcoll[ih][thr],'Projection'+projattr)('p%s_%d'%(projattr,ih),ibin,ibin) )
                allHx[-1].SetLineColor(1+ih)
                allHx[-1].SetMarkerColor(1+ih)
                allHx[-1].SetMarkerStyle(20+ih)
                allHx[-1].Draw('same')
                leg.AddEntry(allHx[-1],allHx[-1].GetTitle(),'lp')

                allHxRatios.append( allHx[-1].Clone( '%s_ratio'%allHx[-1].GetName()) )
                allHxRatios[-1].Divide(allHx[0])

            leg.Draw()
                
            def getPlotHeader():
                tex=ROOT.TLatex()
                tex.SetTextFont(42)
                tex.SetTextSize(0.04)
                tex.SetNDC()
                tex.DrawLatex(0.12,0.96,'#bf{CMS} #it{simulation preliminary}')
                tex.DrawLatex(0.75,0.96,'#scale[0.8]{Threshold: %3.1f MIP}'%(thr*0.25))
            getPlotHeader()

            c.Modified()
            c.Update()
            c.SaveAs('%s/%s_%s%d_thr%d_projection.png'%(outDir,var,bin,ibin,thr) )
            
            #show the ratio to the reference now
            frame.GetYaxis().SetTitle('Ratio to %s'%hcoll[0][thr].GetTitle())
            frame.GetYaxis().SetRangeUser(0.1,4)
            frame.Draw()
            leg=ROOT.TLegend(0.15,0.9,0.4,0.9-0.08*len(hcoll),'%s=%s'%(frameTitle,frameVal))
            leg.SetFillStyle(0)
            leg.SetTextFont(42)
            leg.SetTextSize(0.045)
            leg.SetBorderSize(0)
            for h in allHxRatios:
                h.Draw('same')
                leg.AddEntry(h,h.GetTitle(),'lp')
            leg.Draw()
            getPlotHeader()
            c.Modified()
            c.Update()
            c.SaveAs('%s/%s_%s%d_thr%d_projection_ratio.png'%(outDir,var,bin,ibin,thr) )


def main():
    """parse inputs and run the analysis"""
    
    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--in',          dest='input',       help='input files (csv list file1:title1,...) [%default]',               default=None,      type='string')
    parser.add_option('-o', '--out',         dest='output',      help='output directory [%default]',         default='summary', type='string')
    parser.add_option(      '--var',         dest='var',         help='variable to profile  [%default]',     default='occ',     type='string')
    parser.add_option(      '--title',       dest='title',       help='title for the y-axis  [%default]',    default='Occupancy / cell (median)',    type='string')
    (opt, args) = parser.parse_args()

    os.system('mkdir -p %s'%opt.output)
    fileList=[x.split(':') for x in opt.input.split(',')]
    allH=fillSummaryPlots(var=opt.var,fileList=fileList)
    for bin in ['X','Y']:
        showSummaryPlots(hcoll=allH,var=opt.var,outDir=opt.output,bin=bin,ytitle=opt.title)

if __name__ == "__main__":
    sys.exit(main())
