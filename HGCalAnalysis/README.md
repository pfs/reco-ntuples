# Occupancy analyzer

## Create Min.bias simulation

Check test directory

## Create histograms for analysis

```
for gran in 050 090 100 180 400 710; do
    for sim in RECO RECO_200; do   
        outDir=summary/${sim}
        echo ${outDir} ${gran};
        mkdir -p ${outDir};
        cd ${outDir}
        cmsRun $CMSSW_BASE/src/RecoNtuples/HGCalAnalysis/test/occAnalysisConfig.py granularity=${gran} input=/eos/cms/store/cmst3/user/psilva/HGCal/MinBias_${gran}/${sim}/ &
        cd -;
    done
done
```

## summarize the profiles for a distribution

```
for gran in 050 090 100 180 400 710; do
    for sim in RECO RECO_200; do
        outDir=summary/${sim}

        for var in occ occT; do
            python test/createProfileSummaries.py --var ${var} -i ${outDir}/occ_analysis_${gran}.root -o ${outDir}; 
        done
    done
done
```

## make comparison plots

```
python test/plotProfileSummaries.py -o summary/pu140vs200 -i summary/RECO/occ_summary_occ_analysis_100.root:"PU=140",summary/RECO_200/occ_summary_occ_analysis_100.root:"PU=200" &
python test/plotProfileSummaries.py -o summary/pu140vs200_050 -i summary/RECO/occ_summary_occ_analysis_050.root:"PU=140",summary/RECO_200/occ_summary_occ_analysis_050.root:"PU=200" &
python test/plotProfileSummaries.py -o summary/pu200_data -i summary/RECO_200/occ_summary_occ_analysis_050.root:"0.5 cm^{2}",summary/RECO_200/occ_summary_occ_analysis_090.root:"0.9 cm^{2}",summary/RECO_200/occ_summary_occ_analysis_100.root:"1.0 cm^{2}",summary/RECO_200/occ_summary_occ_analysis_180.root:"1.8 cm^{2}" &
python test/plotProfileSummaries.py -o summary/pu200_trig -i summary/RECO_200/occ_summary_occ_analysis_400.root:"4.0 cm^{2}",summary/RECO_200/occ_summary_occ_analysis_710.root:"7.1 cm^{2}" &
python test/plotProfileSummaries.py -o summary/pu200_trig -i summary/RECO_200/occT_summary_occ_analysis_400.root:"4.0 cm^{2}",summary/RECO_200/occT_summary_occ_analysis_710.root:"7.1 cm^{2}" --var occT&
```
 