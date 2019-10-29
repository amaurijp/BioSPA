
def CropSUF_w(SettingsDic):

    import os
    import MODTopoAnalysis
    #import timeit
    
    diretorio=os.getcwd()
    
    #start2 = timeit.default_timer()
        
    MODTopoAnalysis.CropSUFwithoutBAC(diretorio,
                                      FirstSlice=1,LastSlice=89,
                                      ImportstackRootName=SettingsDic['TOPOFolderName'],
                                      importFormat=SettingsDic['TOPOimageFormat'],
                                      ExportDir='/ExportedData/Topography',
                                      MinLength= int(0.02 * SettingsDic['width']),
                                      MaxLength= int(0.30 * SettingsDic['width']),
                                      lengthStep= int(0.01 * SettingsDic['width']),
                                      BacSubtractionMode=False,
                                      RefImgWithBAC='None')
    
            
    #stop2 = timeit.default_timer()
    
    #print('Tempo A', stop2 - start2)