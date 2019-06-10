from skimage import filters

# Define um nested gaussian filter para ser aplicado nas imagens individuais (2D)
# A entrada eh um ndarray 2D
def NestedFilter2D(ImgArray,GaussMatrix2DVar,filter2DNestNumber=None,index=1):
    
    if filter2DNestNumber==None:
        return(ImgArray)
    
    else:
        
        def GaussianFilter2D(ImgArray,GaussMatrix2DVar):
            return(filters.gaussian(ImgArray,sigma=GaussMatrix2DVar))
    
        if index == filter2DNestNumber:
            return(GaussianFilter2D(ImgArray,GaussMatrix2DVar))
        
        else:
            index = index + 1
            ImgArray2=GaussianFilter2D(ImgArray,GaussMatrix2DVar)
            return(NestedFilter2D(ImgArray2,GaussMatrix2DVar,filter2DNestNumber,index))

# Define um nested gaussian filter para ser aplicado no stack (3D)
# A entrada eh um ndarray 3D
def NestedFilter3D(StackImgArray,GaussMatrix3DVar,filter3DNestNumber=None,index=1):
    
    if filter3DNestNumber==None:
        return(StackImgArray)
    
    else:
        
        def GaussianFilter3D(StackImgArray,GaussMatrix3DVar):
            return(filters.gaussian(StackImgArray,sigma=GaussMatrix3DVar,multichannel=None))
    
        if index == filter3DNestNumber:
            return(GaussianFilter3D(StackImgArray,GaussMatrix3DVar))
        
        else:
            index = index + 1
            StackImgArray2=GaussianFilter3D(StackImgArray,GaussMatrix3DVar)
            return(NestedFilter3D(StackImgArray2,GaussMatrix3DVar,filter3DNestNumber,index))