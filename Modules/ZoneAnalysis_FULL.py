
def ZoneAnalysis_FULL(SettingsDic):

    import MODZoneAnalysis
    import os
    
    diretorio=os.getcwd()
    
    # Análises das regioes com bacterias
    
    MODZoneAnalysis.DetVolume(diretorio,
                              importstackRootName=SettingsDic['FolderName'],
                              FirstStack=1,LastStack=SettingsDic['timePoints'],
                              FirstSlice=1,LastSlice=SettingsDic['SliceNumber'],
                              TXTExportDir='/ExportedData/VolumeValues',
                              importformat=SettingsDic['imageFormat'],
                              RegionAnalysis=False)
            
    
    '''
    # Análises das regioes com EPS
    
    MODZoneAnalysis.DetVolume(diretorio,
                              importstackRootName='/BinarizedCorr/EPS_THR4',
                              FirstStack=1,LastStack=18,
                              FirstSlice=1,LastSlice=123,
                              TXTExportDir='/VolumeValues/EPS_THR4',
                              importformat='.png',
                              RegionAnalysis=False)
    '''