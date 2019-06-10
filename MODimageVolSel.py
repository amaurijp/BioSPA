from skimage import io
from skimage import morphology
from skimage import draw
import os
import numpy as np


# contando o numero de elementos presentes na matrix 3D
# a entrada ImageStackData eh um ndarray
def CountElements(ImageStackData):
            
    print('\n O número de elementos na matrix inicial eh de ', ImageStackData.max())
    
    CountL1=[]
    
    for k in list(range(1,ImageStackData.max()+1)):
        sumC=list(ImageStackData.flatten()).count(k)
        CountL1.append([k,sumC])
    
    return(CountL1)


# A funcao abaixo seleciona somente elementos com determinado valor de área
# a entrada VolumeCountList eh uma lista
def FindVolElements(VolumeCountList,minVolume,maxVolume):
    
    ElementsList=[]
    for x in list(range(len(VolumeCountList))):
        if minVolume <= VolumeCountList[x][1] <= maxVolume:
            ElementsList.append(VolumeCountList[x][0])

    return(ElementsList)


# Encontrando os elementos de maior volume nas matrizes
# a entrada VolumeCountList eh uma lista
def FindLargestElements(VolumeCountList,NumberofElements=1,ElementsList=[]):
    
    print('\n Os elementos de entrada sao', VolumeCountList)
    
    if len(VolumeCountList) == 0:
        NullList=[0]
        return(NullList)
    
    else:
        LargestElement=VolumeCountList[0]
        index=0
        for x in list(range(len(VolumeCountList)-1)):
            if VolumeCountList[x+1][1] > LargestElement[1]:
                LargestElement=VolumeCountList[x+1]
                index=x+1
    
        ElementsList.append(LargestElement[0])
        print('aquiiii' , ElementsList)
        #print('Os maiores elementos são', ElementsList)
        del(VolumeCountList[index])
    
        if len(ElementsList) < NumberofElements:
            return(FindLargestElements(VolumeCountList,NumberofElements,ElementsList))
        
        else:
            print('\n Os maiores elementos da matrix sao', ElementsList)
            return(ElementsList)    


    
# Selecionando nas matrizes somente os elementos de maior volume
# a entrada ImgStackData eh um ndarray e ElementsList uma lista
def ElementsSelectionbyRange(ImgStackData,ElementsList): # o parametro ElementsList indica quais elementos ficarao na matriz
    
    try: 
        ImgStackData[0,0,0]
        for z in list(range(len(ImgStackData))):
            for y in list(range(len(ImgStackData[z]))):
                for x in list(range(len(ImgStackData[z][y]))):
                    if ImgStackData[z][y][x] not in ElementsList:
                        ImgStackData[z][y][x] = 0
        
        print('\n As dimensoes do stack de saida sao ', ImgStackData.shape)
        print('\n O maior valor na matrix da imagem final eh ', ImgStackData.max())

    except IndexError:
        for y in list(range(len(ImgStackData))):
            for x in list(range(len(ImgStackData[y]))):
                if ImgStackData[y][x] not in ElementsList:
                    ImgStackData[y][x] = 0

                    
        print('\n As dimensoes do stack de saida sao ', ImgStackData.shape)
        print('\n O maior valor na matrix da imagem final eh ', ImgStackData.max())
        
    return(ImgStackData)
 

# Selecionando nas matrizes somente os elementos de maior volume
# A entrada ImgStackData eh um ndarray e LargestElementsList eh uma lista
# o parametro LargestElementsList indica quantos dos maiores elementos ficarao na matrix
def ElementsSelectionLarge(ImgStackData,LargestElementsList): 
    
    try: 
        ImgStackData[0,0,0]
        for z in list(range(len(ImgStackData))):
            for y in list(range(len(ImgStackData[z]))):
                for x in list(range(len(ImgStackData[z][y]))):
                    if ImgStackData[z][y][x] not in LargestElementsList:
                        ImgStackData[z][y][x] = 0
            
        print('\n As dimensoes do stack de saida sao ', ImgStackData.shape)
        print('\n O maior valor na matrix da imagem final eh ', ImgStackData.max())

    except IndexError:
        for y in list(range(len(ImgStackData))):
            for x in list(range(len(ImgStackData[y]))):
                if ImgStackData[y][x] not in LargestElementsList:
                    ImgStackData[y][x] = 0
                       
        print('\n As dimensoes do stack de saida sao ', ImgStackData.shape)
        print('\n O maior valor na matrix da imagem final eh ', ImgStackData.max())
    
    return(ImgStackData)


