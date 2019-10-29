import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import spatial
import numpy as np




#plot das posicoes
Fig1=plt.figure(figsize=(10, 4), dpi=100, facecolor='w', edgecolor='k')
g1=plt.subplot2grid((1,2),(0,0), rowspan=1, colspan=1, projection='3d')
g1.set_xlabel('x')
g1.set_ylabel('y')
g1.set_zlabel('z')
g2=plt.subplot2grid((1,2),(0,1), rowspan=1, colspan=1, projection='3d')
g2.set_xlabel('x')
g2.set_ylabel('y')
g2.set_zlabel('z')


# A matrix abaixo eh de teste e nao esta sendo usada

Stack=np.array(
                 [[[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
                        
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 1., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 1., 0., 2., 2., 2., 2., 2., 0.],
                   [ 0., 1., 0., 2., 2., 2., 2., 2., 0.],
                   [ 0., 1., 0., 2., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 2., 2., 2., 2., 2., 0.],
                   [ 0., 0., 2., 2., 2., 2., 2., 2., 0.],
                   [ 0., 0., 2., 2., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
        
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 1., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 1., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 1., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 1., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
        
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
                  
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 2., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
                   
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
                   
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 3., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 2., 2., 2., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
                   
                  [[ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [ 0., 0., 0., 0., 0., 0., 0., 0., 0.]]])

XLength=1
YLength=1
ZStep=1

VolumeList=[]
VolQHullRatioList=[]
VolErrorList=[]
AspectRatioList=[]


elementCount=1
for elementN in list(range(1, int(Stack.max())+1)):
    print('\n\n\n Analisando o elemento ', elementCount, '(total de ', int(Stack.max()), ') \n')
    
    PositionListP=[]
    
    Zmin=len(Stack)
    Zmax=0
    Ymin=len(Stack[0])
    Ymax=0
    Xmin=len(Stack[0, 0])
    Xmax=0
    
    for ZPos in list(range(len(Stack))):
        for YPos in list(range(len(Stack[ZPos]))):
            for XPos in list(range(len(Stack[ZPos, YPos]))):
                if Stack[ZPos, YPos, XPos] == elementN:
                                                
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

    if (Zmin-1) < 0 or (Zmax+1) > (len(Stack)-1) or (Ymin-1) < 0 or (Ymax+1) > (len(Stack[0])-1) or (Xmin-1) < 0 or (Xmax+1) > (len(Stack[0][0])-1):
            
        print('Indices fora da matrix. Excluindo esse elemento.')
        pass
    
    
    else:
        
        # Determinando todas as posicoes do elemento
        # Determinando as maiores distancias dos vertices do elemento                
        
        # Varredura em Z
        
        VolCount=0                
        ZMaxDistanceR=0
        
        for ZPos in list(range(len(Stack))):
            
            ZaxisPositionList=[]
            
            for YPos in list(range(len(Stack[0]))):
                for XPos in list(range(len(Stack[0, 0]))):
                    if Stack[ZPos, YPos, XPos] == elementN:
                        VolCount += 1
                        
                        if Stack[ZPos-1, YPos, XPos] == 0 or Stack[ZPos+1, YPos, XPos] == 0 or Stack[ZPos, YPos-1, XPos] == 0  or Stack[ZPos, YPos+1, XPos] == 0  or Stack[ZPos, YPos, XPos-1] == 0  or Stack[ZPos, YPos, XPos+1] == 0:                                   
                            
                            # Para a coleta de posicoes da varredura, soh os z- serao usados
                            
                            #[x+,y+,z+]
                            voxelVertex1=[(XPos + 1 + 1/2) * XLength, ((len(Stack[0])-YPos) + 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            PositionListP.append(voxelVertex1)
        
                            #[x+,y+,z-]
                            voxelVertex2=[(XPos + 1 + 1/2) * XLength, ((len(Stack[0])-YPos) + 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            PositionListP.append(voxelVertex2)
                            ZaxisPositionList.append(voxelVertex2)
        
                            #[x+,y-,z+]
                            voxelVertex3=[(XPos + 1 + 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            PositionListP.append(voxelVertex3)
        
                            #[x-,y+,z+]                        
                            voxelVertex4=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) + 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            PositionListP.append(voxelVertex4)
        
                            #[x-,y-,z+]                        
                            voxelVertex5=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            PositionListP.append(voxelVertex5)
        
                            #[x+,y-,z-]                        
                            voxelVertex6=[(XPos + 1 + 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            PositionListP.append(voxelVertex6)
                            ZaxisPositionList.append(voxelVertex6)
        
                            #[x-,y+,z-]                        
                            voxelVertex7=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) + 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            PositionListP.append(voxelVertex7)
                            ZaxisPositionList.append(voxelVertex7)
                            
                            #[x-,y-,z-]                        
                            voxelVertex8=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            PositionListP.append(voxelVertex8)
                            ZaxisPositionList.append(voxelVertex8)                                    
                            
            
            if len(ZaxisPositionList) > 1:
                ZDistanceList=spatial.distance.pdist(np.array(ZaxisPositionList))
                if ZDistanceList.max() > ZMaxDistanceR:
                    ZMaxDistanceR = ZDistanceList.max()


            print('Zmax', ZMaxDistanceR)
        
        
        # Em varredura em Y
        
        
        YMaxDistanceR=0
        
        for YPos in list(range(len(Stack[0]))):
            
            YaxisPositionList=[]
            
            for ZPos in list(range(len(Stack))):
                for XPos in list(range(len(Stack[0, 0]))):
                    if Stack[ZPos, YPos, XPos] == elementN:
                        
                        if Stack[ZPos-1, YPos, XPos] == 0 or Stack[ZPos+1, YPos, XPos] == 0 or Stack[ZPos, YPos-1, XPos] == 0  or Stack[ZPos, YPos+1, XPos] == 0  or Stack[ZPos, YPos, XPos-1] == 0  or Stack[ZPos, YPos, XPos+1] == 0:                                   

                            # Para a coleta de posicoes da varredura, soh os y- serao usados
                                            
                            #[x+,y-,z+]
                            voxelVertex3=[(XPos + 1 + 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            YaxisPositionList.append(voxelVertex3)
                
                            #[x-,y-,z+]                        
                            voxelVertex5=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            YaxisPositionList.append(voxelVertex5)
        
                            #[x+,y-,z-]                        
                            voxelVertex6=[(XPos + 1 + 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            YaxisPositionList.append(voxelVertex6)
                                    
                            #[x-,y-,z-]                        
                            voxelVertex8=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            YaxisPositionList.append(voxelVertex8)                                    
                            
            
            if len(YaxisPositionList) > 1:
                YDistanceList=spatial.distance.pdist(np.array(YaxisPositionList))
                if YDistanceList.max() > YMaxDistanceR:
                    YMaxDistanceR = YDistanceList.max()    
            
            print('Ymax', YMaxDistanceR)
        
        
        # Em varredura em X
        
        XMaxDistanceR=0
        
        for XPos in list(range(len(Stack[0, 0]))):
            
            XaxisPositionList=[]
            
            for ZPos in list(range(len(Stack))):
                for YPos in list(range(len(Stack[0]))):
                    if Stack[ZPos, YPos, XPos] == elementN:
                        
                        if Stack[ZPos-1, YPos, XPos] == 0 or Stack[ZPos+1, YPos, XPos] == 0 or Stack[ZPos, YPos-1, XPos] == 0  or Stack[ZPos, YPos+1, XPos] == 0  or Stack[ZPos, YPos, XPos-1] == 0  or Stack[ZPos, YPos, XPos+1] == 0:                                   

                            # Para a coleta de posicoes da varredura, soh os x- serao usados                        
        
                            #[x-,y+,z+]                        
                            voxelVertex4=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) + 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            XaxisPositionList.append(voxelVertex4)
        
                            #[x-,y-,z+]                        
                            voxelVertex5=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) + 1/2) * ZStep]
                            XaxisPositionList.append(voxelVertex5)
                
                            #[x-,y+,z-]                        
                            voxelVertex7=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) + 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            XaxisPositionList.append(voxelVertex7)
                            
                            #[x-,y-,z-]                        
                            voxelVertex8=[(XPos + 1 - 1/2) * XLength, ((len(Stack[0])-YPos) - 1/2) * YLength, ((len(Stack)-ZPos) - 1/2) * ZStep]
                            XaxisPositionList.append(voxelVertex8)                                    
                                                
            
            if len(XaxisPositionList) > 1:
                XDistanceList=spatial.distance.pdist(np.array(XaxisPositionList))
                if XDistanceList.max() > XMaxDistanceR:
                    XMaxDistanceR = XDistanceList.max()
            
            print('Xmax', XMaxDistanceR)
            
        
        # Convex Hull                
        hull = spatial.ConvexHull(PositionListP)        
        
        VolumeList.append([elementCount, hull.volume])
        VolQHullRatioList.append([elementCount, (VolCount*XLength*YLength*ZStep)/hull.volume])
        VolErrorList.append([elementCount, (hull.volume/(VolCount*YLength*YLength*ZStep)-1)*100])
        
        #Determinando a maior distancia dos vertices do elemento
        DistanceList=spatial.distance.pdist(np.array(PositionListP))
        MaxDistance=DistanceList.max()
        MinDistance=min([XMaxDistanceR,YMaxDistanceR,ZMaxDistanceR])
        
        AspectRatioList.append([elementCount, MaxDistance/MinDistance])                

        print('\n O elemento tem ', VolCount, ' pixels')
        print('\n (Pixel count) Volume do elemento ', elementCount, ' = ', (VolCount*YLength*YLength*ZStep))
        print('\n (qhull) Volume do elemento ', elementCount, ' = ', hull.volume)
        print('\n Erro no volume de ', (hull.volume/(VolCount*YLength*YLength*ZStep)-1)*100)
        print('\n A razao Vol/qhullVol eh = ', (VolCount*XLength*YLength*ZStep)/hull.volume)
        print('\n A razao de aspecto do elemento ', elementCount, ' = ', MaxDistance/MinDistance)
        
        
        g1.scatter(np.array(PositionListP)[:,0], np.array(PositionListP)[:,1], np.array(PositionListP)[:,2])       
        g2.scatter(np.array(PositionListP)[hull.vertices, 0], np.array(PositionListP)[hull.vertices, 1], np.array(PositionListP)[hull.vertices, 2])       
        
        elementCount +=1
       
plt.tight_layout()
plt.show()