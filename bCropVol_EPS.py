import os
import MODimageVolSel
import timeit

diretorio=os.getcwd()

start2 = timeit.default_timer()

StackList=list(range(16,19+1))
  
for stackNumber in StackList:
    MODimageVolSel.SelectionbyRange(diretorio,
                                    stackNumber,
                                    FirstSlice=1,LastSlice=104,
                                    Xmin=0,Xmax=1023,Ymin=0,Ymax=1023,
                                    minVolume=0,maxVolume=400000000,
                                    
                                    ImportstackRootName='/BinarizedCorr/EPS',
                                    importFormat='.png',
                                    ExportDir='/BinarizedProc/EPS',
                                    AreaBorderSize=5,
                                    Channel='EPS',
                                     
                                    CropVolMode=True,
                                    ReferenceStackToCrop='/Binarized/bac/ImageJ/t19',
                                    RefminArea=5,RefmaxArea=4000,
                                    MAXElementsToCrop=1000)
         
stop2 = timeit.default_timer()

print('Tempo A', stop2 - start2)