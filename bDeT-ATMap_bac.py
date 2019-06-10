import os
import MODimageVolSel
import timeit

diretorio=os.getcwd()

start2 = timeit.default_timer()

StackList=list(range(1,19+1))
  
for stackNumber in StackList:
    MODimageVolSel.SelectionbyRange(diretorio,
                                    stackNumber,
                                    FirstSlice=1,LastSlice=104,
                                    Xmin=0,Xmax=1023,Ymin=0,Ymax=1023,
                                    minVolume=0,maxVolume=400000000,
                                    
                                    ImportstackRootName='/BinarizedCorr/bac',
                                    importFormat='.png',
                                    ExportDir='/BinarizedProc/bac',
                                    AreaBorderSize=5,
                                    Channel='bac',
                                 
                                    CropVolMode=False,
                                    ReferenceStackToCrop='/Binarized/bac/ImageJ/t19',
                                    RefminArea=5,RefmaxArea=4000,
                                    MAXElementsToCrop=1000,
                                 
                                    ColonyTimeCheckMode=True,
                                    ReferenceImgToCheckAttachment='/Binarized/bac/ImageJ/t14',
                                    ReferenceImgToCheckDetachment='/Binarized/bac/ImageJ/t1',
                                    RefminAreaCheck=5,RefmaxAreaCheck=4000,
                                    MAXElementsToCheck=10000,
                                    MaxTimePoint=19)
         
stop2 = timeit.default_timer()

print('Tempo A', stop2 - start2)