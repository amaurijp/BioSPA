import MODZoneAnalysis
import os

diretorio=os.getcwd()

# Análises das regioes com bacterias

MODZoneAnalysis.DetVolume(diretorio,
                          importstackRootName='/BinarizedCorr/bac',
                          FirstStack=1,LastStack=25,
                          FirstSlice=1,LastSlice=104,
                          TXTExportDir='/VolumeValues/bac',
                          importformat='.png',
                          RegionAnalysis=False,
                          FirstRegion=1,LastRegion=335)
        

# Análises das regioes com EPS

MODZoneAnalysis.DetVolume(diretorio,
                          importstackRootName='/BinarizedCorr/EPS',
                          FirstStack=1,LastStack=25,
                          FirstSlice=1,LastSlice=104,
                          TXTExportDir='/VolumeValues/EPS',
                          importformat='.png',
                          RegionAnalysis=False,
                          FirstRegion=1,LastRegion=335)