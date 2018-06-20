#ifndef _HGCOccupancyAnalyzer_h_
#define _HGCOccupancyAnalyzer_h_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESTransientHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DetectorDescription/Core/interface/DDCompactView.h"

#include "SimDataFormats/CaloHit/interface/PCaloHit.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
//#include "SimG4CMS/Calo/interface/HGCNumberingScheme.h"

#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/ForwardDetId/interface/HGCalDetId.h"
#include "DataFormats/HGCDigi/interface/HGCDigiCollections.h"

#include "SimCalorimetry/HGCalSimProducers/interface/HGCDigitizerBase.h"  

#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "DataFormats/TrajectorySeed/interface/PropagationDirection.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateTransform.h"
#include "TrackingTools/MaterialEffects/interface/PropagatorWithMaterial.h"
#include "DataFormats/GeometrySurface/interface/BoundDisk.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "Geometry/HGCalGeometry/interface/HGCalGeometry.h"

#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TString.h"

#include <string>

/**
   @class SubdetectorOccupancyHisto
   @author P. Silva (CERN)
*/
class SubdetectorOccupancyHisto
{
public:
  
  /**
     @short CTOR
   */
  SubdetectorOccupancyHisto(std::string sdcode,edm::Service<TFileService> *fs); 
  
  /**
     @short check if layer exists already
   */
  bool hasLayer(int layer);
  
  /**
     @short initiate montoring histos for a layer
   */
  void initLayer(int layer);


  /**
     @short accumulate counts for a new hit
  */
  void count(int layer,float eta,int adc);


  /**
     @short computes number of bits to send
   */
  int computeDataVol(float adc,float eta);
  int computeTriggerVol(float adc,float eta);

  /**
     @short to be called at the end of an event
  */
  float endEvent(bool reset=true);

  /**
     @short normalize according to the number of events analyzed
   */
  int finalize();

  /**
     @short DTOR
   */
  ~SubdetectorOccupancyHisto();

  //all histos are public and can be manipulated...
  std::map< int, TH1F *>                normHistos_;
  std::map< int, TH1F *>                dataCountHistos_, trigCountHistos_;
  std::map< int, TH2F *>                dataVolHistos_,   trigVolHistos_, dataVolTypeHistos_;
  std::map< int, std::map<int,TH1F *> > countHistos_;
  std::map< int, std::map<int,TH2F *> > occHistos_;
  std::map< int, TH3F *>                mipHistos_, totHistos_;
  std::map< int, TH2F *>                busyHistos_;
 
 private:
  
  std::string sdcode_;
  edm::Service<TFileService> *fs_;
  std::vector<int> thr_;
  int nEvents_;
};


/**
   @class HGCOccupancyAnalyzer
   @author P. Silva (CERN)
*/

class HGCOccupancyAnalyzer : public edm::EDAnalyzer 
{
  
 public:
  
  explicit HGCOccupancyAnalyzer( const edm::ParameterSet& );
  ~HGCOccupancyAnalyzer();
  virtual void analyze( const edm::Event&, const edm::EventSetup& );
  void endJob();

 private:
  /**
     @short starts histograms
   */
  void prepareAnalysis(std::map<std::string,const HGCalGeometry *> &hgcGeometries);
  
  /**
     @short digi analyzers
   */
  float analyzeEEDigis(std::string isd,edm::Handle<HGCEEDigiCollection> &eeDigis,const HGCalGeometry *geom);
  float analyzeHEDigis(std::string isd,edm::Handle<HGCHEDigiCollection> &heDigis,const HGCalGeometry *geom);
  
  //gen level
  bool isInit_;

  //hgcal
  std::map<std::string,SubdetectorOccupancyHisto> occHistos_;
  std::string geoEE_;
  edm::EDGetTokenT<HGCEEDigiCollection> digisEE_;
  std::string geoFH_;
  edm::EDGetTokenT<HGCHEDigiCollection> digisFH_;

  //event size 
  TH2F *evtSizeH_;

  std::map<std::string,SubdetectorOccupancyHisto *> subDetHistos_;
};
 

#endif
