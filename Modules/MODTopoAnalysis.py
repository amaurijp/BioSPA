import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import MODimageVolSel
from skimage import draw
from skimage import morphology
from skimage import io
import numpy as np
import os


# Função para importar Imagens e filtrar elementos por range de volume
def CropSUFwithBAC(diretorio,
                   BACstackNumber,
                   FirstSlice,LastSlice,
                   ImportstackRootName='/Raw',
                   importFormat='.png',
                   ExportDir='/Processed',
                   AreaBorderSize=5,
                 
                   ReferenceStackToCrop='/Binarize/bac/ImageJ/t1',
                   RefminArea=1,RefmaxArea=2000000,
                   MAXElementsToCrop=10,
                   
                   Det_TopoXVol_relation=False,
                   ImportstackRootName_DetVol='/Binarized/bac'):
    
    
    SliceRange=list(range(FirstSlice,LastSlice+1))
    Imglist1=[]
    
    print('\nImporting images... \n')
    
    for x in SliceRange:
        if x < 10:
            a=io.imread(diretorio + ImportstackRootName + '/Slice00' + str(x) + importFormat)
            
        elif 10 <= x < 100:
            a=io.imread(diretorio + ImportstackRootName + '/Slice0' + str(x) + importFormat)

        elif 100 <= x < 1000:
            a=io.imread(diretorio + ImportstackRootName + '/Slice' + str(x) + importFormat)            
        
        Imglist1.append(a)
    
    ImgArray3D=np.array(Imglist1)
    
    print('The stack has ',len(ImgArray3D),' slices')
    print('The image has ',len(ImgArray3D[0]),' lines')
    print('The image has ',len(ImgArray3D[0][0]),' columns')
    print('The largest value in the stack is ', ImgArray3D.max())
    
    try:
        print('The image has ',len(ImgArray3D[0][0][0]),' channels')
    
    except TypeError:         
        print('The image has only 1 channel')
        
    print('\nInitiating the CropRegion module for the stack ', str(BACstackNumber), ' ... \n')
    
    refImage=io.imread(diretorio + ReferenceStackToCrop + '/t1/ZProjection' + importFormat)
    
    refImageNorm=np.where(refImage > 0, 1, 0)
    RefimgLab=morphology.label(refImageNorm,connectivity=1)

    RefP1=MODimageVolSel.CountElements(RefimgLab)
    RefP2=MODimageVolSel.FindVolElements(RefP1,RefminArea,RefmaxArea)
    
    if len(RefP2) > MAXElementsToCrop:
        
        print('\n\nElements to be cropped ', len(RefP2), '\n\n ')            
        print('\n\nAborting due to the excess of elements to be cropped\n\n ')
    
    else:
        RefP3=MODimageVolSel.ElementsSelectionbyRange(RefimgLab,RefP2)
                    
        RefP4 = np.where(RefP3 > 0, 255, 0)
        io.imsave(diretorio + ReferenceStackToCrop + '/t1/ZProjectionFiltered' + importFormat, RefP4, check_contrast=False)
                    
        print('\n\nIt will be ', len(RefP2), ' elements to crop \n \n ')
        
        del(RefP1)      
        
        indexToSave=1
        for elem in list(range(len(RefP2))):
            print('\nSearching for element ', RefP2[elem], '\n')
            XPosList=[]
            YPosList=[]
            for YPos in list(range(len(RefP3))):
                for XPos in list(range(len(RefP3[YPos]))):
                    if RefP3[YPos,XPos] == RefP2[elem]:
                        YPosList.append(YPos)
                        XPosList.append(XPos)
            
            Ymin=min(YPosList)
            Ymax=max(YPosList)
            Xmin=min(XPosList)
            Xmax=max(XPosList)
            
            del(XPosList)
            del(YPosList)
                        
            if (Ymin-AreaBorderSize) <= 0 or (Ymax+AreaBorderSize) >= len(RefP3) or (Xmin-AreaBorderSize) <= 0 or (Xmax+AreaBorderSize) >= len(RefP3[0]):
                    
                print('Indexes out of the matrix. Excluding element ', RefP2[elem])
                continue    
            
            else:
                try:
                    
                    print('\nCropping Region ', indexToSave)
                    
                    for imgN in list(range(len(ImgArray3D))):
                        aa1F=ImgArray3D[imgN][Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize]
                            
                        if not os.path.exists(diretorio + ExportDir + '/With_BAC/Region' + str(indexToSave)):
                            os.makedirs(diretorio + ExportDir + '/With_BAC/Region' + str(indexToSave))
            
                        io.imsave(diretorio + ExportDir + '/With_BAC/Region' + str(indexToSave) + '/Slice' + str(SliceRange[imgN]) + importFormat, aa1F, check_contrast=False)
                    
                        if not os.path.exists(diretorio + '/Images'):
                            os.makedirs(diretorio + '/Images')
                        
                        try:
                            RefImgwithRegOverlay=io.imread(diretorio + '/Images/ZProjection_SUFCropped' + importFormat)
                        
                        except FileNotFoundError:
                            RefImgwithRegOverlay = np.zeros((len(ImgArray3D[0]), len(ImgArray3D[0][0])), dtype=np.uint8)
                        
                        #Salvando a imagem da area coprada para analise topografica
                        rectangle=np.array(((Ymin-AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmin-AreaBorderSize)))
                        rr, cc = draw.polygon(rectangle[:,0], rectangle[:,1])
                        RefImgwithRegOverlay[rr, cc] = 255
                        
                        io.imsave(diretorio + '/Images/ZProjection_SUFCropped' + importFormat, RefImgwithRegOverlay, check_contrast=False)
                    
                    #Salvando a imagem do cross section da bacteria
                    RefCIm1=refImageNorm[Ymin-1:Ymax+1,Xmin-1:Xmax+1]
                    RefCIm2=np.where(RefCIm1 > 0, 255, 0)
                    io.imsave(diretorio + ExportDir + '/With_BAC/Region' + str(indexToSave) + '/ZProjectionBAC' + importFormat, RefCIm2, check_contrast=False)
                    
                    if Det_TopoXVol_relation == True:
                        
                        DetVol_BACImglist=[]
                        
                        for sliceNumber in list(np.arange(1, 1+len(os.listdir(diretorio + ImportstackRootName_DetVol + '/t' + str(BACstackNumber))))):                            
                            if sliceNumber < 10:
                                aa=io.imread(diretorio + ImportstackRootName_DetVol + '/t' + str(BACstackNumber) + '/Slice00' + str(sliceNumber) + importFormat)
                                bb=aa[Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize]
                                
                            elif 10 <= sliceNumber < 100:
                                aa=io.imread(diretorio + ImportstackRootName_DetVol + '/t' + str(BACstackNumber) + '/Slice0' + str(sliceNumber) + importFormat)
                                bb=aa[Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize]                                
                    
                            elif 100 <= sliceNumber < 1000:
                                aa=io.imread(diretorio + ImportstackRootName_DetVol + '/t' + str(BACstackNumber) + '/Slice' + str(sliceNumber) + importFormat)            
                                bb=aa[Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize]                                            
                                
                            DetVol_BACImglist.append(bb)
                        
                        DetVol_BACImgArray3D=np.array(DetVol_BACImglist)
                        VolVal=np.where(DetVol_BACImgArray3D > 0, 1, 0).sum()            
                                
                        with open(diretorio + ExportDir + '/With_BAC/Region' + str(indexToSave) + '/Bac_Vol.txt', 'w') as BacVOL_FILE:
                            BacVOL_FILE.write(str(VolVal))
                        
                        BacVOL_FILE.close()
                    
                    
                    indexToSave += 1
                    
                except PermissionError or OSError:
                    continue



