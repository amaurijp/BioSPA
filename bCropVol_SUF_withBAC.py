import os
import MODTopoAnalysis
import timeit

diretorio=os.getcwd()

start2 = timeit.default_timer()

SUFstackNumber=1
BACstackNumber=10
                               
MODTopoAnalysis.CropSUFwithBAC(diretorio,
                               SUFstackNumber,
                               BACstackNumber,
                               FirstSlice=1,LastSlice=54,
                               ImportstackRootName='/SUFAdjusted',
                               importFormat='.png',
                               ExportDir='/SUFAdjusted',
                               AreaBorderSize=5,
                                 
                               ReferenceStackToCrop='/Binarized/bac/ImageJ/t' + str(BACstackNumber),
                               RefminArea=5,RefmaxArea=200,
                               MAXElementsToCrop=10000,
                               
                               Det_TopoXVol_relation=True,
                               ImportstackRootName_DetVol='/BinarizedCorr/bac')

'''
BACstackNumber=2
                               
MODTopoAnalysis.CropSUFwithBAC(diretorio,
                               SUFstackNumber,
                               BACstackNumber,
                               FirstSlice=1,LastSlice=54,
                               ImportstackRootName='/SUFAdjusted',
                               importFormat='.png',
                               ExportDir='/SUFAdjusted',
                               AreaBorderSize=5,
                                 
                               ReferenceStackToCrop='/Binarized/bac/ImageJ/t' + str(BACstackNumber),
                               RefminArea=5,RefmaxArea=200,
                               MAXElementsToCrop=10000,
                               
                               Det_TopoXVol_relation=False,
                               ImportstackRootName_DetVol='/BinarizedCorr/bac')
    
stop2 = timeit.default_timer()

print('Tempo A', stop2 - start2)
'''