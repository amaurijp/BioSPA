import MODShapeAnalysis
import os

diretorio=os.getcwd()

stackList=list(range(1,19+1))

for Stack in stackList:
    MODShapeAnalysis.ShapeAnalysis(diretorio,
                                   stackNumber=Stack,
                                   importstackRootName='/BinarizedProc',
                                   FirstRegion=1,LastRegion=377,
                                   FirstSlice=1,LastSlice=104,
                                   ZStep=0.4,
                                   XYField=[319.45,319.45],
                                   RawImageDefinition=[1024,1024],
                                   importFormat='.png',
                                   Channel='bac',
                                   SmallestVolumeToConsider=5,
                                   
                                   CalculateAspectRatio=True,
                                   CalculateQhullRatio=True)

