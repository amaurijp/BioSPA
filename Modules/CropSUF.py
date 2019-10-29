    
def CropSUF(SettingsDic):

    import os
    import MODTopoAnalysis
    #import timeit
    
    diretorio=os.getcwd()
    
    #start2 = timeit.default_timer()

    
    MODTopoAnalysis.CropSUFwithBAC(diretorio,
                                   1,
                                   FirstSlice=1,LastSlice=SettingsDic['TOPOSliceNumber'],
                                   ImportstackRootName=SettingsDic['TOPOFolderName'],
                                   importFormat=SettingsDic['TOPOimageFormat'],
                                   ExportDir='/ExportedData/Topography',
                                   AreaBorderSize=5,
                                     
                                   ReferenceStackToCrop=SettingsDic['FolderName'],
                                   RefminArea=5,RefmaxArea=200,
                                   MAXElementsToCrop=10000)
    
    
    #stop2 = timeit.default_timer()
    
    #print('Tempo A', stop2 - start2)