# Função para importar Imagens e filtrar elementos onde nao ha bacterias
def CropSUFwithoutBAC(diretorio,
                      FirstSlice,LastSlice,
                      ImportstackRootName='/Raw',
                      importFormat='.png',
                      ExportDir='/Processed',
                      RefImgWithBAC='/Images/Ref.png',
                      MinLength=25,
                      MaxLength=500,
                      lengthStep=25,
                      BacSubtractionMode=False):
    
    SliceRange=list(range(FirstSlice,LastSlice+1))
    Imglist1=[]
    

    for x in SliceRange:
        if x < 10:
            a=io.imread(diretorio + ImportstackRootName + '/Slice00' + str(x) + importFormat)
            
        elif 10 <= x < 100:
            a=io.imread(diretorio + ImportstackRootName + '/Slice0' + str(x) + importFormat)

        elif 100 <= x < 1000:
            a=io.imread(diretorio + ImportstackRootName + '/Slice' + str(x) + importFormat)            
        
        Imglist1.append(a)
         
    
    ImgArray3D=np.array(Imglist1)
    
    print('The stack has ',len(ImgArray3D),' slices')
    print('The images has ',len(ImgArray3D[0]),' lines')
    print('The images has ',len(ImgArray3D[0][0]),' columns')
    print('The largest value in the stack is ', ImgArray3D.max())
    
    try:
        print('The image has ',len(ImgArray3D[0][0][0]),' channels')
    
    except TypeError:         
        print('The image has only 1 channel')
    
    
    print('\nImporting the reference image (with elements)... \n')

    for imgN in list(range(len(ImgArray3D))):
        
        if BacSubtractionMode == True:
            
            refImage=io.imread(diretorio + RefImgWithBAC + importFormat)    
            refImageNorm=np.where(refImage > 0, 1, 0)
            
            for Ypos in list(range(len(ImgArray3D[imgN]))):
                for Xpos in list(range(len(ImgArray3D[imgN,Ypos]))):
                    if refImageNorm[Ypos,Xpos] == 1:
                         ImgArray3D[imgN,Ypos,Xpos] = 0
                    
                    else:
                        continue
            
        ScaleList=list(range(MinLength, MaxLength+1, lengthStep))
        
        RegionNumber=1
        for scaleN in ScaleList:
            CropYposList=list(range(0,len(ImgArray3D[imgN])+1,scaleN))
            CropXposList=list(range(0,len(ImgArray3D[imgN])+1,scaleN))
            
            print('\nCropping Region ', RegionNumber)
            
            for CropYpos in list(range(len(CropYposList))):
                for CropXpos in list(range(len(CropXposList))):

                    try:
                        aaf1=ImgArray3D[imgN][CropYposList[CropYpos]:CropYposList[CropYpos+1],CropXposList[CropXpos]:CropXposList[CropXpos+1]]
                        
                        if not os.path.exists(diretorio + ExportDir + '/WithoutBACScaled/Region' + str(RegionNumber)):
                            os.makedirs(diretorio + ExportDir + '/WithoutBACScaled/Region' + str(RegionNumber))
                        
                        io.imsave(diretorio + ExportDir + '/WithoutBACScaled/Region' + str(RegionNumber) + '/Slice' + str(SliceRange[imgN]) + importFormat, aaf1, check_contrast=False)
                        RegionNumber += 1
                        
                    except IndexError:
                        continue
        


