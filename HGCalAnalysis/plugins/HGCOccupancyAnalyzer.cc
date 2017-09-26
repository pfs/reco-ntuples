#include "RecoNtuples/HGCalAnalysis/plugins/HGCOccupancyAnalyzer.h"


#include "DetectorDescription/OfflineDBLoader/interface/GeometryInfoDump.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"
#include "SimG4CMS/Calo/interface/CaloHitID.h"

#include "DetectorDescription/Core/interface/DDFilter.h"
#include "DetectorDescription/Core/interface/DDFilteredView.h"
#include "DetectorDescription/Core/interface/DDSolid.h"

#include "DataFormats/GeometryVector/interface/Basic3DVector.h"

#include "CLHEP/Units/GlobalSystemOfUnits.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CLHEP/Geometry/Point3D.h"
#include "CLHEP/Geometry/Plane3D.h"
#include "CLHEP/Geometry/Vector3D.h"

#include "TVector2.h"

#include <iostream>

using namespace std;

//
SubdetectorOccupancyHisto::SubdetectorOccupancyHisto(std::string sdcode,edm::Service<TFileService> *fs) : 
  sdcode_(sdcode),fs_(fs), nEvents_(0)
{ 
  thr_.push_back(2);
  thr_.push_back(4);
  thr_.push_back(20);
  thr_.push_back(40);
}

//
bool SubdetectorOccupancyHisto::hasLayer(int layer) 
{ 
  return normHistos_.find(layer)!=normHistos_.end();
}

//
void SubdetectorOccupancyHisto::initLayer(int layer)
{
  if(hasLayer(layer)) return;
  TString name("sd_"); name += sdcode_; name += "_layer"; name += layer;
  normHistos_[layer] = (*fs_)->make<TH1F>(name+"_nch",";Pseudo-rapidity;Number of channels",10,1.5,3.0);
  
  mipHistos_[layer] = (*fs_)->make<TH3F>(name+"_mip",";# MIPs;Pseudo-rapidity;Time sample [bx]",200,0,50,10,1.5,3.0,10,0,10);
  mipHistos_[layer]->Sumw2();
  
  totHistos_[layer] = (*fs_)->make<TH3F>(name+"_tot",";ToT [bx];Pseudo-rapidity;Time sample [bx]",9,1,10,10,1.5,3.0,10,0,10);
  totHistos_[layer]->Sumw2();
  
  busyHistos_[layer] = (*fs_)->make<TH3F>(name+"_busy",";Busy state;Pseudo-rapidity;Time sample [bx]",2,0,2,10,1.5,3.0,10,0,10);
  busyHistos_[layer]->Sumw2();
  
  dataCountHistos_[layer] = new TH1F(name+"_datacount",";Pseudo-rapidity;Data volume [bit]",10,1.5,3.0);
  dataCountHistos_[layer]->SetDirectory(0);
  
  dataVolHistos_[layer] = (*fs_)->make<TH2F>(name+"_datavol",";Data volume [bit];Pseudo-rapidity",60,0,12,10,1.5,3.0);
  dataVolHistos_[layer]->Sumw2();
  
  dataVolTypeHistos_[layer] = (*fs_)->make<TH2F>(name+"_datavoltype",";Data volume [bit];Pseudo-rapidity",3,0,3,10,1.5,3.0);
  dataVolTypeHistos_[layer]->GetXaxis()->SetBinLabel(1,"=1 bit");
  dataVolTypeHistos_[layer]->GetXaxis()->SetBinLabel(2,"=8 bits");
  dataVolTypeHistos_[layer]->GetXaxis()->SetBinLabel(3,"=12 bits");
  dataVolTypeHistos_[layer]->Sumw2();
  
  trigCountHistos_[layer] = new TH1F(name+"_trigcount",";Trigger volume [bit];Pseudo-rapidity",10,1.5,3.0);
  trigCountHistos_[layer]->SetDirectory(0);
  
  trigVolHistos_[layer] = (*fs_)->make<TH2F>(name+"_trigvol",";Trigger volume [bit];Pseudo-rapidity",60,0,6,10,1.5,3.0);
  trigVolHistos_[layer]->Sumw2();
  
  std::map<int,TH1F *> layerCountHistos;   
  std::map<int,TH2F *> layerOccHistos;
  
  /* Double_t occbins[100]; */
  /* for(size_t ibin=0; ibin<10; ibin++)   occbins[ibin]=ibin*1e-4; */
  /* for(size_t ibin=10; ibin<19; ibin++)  occbins[ibin]=(ibin-9.)*1e-3; */
  /* for(size_t ibin=19; ibin<29; ibin++)  occbins[ibin]=(ibin-18)*1e-2; */
  /* for(size_t ibin=29; ibin<100; ibin++) occbins[ibin]=0.1+(1-0.1)/(100-29)*(ibin-28); */
  for(size_t ithr=0; ithr<thr_.size(); ithr++)
    {
      TString thrName(name); thrName += "_thr"; thrName += thr_[ithr];
      layerCountHistos[ thr_[ithr] ] = new TH1F(thrName+"_count",";Counts;Pseudo-rapidity",10,1.5,3.0);
      layerCountHistos[ thr_[ithr] ]->SetDirectory(0);
      
      layerOccHistos[ thr_[ithr] ] = (*fs_)->make<TH2F>(thrName+"_occ",";Occupancy;Pseudo-rapidity",100,0,1,10,1.5,3.0);
      //layerOccHistos[ thr_[ithr] ] = (*fs_)->make<TH2F>(thrName+"_occ",";Occupancy;Pseudo-rapidity",99,occbins,10,1.5,3.0);
      layerOccHistos[ thr_[ithr] ]->Sumw2();
    }
  
  countHistos_[layer]=layerCountHistos;
  occHistos_[layer]=layerOccHistos;
}

