import MODimageVolSel
import os

diretorio=os.getcwd()

stackList=list(range(1,19+1))

for stackNumber in stackList:
    MODimageVolSel.SelectionInnerElements(diretorio,
                                          stackNumber,
                                          FirstSlice=1,LastSlice=104,
                                          ImportstackRootName='/BinarizedProc/bac',
                                          importFormat='.png',
                                          ExportDir='/BinarizedFiltered/bac',
                                          RegionAnalysis=True,
                                          FirstRegion=1,LastRegion=377)