import numpy as np
from skimage import io
import os


def DetVolume(diretorio,
              importstackRootName,
              FirstStack,LastStack,
              FirstSlice,LastSlice,
              TXTExportDir,
              importformat='.png',
              RegionAnalysis=False,
              FirstRegion=1,LastRegion=2):
    
    StackList=list(range(FirstStack,LastStack+1))
    
    for stackNumber in StackList:
    
        if RegionAnalysis == False:
            
            print('\n Calculando o volume do Stack ', str(stackNumber), ' \n')
            
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
            
            print('O imageStack tem ', len(ImgArray3D), 'posições em Z')
            print('O imageStack tem ', len(ImgArray3D[0]), 'posições em Y')
            print('O imageStack tem ', len(ImgArray3D[0][0]), 'posições em X')
                    
            if not os.path.exists(diretorio + TXTExportDir):
                os.makedirs(diretorio + TXTExportDir)
        
            fileXport1=open(diretorio + TXTExportDir + '/FullVolume_t' + str(stackNumber) + '.txt','w')
            fileXport1.write(str(ImgArray3DNorm.sum()))
            fileXport1.close()
    
        if RegionAnalysis == True:       
            RegionRange=list(range(FirstRegion,LastRegion+1))
            
            for region in RegionRange:            
                
                SliceRange=list(range(FirstSlice,LastSlice+1))
                
                imgList=[]
                for SliceN in SliceRange:
                    aaf1=io.imread(diretorio + importstackRootName + '/t' + str(stackNumber) + '/CropRegions/Region' + str(region) + '/Slice' + str(SliceN) + importformat)
                    imgList.append(aaf1)
                            
                ImgArray3D=np.array(imgList)
                ImgArray3DNorm=np.where(ImgArray3D > ImgArray3D.mean(), 1, 0)
                
                print('O imageStack tem ', len(ImgArray3D), 'posições em Z')
                print('O imageStack tem ', len(ImgArray3D[0]), 'posições em Y')
                print('O imageStack tem ', len(ImgArray3D[0][0]), 'posições em X')
                                
                if not os.path.exists(diretorio + TXTExportDir + '/Region' + str(region)):
                    os.makedirs(diretorio + TXTExportDir + '/Region' + str(region))
            
                fileXport1=open(diretorio + TXTExportDir + '/Region' + str(region) + '/Volume_t' + str(stackNumber) + '.txt','w')
                fileXport1.write(str(ImgArray3DNorm.sum()))
                fileXport1.close()
                      