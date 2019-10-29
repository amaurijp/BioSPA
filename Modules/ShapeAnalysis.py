
def ShapeAnalysis(SettingsDic):

    import MODShapeAnalysis
    import os
    
    diretorio=os.getcwd()
    
    stackList=list(range(1, SettingsDic['timePoints']+1))
    
    for Stack in stackList:
        MODShapeAnalysis.ShapeAnalysis(diretorio,
                                       stackNumber=Stack,
                                       importstackRootName='/ExportedData/Filtered',
                                       FirstSlice=1,LastSlice=SettingsDic['SliceNumber'],
                                       ZStep=SettingsDic['Zstep'],
                                       XYField=[SettingsDic['height_field'],SettingsDic['width_field']],
                                       RawImageDefinition=[SettingsDic['height'], SettingsDic['width']],
                                       importFormat=SettingsDic['imageFormat'],
                                       SmallestVolumeToConsider=5,
                                                                        
                                       CalculateAspectRatio=True,
                                       CalculateQhullRatio=False)
        
        
        MODShapeAnalysis.ShapeAnalysis(diretorio,
                                       stackNumber=Stack,
                                       importstackRootName='/ExportedData/Filtered',
                                       FirstSlice=1,LastSlice=SettingsDic['SliceNumber'],
                                       ZStep=SettingsDic['Zstep'],
                                       XYField=[SettingsDic['height_field'],SettingsDic['width_field']],
                                       RawImageDefinition=[SettingsDic['height'], SettingsDic['width']],
                                       importFormat=SettingsDic['imageFormat'],
                                       SmallestVolumeToConsider=5,
                                                                        
                                       CalculateAspectRatio=False,
                                       CalculateQhullRatio=True)