//
void SubdetectorOccupancyHisto::count(int layer,float eta,int adc)
{
  eta=fabs(eta);
  
  int dataVol=computeDataVol(adc,eta);
  dataCountHistos_[layer]->Fill(eta,dataVol);
  if(dataVol==1)  dataVolTypeHistos_[layer]->Fill(0.,eta);
  if(dataVol==8)  dataVolTypeHistos_[layer]->Fill(1.,eta);
  if(dataVol==12) dataVolTypeHistos_[layer]->Fill(2.,eta);
  
  trigCountHistos_[layer]->Fill(eta,computeTriggerVol(adc,eta));
  for(size_t ithr=0; ithr<thr_.size(); ithr++)
    {
      if(adc<thr_[ithr]) continue;
      countHistos_[layer][ thr_[ithr] ]->Fill(eta);
    }
}

//
int SubdetectorOccupancyHisto::computeDataVol(float adc,float eta)
{
  float nmips=0.25*adc;
  int nbits(1);
  if(nmips>6.4)      nbits=12;
  else if(nmips>0.4) nbits=8;
  return nbits;
}

//
int SubdetectorOccupancyHisto::computeTriggerVol(float adc,float eta)
{
  float nmips=0.25*adc;
  int nbits(1);
  if(fabs(eta)<2)
    {
      if(nmips>96)      nbits=10;
      else if(nmips>10) nbits=6;
    }
  else if(fabs(eta)<2.5)
    {
      if(nmips>96)      nbits=10;
      else if(nmips>10) nbits=6;
    }
  else
    {
      if(nmips>192)     nbits=10;
      else if(nmips>25) nbits=6;
    }
  return nbits;
}