# Filtrando os elementos que estão nos edges da matrix
# A entrada ImgStackData eh um labelled ndarray
def ElementsSelectionOutEdge(ImgStackData):

    LabelledImgStack=morphology.label(ImgStackData, connectivity=1)
    MaxElement=LabelledImgStack.max()    
    
    try:
        ImgStackData[0,0,0]        
        for z in list(range(len(LabelledImgStack))):
            for y in list(range(len(LabelledImgStack[z]))):
                for x in list(range(len(LabelledImgStack[z,y]))):
                    for elemN in list(np.arange(1, 1+MaxElement)):
                        if LabelledImgStack[z, y, x] == elemN:
                            try:
                                LabelledImgStack[z-1, y, x]
                                LabelledImgStack[z+1, y, x]
                                LabelledImgStack[z, y-1, x]
                                LabelledImgStack[z, y+1, x]
                                LabelledImgStack[z, y, x-1]
                                LabelledImgStack[z, y, x+1]
                            
                            except IndexError:
                                LabelledImgStack=np.where(LabelledImgStack == elemN, 0, LabelledImgStack)
                                continue
    except IndexError:           
            for y in list(range(len(LabelledImgStack))):
                for x in list(range(len(LabelledImgStack[y]))):
                    if LabelledImgStack[y, x] == elemN:
                        for elemN in list(np.arange(1, 1+MaxElement)): 
                            try: 
                                LabelledImgStack[y-1, x]
                                LabelledImgStack[y+1, x]
                                LabelledImgStack[y, x-1]
                                LabelledImgStack[y, x+1]
                            
                            except IndexError:
                                LabelledImgStack=np.where(LabelledImgStack == elemN, 0, LabelledImgStack)
    
    
    return(LabelledImgStack)


