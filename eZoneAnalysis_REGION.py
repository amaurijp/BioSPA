import MODZoneAnalysis
import os

diretorio=os.getcwd()

# Análises das regioes com bacterias

MODZoneAnalysis.DetVolume(diretorio,
                          importstackRootName='/BinarizedFiltered/bac',
                          FirstStack=1,LastStack=19,
                          FirstSlice=1,LastSlice=104,
                          TXTExportDir='/VolumeValues/bac',
                          importformat='.png',
                          RegionAnalysis=True,
                          FirstRegion=1,LastRegion=377)
       

# Análises das regioes com EPS

MODZoneAnalysis.DetVolume(diretorio,
                          importstackRootName='/BinarizedProc/EPS',
                          FirstStack=1,LastStack=19,
                          FirstSlice=1,LastSlice=104,
                          TXTExportDir='/VolumeValues/EPS',
                          importformat='.png',
                          RegionAnalysis=True,
                          FirstRegion=1,LastRegion=377)
