
def ShapeAnalysisPLOT(SettingsDic):

    import matplotlib.pyplot as plt
    import os
    import MODImpExp
    import numpy as np
    
    diretorio=os.getcwd()
    
    stackList=list(range(1,SettingsDic['timePoints']+1))
    timeInterval=SettingsDic['timeinterval']
    initialTimePoint=0
    
    
    VolumeList=[]
    VolQhullRatioList=[]
    AspRatioList=[]
    
    
    for Stack in stackList:
        
        aa=open(diretorio+'/Shape' + '/Volume_t' + str(Stack) + '.txt', 'r')
        VolumeList.append(np.array(MODImpExp.ConvertStrTOData2(aa, ',', 100)))
        aa.close()
        
        bb=open(diretorio+'/Shape' + '/QhullVolRatio_t' + str(Stack) + '.txt', 'r')
        VolQhullRatioList.append(np.array(MODImpExp.ConvertStrTOData2(bb, ',', 100)))
        bb.close()   
    
        cc=open(diretorio+'/Shape' + '/AspRatio_t' + str(Stack) + '.txt', 'r')
        AspRatioList.append(np.array(MODImpExp.ConvertStrTOData2(cc, ',', 100)))
        cc.close()
    
    
    fig1a=plt.figure(figsize=(7, 7), facecolor='w', edgecolor='k') 
    
    g1_1=plt.subplot2grid((1,2),(0,0),rowspan=1,colspan=1)
    g1_1.set_title('Convex hull',fontsize=13)
    g1_1.set_ylabel('(qhull Volume / Volume) Ratio', fontsize=13)
    g1_1.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
    g1_1.set_ylim(0.05, 11)
    g1_1.set_xlim(-30,2400)
    g1_1.set_xticks([0,500,1000,1500,2000])
    g1_1.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
    g1_1.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
    g1_1.axhline(y=4, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    g1_1.axvline(x=150, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    
    g1_2=plt.subplot2grid((1,2),(0,1),rowspan=1,colspan=1)
    g1_2.set_title('Zoom in',fontsize=13)
    g1_2.set_ylabel('(qhull Volume / Volume) Ratio', fontsize=13)
    g1_2.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
    g1_2.set_ylim(0.05, 11)
    g1_2.set_xlim(-20,350)
    g1_2.set_xticks([0,100,200,300])
    g1_2.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
    g1_2.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
    g1_2.axhline(y=4, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    g1_2.axvline(x=150, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    
    
    fig1b=plt.figure(figsize=(7, 7), facecolor='w', edgecolor='k') 
    
    g2_1=plt.subplot2grid((1,2),(0,0),rowspan=1,colspan=1)
    g2_1.set_title('Aspect Ratio',fontsize=13)
    g2_1.set_ylabel('Aspect Ratio', fontsize=13)
    g2_1.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
    g2_1.set_ylim(0.9, 7)
    g1_1.set_xlim(-30,2000)
    g1_1.set_xticks([0,500,1000,1500,2000])
    g2_1.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
    g2_1.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
    g2_1.axhline(y=2, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    g2_1.axvline(x=50, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    
    g2_2=plt.subplot2grid((1,2),(0,1),rowspan=1,colspan=1)
    #g2_2.set_title('Histogram ',fontsize=8)
    g2_2.set_ylabel('Aspect Ratio', fontsize=13)
    g2_2.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
    g2_2.set_ylim(0.9, 7)
    g2_2.set_xlim(-3,60)
    g2_2.set_xticks([0,20,40,60])
    g2_2.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
    g2_2.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
    g2_2.axhline(y=2, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
    
    
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    
    HexColors=[]
    openHexColors=open(diretorio + '/HexColorsSelected.txt', 'r')
    for line in openHexColors:
        HexColors.append(str(line)[:-1])
        
    ColorList=[]
    for StackNumber in list(range(len(stackList))):
        ColorList.append(HexColors[StackNumber])
    
    for StackNumber in list(range(len(stackList))):   
        g1_1.scatter(VolumeList[StackNumber][:,1], VolQhullRatioList[StackNumber][:,1], color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
        g1_1.legend(bbox_to_anchor=(0.5, 0.99), loc=2, borderaxespad=0.)
        g1_2.scatter(VolumeList[StackNumber][:,1], VolQhullRatioList[StackNumber][:,1], color=ColorList[StackNumber], alpha=0.7)
        #if stackList[StackNumber] == 2 or stackList[StackNumber] == 7 or stackList[StackNumber] == 15:
            #g1_2.hist(VolQhullRatioList[StackNumber][:,1], bins=15, color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
            #g1_2.legend(bbox_to_anchor=(0.65, 0.99), loc=2, borderaxespad=0.)
            
        g2_1.scatter(VolumeList[StackNumber][:,1], AspRatioList[StackNumber][:,1], color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
        g2_1.legend(bbox_to_anchor=(0.6, 0.99), loc=2, borderaxespad=0.)
        g2_2.scatter(VolumeList[StackNumber][:,1], AspRatioList[StackNumber][:,1], color=ColorList[StackNumber], alpha=0.7)    
        #if stackList[StackNumber] == 2 or stackList[StackNumber] == 7 or stackList[StackNumber] == 15:
            #g2_2.hist(AspRatioList[StackNumber][:,1], bins=15, color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
            #g2_2.legend(bbox_to_anchor=(0.65, 0.99), loc=2, borderaxespad=0.)
            
    plt.tight_layout()
    fig1a.savefig(diretorio + '/Images/ShapeAnalysis1.png', dpi = 300)
    fig1b.savefig(diretorio + '/Images/ShapeAnalysis2.png', dpi = 300)
    plt.show()