# Função para importar imagens e filtrar elementos por range de volume
def SelectionbyRange(diretorio,
                     stackNumber,
                     FirstSlice,LastSlice,
                     Xmin,Xmax,Ymin,Ymax,
                     minVolume,maxVolume,
                     ImportstackRootName='/Raw',
                     importFormat='.png',
                     ExportDir='/Processed',
                     AreaBorderSize=5,
                     Channel='',
                     
                     CropVolMode=False,
                     ReferenceStackToCrop='/Binarize/bac/ImageJ/t1',
                     RefminArea=1,RefmaxArea=2000000,
                     MAXElementsToCrop=10,
                     
                     ColonyTimeCheckMode=False,
                     ReferenceImgToCheckAttachment='/Binarize/bac/ImageJ/t1',
                     ReferenceImgToCheckDetachment='/Binarize/bac/ImageJ/t2',
                     RefminAreaCheck=1,RefmaxAreaCheck=2000000,
                     MAXElementsToCheck=10,
                     MaxTimePoint=15):
    
    
    SliceRange=list(range(FirstSlice,LastSlice+1))
    Imglist1=[]
    
    print('\n Importando as imagens... \n')
    
    for x in SliceRange:
        if x < 10:
            a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice00' + str(x) + importFormat)
            b=a[Ymin:Ymax,Xmin:Xmax]
            
        elif 10 <= x < 100:
            a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice0' + str(x) + importFormat)
            b=a[Ymin:Ymax,Xmin:Xmax]

        elif 100 <= x < 1000:
            a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)            
            b=a[Ymin:Ymax,Xmin:Xmax]
            
        Imglist1.append(b)
    
    ImgArray3D=np.array(Imglist1)
    
    print('O stack tem ', len(ImgArray3D),' slices')
    print('A imagem tem ', len(ImgArray3D[0]),' linhas')
    print('A imagem tem ', len(ImgArray3D[0][0]),' colunas')
    print('O maior valor do stack eh ', ImgArray3D.max())
    
    try:
        print('A imagem tem ',len(ImgArray3D[0][0][0]),' canais')
    
    except TypeError:         
        print('A imagem soh tem 1 canal')
    
    ImgArray3DNorm = np.where(ImgArray3D > 0, 1, 0)
    print('O maior valor do stack normalizado eh ', ImgArray3DNorm.max())
    
    print('\n Identificando os elementos... \n')
       
    LabelledImgs=morphology.label(ImgArray3DNorm,connectivity=1)
    
    #print('Type morphImgs',type(LabelledImgs))


    
    if CropVolMode == False and ColonyTimeCheckMode == False:
        
        print('\n Iniciando a seleção de tamanhos para o stack inteiro... \n')
        
        SelP1=CountElements(LabelledImgs)
        SelP2=FindVolElements(SelP1,minVolume,maxVolume)    
        SelP3=ElementsSelectionbyRange(LabelledImgs,SelP2)
        
        del(SelP1)
        del(SelP2)
        
        for imgN in list(range(len(SelP3))):
            
            if not os.path.exists(diretorio + ExportDir + '/t' + str(stackNumber)):
                os.makedirs(diretorio + ExportDir + '/t' + str(stackNumber))
            
            abc1=np.where(SelP3[imgN] > 0, 255, 0)
            io.imsave(diretorio + ExportDir + '/t' + str(stackNumber) + '/Slice' + str(SliceRange[imgN]) + importFormat, abc1)



    elif CropVolMode == True:
        print('\n Iniciando o CropRegion module para o stack ', str(stackNumber), ' ... \n')
        
        refImage=io.imread(diretorio + ReferenceStackToCrop + '/ZProjection' + importFormat)
        
        refImageNorm=np.where(refImage > 0, 1, 0)
        RefimgLab=morphology.label(refImageNorm,connectivity=1)

        RefP1=CountElements(RefimgLab)
        RefP2=FindVolElements(RefP1,RefminArea,RefmaxArea)
        
        if len(RefP2) > MAXElementsToCrop:
            
            print('\n \n Elementos a serem cropados ', len(RefP2), '\n \n ')            
            print('\n \n Abortando por excesso de elementos a serem cropados \n \n ')
        
        else:
            RefP3=ElementsSelectionbyRange(RefimgLab,RefP2)
            
            if not os.path.exists(diretorio + '/Imagens'):
                os.makedirs(diretorio + '/Imagens')
            
            RefP4 = np.where(RefP3 > 0, 255, 0)
            io.imsave(diretorio + ReferenceStackToCrop + '/ZProjectionFiltered' + importFormat, RefP4)
                        
            print('\n \n Serao ', len(RefP2), 'para cropar \n \n ')
            
            del(RefP1)      
            
            indexToSave=1
            for elem in list(range(len(RefP2))):
                print('\n Procurando o elemento', RefP2[elem], '\n')
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
                        
                    print('Indices fora da matrix. Excluindo o elemento ', RefP2[elem])
                    pass    
                
                else:
                    try:
                        for imgN in list(range(len(LabelledImgs))):
                            aa1F=LabelledImgs[imgN][Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize]
                            bb1F=np.where(aa1F > 0, 255, 0)                            
                            
                            if not os.path.exists(diretorio + ExportDir + '/t' + str(stackNumber) + '/CropRegions/Region' + str(indexToSave)):
                                os.makedirs(diretorio + ExportDir + '/t' + str(stackNumber) + '/CropRegions/Region' + str(indexToSave))
                
                            io.imsave(diretorio + ExportDir + '/t' + str(stackNumber) + '/CropRegions/Region' + str(indexToSave) + '/Slice' + str(SliceRange[imgN]) + importFormat, bb1F)
                            
                            if not os.path.exists(diretorio + '/Imagens'):
                                os.makedirs(diretorio + '/Imagens')
                            
                            try:
                                RefImgwithRegOverlay=io.imread(diretorio + '/Imagens/ZProjectionCropped_'+ str(Channel) + importFormat)
                            
                            except FileNotFoundError:
                                RefImgwithRegOverlay = np.zeros((len(ImgArray3D[0]), len(ImgArray3D[0][0])), dtype=np.uint8)
                            
                            rectangle=np.array(((Ymin-AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmin-AreaBorderSize)))
                            rr, cc = draw.polygon(rectangle[:,0], rectangle[:,1])
                            RefImgwithRegOverlay[rr, cc] = 255

                            io.imsave(diretorio + '/Imagens/ZProjectionCropped_'+ str(Channel) + importFormat, RefImgwithRegOverlay)
                            
                        indexToSave = indexToSave+1
                    
                    except PermissionError or OSError or IndexError:
                        pass



    elif ColonyTimeCheckMode == True:
        print('\n Iniciando o ColonyTimeCheckMode module para o stack ', str(stackNumber), ' ... \n')
        refImageCheckAT=io.imread(diretorio + ReferenceImgToCheckAttachment + '/ZProjection' + importFormat)
        
        refImageNormCheckAT=np.where(refImageCheckAT > 0, 1, 0)
        RefimgLabCheckAT=morphology.label(refImageNormCheckAT, connectivity=1)
        RefP1b=CountElements(RefimgLabCheckAT)
        RefP2b=FindVolElements(RefP1b,RefminAreaCheck,RefmaxAreaCheck)

        
        refImageCheckDeT=io.imread(diretorio + ReferenceImgToCheckDetachment + '/ZProjection' + importFormat)
        
        refImageNormCheckDeT=np.where(refImageCheckDeT > 0, 1, 0)
        RefimgLabCheckDeT=morphology.label(refImageNormCheckDeT, connectivity=1)
        RefP1c=CountElements(RefimgLabCheckDeT)
        RefP2c=FindVolElements(RefP1c,RefminAreaCheck,RefmaxAreaCheck)

        
        if len(RefP2b) > MAXElementsToCheck or len(RefP2c) > MAXElementsToCheck:
            
            print('\n \n Elementos a serem checados para o Attachment', len(RefP2b), '\n \n ')
            print('\n \n Elementos a serem checados  para o Dettachment', len(RefP2c), '\n \n ')
            print('\n \n Abortando por excesso de elementos a serem cropados \n \n ')
        
        else:
            RefP3b=ElementsSelectionbyRange(RefimgLabCheckAT, RefP2b)
            RefP3c=ElementsSelectionbyRange(RefimgLabCheckDeT, RefP2c)
            
            if not os.path.exists(diretorio + '/Imagens'):
                os.makedirs(diretorio + '/Imagens')
            
            RefP4b = np.where(RefP3b > 0, 255, 0)
            RefP4c = np.where(RefP3c > 0, 255, 0)
            io.imsave(diretorio + ReferenceImgToCheckAttachment + '/ZProjectionFiltered_AT' + importFormat, RefP4b)
            io.imsave(diretorio + ReferenceImgToCheckDetachment + '/ZProjectionFiltered_DeT' + importFormat, RefP4c)            
            
            print('\n \n Serao ', len(RefP2b), 'para checar para o Attachment Analysis \n \n ')
            print('\n \n Serao ', len(RefP2c), 'para checar para o Detachment Analysis \n \n ')
        
            del(RefP1b)  
            del(RefP1c)
            
            #Attachment Analysis
            for elem in list(range(len(RefP2b))):
                print('\n Procurando o elemento', RefP2b[elem], '\n')
                XPosList=[]
                YPosList=[]
                for YPos in list(range(len(RefP3b))):
                    for XPos in list(range(len(RefP3b[YPos]))):
                        if RefP3b[YPos,XPos] == RefP2b[elem]:
                            YPosList.append(YPos)
                            XPosList.append(XPos)
                
                Ymin=min(YPosList)
                Ymax=max(YPosList)
                Xmin=min(XPosList)
                Xmax=max(XPosList)
                
                del(XPosList)
                del(YPosList)
                            
                if (Ymin-AreaBorderSize) <= 0 or (Ymax+AreaBorderSize) >= len(RefP3b) or (Xmin-AreaBorderSize) <= 0 or (Xmax+AreaBorderSize) >= len(RefP3b[0]):
                        
                    print('Indices fora da matrix. Excluindo o elemento ', RefP2b[elem])
                    pass    
                
                else:
                    if LabelledImgs[:,Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize].sum() > 0:
                        
                        try:
                            RefImgwithRegOverlayb=io.imread(diretorio + '/Imagens/TimeAnalysis_AT' + importFormat)
                        
                        except FileNotFoundError:
                            RefImgwithRegOverlayb = np.zeros((len(ImgArray3D[0]), len(ImgArray3D[0][0])), dtype=np.uint8)
                        
                        rectangleb=np.array(((Ymin-AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmin-AreaBorderSize)))
                        rr, cc = draw.polygon(rectangleb[:,0], rectangleb[:,1])
                        
                        try:
                            if RefImgwithRegOverlayb[Ymin-1:Ymax+1,Xmin-1:Xmax+1].sum() == 0:
                                RefImgwithRegOverlayb[rr, cc] = int((stackNumber/MaxTimePoint) * 255)
                                io.imsave(diretorio + '/Imagens/TimeAnalysis_AT' + importFormat, RefImgwithRegOverlayb)
                            
                        except IndexError:
                            pass
                    
                    else:
                        pass
                
                
            #Detachment Analysis
            for elem in list(range(len(RefP2c))):
                print('\n Procurando o elemento', RefP2c[elem], '\n')
                XPosList=[]
                YPosList=[]
                for YPos in list(range(len(RefP3c))):
                    for XPos in list(range(len(RefP3c[YPos]))):
                        if RefP3c[YPos,XPos] == RefP2c[elem]:
                            YPosList.append(YPos)
                            XPosList.append(XPos)
                
                Ymin=min(YPosList)
                Ymax=max(YPosList)
                Xmin=min(XPosList)
                Xmax=max(XPosList)
                
                del(XPosList)
                del(YPosList)
                            
                if (Ymin-AreaBorderSize) <= 0 or (Ymax+AreaBorderSize) >= len(RefP3c) or (Xmin-AreaBorderSize) <= 0 or (Xmax+AreaBorderSize) >= len(RefP3c[0]):
                        
                    print('Indices fora da matrix. Excluindo o elemento ', RefP2c[elem])
                    pass    
                
                else:
                    if LabelledImgs[:,Ymin-AreaBorderSize:Ymax+AreaBorderSize,Xmin-AreaBorderSize:Xmax+AreaBorderSize].sum() == 0:
                        
                        try:
                            RefImgwithRegOverlayb=io.imread(diretorio + '/Imagens/TimeAnalysis_DeT' + importFormat)
                        
                        except FileNotFoundError:
                            RefImgwithRegOverlayb = np.zeros((len(ImgArray3D[0]), len(ImgArray3D[0][0])), dtype=np.uint8)
                        
                        rectangleb=np.array(((Ymin-AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmin-AreaBorderSize),(Ymax+AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmax+AreaBorderSize),(Ymin-AreaBorderSize,Xmin-AreaBorderSize)))
                        rr, cc = draw.polygon(rectangleb[:,0], rectangleb[:,1])
                        
                        try:
                            if RefImgwithRegOverlayb[Ymin-1:Ymax+1,Xmin-1:Xmax+1].sum() == 0:
                                RefImgwithRegOverlayb[rr, cc] = int((stackNumber/MaxTimePoint) * 255)
                                io.imsave(diretorio + '/Imagens/TimeAnalysis_DeT' + importFormat, RefImgwithRegOverlayb)
                            
                        except IndexError:
                            pass
                    
                    else:
                        pass
                        

              
