# Occupancy analyzer

## Create Min.bias simulation

Check test directory

## Create histograms for analysis

```
cmsRun test/occAnalysisConfig.py granularity=090
```

## summarize the profiles for a distribution

```
python test/createProfileSummaries.py --var occ -i occ_analysis_090.root; done
```
