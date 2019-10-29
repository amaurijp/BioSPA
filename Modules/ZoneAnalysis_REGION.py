
def ZoneAnalysis_REGION(SettingsDic):

    import MODZoneAnalysis
    import os
    
    diretorio=os.getcwd()
    
    # Análises das regioes com bacterias
    
    MODZoneAnalysis.DetVolume(diretorio,
                              importstackRootName='/ExportedData/Filtered',
                              FirstStack=1,LastStack=SettingsDic['timePoints'],
                              FirstSlice=1,LastSlice=SettingsDic['SliceNumber'],
                              TXTExportDir='/ExportedData/VolumeValues',
                              importformat=SettingsDic['imageFormat'],
                              RegionAnalysis=True)
            
    
    '''
    # Análises das regioes com EPS
    
    MODZoneAnalysis.DetVolume(diretorio,
                              importstackRootName='/BinarizedProc/EPS_THR4',
                              FirstStack=1,LastStack=15,
                              FirstSlice=1,LastSlice=123,
                              TXTExportDir='/VolumeValues/EPS_THR4',
                              importformat='.png',
                              RegionAnalysis=True)
    '''