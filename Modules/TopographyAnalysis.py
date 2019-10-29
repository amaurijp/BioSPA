
def TopographyAnalysis(SettingsDic):

    import os
    import MODTopoAnalysis
    
    
    diretorio=os.getcwd()
    
    
    #Análise das superfícies com bacterias
    MODTopoAnalysis.TopographicAnalysisFunc(diretorio,
                                            BACstackNumber=1,
                                            importstackRootName='/ExportedData/Topography',
                                            FirstSlice=1,LastSlice=SettingsDic['TOPOSliceNumber'],
                                            ZStep=SettingsDic['TOPOZstep'],
                                            heightValuetoGet=3,
                                            RegionAnalysis=True,
                                            XYField=[SettingsDic['height_field'], SettingsDic['width_field']],
                                            RawImageDefinition=[SettingsDic['height'] + 1, SettingsDic['width'] + 1],
                                            MaxScaledAreaToConsider=int(0.30 * SettingsDic['width']) * int(0.30 * SettingsDic['width']),
                                            
                                            Det_TopoXVol_relation = False)