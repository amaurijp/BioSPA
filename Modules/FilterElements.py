
def FilterElements(SettingsDic):

    import MODimageVolSel
    import os
    
    diretorio=os.getcwd()
    
    stackList=list(range(1,SettingsDic['timePoints'] + 1))
    
    for stackNumber in stackList:
        MODimageVolSel.SelectionInnerElements(diretorio,
                                              stackNumber,
                                              FirstSlice=1,LastSlice=SettingsDic['SliceNumber'],
                                              ImportstackRootName=SettingsDic['FolderName'],
                                              ImageBaseName=SettingsDic['ImageBaseName'],
                                              importFormat=SettingsDic['imageFormat'],
                                              ExportDir='/ExportedData/Filtered',
                                              RegionAnalysis=True)