# Funcao para calcular as alturas
def TopographicAnalysisFunc(diretorio,
                            BACstackNumber,
                            importstackRootName,
                            FirstSlice,LastSlice,
                            ZStep=1,
                            heightValuetoGet=1,
                            RegionAnalysis=False,
                            XYField=[319.45,319.45],
                            RawImageDefinition=[1024,1024],
                            MaxScaledAreaToConsider=300,
                            
                            Det_TopoXVol_relation = False):
    
    if RegionAnalysis == False:
        print('\n Mode Region Analysis is OFF \n')
        print('\nTopography of the whole image will be analyzed\n')
        SliceRange=list(range(FirstSlice,LastSlice+1))
            
        Imglist=[]
        for sliceN in SliceRange:
            if sliceN < 10:
                a11=io.imread(diretorio + importstackRootName + "/Slice00" + str(sliceN) + ".png")
                
            elif sliceN < 100:
                a11=io.imread(diretorio + importstackRootName + "/Slice0" + str(sliceN) + ".png")
            
            elif sliceN < 1000:
                a11=io.imread(diretorio + importstackRootName + "/Slice" + str(sliceN) + ".png")
                
            
            Imglist.append(a11)
    
        ImglistF=np.array(Imglist)
            
        if heightValuetoGet == 1:
            HeighvalYX=[]
            for j in list(range(len(ImglistF[0]))):
                HeighvalX=[]
                for i in list(range(len(ImglistF[0][j]))):
                    try:            
                        for k in list(range(len(ImglistF))):
                            if ImglistF[k+1][j][i] > ImglistF[k][j][i]:
                                HeighvalX.append(len(ImglistF)-(k+2))
                                break
        
                    except IndexError:
                        HeighvalX.append(0)
                
                HeighvalYX.append(HeighvalX)
        
        elif heightValuetoGet == 2:
            HeighvalYX=[]
            for j in list(range(len(ImglistF[0]))):
                HeighvalX=[]
                for i in list(range(len(ImglistF[0][j]))):
                    try:            
                        for k in list(range(len(ImglistF))):
                            if ImglistF[k+2][j][i] > ImglistF[k+1][j][i] and ImglistF[k+1][j][i] > ImglistF[k][j][i]:
                                HeighvalX.append(len(ImglistF)-(k+3))
                                break
        
                    except IndexError:
                        HeighvalX.append(0)
                
                HeighvalYX.append(HeighvalX)
        
        
        elif heightValuetoGet == 3:
            HeighvalYX=[]
            for j in list(range(len(ImglistF[0]))):
                HeighvalX=[]
                for i in list(range(len(ImglistF[0][j]))):
                    try:            
                        for k in list(range(len(ImglistF))):
                            if ImglistF[k+3][j][i] > ImglistF[k+2][j][i] and ImglistF[k+2][j][i] > ImglistF[k+1][j][i] and ImglistF[k+1][j][i] > ImglistF[k][j][i]:
                                HeighvalX.append(len(ImglistF)-(k+4))
                                break
        
                    except IndexError:
                        HeighvalX.append(0)
                
                HeighvalYX.append(HeighvalX)
        
        print('The dimensions of the analyzed matrix are ', len(HeighvalYX), len(HeighvalYX[0]))            
        
        SaV=SaFunc(np.array(HeighvalYX), ZStep)
        SqVal=SqFunc(np.array(HeighvalYX), ZStep)
        SskVal=SskFunc(np.array(HeighvalYX), SqVal, ZStep)
        
        TOPOResults=open(diretorio + importstackRootName + '/TopoResultsFullArea.txt', 'w')
        TOPOResults.write('\nSa value for the total area is ' + str(SaV) + '\n')
        TOPOResults.write('\nSq value for the total area is ' + str(SqVal)+ '\n')
        TOPOResults.write('\nSsk value for the total area is ' + str(SskVal) + '\n')
        TOPOResults.close()
        
        imHeights=np.array(HeighvalYX,dtype='uint8')
        io.imsave(diretorio + '/Images/HeightsImage_get' + str(heightValuetoGet) + '.png', imHeights, check_contrast=False)
        
        HeightTicks=list(np.arange(0, imHeights.max(), (imHeights.max()/8)))
        figTOPOFull=plt.figure(figsize=(8, 7), dpi=100, facecolor='w', edgecolor='k')
        mapFull=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
        mapFull.set_title('Height map',fontsize=14)
        
        mapFull.tick_params(which='both',
                            bottom='off', labelbottom='on',
                            top='off', labeltop='off',
                            left='off', labelleft='on', 
                            right='off', labelright='off',
                            labelsize='9')
        
        mapFull.set_xlabel('$\\mu$m', fontsize=14)
        mapFull.set_xticks([0,int(len(imHeights[0])/2),len(imHeights[0])-1])
        mapFull.set_xticklabels([str(0), str(int(XYField[0]/2)), str(XYField[0])])
        mapFull.set_yticks([0,int(len(imHeights)/2),len(imHeights)-1])
        mapFull.set_yticklabels([str(XYField[1]), str(int(XYField[1]/2)), str(0)])
        mapFull.tick_params(axis="y", colors='k', labelsize=14, width=1.5,length=3.5)
        mapFull.tick_params(axis="x", colors='k', labelsize=14, width=1.5,length=3.5)

        mapFullaxi=mapFull.imshow(imHeights, cmap='coolwarm')
        ColbarFull=figTOPOFull.colorbar(mapFullaxi, fraction=0.1, pad=0.02, orientation='vertical')
        ColbarFull.set_label('$\\mu$m', fontsize=14)
        ColbarFull.set_ticks(HeightTicks)
        ColbarFull.set_ticklabels([str(i * ZStep) for i in HeightTicks])
        ColbarFull.ax.tick_params(labelsize=14)

        plt.tight_layout()
        figTOPOFull.savefig(diretorio + '/Images/HeightsImageMap_get' + str(heightValuetoGet) + '.png', dpi = 300)
        plt.show()
        
        
    elif RegionAnalysis == True:
        
        AreaPixelRatio=(XYField[0]/RawImageDefinition[0]) * (XYField[1]/RawImageDefinition[1])
        
        BACLastRegion = len(os.listdir(diretorio + '/ExportedData/Topography/With_BAC'))
        BACRegionRange=list(range(1,BACLastRegion+1))
        
        WithoutBACLastRegion = len(os.listdir(diretorio + '/ExportedData/Topography/WithoutBACScaled'))
        WithoutBACRegionRange=list(range(1,WithoutBACLastRegion+1))       
        
        BACAreaList=[]
        
        BACAreaScaleValList=[]
        BACSaValList=[]
        BACSqValList=[]
        BACSskValList=[]
        
        
        '''
        #Figura 1 - Roughness values
        fig1=plt.figure(figsize=(10, 7), dpi=100, facecolor='w', edgecolor='k') 
        g1_1=plt.subplot2grid((3,1),(0,0),rowspan=1,colspan=1)
        g1_1.set_title('Sa values',fontsize=9)
        g1_1.set_ylabel('Sa ($\\mu$m)', fontsize=9)
        g1_1.set_xlabel('Area ($\\mu$$m^2$)', fontsize=9)
        
        g1_2=plt.subplot2grid((3,1),(1,0),rowspan=1,colspan=1)
        g1_2.set_title('Sq values',fontsize=9)
        g1_2.set_ylabel('Sq ($\\mu$m)', fontsize=9)
        g1_2.set_xlabel('Area ($\\mu$$m^2$)', fontsize=9)
        
        g1_3=plt.subplot2grid((3,1),(2,0),rowspan=1,colspan=1)
        g1_3.set_title('Ssk values',fontsize=9)
        g1_3.set_ylabel('Ssk', fontsize=9)
        g1_3.set_xlabel('Area ($\\mu$$m^2$)', fontsize=9)
        
        plt.subplots_adjust(wspace=0.3, hspace=0.8)
        
        #Figura 2 - Area Distribution
        fig2=plt.figure(figsize=(4, 4), dpi=100, facecolor='w', edgecolor='k')
        g2=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
        g2.set_title('Cross-section area values',fontsize=9)
        g2.set_ylabel('Frequency', fontsize=9)
        g2.set_xlabel('Area ($\\mu$$m^2$)', fontsize=9)
        '''
        
        #Tratamento para as regioes que tem bacteria        
        for BACregion in BACRegionRange:
        
            print('\nTOPO_Analysis with BAC: Analyzing region ', BACregion)
            
            SliceRange=list(range(FirstSlice,LastSlice+1))
            
            ImglistBAC=[]
            
            RefBACArea=io.imread(diretorio + importstackRootName + '/With_BAC/Region' + str(BACregion) + '/ZProjectionBAC.png')            
            BACAreaList.append(float(np.count_nonzero(RefBACArea.flatten()) * AreaPixelRatio))
            
            for sliceN in SliceRange:
                a11=io.imread(diretorio + importstackRootName + '/With_BAC/Region' + str(BACregion) + "/Slice" + str(sliceN) + ".png")
                
                ImglistBAC.append(a11)
        
            ImglistBACF=np.array(ImglistBAC)

            if heightValuetoGet == 1:
                HeighvalYXBAC=[]
                for j in list(range(len(ImglistBACF[0]))):
                    HeighvalXBAC=[]
                    for i in list(range(len(ImglistBACF[0][j]))):
                        try:            
                            for k in list(range(len(ImglistBACF))):
                                if ImglistBACF[k+1][j][i] > ImglistBACF[k][j][i]:
                                    HeighvalXBAC.append(len(ImglistBACF)-(k+2))
                                    break
            
                        except IndexError:
                            HeighvalXBAC.append(0)
                    
                    HeighvalYXBAC.append(HeighvalXBAC)
            
            elif heightValuetoGet == 2:
                HeighvalYXBAC=[]
                for j in list(range(len(ImglistBACF[0]))):
                    HeighvalXBAC=[]
                    for i in list(range(len(ImglistBACF[0][j]))):
                        try:            
                            for k in list(range(len(ImglistBACF))):
                                if ImglistBACF[k+2][j][i] > ImglistBACF[k+1][j][i] and ImglistBACF[k+1][j][i] > ImglistBACF[k][j][i]:
                                    HeighvalXBAC.append(len(ImglistBACF)-(k+3))
                                    break
            
                        except IndexError:
                            HeighvalXBAC.append(0)
                    
                    HeighvalYXBAC.append(HeighvalXBAC)
            
            elif heightValuetoGet == 3:
                HeighvalYXBAC=[]
                for j in list(range(len(ImglistBACF[0]))):
                    HeighvalXBAC=[]
                    for i in list(range(len(ImglistBACF[0][j]))):
                        try:            
                            for k in list(range(len(ImglistBACF))):
                                if ImglistBACF[k+3][j][i] > ImglistBACF[k+2][j][i] and ImglistBACF[k+2][j][i] > ImglistBACF[k+1][j][i] and ImglistBACF[k+1][j][i] > ImglistBACF[k][j][i]:
                                    HeighvalXBAC.append(len(ImglistBACF)-(k+4))
                                    break
            
                        except IndexError:
                            HeighvalXBAC.append(0)
                    
                    HeighvalYXBAC.append(HeighvalXBAC)
            
            print(len(HeighvalYXBAC),len(HeighvalYXBAC[0]))

            BACSaV=SaFunc(np.array(HeighvalYXBAC), ZStep)            
            BACSqVal=SqFunc(np.array(HeighvalYXBAC), ZStep)
            BACSskVal=SskFunc(np.array(HeighvalYXBAC), BACSqVal, ZStep)

            
            BACAreaScaleValList.append([BACregion, float(ImglistBACF[0].shape[0] * ImglistBACF[0].shape[1] * AreaPixelRatio)])
            
            
            if Det_TopoXVol_relation == True:
                with open(diretorio + importstackRootName + '/With_BAC/Region' + str(BACregion) + "/Bac_Vol.txt", 'r') as BacVolValue_str:
                    BacVolValue = int(BacVolValue_str.read())
                
                # As entradas sao [Regiao, Medida topografica, valor do volume da bacteria]
                BACSaValList.append([BACregion, BACSaV, BacVolValue])
                BACSqValList.append([BACregion, BACSqVal, BacVolValue])
                BACSskValList.append([BACregion, BACSskVal, BacVolValue])
            
            elif Det_TopoXVol_relation == False:
                # As entradas sao [Regiao, Medida topografica, valor do volume da bacteria]
                BACSaValList.append([BACregion, BACSaV])
                BACSqValList.append([BACregion, BACSqVal])
                BACSskValList.append([BACregion, BACSskVal])
                        
        
        #Tratamento para as regioes que NAO tem bacteria        
        
        if not os.path.exists(diretorio + importstackRootName + '/WithoutBAC_SaList_t1' + '.txt'):
            for WithoutBACregion in WithoutBACRegionRange:
                
                SliceRange=list(range(FirstSlice,LastSlice+1))
                
                ImglistWithoutBAC=[]
                
                for sliceN in SliceRange:
                    b11=io.imread(diretorio + importstackRootName + '/WithoutBACScaled' + '/Region' + str(WithoutBACregion) + '/Slice' + str(sliceN) + '.png')
                    
                    ImglistWithoutBAC.append(b11)
            
                ImglistWithoutBACF=np.array(ImglistWithoutBAC)
                
                if float(ImglistWithoutBACF[0].shape[0] * ImglistWithoutBACF[0].shape[1]) > MaxScaledAreaToConsider:
                    break
                
                else:
                    
                    if heightValuetoGet == 1:
                        HeighvalYXWithoutBAC=[]
                        for j in list(range(len(ImglistWithoutBACF[0]))):
                            HeighvalXWithoutBAC=[]
                            for i in list(range(len(ImglistWithoutBACF[0][j]))):
                                try:            
                                    for k in list(range(len(ImglistWithoutBACF))):
                                            if ImglistWithoutBACF[k+1][j][i] > ImglistWithoutBACF[k][j][i]:
                                                HeighvalXWithoutBAC.append(len(ImglistWithoutBACF)-(k+2))
                                                break
                    
                                except IndexError:
                                    HeighvalXWithoutBAC.append(0)
                            
                            HeighvalYXWithoutBAC.append(HeighvalXWithoutBAC)
                    
                    
                    elif heightValuetoGet == 2:
                        HeighvalYXWithoutBAC=[]
                        for j in list(range(len(ImglistWithoutBACF[0]))):
                            HeighvalXWithoutBAC=[]
                            for i in list(range(len(ImglistWithoutBACF[0][j]))):
                                try:            
                                    for k in list(range(len(ImglistWithoutBACF))):
                                            if ImglistWithoutBACF[k+2][j][i] > ImglistWithoutBACF[k+1][j][i] and ImglistWithoutBACF[k+1][j][i] > ImglistWithoutBACF[k][j][i]:
                                                HeighvalXWithoutBAC.append(len(ImglistWithoutBACF)-(k+3))
                                                break
                    
                                except IndexError:
                                    HeighvalXWithoutBAC.append(0)
                            
                            HeighvalYXWithoutBAC.append(HeighvalXWithoutBAC)
                    
                    
                    elif heightValuetoGet == 3:
                        HeighvalYXWithoutBAC=[]
                        for j in list(range(len(ImglistWithoutBACF[0]))):
                            HeighvalXWithoutBAC=[]
                            for i in list(range(len(ImglistWithoutBACF[0][j]))):
                                try:            
                                    for k in list(range(len(ImglistWithoutBACF))):
                                            if ImglistWithoutBACF[k+3][j][i] > ImglistWithoutBACF[k+2][j][i] and ImglistWithoutBACF[k+2][j][i] > ImglistWithoutBACF[k+1][j][i] and ImglistWithoutBACF[k+1][j][i] > ImglistWithoutBACF[k][j][i]:
                                                HeighvalXWithoutBAC.append(len(ImglistWithoutBACF)-(k+4))
                                                break
                    
                                except IndexError:
                                    HeighvalXWithoutBAC.append(0)
                            
                            HeighvalYXWithoutBAC.append(HeighvalXWithoutBAC)
    
                    print('\nTOPO_Analysis without BAC: Analyzing region ', WithoutBACregion)
                    print(len(HeighvalYXWithoutBAC),len(HeighvalYXWithoutBAC[0]))            
                    
                    WithoutBACSaV=SaFunc(np.array(HeighvalYXWithoutBAC), ZStep)
                    WithoutBACSqVal=SqFunc(np.array(HeighvalYXWithoutBAC), ZStep)
                    WithoutBACSskVal=SskFunc(np.array(HeighvalYXWithoutBAC), WithoutBACSqVal, ZStep)
        
                    File4=open(diretorio + importstackRootName + '/WithoutBAC_SaList' + '.txt', 'a')
                    File5=open(diretorio + importstackRootName + '/WithoutBAC_SqList' + '.txt', 'a')
                    File6=open(diretorio + importstackRootName + '/WithoutBAC_SsKList' + '.txt', 'a')
                   
                    File4.write('[' + str(WithoutBACregion) + ', ' + str(float(np.count_nonzero(np.array(HeighvalYXWithoutBAC).flatten())) * AreaPixelRatio) + ', ' + str(WithoutBACSaV) + ']\n')
            
                    File5.write('[' + str(WithoutBACregion) + ', ' + str(float(np.count_nonzero(np.array(HeighvalYXWithoutBAC).flatten())) * AreaPixelRatio) + ', ' + str(WithoutBACSqVal) + ']\n')
                    
                    File6.write('[' + str(WithoutBACregion) + ', ' + str(float(np.count_nonzero(np.array(HeighvalYXWithoutBAC).flatten())) * AreaPixelRatio) + ', ' + str(WithoutBACSskVal) + ']\n')
        
                    File4.close()
                    File5.close()
                    File6.close()
            

        '''
        g1_1.scatter(np.array(WithoutBACAreaScaleValList)[:,1], np.array(WithoutBACSaValList)[:,1], color='y', alpha=0.7, label='non colonized')
        g1_1.scatter(np.array(BACAreaScaleValList)[:,1], np.array(BACSaValList)[:,1], color='g', alpha=0.4, label='colonized')
        g1_1.legend(bbox_to_anchor=(0.8, 0.95), loc=2, borderaxespad=0.)
        
        g1_2.scatter(np.array(WithoutBACAreaScaleValList)[:,1], np.array(WithoutBACSqValList)[:,1], color='c', alpha=0.7, label='non colonized')
        g1_2.scatter(np.array(BACAreaScaleValList)[:,1], np.array(BACSqValList)[:,1], color='r', alpha=0.4, label='colonized')
        g1_2.legend(bbox_to_anchor=(0.8, 0.95), loc=2, borderaxespad=0.)
        
        g1_3.scatter(np.array(WithoutBACAreaScaleValList)[:,1], np.array(WithoutBACSskValList)[:,1], color='g', alpha=0.7, label='non colonized')
        g1_3.scatter(np.array(BACAreaScaleValList)[:,1], np.array(BACSskValList)[:,1], color='b', alpha=0.4, label='colonized')
        g1_3.legend(bbox_to_anchor=(0.8, 0.95), loc=2, borderaxespad=0.)

        g2.hist(BACAreaList, bins=50, color='r', alpha=0.5, label='Colonizers at t=0')
        g2.legend(bbox_to_anchor=(0.4, 0.9), loc=2, borderaxespad=0.)
        
        #fig1.savefig(diretorio + '/Topography1' + '_t' + str(BACstackNumber) + '.png')
        #fig2.savefig(diretorio + '/Topography2' + '_t' + str(BACstackNumber) + '.png')
        #plt.show()
        '''
        
        File1=open(diretorio + importstackRootName + '/WithBAC_SaList_t' + str(BACstackNumber) + '.txt', 'w')
        File2=open(diretorio + importstackRootName + '/WithBAC_SqList_t' + str(BACstackNumber) + '.txt', 'w')
        File3=open(diretorio + importstackRootName + '/WithBAC_SsKList_t' + str(BACstackNumber) + '.txt', 'w')
        
        
        if Det_TopoXVol_relation == True:
            for elementN in list(range(len(BACSaValList))):
                File1.write('[' + str(BACSaValList[elementN][0]) + ', ' + str(BACAreaScaleValList[elementN][1]) + ', ' + str(BACSaValList[elementN][1]) + ', ' + str(BACSaValList[elementN][2]) + ']\n')
            
            for elementN in list(range(len(BACSqValList))):
                File2.write('[' + str(BACSqValList[elementN][0]) + ', ' + str(BACAreaScaleValList[elementN][1]) + ', ' + str(BACSqValList[elementN][1]) + ', ' + str(BACSqValList[elementN][2]) + ']\n')
                
            for elementN in list(range(len(BACSskValList))):
                File3.write('[' + str(BACSskValList[elementN][0]) + ', ' + str(BACAreaScaleValList[elementN][1]) + ', ' + str(BACSskValList[elementN][1]) + ', ' + str(BACSskValList[elementN][2]) + ']\n')
                 
        
        elif Det_TopoXVol_relation == False:
            for elementN in list(range(len(BACSaValList))):
                File1.write('[' + str(BACSaValList[elementN][0]) + ', ' + str(BACAreaScaleValList[elementN][1]) + ', ' + str(BACSaValList[elementN][1]) + ']\n')
            
            for elementN in list(range(len(BACSqValList))):
                File2.write('[' + str(BACSqValList[elementN][0]) + ', ' + str(BACAreaScaleValList[elementN][1]) + ', ' + str(BACSqValList[elementN][1]) + ']\n')
                
            for elementN in list(range(len(BACSskValList))):
                File3.write('[' + str(BACSskValList[elementN][0]) + ', ' + str(BACAreaScaleValList[elementN][1]) + ', ' + str(BACSskValList[elementN][1]) + ']\n')

        
        File1.close()
        File2.close()
        File3.close()
        