//
float SubdetectorOccupancyHisto::endEvent(bool reset)
{
  nEvents_++;
  
  //iterate over layers
  float totalEvtSize(0);
  for(std::map< int, std::map<int,TH2F *> >::iterator it=occHistos_.begin();
      it!=occHistos_.end();
      it++)
    {
      
      //occupancies
      TH1F *normH=normHistos_[it->first];
      
      //iterate over thresholds
      for(std::map<int,TH2F *>::iterator jt=it->second.begin();
          jt!=it->second.end();
          jt++)
        {
          TH2F *occH=jt->second;
          TH1F *countH=countHistos_[it->first][jt->first];
          
          //fill occupancy histos
          for(int xbin=1; xbin<=countH->GetXaxis()->GetNbins(); xbin++)
            {
              float eta=countH->GetXaxis()->GetBinCenter(xbin);
              float cts=countH->GetBinContent(xbin);
              float norm=normH->GetBinContent(xbin)*2; //we have two endcaps
              float occ(norm>0 ? cts/norm : 0.);
              occH->Fill(occ,eta);
            }
          
          //reset counts
          if(reset) countH->Reset("ICE");
        }
      
      //data volumes
      TH1F *dataH=dataCountHistos_[it->first];
      TH1F *trigH=trigCountHistos_[it->first];
      for(int xbin=1; xbin<=dataH->GetXaxis()->GetNbins(); xbin++)
        {
          float ncells=normH->GetBinContent(xbin)*2; //we have two endcaps
          float eta=dataH->GetXaxis()->GetBinCenter(xbin);
          
          float data=dataH->GetBinContent(xbin);
          totalEvtSize += data;
          dataVolHistos_[it->first]->Fill(ncells>0 ? data/ncells : 1. ,eta);
          
          float trig=trigH->GetBinContent(xbin);
          trigVolHistos_[it->first]->Fill(ncells>0 ? trig/ncells : 1. ,eta);
        }
      
      dataH->Reset("ICE");
      trigH->Reset("ICE");
    }
  
  return  totalEvtSize;
}

//
int SubdetectorOccupancyHisto::finalize()
{
  if(nEvents_==0) return 0;
  
  for(std::map< int, TH3F *>::iterator it=mipHistos_.begin();
      it!=mipHistos_.end();
      it++)
    {
      
      //divide by the number of cells analyzed
      TH1F *normH=normHistos_[it->first];
      for(int ybin=1; ybin<=it->second->GetYaxis()->GetNbins(); ybin++)
        {
          float ncells=normH->GetBinContent(ybin)*2; //we have two endcaps
          if(ncells==0) continue;
          
          //energy spectrum 
          for(int xbin=0; xbin<=it->second->GetXaxis()->GetNbins()+1; xbin++)
            {
              for(int zbin=0; zbin<=it->second->GetZaxis()->GetNbins()+1; zbin++)
                {
                  float counts=it->second->GetBinContent(xbin,ybin,zbin);
                  float countsErr=it->second->GetBinError(xbin,ybin,zbin);
                  it->second->SetBinContent(xbin,ybin,counts/(nEvents_*ncells));
                  it->second->SetBinError(xbin,ybin,countsErr/(nEvents_*ncells));
                }
            }
          
          //data type sent
          for(int xbin=0; xbin<=dataVolTypeHistos_[it->first]->GetXaxis()->GetNbins(); xbin++)
            {
              float counts=dataVolTypeHistos_[it->first]->GetBinContent(xbin,ybin);
              float countsErr=dataVolTypeHistos_[it->first]->GetBinError(xbin,ybin);
              dataVolTypeHistos_[it->first]->SetBinContent(xbin,ybin,counts/(nEvents_*ncells));
              dataVolTypeHistos_[it->first]->SetBinError(xbin,ybin,countsErr/(nEvents_*ncells));
            }
        }
      
      
      
      //normalized by the number of events (already averaged per cells)
      for(std::map<int,TH2F *>::iterator jt=occHistos_[it->first].begin();
          jt!=occHistos_[it->first].end();
          jt++)
        jt->second->Scale(1./nEvents_);
      
      dataVolHistos_[it->first]->Scale(1./nEvents_);
      trigVolHistos_[it->first]->Scale(1./nEvents_);
      
      mipHistos_[it->first]->Scale(1./nEvents_);
      totHistos_[it->first]->Scale(1./nEvents_);
      busyHistos_[it->first]->Scale(1./nEvents_);    
    }
  return nEvents_;
}

//
SubdetectorOccupancyHisto::~SubdetectorOccupancyHisto() {}

//
// PLUGIN IMPLEMENTATION
//


