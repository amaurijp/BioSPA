import os
import MODTopoAnalysis


diretorio=os.getcwd()


#Análise das superfícies com bacterias
MODTopoAnalysis.TopographicAnalysisFunc(diretorio,
                                        SUFstackNumber=1,
                                        BACstackNumber=10,
                                        importstackRootName='/SUFAdjusted',
                                        FirstSlice=1,LastSlice=54,
                                        ZStep=0.41,
                                        heightValuetoGet=3,
                                        RegionAnalysis=True,
                                        BACFirstRegion=1, BACLastRegion=462,
                                        WithoutBACFirstRegion=1,WithoutBACLastRegion=30394,
                                        XYField=[319.45, 319.45],
                                        RawImageDefinition=[1024, 1024],
                                        MaxScaledAreaToConsider=36*36,
                                        
                                        Det_TopoXVol_relation = True)