#Funcoes de analise de topografia
def SaFunc(HeightimgArray, ZStep=1):    
    aab1=HeightimgArray.flatten() * ZStep
    
    indexList=[]
    for elemPOS in list(range(len(aab1))):
        if aab1[elemPOS] == 0 or aab1[elemPOS] == 1:
            indexList.append(elemPOS)
    
    aa2=np.delete(aab1,indexList)     
    
    bb1=aa2-aa2.mean()
    bb2=np.absolute(bb1)    
    
    try:
        SaValue= (1/len(bb2)) * bb2.sum()
    
    except ZeroDivisionError:
        SaValue = 0
    
    return(SaValue)
    
def SqFunc(HeightimgArray, ZStep=1):
    aab1=HeightimgArray.flatten() * ZStep
    
    indexList=[]
    for elemPOS in list(range(len(aab1))):
        if aab1[elemPOS] == 0 or aab1[elemPOS] == 1:
            indexList.append(elemPOS)
    
    aa2=np.delete(aab1,indexList)
    
    bb1=aa2-aa2.mean()
    bb2= bb1 ** 2    
    
    try:
        SqValue= ((1/len(bb2)) * bb2.sum()) ** (1/2)
    
    except ZeroDivisionError:
        SqValue = 0
    
    return(SqValue)

def SskFunc(HeightimgArray, SqValue, ZStep=1):
    aab1=HeightimgArray.flatten() * ZStep
    
    indexList=[]
    for elemPOS in list(range(len(aab1))):
        if aab1[elemPOS] == 0 or aab1[elemPOS] == 1:
            indexList.append(elemPOS)
    
    aa2=np.delete(aab1, indexList)
    
    bb1=aa2-aa2.mean()
    bb2= bb1 ** 3
    
    try:
        SskValue=(1/(SqValue**3))*(1/len(bb2))*bb2.sum()
    
    except ZeroDivisionError:
        SskValue=0            
    
    return(SskValue)
    