//
HGCOccupancyAnalyzer::HGCOccupancyAnalyzer( const edm::ParameterSet &iConfig ) : 
  isInit_(false), 
  geoEE_("HGCalEESensitive"),
  digisEE_( consumes<HGCEEDigiCollection>(edm::InputTag("mix","HGCDigisEE")) ),
  geoFH_("HGCalHESiliconSensitive"),
  digisFH_( consumes<HGCHEDigiCollection>(edm::InputTag("mix","HGCDigisHEfront")) )
{  
  edm::Service<TFileService> fs;
  evtSizeH_ = fs->make<TH2F>("evtsize",";Event size (log_{10} byte);Sub-detector",100,0,10,3,0,3);
  evtSizeH_->GetYaxis()->SetBinLabel(1,"HGC");
  evtSizeH_->GetYaxis()->SetBinLabel(2,"EE");
  evtSizeH_->GetYaxis()->SetBinLabel(3,"FH");
}

//
HGCOccupancyAnalyzer::~HGCOccupancyAnalyzer()
{
}

//
void HGCOccupancyAnalyzer::endJob()
{
  //normalize to the number of events analyzed
  int nEvents_(0);
  for(auto &it : subDetHistos_) nEvents_=it.second->finalize();

  if(nEvents_==0) return;
  std::cout << "[endJob] analyzed " << nEvents_ << " events" << std::endl;
  evtSizeH_->Scale(1./nEvents_);
}

//
void HGCOccupancyAnalyzer::prepareAnalysis(std::map<std::string,const HGCalGeometry *> &hgcGeometries)
{
  if(isInit_) return;
  isInit_=true;

  //init histograms
  edm::Service<TFileService> fs;
  for(auto &it : hgcGeometries )
    {
      std::string key(it.first);
      const std::vector<DetId> &detIds=it.second->getValidDetIds();
      std::cout << "\t HGC subdet: " << key << " has " << detIds.size() << " valid detIds" <<  std::endl;
      
      //init new histogram class
      subDetHistos_[key]=new SubdetectorOccupancyHisto(key,&fs);
      for(size_t i=0; i<detIds.size(); i++)
	{
          //decode layer from detId
          int layer(-1);
          if(key=="EE")
            {
              HGCEEDetId detId(detIds[i].rawId());
              layer=detId.layer();
            }
          if(key=="FH")
            {
              HGCHEDetId detId(detIds[i].rawId());
              layer=detId.layer();
            }
          if(layer<0) continue;

          //get position
	  float eta(it.second->getPosition( detIds[i] ).eta());
	  subDetHistos_[key]->initLayer(layer);
	  subDetHistos_[key]->normHistos_[layer]->Fill(eta);
	}
    }
}

  
//
void HGCOccupancyAnalyzer::analyze( const edm::Event &iEvent, const edm::EventSetup &iSetup)
{
  //read geometry from event setup
  std::map<std::string,const HGCalGeometry *> hgcGeometries;
  edm::ESHandle<HGCalGeometry> eeGeoHandle;
  iSetup.get<IdealGeometryRecord>().get(geoEE_,eeGeoHandle);
  hgcGeometries["EE"]=eeGeoHandle.product();
  edm::ESHandle<HGCalGeometry> fhGeoHandle;
  iSetup.get<IdealGeometryRecord>().get(geoFH_,fhGeoHandle);
  hgcGeometries["FH"]=fhGeoHandle.product();
  prepareAnalysis(hgcGeometries);

  //analyze digi collections
  edm::Handle<HGCEEDigiCollection> eeDigisHandle;
  iEvent.getByToken(digisEE_,eeDigisHandle);
  float eeEvtSize=analyzeEEDigis("EE",eeDigisHandle,hgcGeometries["EE"]);

  edm::Handle<HGCHEDigiCollection> fhDigisHandle;
  iEvent.getByToken(digisFH_,fhDigisHandle);
  float fhEvtSize=analyzeHEDigis("FH",fhDigisHandle,hgcGeometries["FH"]);

  //monitor event size
  float totalEvtSize=eeEvtSize+fhEvtSize;
  evtSizeH_->Fill(TMath::Log10(eeEvtSize/8.),1);
  evtSizeH_->Fill(TMath::Log10(fhEvtSize/8.),1);
  evtSizeH_->Fill(TMath::Log10(totalEvtSize/8.),0.);
}


