import os


#Convertendo a lista de str em lista de números
def ConvertStrTOData(TXTData, delimiter=False):
    DataMod=[] # Achando os delimitadores
    if delimiter == False:
        for line in list(TXTData):
            DataMod.append(float(line[0:-1]))
        
        return(DataMod)
    
    else:    
        for line in list(TXTData):
            DataMod.append(delimiter + ' ' + line[1:-2] + delimiter)
            
        # return(ImgDataMod)
            
        ListDelim=[] # Achando os delimitadores        
        for line in DataMod:
            Delimiters=[]
            for x in list(range(len(line))):
                if line[x] == delimiter: #o delimiter é uma str
                    Delimiters.append(x)
                    
            ListDelim.append(Delimiters)
    
        # return(ListDelim)
        
        Data=[]
        for lineNumber in list(range(len(DataMod))): #convertend str to floats
            RowElements=[]
            for y in list(range(len(ListDelim[lineNumber])-1)):
                try:
                    RowElements.append(float(DataMod[lineNumber][ListDelim[lineNumber][y]+2:ListDelim[lineNumber][y+1]]))
                
                except ValueError:
                    RowElements.append(DataMod[lineNumber][ListDelim[lineNumber][y]+2:ListDelim[lineNumber][y+1]])
                
            Data.append(RowElements)
    
        return(Data)
    

#Convertendo a lista de str em lista de números
def ConvertStrTOData2(TXTData, delimiter, LinesToTake):
    DataMod=[] # Achando os delimitadores
    Input=list(TXTData)
    for lineNumber in list(range(len(Input))):
        if lineNumber+1 <= LinesToTake:
            DataMod.append(delimiter + ' ' + Input[lineNumber][1:-2] + delimiter)
        
    # return(ImgDataMod)
        
    ListDelim=[] # Achando os delimitadores        
    for line in DataMod:
        Delimiters=[]
        for x in list(range(len(line))):
            if line[x] == delimiter: #o delimiter é uma str
                Delimiters.append(x)
                
        ListDelim.append(Delimiters)

    # return(ListDelim)
    
    Data=[]
    for lineNumber in list(range(len(DataMod))): #convertend str to floats
        RowElements=[]
        for y in list(range(len(ListDelim[lineNumber])-1)):
            try:
                RowElements.append(float(DataMod[lineNumber][ListDelim[lineNumber][y]+2:ListDelim[lineNumber][y+1]]))
            
            except ValueError:
                RowElements.append(DataMod[lineNumber][ListDelim[lineNumber][y]+2:ListDelim[lineNumber][y+1]])
            
        Data.append(RowElements)

    return(Data)


#Importando as matrizes das imagens extraidas pelo Mathematica e convertendo de string para listas
def ImportImgTXTToData(diretorio,fileRoot):

    DataList1=[]
    MatrixImp=open(diretorio + fileRoot + '.txt','r')
    ImportedMatrix=ConvertStrTOData(MatrixImp,',') #essa função converte de string para lista no python
    DataList1.append(ImportedMatrix)
    MatrixImp.close()
    
    return(DataList1)


# Função para exportar em txt as matrizes das imagens
# A entrada eh uma lista
def ExportImgToData(diretorio,stackRootName,ImgData,stackNumber,SliceNumber):

    if not os.path.exists(diretorio + stackRootName + '/TXTData/t' + str(stackNumber)):
        os.makedirs(diretorio + stackRootName + '/TXTData/t' + str(stackNumber))

    fileXport=open(diretorio + stackRootName + '/TXTData/t' + str(stackNumber) + '/Slice' + str(SliceNumber) + '.txt','w')
    
    for line in ImgData:
        fileXport.write(str(line) + '\n')
    
    fileXport.close()
    
    

# Função normalizar
# A entrada é uma Image ou Stack no formato de lista
def NormalizeList(imgStackData):
    try:
        imgStackData[0,0,0]
        flat_list=[]
        for k in imgStackData:
            for j in k:
                for i in j:
                    flat_list.append(i)
    
        MAX=max(flat_list)
        
        list1=[]
        for k in imgStackData:
            list2=[]
            for j in k:
                list2.append([i/MAX for i in j])
            
            list1.append(list2)
    
    except IndexError: 
        flat_list=[]
        for j in imgStackData:
            for i in j:
                    flat_list.append(i)
    
        MAX=max(flat_list)
        
        list1=[]
        for j in imgStackData:
            list1.append([i/MAX for i in j])       
        
    return(list1)


# Função para converter as imagens em matrizes de posicao
def getPositions3D(imgStack):
    POSlistZ=[]
    for k in list(range(len(imgStack))):
        POSlistY=[]
        for j in list(range(len(imgStack[k]))):
            POSlistX=[]
            for i in list(range(len(imgStack[k][j]))):
                POSlistX.append([[i+1,j+1,k+1],imgStack[len(imgStack)-k-1][len(imgStack[k])-j-1][i]])
            
            POSlistY.append(POSlistX)
        POSlistZ.append(POSlistY)
    
    return(POSlistZ)