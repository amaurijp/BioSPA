from scipy import spatial
from skimage import morphology
from skimage import io
import numpy as np
import os
    

def ShapeAnalysis(diretorio,
                  stackNumber=1,
                  importstackRootName='',
                  FirstSlice=1,LastSlice=2,
                  ZStep=1,
                  XYField=[100,100],
                  RawImageDefinition=[500,500],
                  importFormat='.png',
                  SmallestVolumeToConsider=1,
                  
                  CalculateAspectRatio=False,
                  CalculateQhullRatio=True):

    
    LastRegion = len(os.listdir(diretorio + '/ExportedData/Filtered/t1/CropRegions'))
    RegionList=list(range(1,LastRegion+1))
    SliceRange=list(range(1,LastSlice+1))

    YLength =  (XYField[0]/RawImageDefinition[0])
    XLength =  (XYField[1]/RawImageDefinition[1])
        
    print('\nImporting images... \n')
    
    elementCount=1
    for Region in RegionList:
        
        print('\nAnalysing region ', Region)
        
        ImgList1=[]
        for x in SliceRange:
            a=io.imread(diretorio + importstackRootName + '/t' + str(stackNumber) + '/CropRegions/Region' + str(Region) + '/Slice' + str(x) + importFormat)
                  
            ImgList1.append(a)
        
        ImgArray3D=np.array(ImgList1)
        
        print('The stack has ', len(ImgArray3D),' slices')
        print('The stack has ', len(ImgArray3D[0]),' lines')
        print('The stack has ', len(ImgArray3D[0][0]),' columns')
        print('The largest value in the stack is ', ImgArray3D.max())
        
        try:
            print('The images has ',len(ImgArray3D[0][0][0]),' channels')
        
        except TypeError:         
            print('The image has only 1 channel')
    
        
        StackNorm=np.where(ImgArray3D > 0, 1, 0)
        RefStackLab=morphology.label(StackNorm, connectivity=2)
        print('The number of elements in the stack is ', RefStackLab.max())
        
        
        for elementN in list(range(1, int(RefStackLab.max())+1)):
            print('\n\n\nAnalysing element ', elementCount, ' (total of ', int(RefStackLab.max()), ') \n')
            
            PositionListP=[]
            
            Zmin=len(RefStackLab)
            Zmax=0
            Ymin=len(RefStackLab[0])
            Ymax=0
            Xmin=len(RefStackLab[0, 0])
            Xmax=0
            
            for ZPos in list(range(len(RefStackLab))):
                for YPos in list(range(len(RefStackLab[ZPos]))):
                    for XPos in list(range(len(RefStackLab[ZPos, YPos]))):
                        if RefStackLab[ZPos, YPos, XPos] == elementN:
                                                        
                            if XPos < Xmin:
                                Xmin = XPos
                            if XPos > Xmax:
                                Xmax = XPos
                            if YPos < Ymin:
                                Ymin = YPos
                            if YPos > Ymax:
                                Ymax = YPos
                            if ZPos < Zmin:
                                Zmin = ZPos
                            if ZPos > Zmax:
                                Zmax = ZPos
    
            if (Zmin-1) < 0 or (Zmax+1) > (len(RefStackLab)-1) or (Ymin-1) < 0 or (Ymax+1) > (len(RefStackLab[0])-1) or (Xmin-1) < 0 or (Xmax+1) > (len(RefStackLab[0][0])-1):
                    
                print('Indexes out of the matrix. Excluding element.')
                pass
            
            
            else:
                
                # Determinando todas as posicoes do elemento
                # Determinando as maiores distancias dos vertices do elemento                
                
                # Varredura em Z
                
                VolCount=0                
                ZMaxDistanceR=0
                
                for ZPos in list(range(len(RefStackLab))):
                    
                    ZaxisPositionList=[]
                    
                    for YPos in list(range(len(RefStackLab[0]))):
                        for XPos in list(range(len(RefStackLab[0, 0]))):
                            if RefStackLab[ZPos, YPos, XPos] == elementN:
                                VolCount += 1
                                
                                if RefStackLab[ZPos-1, YPos, XPos] == 0 or RefStackLab[ZPos+1, YPos, XPos] == 0 or RefStackLab[ZPos, YPos-1, XPos] == 0  or RefStackLab[ZPos, YPos+1, XPos] == 0  or RefStackLab[ZPos, YPos, XPos-1] == 0  or RefStackLab[ZPos, YPos, XPos+1] == 0:
    
                                    # Para a coleta de posicoes da varredura, soh os z- serao usados
                                    
                                    #[x+,y+,z+]
                                    voxelVertex1=[(XPos + 1 + 1/2) * XLength, ((len(RefStackLab[0])-YPos) + 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                    PositionListP.append(voxelVertex1)
                
                                    #[x+,y+,z-]
                                    voxelVertex2=[(XPos + 1 + 1/2) * XLength, ((len(RefStackLab[0])-YPos) + 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                    PositionListP.append(voxelVertex2)
                
                                    #[x+,y-,z+]
                                    voxelVertex3=[(XPos + 1 + 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                    PositionListP.append(voxelVertex3)
                
                                    #[x-,y+,z+]                        
                                    voxelVertex4=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) + 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                    PositionListP.append(voxelVertex4)
                
                                    #[x-,y-,z+]                        
                                    voxelVertex5=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                    PositionListP.append(voxelVertex5)
                
                                    #[x+,y-,z-]                        
                                    voxelVertex6=[(XPos + 1 + 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                    PositionListP.append(voxelVertex6)
                
                                    #[x-,y+,z-]                        
                                    voxelVertex7=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) + 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                    PositionListP.append(voxelVertex7)
                                    
                                    #[x-,y-,z-]                        
                                    voxelVertex8=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                    PositionListP.append(voxelVertex8)                                 
                                    
                                    if CalculateAspectRatio == True:
                    
                                        ZaxisPositionList.append(voxelVertex2)
                                        ZaxisPositionList.append(voxelVertex6)
                                        ZaxisPositionList.append(voxelVertex7)
                                        ZaxisPositionList.append(voxelVertex8)
                   
                if CalculateAspectRatio == True and CalculateQhullRatio == False:
                    
                    if len(ZaxisPositionList) > 1:                    
                        
                        ZDistanceList=spatial.distance.pdist(np.array(ZaxisPositionList))
                        if ZDistanceList.max() > ZMaxDistanceR:
                            ZMaxDistanceR = ZDistanceList.max()
        
                    #print('Zmax', ZMaxDistanceR)
                            
                    

                    # Em varredura em Y
                    
                    YMaxDistanceR=0
                    
                    for YPos in list(range(len(RefStackLab[0]))):
                        
                        YaxisPositionList=[]
                        
                        for ZPos in list(range(len(RefStackLab))):
                            for XPos in list(range(len(RefStackLab[0, 0]))):
                                if RefStackLab[ZPos, YPos, XPos] == elementN:
                                    
                                    if RefStackLab[ZPos-1, YPos, XPos] == 0 or RefStackLab[ZPos+1, YPos, XPos] == 0 or RefStackLab[ZPos, YPos-1, XPos] == 0  or RefStackLab[ZPos, YPos+1, XPos] == 0  or RefStackLab[ZPos, YPos, XPos-1] == 0  or RefStackLab[ZPos, YPos, XPos+1] == 0:                                   
        
                                        # Para a coleta de posicoes da varredura, soh os y- serao usados
                                                        
                                        #[x+,y-,z+]
                                        voxelVertex3=[(XPos + 1 + 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                        YaxisPositionList.append(voxelVertex3)
                            
                                        #[x-,y-,z+]                        
                                        voxelVertex5=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                        YaxisPositionList.append(voxelVertex5)
                    
                                        #[x+,y-,z-]                        
                                        voxelVertex6=[(XPos + 1 + 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                        YaxisPositionList.append(voxelVertex6)
                                                
                                        #[x-,y-,z-]                        
                                        voxelVertex8=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                        YaxisPositionList.append(voxelVertex8)                                    
                                        
                        
                        if len(YaxisPositionList) > 1:
                            YDistanceList=spatial.distance.pdist(np.array(YaxisPositionList))
                            if YDistanceList.max() > YMaxDistanceR:
                                YMaxDistanceR = YDistanceList.max()    
                        
                        #print('Ymax', YMaxDistanceR)    
                    
                    
                    
                    # Em varredura em X
                    
                    XMaxDistanceR=0
                    
                    for XPos in list(range(len(RefStackLab[0, 0]))):
                        
                        XaxisPositionList=[]
                        
                        for ZPos in list(range(len(RefStackLab))):
                            for YPos in list(range(len(RefStackLab[0]))):
                                if RefStackLab[ZPos, YPos, XPos] == elementN:
                                    
                                    if RefStackLab[ZPos-1, YPos, XPos] == 0 or RefStackLab[ZPos+1, YPos, XPos] == 0 or RefStackLab[ZPos, YPos-1, XPos] == 0  or RefStackLab[ZPos, YPos+1, XPos] == 0  or RefStackLab[ZPos, YPos, XPos-1] == 0  or RefStackLab[ZPos, YPos, XPos+1] == 0:                                   
        
                                        # Para a coleta de posicoes da varredura, soh os x- serao usados                        
                    
                                        #[x-,y+,z+]                        
                                        voxelVertex4=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) + 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                        XaxisPositionList.append(voxelVertex4)
                    
                                        #[x-,y-,z+]                        
                                        voxelVertex5=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) + 1/2) * ZStep]
                                        XaxisPositionList.append(voxelVertex5)
                            
                                        #[x-,y+,z-]                        
                                        voxelVertex7=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) + 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                        XaxisPositionList.append(voxelVertex7)
                                        
                                        #[x-,y-,z-]                        
                                        voxelVertex8=[(XPos + 1 - 1/2) * XLength, ((len(RefStackLab[0])-YPos) - 1/2) * YLength, ((len(RefStackLab)-ZPos) - 1/2) * ZStep]
                                        XaxisPositionList.append(voxelVertex8)                                    
                                                            
                        
                        if len(XaxisPositionList) > 1:
                            XDistanceList=spatial.distance.pdist(np.array(XaxisPositionList))
                            if XDistanceList.max() > XMaxDistanceR:
                                XMaxDistanceR = XDistanceList.max()
                        
                        #print('Xmax', XMaxDistanceR)

                    
                    if VolCount > SmallestVolumeToConsider:
                        
                        #Determinando a maior distancia dos vertices do elemento
                        DistanceList=spatial.distance.pdist(np.array(PositionListP))
                        MaxDistance=DistanceList.max()
                        MinDistance=min([XMaxDistanceR,YMaxDistanceR,ZMaxDistanceR])            
                        
                        if MinDistance == 0:
                            AspectRatioVal=[elementCount, MaxDistance/1]
                        
                        elif MinDistance != 0:
                            AspectRatioVal=[elementCount, MaxDistance/MinDistance]                        
                        
                        print('\nAspect ratio of the element is ', elementCount, ' = ', AspectRatioVal)

                        if not os.path.exists(diretorio + '/ExportedData/Shape'):
                            os.makedirs(diretorio + '/ExportedData/Shape')
                        
                        if not os.path.exists(diretorio + '/ExportedData/Shape' + '/AspRatio_t' + str(stackNumber) + '.txt'):
                            with open(diretorio + '/ExportedData/Shape' + '/AspRatio_t' + str(stackNumber) + '.txt', 'w') as file:
                                file.close()
                    
                        File1=open(diretorio + '/ExportedData/Shape' + '/AspRatio_t' + str(stackNumber) + '.txt', 'a')
                        File1.write(str(AspectRatioVal) + '\n')
                        File1.close()
    
                        elementCount += 1                    
                
                elif CalculateAspectRatio == False and CalculateQhullRatio == True:
                    # Convex Hull                
                    hull = spatial.ConvexHull(PositionListP)        
                    
                    if VolCount > SmallestVolumeToConsider:
                    
                        VolumeVal=[elementCount, (VolCount*YLength*YLength*ZStep)]
                        VolQHullRatioVal=[elementCount, (VolCount*XLength*YLength*ZStep)/hull.volume]
                        QHullVolRatioVal=[elementCount, hull.volume/(VolCount*XLength*YLength*ZStep)]
                        VolErrorVal=[elementCount, (hull.volume/(VolCount*YLength*YLength*ZStep)-1)*100]
                        
        
                        print('\nThe element has ', VolCount, ' pixels')
                        print('\n(Pixel count) Element volume ', elementCount, ' = ', (VolCount*YLength*YLength*ZStep))
                        print('\n(qhull) Element volume ', elementCount, ' = ', hull.volume)
                        print('\nVolume error of ', (hull.volume/(VolCount*YLength*YLength*ZStep)-1)*100)
                        print('\nVol/qhullVol ratio = ', (VolCount*XLength*YLength*ZStep)/hull.volume)
    
                        if not os.path.exists(diretorio + '/ExportedData/Shape'):
                            os.makedirs(diretorio + '/ExportedData/Shape')
                        
                        if not os.path.exists(diretorio + '/ExportedData/Shape' + '/Volume_t' + str(stackNumber) + '.txt'):
                            with open(diretorio + '/ExportedData/Shape' + '/Volume_t' + str(stackNumber) + '.txt', 'w') as file:
                                file.close()

                        if not os.path.exists(diretorio + '/ExportedData/Shape' + '/VolQhullRatio_t' + str(stackNumber) + '.txt'):
                            with open(diretorio + '/ExportedData/Shape' + '/VolQhullRatio_t' + str(stackNumber) + '.txt', 'w') as file:
                                file.close()

                        if not os.path.exists(diretorio + '/ExportedData/Shape' + '/QhullVolRatio_t' + str(stackNumber) + '.txt'):
                            with open(diretorio + '/ExportedData/Shape' + '/QhullVolRatio_t' + str(stackNumber) + '.txt', 'w') as file:
                                file.close()                        

                        if not os.path.exists(diretorio + '/ExportedData/Shape' + '/VolumeError_t' + str(stackNumber) + '.txt'):
                            with open(diretorio + '/ExportedData/Shape' + '/VolumeError_t' + str(stackNumber) + '.txt', 'w') as file:
                                file.close()

                        File2=open(diretorio + '/ExportedData/Shape' + '/Volume_t' + str(stackNumber) + '.txt', 'a')
                        File3=open(diretorio + '/ExportedData/Shape' + '/VolQhullRatio_t' + str(stackNumber) + '.txt', 'a')
                        File4=open(diretorio + '/ExportedData/Shape' + '/QhullVolRatio_t' + str(stackNumber) + '.txt', 'a')
                        File5=open(diretorio + '/ExportedData/Shape' + '/VolumeError_t' + str(stackNumber) + '.txt', 'a')
                    
                
                        File2.write(str(VolumeVal) + '\n')
                        File3.write(str(VolQHullRatioVal) + '\n')
                        File4.write(str(QHullVolRatioVal) + '\n')
                        File5.write(str(VolErrorVal) + '\n')      
                    
                        File2.close()
                        File3.close()
                        File4.close()
                        File5.close()
        
                        elementCount += 1
                        
                
                elif CalculateAspectRatio == False and CalculateQhullRatio == False:
                    print('\n\n\nClosing...')
                
                elif CalculateAspectRatio == True and CalculateQhullRatio == True:
                    print('\n\n\nClosing...')       