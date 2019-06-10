import MODAnalysisData
import os

diretorio=os.getcwd()


MODAnalysisData(ExperimentNumber = 2,
                            ImportRootFolderBAC='/VolumeValues/bac',
                            ImportRootFolderEPS='/VolumeValues/EPS',
                            FirstStack=2,LastStack=19,
                            initialTimePoint=20,
                            timeinterval=20,
                            ZStep=0.3,
                            XYField=[319.45,319.45],
                            RawImageDefinition=[1024,1024],
                            RegionAnalysis=True,
                            FirstRegion=1,Lastregion=362,
                            SmutansRadius=0.44, #em microns
                            Max_a_FitError=0.002,
                            Max_b_FitError=0.2,
                
                            p0_THR_val1=5,
                            p0_THR_val2=20,
                            
                            Det_TopoXVol_relation=True,
                            StackToFindRelation=10)