//
float HGCOccupancyAnalyzer::analyzeHEDigis(std::string isd,edm::Handle<HGCHEDigiCollection> &heDigis, const HGCalGeometry *geom)
{
  //check inputs
  if(!heDigis.isValid()) return 0;
  
  //analyze hits
  for(HGCHEDigiCollection::const_iterator hit_it = heDigis->begin(); hit_it != heDigis->end(); ++hit_it) 
    {
      if(hit_it->size()==0) continue;
      int itSampleIdx=(hit_it->size()-1);
      HGCHEDetId detId(hit_it->id());
      int layer=detId.layer();
      float eta( geom->getPosition(detId).eta());
      
      for(int it=0; it<=itSampleIdx; it++)
	{
	  int gain_i=hit_it->sample(it).threshold();
	  int adc_i=hit_it->sample(it).data();
	  
	  //for the IT sample extract occupancies
	  if(it==itSampleIdx) subDetHistos_[isd]->count(layer,eta,adc_i);
	  
	  //monitor energy profiles, integration times and busy states
	  subDetHistos_[isd]->mipHistos_[layer]->Fill(adc_i*0.25,fabs(eta),it);
	  subDetHistos_[isd]->busyHistos_[layer]->Fill((gain_i==1 && adc_i==0),fabs(eta),it);
	  if (gain_i==1 && adc_i!=0)
	    {
	      size_t totalIntegTime(1);
	      for(int jt=it+1; jt<=itSampleIdx; jt++)
		{
		  int gain_j=hit_it->sample(jt).threshold();
		  int adc_j=hit_it->sample(jt).data();
		  if(adc_j !=0 ) break;
		  if(gain_j ==0 ) break;
		  totalIntegTime++;
		}
	      subDetHistos_[isd]->totHistos_[layer]->Fill(totalIntegTime,fabs(eta),it);
	    }
	}
    }     
  return subDetHistos_[isd]->endEvent();
}

//
float HGCOccupancyAnalyzer::analyzeEEDigis(std::string isd,edm::Handle<HGCEEDigiCollection> &eeDigis, const HGCalGeometry *geom)
{
  //check inputs
  if(!eeDigis.isValid()) return 0.;

  //analyze hits
  for(HGCEEDigiCollection::const_iterator hit_it = eeDigis->begin(); hit_it != eeDigis->end(); ++hit_it) 
    {
      if(hit_it->size()==0) continue;
      int itSampleIdx=(hit_it->size()-1);
      HGCEEDetId detId(hit_it->id());
      int layer=detId.layer();
      float eta( geom->getPosition(detId).eta());

      for(int it=0; it<=itSampleIdx; it++)
	{
	  int gain_i=hit_it->sample(it).threshold();
	  int adc_i=hit_it->sample(it).data();
	  
	  //for the IT sample extract occupancies
	  if(it==itSampleIdx) subDetHistos_[isd]->count(layer,eta,adc_i);
	  
	  //monitor energy profiles, integration times and busy states
	  subDetHistos_[isd]->mipHistos_[layer]->Fill(adc_i*0.25,fabs(eta),it);
	  subDetHistos_[isd]->busyHistos_[layer]->Fill((gain_i==1 && adc_i==0),fabs(eta),it);
	  if (gain_i==1 && adc_i!=0)
	    {
	      size_t totalIntegTime(1);
	      for(int jt=it+1; jt<=itSampleIdx; jt++)
		{
		  int gain_j=hit_it->sample(jt).threshold();
		  int adc_j=hit_it->sample(jt).data();
		  if(adc_j !=0 ) break;
		  if(gain_j ==0 ) break;
		  totalIntegTime++;
		}
	      subDetHistos_[isd]->totHistos_[layer]->Fill(totalIntegTime,fabs(eta),it);
	    }

	}
    }
  
  return subDetHistos_[isd]->endEvent();
}


//define this as a plug-in
DEFINE_FWK_MODULE(HGCOccupancyAnalyzer);
