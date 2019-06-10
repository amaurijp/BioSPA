from scipy import spatial
from skimage import morphology
from skimage import io
import numpy as np
import os
    

def ShapeAnalysis(diretorio,
                  stackNumber,
                  importstackRootName,
                  FirstRegion,LastRegion,
                  FirstSlice,LastSlice,
                  ZStep=1,
                  XYField=[100,100],
                  RawImageDefinition=[500,500],
                  importFormat='.png',
                  Channel='bac',
                  SmallestVolumeToConsider=1,
                  
                  CalculateAspectRatio=False,
                  CalculateQhullRatio=True):

    
    RegionList=list(range(FirstRegion,LastRegion+1))
    SliceRange=list(range(FirstSlice,LastSlice+1))

    YLength =  (XYField[0]/RawImageDefinition[0])
    XLength =  (XYField[1]/RawImageDefinition[1])
        
    print('\n Importando as Imagens... \n')
    
    elementCount=1
    for Region in RegionList:
        
        ImgList1=[]
        for x in SliceRange:
            a=io.imread(diretorio + importstackRootName + '/' + Channel + '/t' + str(stackNumber) + '/CropRegions/Region' + str(Region) + '/Slice' + str(x) + importFormat)
                  
            ImgList1.append(a)
        
        ImgArray3D=np.array(ImgList1)
        
        print('O stack tem ', len(ImgArray3D),' slices')
        print('A imagem tem ', len(ImgArray3D[0]),' linhas')
        print('A imagem tem ', len(ImgArray3D[0][0]),' colunas')
        print('O maior valor do stack eh ', ImgArray3D.max())
        
        try:
            print('A imagem tem ',len(ImgArray3D[0][0][0]),' canais')
        
        except TypeError:         
            print('A imagem soh tem 1 canal')
    
        
        StackNorm=np.where(ImgArray3D > 0, 1, 0)
        RefStackLab=morphology.label(StackNorm, connectivity=2)
        print('O numero de elementos do stack eh ', RefStackLab.max())
        
        
        for elementN in list(range(1, int(RefStackLab.max())+1)):
            print('\n\n\n Analisando o elemento ', elementCount, '(total de ', int(RefStackLab.max()), ') \n')
            
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
                    
                print('Indices fora da matrix. Excluindo esse elemento.')
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
                        
                        AspectRatioVal=[elementCount, MaxDistance/MinDistance]    
                        
                        print('\n A razao de aspecto do elemento ', elementCount, ' = ', MaxDistance/MinDistance)
                    
                        File1=open(diretorio + '/Shape' + '/AspRatio_t' + str(stackNumber) + '.txt', 'a')
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
                        
        
                        print('\n O elemento tem ', VolCount, ' pixels')
                        print('\n (Pixel count) Volume do elemento ', elementCount, ' = ', (VolCount*YLength*YLength*ZStep))
                        print('\n (qhull) Volume do elemento ', elementCount, ' = ', hull.volume)
                        print('\n Erro no volume de ', (hull.volume/(VolCount*YLength*YLength*ZStep)-1)*100)
                        print('\n A razao Vol/qhullVol eh = ', (VolCount*XLength*YLength*ZStep)/hull.volume)
    
                        if not os.path.exists(diretorio + '/Shape'):
                            os.makedirs(diretorio + '/Shape')
                        
                        File2=open(diretorio + '/Shape' + '/Volume_t' + str(stackNumber) + '.txt', 'a')
                        File3=open(diretorio + '/Shape' + '/VolQhullRatio_t' + str(stackNumber) + '.txt', 'a')
                        File4=open(diretorio + '/Shape' + '/QhullVolRatio_t' + str(stackNumber) + '.txt', 'a')
                        File5=open(diretorio + '/Shape' + '/VolumeError_t' + str(stackNumber) + '.txt', 'a')
                    
                
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
                    print('\n\n\nAtivar um dos modos de análise\n\n\nEncerrando o calculo...')
                
                elif CalculateAspectRatio == True and CalculateQhullRatio == True:
                    print('\n\n\nApenas um dos modos de análise deve ser ativado\n\n\nEncerrando o calculo...')       