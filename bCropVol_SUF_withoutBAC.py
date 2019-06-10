import os
import MODTopoAnalysis
import timeit

diretorio=os.getcwd()

start2 = timeit.default_timer()

SUFstackNumber=1

MODTopoAnalysis.CropSUFwithoutBAC(diretorio,
                                  SUFstackNumber,
                                  FirstSlice=1,LastSlice=54,
                                  ImportstackRootName='/SUFAdjusted',
                                  importFormat='.png',
                                  ExportDir='/SUFAdjusted',
                                  MinLength=10,
                                  MaxLength=36,
                                  lengthStep=3,
                                  BacSubtractionMode=False,
                                  RefImgWithBAC='None')

        
stop2 = timeit.default_timer()

print('Tempo A', stop2 - start2)