# Função para importar imagens e filtrar maiores elementos escolhidos
def SelectionInnerElements(diretorio,stackNumber,
                           FirstSlice,LastSlice,
                           ImportstackRootName='/Raw',
                           importFormat='.png',
                           ExportDir='/Processed',
                           RegionAnalysis=False,
                           FirstRegion=1,LastRegion=2):
    
    SliceRange=list(range(FirstSlice,LastSlice+1))
    
    if RegionAnalysis == False:
        
        Imglist1=[]
        for x in SliceRange:
            a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/Slice' + str(x) + importFormat)
            
            Imglist1.append(a)
    
        ImgArray3D=np.array(Imglist1)
    
        print('\n O stack tem ',len(ImgArray3D),' slices')
        print('\n A imagem tem ',len(ImgArray3D[0]),' linhas')
        print('\n A imagem tem ',len(ImgArray3D[0][0]),' colunas')
        print('\n O maior valor do stack eh ', ImgArray3D.max())
        
        try:
            print('\n A imagem tem ',len(ImgArray3D[0][0][0]),' canais')
        
        except TypeError:         
            print('\n A imagem soh tem 1 canal')
        
        ImgArray3DNorm = np.where(ImgArray3D > 0, 1, 0)
        print('\n O maior valor do stack normalizado eh ', ImgArray3DNorm.max())    
        
        #print('Type morphImgs',type(LabelledImgs))
        
        SelP3=ElementsSelectionOutEdge(ImgArray3DNorm)
    
        #print('SelP3',type(SelP3))
        
        for imgN in list(range(len(SelP3))):
            
            if not os.path.exists(diretorio + ExportDir + '/t' + str(stackNumber)):
                os.makedirs(diretorio + ExportDir + '/t' + str(stackNumber))
            
            abc1=np.where(SelP3[imgN] > 0, 255, 0)
            io.imsave(diretorio + ExportDir + '/t' + str(stackNumber) + '/Slice' + str(SliceRange[imgN]) + importFormat, abc1)
            
    if RegionAnalysis == True:
        RegionList=list(range(FirstRegion,LastRegion+1))
        
        for region in RegionList:
            
            Imglist1=[]
            for x in SliceRange:
                a=io.imread(diretorio + ImportstackRootName + '/t' + str(stackNumber) + '/CropRegions/Region' + str(region) + '/Slice' + str(x) + importFormat)
                
                Imglist1.append(a)
        
            ImgArray3D=np.array(Imglist1)
        
            print('\n O stack tem ',len(ImgArray3D),' slices')
            print('\n A imagem tem ',len(ImgArray3D[0]),' linhas')
            print('\n A imagem tem ',len(ImgArray3D[0][0]),' colunas')
            print('\n O maior valor do stack eh ', ImgArray3D.max())
            
            try:
                print('\n A imagem tem ',len(ImgArray3D[0][0][0]),' canais')
            
            except TypeError:         
                print('\n A imagem soh tem 1 canal')
            
            ImgArray3DNorm = np.where(ImgArray3D > 0, 1, 0)
            print('\n O maior valor do stack normalizado eh ', ImgArray3DNorm.max())
                        
            #print('Type morphImgs',type(LabelledImgs))
            
            SelP3=ElementsSelectionOutEdge(ImgArray3DNorm)
        
            #print('SelP3',type(SelP3))
            
            for imgN in list(range(len(SelP3))):
                
                if not os.path.exists(diretorio + ExportDir + '/t' + str(stackNumber) + '/CropRegions/Region' + str(region)):
                    os.makedirs(diretorio + ExportDir + '/t' + str(stackNumber) + '/CropRegions/Region' + str(region))
                
                abc1=np.where(SelP3[imgN] > 0, 255, 0)
                io.imsave(diretorio + ExportDir + '/t' + str(stackNumber) + '/CropRegions/Region' + str(region) + '/Slice' + str(SliceRange[imgN]) + importFormat, abc1)
