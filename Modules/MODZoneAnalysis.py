import numpy as np
from skimage import io
import os


def DetVolume(diretorio,
              importstackRootName,
              FirstStack,LastStack,
              FirstSlice,LastSlice,
              TXTExportDir,
              importformat='.png',
              RegionAnalysis=False):
    
    StackList=list(range(FirstStack,LastStack+1))
    
    for stackNumber in StackList:
    
        if RegionAnalysis == False:
            
            print('\nCalculating the volume of stack ', str(stackNumber), ' \n')
            
            SliceRange=list(range(FirstSlice,LastSlice+1))
            
            imgList=[]
            for x in SliceRange:
                if x < 10:
                    a=io.imread(diretorio + importstackRootName + '/t' + str(stackNumber) + '/Slice00' + str(x) + importformat)
                    
                elif 10 <= x < 100:
                    a=io.imread(diretorio + importstackRootName + '/t' + str(stackNumber) + '/Slice0' + str(x) + importformat)
    
                elif 100 <= x < 1000:
                    a=io.imread(diretorio + importstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importformat)            

                imgList.append(a)    
                
            ImgArray3D=np.array(imgList)
            ImgArray3DNorm=np.where(ImgArray3D > ImgArray3D.mean(), 1, 0)
            
            print('The stack has ', len(ImgArray3D), 'positions on Z')
            print('The stack has ', len(ImgArray3D[0]), 'positions on Y')
            print('The stack has ', len(ImgArray3D[0][0]), 'positions on X')
                    
            if not os.path.exists(diretorio + TXTExportDir):
                os.makedirs(diretorio + TXTExportDir)
        
            fileXport1=open(diretorio + TXTExportDir + '/FullVolume_t' + str(stackNumber) + '.txt','w')
            fileXport1.write(str(ImgArray3DNorm.sum()))
            fileXport1.close()
    
        if RegionAnalysis == True:       
            
            LastRegion = len(os.listdir(diretorio + '/ExportedData/Filtered/t1/CropRegions'))
            RegionRange=list(range(1,LastRegion+1))
            
            for region in RegionRange:            
                
                print('\nDetermining the volume of region: ', region, '; Timepoint: ', stackNumber)
                
                SliceRange=list(range(FirstSlice,LastSlice+1))
                
                imgList=[]
                for SliceN in SliceRange:
                    aaf1=io.imread(diretorio + importstackRootName + '/t' + str(stackNumber) + '/CropRegions/Region' + str(region) + '/Slice' + str(SliceN) + importformat)
                    imgList.append(aaf1)
                            
                ImgArray3D=np.array(imgList)
                ImgArray3DNorm=np.where(ImgArray3D > ImgArray3D.mean(), 1, 0)
                
                print('The stack has ', len(ImgArray3D), 'positions on Z')
                print('The stack has ', len(ImgArray3D[0]), 'positions on Y')
                print('The stack has ', len(ImgArray3D[0][0]), 'positions on X')
                                
                if not os.path.exists(diretorio + TXTExportDir + '/Region' + str(region)):
                    os.makedirs(diretorio + TXTExportDir + '/Region' + str(region))
            
                fileXport1=open(diretorio + TXTExportDir + '/Region' + str(region) + '/Volume_t' + str(stackNumber) + '.txt','w')
                fileXport1.write(str(ImgArray3DNorm.sum()))
                fileXport1.close()
                      