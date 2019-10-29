
def VolumeAnalysisPLOT(SettingsDic):

    import MODAnalysisData
    import os
    
    MODAnalysisData.VolAnalysis(ExperimentNumber = 1,
                                ImportRootFolderBAC='/ExportedData/VolumeValues',
                                ImportRootFolder=SettingsDic['FolderName'],
                                FirstStack=1,LastStack=SettingsDic['timePoints'],
                                initialTimePoint=0,
                                timeinterval=SettingsDic['timeinterval'],
                                ZStep=SettingsDic['Zstep'],
                                XYField=[SettingsDic['height_field'], SettingsDic['width_field']],
                                RawImageDefinition=[SettingsDic['height'] + 1, SettingsDic['width'] + 1],
                                RegionAnalysis=True,
                                SmutansRadius=SettingsDic['Microorganism_Radius'], #em microns
                                Max_a_FitError=1000000,
                                Max_b_FitError=1000000,
                    
                                p0_THR_val1=5,
                                p0_THR_val2=20,
                                
                                Det_TopoXVol_relation=False)
     
