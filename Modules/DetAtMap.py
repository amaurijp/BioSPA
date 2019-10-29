
def DetAtMap(SettingsDic):

    import os
    import MODimageVolSel
    #import timeit
    
    diretorio=os.getcwd()
    
    #start2 = timeit.default_timer()
    
    StackList=list(range(1, SettingsDic['timePoints'] + 1))
      
    for stackNumber in StackList:
        MODimageVolSel.SelectionbyRange(diretorio,
                                        stackNumber,
                                        FirstSlice=1,LastSlice=SettingsDic['SliceNumber'],
                                        Xmin=0,Xmax=SettingsDic['width'],Ymin=0,Ymax=SettingsDic['height'],
                                        minVolume=0,maxVolume=400000000,
                                        
                                        ImportstackRootName=SettingsDic['FolderName'],
                                        ImageBaseName=SettingsDic['ImageBaseName'],
                                        importFormat=SettingsDic['imageFormat'],
                                        ExportDir='/ExportedData/Cropped',
                                        AreaBorderSize=5,
                                     
                                        CropVolMode=False,
                                        ReferenceStackToCrop=SettingsDic['FolderName']  + '/t' + str(SettingsDic['timePoints']),
                                        RefminArea=5,RefmaxArea=100000,
                                        MAXElementsToCrop=10000,
                                     
                                        ColonyTimeCheckMode=True,
                                        ReferenceImgToCheckAttachment=SettingsDic['FolderName']  + '/t' + str(SettingsDic['timePoints']),
                                        ReferenceImgToCheckDetachment=SettingsDic['FolderName']  + '/t1',
                                        RefminAreaCheck=5,RefmaxAreaCheck=100000,
                                        MAXElementsToCheck=100000,
                                        MaxTimePoint=SettingsDic['timePoints'])
             
    #stop2 = timeit.default_timer()
    
    #print('Tempo A', stop2 - start2)