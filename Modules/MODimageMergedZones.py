import os
import numpy as np
from skimage import io
from skimage import morphology
from skimage import measure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors

diretorio=os.getcwd()

def AnalyzeMergedZones(diretorio,
                       ImgRefRoot='/Binarized',
                       XYField=[319.45,319.45],
                       RawImageDefinition=[1024,1024],
                       ZStep=1,
                       ImportstackRootName='/Binarized',
                       importFormat='.png',
                       MergedRegion=1,
                       FirstStack=1,LastStack=2,
                       FirstSlice=1,LastSlice=2,
                       initialTimePoint=30,
                       timeinterval=30,

                       BACVol_ylim=800,
                       BACVel_ylim=800,
                       EPSVol_ylim=800,
                       EPSVel_ylim=800):
    
    StackList=list(range(FirstStack,LastStack+1))
    SliceRange=list(range(FirstSlice,LastSlice+1))
    
    print('\n Encontrando as regioes para calcular \n')
    
    LengthPixelRatio= XYField[0]/RawImageDefinition[0]
    VoxelVal = ZStep * (XYField[0]/RawImageDefinition[0]) * (XYField[1]/RawImageDefinition[1])    

    ImgZProj1=io.imread(diretorio + ImgRefRoot + '/bac' + '/ZProjection_t18' + importFormat, dtype='i4')        
    ImgZProj2=io.imread(diretorio + ImgRefRoot + '/bac' + '/ZProjection_t15' + importFormat, dtype='i4')
    ImgZProj3=io.imread(diretorio + ImgRefRoot + '/bac' + '/ZProjection_t10' + importFormat, dtype='i4')
    ImgZProj4=io.imread(diretorio + ImgRefRoot + '/bac' + '/ZProjection_t5' + importFormat, dtype='i4')
    ImgZProj5=io.imread(diretorio + ImgRefRoot + '/bac' + '/ZProjection_t2' + importFormat, dtype='i4')
    ImgZProjF1=ImgZProj1 + ImgZProj2 + ImgZProj3 + ImgZProj4 + ImgZProj5
    ImgZProjF2=(ImgZProjF1/ImgZProjF1.max())*255

    
    # Plot Imagens
    #Figura 1 - Grid
    fig1=plt.figure(figsize=(12, 7), facecolor='w', edgecolor='k')
    plt.subplots_adjust(wspace=1.5, hspace=0.6)
    
    #Mapa 1
    map1=plt.subplot2grid((2,3),(0,0),rowspan=1,colspan=1)    
    map1axi=map1.imshow(ImgZProjF2, alpha=0.8, cmap='jet') 
    map1.set_title('Colony merging',fontsize=11)
    map1.tick_params(which='both',
                 bottom='off', labelbottom='on',
                 top='off', labeltop='off',
                 left='off', labelleft='on', 
                 right='off', labelright='off',
                 labelsize=11)
    
    map1.set_xlabel('$\\mu$m', fontsize=11)
    map1.set_xticks([0, int(ImgZProjF2.shape[1]/2), ImgZProjF2.shape[1]])
    map1.set_xticklabels([str(0), str(int((ImgZProjF2.shape[1]/2) * LengthPixelRatio)), str(int(ImgZProjF2.shape[1] * LengthPixelRatio))])
    map1.set_yticks([0,int(ImgZProjF2.shape[0]/2), ImgZProjF2.shape[0]])
    map1.set_yticklabels([str(int(ImgZProjF2.shape[0] * LengthPixelRatio)), str(int((ImgZProjF2.shape[0]/2) * LengthPixelRatio)), str(0)])

    Colbar1=fig1.colorbar(map1axi, fraction=0.04, 
                          pad=0.08, orientation='vertical',
                          ticks=list(np.arange(0, ImgZProjF2.max()+1, int(ImgZProjF2.max()/5))))
    Colbar1.set_label('time (min)', fontsize=11)
    Colbar1.set_ticklabels(['B']+[str(i) for i in [510,420,270,120,30]])
    Colbar1.ax.tick_params(labelsize=11)

    
    #Mapa 2
    ImgRef1a=io.imread(diretorio + ImgRefRoot + '/bac' + '/ConvexHull1' + importFormat)
    ImgRef1b=morphology.label(ImgRef1a, connectivity=1)
    ImgRef1Props=measure.regionprops(ImgRef1b)
    
    CentroidList=[]
    for elementN in list(range(ImgRef1b.max())):
        CentroidList.append([ImgRef1Props[elementN].centroid[0], ImgRef1Props[elementN].centroid[1]])
    
    ImgConvex1a=io.imread(diretorio + ImgRefRoot + '/bac' + '/ConvexHull2' + importFormat)    
    ImgConvex1b=morphology.convex_hull_object(ImgConvex1a)
    ImgConvex2=np.where(ImgConvex1b == True, 1, 0)
    ImgConvex3=morphology.label(ImgConvex2, connectivity=1)    
    
    HexColors=[]
    openHexColors=open(diretorio + '/HexColors.txt', 'r')
    for line in openHexColors:
        HexColors.append(str(line)[:-1])
    
    colorlist=[]

    for labels in list(range(0,ImgConvex3.max()+1)):
        colorlist.append(HexColors[labels+47])
    
    ColorBounds=list(range(0,ImgConvex3.max()+1))    
    Colormap2=colors.ListedColormap(colorlist)
    ColorNormalization = colors.BoundaryNorm(ColorBounds, Colormap2.N)
    
    map2=plt.subplot2grid((2,3),(1,0),rowspan=1,colspan=1)
    
    map2final=map2.imshow(ImgConvex3, alpha=0.9, cmap=Colormap2)   
    map2.set_title('Convex hull regions',fontsize=11)
    map2.tick_params(which='both',
                     bottom='off', labelbottom='on',
                     top='off', labeltop='off',
                     left='off', labelleft='on', 
                     right='off', labelright='off',
                     labelsize=11)
    
    map2.set_xlabel('$\\mu$m', fontsize=11)
    map2.set_xticks([0, int(ImgConvex3.shape[1]/2), ImgConvex3.shape[1]-1])
    map2.set_xticklabels([str(0), str(int((ImgConvex3.shape[1]/2) * LengthPixelRatio)), str(int(ImgConvex3.shape[1] * LengthPixelRatio))])
    map2.set_yticks([0,int(ImgConvex3.shape[0]/2), ImgConvex3.shape[0]-1])
    map2.set_yticklabels([str(int(ImgConvex3.shape[0] * LengthPixelRatio)), str(int((ImgConvex3.shape[0]/2) * LengthPixelRatio)), str(0)])
    

    Colbar2=fig1.colorbar(map2final, cmap=Colormap2, norm=ColorNormalization, 
                          ticks=list(np.arange(0, ColorBounds[-1], ColorBounds[-1]/len(ColorBounds))),
                          fraction=0.04, pad=0.08, orientation='vertical')
    Colbar2.set_label('Regions', fontsize=11)
    Colbar2.set_ticklabels(['B']+[str(i) for i in ColorBounds[1:]])
    Colbar2.ax.tick_params(labelsize=11)

    #Adicionando os centroides e img referencia
    map2.imshow(ImgRef1a, alpha=0.5, cmap='Greens')
    map2.scatter(np.array(CentroidList)[:,1],np.array(CentroidList)[:,0], color='k', s=5)
    
    # Grafico 1. Growth BAC
    g1=plt.subplot2grid((2,3),(0,1),rowspan=1,colspan=1)
    g1.set_title('Bacteria growth', fontsize=11)
    g1.set_ylabel('Growth ($\\mu$$m^3$)', labelpad=5, fontsize=11)
    g1.set_xlabel('Time (min)', labelpad=5, fontsize=11)
    g1.tick_params(axis="y", labelleft='on', left='on', labelright='off', right='off', colors='k', width=1.5, length=3.5, labelsize=11)
    g1.tick_params(axis="x", labelbottom='on', bottom='on', labeltop='off', top='off', colors='k', width=1.5,length=3.5, labelsize=11)
    g1.grid(True, color='k', linestyle='-', linewidth=0.4, alpha=0.1)
    
    # Grafico 2. Growth EPS    
    g2=plt.subplot2grid((2,3),(1,1),rowspan=1,colspan=1)
    g2.set_title('EPS growth', fontsize=11)
    g2.set_ylabel('Growth ($\\mu$$m^3$)', labelpad=5, fontsize=11)
    g2.set_xlabel('Time (min)', labelpad=5, fontsize=11)
    g2.tick_params(axis="y", labelleft='on', left='on', labelright='off', right='off', colors='k', width=1.5, length=3.5, labelsize=11)
    g2.tick_params(axis="x", labelbottom='on', bottom='on', labeltop='off', top='off', colors='k', width=1.5,length=3.5, labelsize=11)
    g2.grid(True, color='k', linestyle='-', linewidth=0.4, alpha=0.1)
    
    # Grafico 3. Growth rate BAC
    g3=plt.subplot2grid((2,3),(0,2),rowspan=1,colspan=1)
    g3.set_title('Bacteria growth rate', fontsize=11)
    g3.set_ylabel('Growth rate ($\\mu$$m^3$/min)', labelpad=5, fontsize=11)
    g3.set_xlabel('Time (min)', labelpad=5, fontsize=11)
    g3.tick_params(axis="y", labelleft='on', left='on', labelright='off', right='off', colors='k', width=1.5, length=3.5, labelsize=11)
    g3.tick_params(axis="x", labelbottom='on', bottom='on', labeltop='off', top='off', colors='k', width=1.5,length=3.5, labelsize=11)
    g3.grid(True, color='k', linestyle='-', linewidth=0.4, alpha=0.1)
    
    # Grafico 4. Growth rate EPS    
    g4=plt.subplot2grid((2,3),(1,2),rowspan=1,colspan=1)   
    g4.set_title('EPS growth rate', fontsize=11)
    g4.set_ylabel('Growth rate ($\\mu$$m^3$/min)', labelpad=5, fontsize=11)
    g4.set_xlabel('Time (min)', labelpad=5, fontsize=11)
    g4.tick_params(axis="y", labelleft='on', left='on', labelright='off', right='off', colors='k', width=1.5, length=3.5, labelsize=11)
    g4.tick_params(axis="x", labelbottom='on', bottom='on', labeltop='off', top='off', colors='k', width=1.5,length=3.5, labelsize=11)
    g4.grid(True, color='k', linestyle='-', linewidth=0.4, alpha=0.1)

    
    #Figura 2 - Campo escalar
    #fig2=plt.figure(figsize=(6, 6), facecolor='w', edgecolor='k')
    #plotPositions=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
    
    g1_YboundMAX=0
    g2_YboundMAX=0
    g3_YboundMAX=0
    g4_YboundMAX=0
    
    for elementN in list(range(1,ImgConvex3.max()+1)):
        
        YXPosList=[]
        for Ypos in list(range(ImgConvex3.shape[0])):
            for Xpos in list(range(ImgConvex3.shape[1])):
                if ImgConvex3[Ypos, Xpos] == elementN:
                   YXPosList.append([Ypos, Xpos])

        ElementPlotListBAC=[]  
        ElementPlotListEPS=[]
        
        time=initialTimePoint
        for stackNumber in StackList:
            
            print('\n Encontrando os volume para o stack ', str(stackNumber) ,' \n')
            
            ImgListBAC=[]
            ImgListEPS=[]            
            for x in SliceRange:
                aa=io.imread(diretorio + ImportstackRootName + '/bac' + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)
                bb=io.imread(diretorio + ImportstackRootName + '/EPS' + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)
                
                ImgListBAC.append(aa)
                ImgListEPS.append(bb)
            
            Img3DarrayBAC=np.array(ImgListBAC)
            Img3DarrayBACF=np.where(Img3DarrayBAC > 0, 1, 0)

            Img3DarrayEPS=np.array(ImgListEPS)
            Img3DarrayEPSF=np.where(Img3DarrayEPS > 0, 1, 0)            
            
            VolElemCountListBAC=[]
            VolElemCountListEPS=[]
            for sliceN in list(range(Img3DarrayBACF.shape[0])):
                for Position in YXPosList:
                    VolElemCountListBAC.append(Img3DarrayBACF[sliceN, Position[0], Position[1]])
                    VolElemCountListEPS.append(Img3DarrayEPSF[sliceN, Position[0], Position[1]])            
            
            ElementPlotListBAC.append([elementN, time, sum(VolElemCountListBAC) * VoxelVal])
            ElementPlotListEPS.append([elementN, time, sum(VolElemCountListEPS) * VoxelVal])              
                  
            time += timeinterval

        
        with open(diretorio + '/Images/MergedRegion.txt', 'a') as textfile:
            for val in ElementPlotListBAC:
                textfile.write(str(val) + '\n')
            
            textfile.close()

        
        # Calculando as velocidades
        VelListBAC=AvgVelocity(np.array(ElementPlotListBAC)[:,2], initialTimePoint, timeinterval, elementN)
        VelListEPS=AvgVelocity(np.array(ElementPlotListEPS)[:,2], initialTimePoint, timeinterval, elementN)
        
        #Acertando os limites do gráfico
        if g1_YboundMAX < np.array(ElementPlotListBAC)[:,2].max():
            g1_YboundMAX=np.array(ElementPlotListBAC)[:,2].max()
        if g2_YboundMAX < np.array(ElementPlotListEPS)[:,2].max():
            g2_YboundMAX=np.array(ElementPlotListEPS)[:,2].max()
        if g3_YboundMAX < np.array(VelListBAC)[:,2].max():
            g3_YboundMAX=np.array(VelListBAC)[:,2].max()
        if g4_YboundMAX < np.array(VelListEPS)[:,2].max():
            g4_YboundMAX=np.array(VelListEPS)[:,2].max()
        

        #Plot graficos Growth
        g1.plot(np.array(ElementPlotListBAC)[:,1], np.array(ElementPlotListBAC)[:,2], color=colorlist[elementN], alpha=0.5)
        g1.scatter(np.array(ElementPlotListBAC)[:,1], np.array(ElementPlotListBAC)[:,2], color=colorlist[elementN], label='Element' + str(elementN), alpha=0.5, s=20)
        g1.axvline(x=(10*30)-30, color="r",linewidth=1.5,alpha=0.1)
        g1.axvline(x=(11*30)-30, color="b",linewidth=1.5,alpha=0.1)
        g1.axvline(x=(15*30)-30, color="y",linewidth=1.5,alpha=0.1)
        
        g2.plot(np.array(ElementPlotListEPS)[:,1], np.array(ElementPlotListEPS)[:,2], color=colorlist[elementN], alpha=0.5)
        g2.scatter(np.array(ElementPlotListEPS)[:,1], np.array(ElementPlotListEPS)[:,2], color=colorlist[elementN], label='Element' + str(elementN), alpha=0.5, s=20)
        g2.axvline(x=(10*30)-30, color="r",linewidth=1.5,alpha=0.1)
        g2.axvline(x=(11*30)-30, color="b",linewidth=1.5,alpha=0.1)
        g2.axvline(x=(15*30)-30, color="y",linewidth=1.5,alpha=0.1)        
        
        #Plot graficos Growth rate        
        g3.plot(np.array(VelListBAC)[:,1], np.array(VelListBAC)[:,2], color=colorlist[elementN], alpha=0.5)
        g3.scatter(np.array(VelListBAC)[:,1], np.array(VelListBAC)[:,2], color=colorlist[elementN], label='Element' + str(elementN), alpha=0.5, s=20)
        g3.axvline(x=(10*30)-30, color="r",linewidth=1.5,alpha=0.1)
        g3.axvline(x=(11*30)-30, color="b",linewidth=1.5,alpha=0.1)
        g3.axvline(x=(15*30)-30, color="y",linewidth=1.5,alpha=0.1)
            
        g4.plot(np.array(VelListEPS)[:,1], np.array(VelListEPS)[:,2], color=colorlist[elementN], alpha=0.5)
        g4.scatter(np.array(VelListEPS)[:,1], np.array(VelListEPS)[:,2], color=colorlist[elementN], label='Element' + str(elementN), alpha=0.5, s=20)            
        g4.axvline(x=(10*30)-30, color="r",linewidth=1.5,alpha=0.1)
        g4.axvline(x=(11*30)-30, color="b",linewidth=1.5,alpha=0.1)
        g4.axvline(x=(15*30)-30, color="y",linewidth=1.5,alpha=0.1)

        #Plotar as posicoes usadas no campo escalar
        #plotPositions.scatter(np.array(YXPosList)[:,1], np.array(YXPosList)[:,0], color=colorlist[elementN])            

        # Definindo os eixos do gráfico
        g1.set_ylim(-40, BACVol_ylim)
        g1.spines["left"].set_visible(True)
        g1.spines["left"].set_linewidth(1.0)
        g1.spines["right"].set_visible(False)
        g1.spines["top"].set_visible(False)
        g1.spines["bottom"].set_visible(True)
        g1.spines["bottom"].set_linewidth(1.0)
        g1.set_aspect('auto') 

        g2.set_ylim(-40, EPSVol_ylim)    
        g2.spines["left"].set_visible(True)
        g2.spines["left"].set_linewidth(1.0)
        g2.spines["right"].set_visible(False)
        g2.spines["top"].set_visible(False)
        g2.spines["bottom"].set_visible(True)
        g2.spines["bottom"].set_linewidth(1.0)
        g2.set_aspect('auto') 

        g3.set_ylim(-5, BACVel_ylim)
        g3.spines["left"].set_visible(True)
        g3.spines["left"].set_linewidth(1.0)
        g3.spines["right"].set_visible(False)
        g3.spines["top"].set_visible(False)
        g3.spines["bottom"].set_visible(True)
        g3.spines["bottom"].set_linewidth(1.0)
        g3.set_aspect('auto') 

        g4.set_ylim(-5, EPSVel_ylim)        
        g4.spines["left"].set_visible(True)
        g4.spines["left"].set_linewidth(1.0)
        g4.spines["right"].set_visible(False)
        g4.spines["top"].set_visible(False)
        g4.spines["bottom"].set_visible(True)
        g4.spines["bottom"].set_linewidth(1.0)
        g4.set_aspect('auto') 
      
        
    plt.tight_layout()    
    fig1.savefig(diretorio + '/Images/MergedRegion' + str(MergedRegion) + '.png', dpi = 300)
    #fig2.savefig(diretorio + '/Images/MergedRegion' + str(MergedRegion) + '_PLOT.png')
    plt.show()
    

# A entrada da função são arrays
# A saida eh uma lista do tipo [[tempo1,velocidadeMedia1], [tempo2,velocidadeMedia2],...]
def AvgVelocity(volumeValsArray, initialTimePoint, timeinterval, element):
    
    VelocList=[]
    time=initialTimePoint
    for volVal in list(range(volumeValsArray.shape[0]-1)):
        VelocList.append([element, time + (timeinterval/2), (volumeValsArray[volVal+1] - volumeValsArray[volVal])/timeinterval])
        time += timeinterval
        
    return(VelocList)
      