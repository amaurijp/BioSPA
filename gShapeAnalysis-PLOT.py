import matplotlib.pyplot as plt
import os
import MODImpExp
import numpy as np

diretorio=os.getcwd()

stackList=list(range(1,17+1))
timeInterval=20
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


fig1=plt.figure(figsize=(13, 8), facecolor='w', edgecolor='k') 
g1_1=plt.subplot2grid((1,4),(0,0),rowspan=1,colspan=1)
g1_1.set_title('Convex shapes ',fontsize=13)
g1_1.set_ylabel('(qhull Volume / Volume) Ratio', fontsize=13)
g1_1.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
g1_1.set_ylim(0.05, 13)
g1_1.set_xlim(-100,1500)
g1_1.set_xticks([0,500,1000,1500])
g1_1.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
g1_1.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
g1_1.axhline(y=4, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
g1_1.axvline(x=150, color="r",linewidth=1.5, linestyle=':', alpha=0.8)

g1_2=plt.subplot2grid((1,4),(0,1),rowspan=1,colspan=1)
g1_2.set_ylabel('(qhull Volume / Volume) Ratio', fontsize=13)
g1_2.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
g1_2.set_ylim(0.05, 13)
g1_2.set_xlim(-20,750)
g1_2.set_xticks([0,200,400,600])
g1_2.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
g1_2.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
g1_2.axhline(y=1, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
g1_2.axhline(y=4, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
g1_2.axhline(y=10, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
g1_2.axvline(x=150, color="r",linewidth=1.5, linestyle=':', alpha=0.8)

g2_1=plt.subplot2grid((1,4),(0,2),rowspan=1,colspan=1)
g2_1.set_title('Aspect Ratio',fontsize=13)
g2_1.set_ylabel('Aspect Ratio', fontsize=13)
g2_1.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
#g2_1.set_ylim(0.9, 7)
g2_1.set_xlim(-100,1500)
g2_1.set_xticks([0,500,1000,1500])
g2_1.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
g2_1.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
g2_1.axhline(y=2, color="r",linewidth=1.5, linestyle=':', alpha=0.8)
g2_1.axvline(x=50, color="r",linewidth=1.5, linestyle=':', alpha=0.8)

g2_2=plt.subplot2grid((1,4),(0,3),rowspan=1,colspan=1)
#g2_2.set_title('Histogram ',fontsize=8)
g2_2.set_ylabel('Aspect Ratio', fontsize=13)
g2_2.set_xlabel('Volume ($\\mu$$m^3$)', fontsize=13)
#g2_2.set_ylim(0.9, 7)
g2_2.set_xlim(-3,60)
g2_2.set_xticks([0,20,40,60])
g2_2.tick_params(axis="y", colors='k', labelsize=12, width=1.5,length=3.5)
g2_2.tick_params(axis="x", colors='k', labelsize=12, width=1.5,length=3.5)
g2_2.axhline(y=2, color="r",linewidth=1.5, linestyle=':', alpha=0.8)


plt.subplots_adjust(wspace=0.3, hspace=0.8)

HexColors=[]
openHexColors=open(diretorio + '/HexColorsSelected.txt', 'r')
for line in openHexColors:
    HexColors.append(str(line)[:-1])
    
ColorList=[]
for StackNumber in list(range(len(stackList))):
    ColorList.append(HexColors[StackNumber])

for StackNumber in list(range(len(stackList))):   
    g1_1.scatter(np.array(VolumeList[StackNumber])[:,1], np.array(VolQhullRatioList[StackNumber])[:,1], color=ColorList[StackNumber], alpha=0.7)
    g1_2.scatter(np.array(VolumeList[StackNumber])[:,1], np.array(VolQhullRatioList[StackNumber])[:,1], color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
    g1_2.legend(bbox_to_anchor=(0.5, 0.99), loc=2, borderaxespad=0.)
    #if stackList[StackNumber] == 2 or stackList[StackNumber] == 7 or stackList[StackNumber] == 15:
        #g1_2.hist(VolQhullRatioList[StackNumber][:,1], bins=15, color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
        #g1_2.legend(bbox_to_anchor=(0.65, 0.99), loc=2, borderaxespad=0.)
    
    #print(np.array(AspRatioList[StackNumber])[:,1])    
    #g2_1.scatter(np.array(VolumeList[StackNumber])[:,1], np.array(AspRatioList[StackNumber])[:,1], color=ColorList[StackNumber], alpha=0.7)
    #g2_2.scatter(np.array(VolumeList[StackNumber])[:,1], np.array(AspRatioList[StackNumber])[:,1], color=ColorList[StackNumber], alpha=0.7)    
    #if stackList[StackNumber] == 2 or stackList[StackNumber] == 7 or stackList[StackNumber] == 15:
        #g2_2.hist(AspRatioList[StackNumber][:,1], bins=15, color=ColorList[StackNumber], alpha=0.7, label=str(stackList[StackNumber]*timeInterval-initialTimePoint)+'min')
        #g2_2.legend(bbox_to_anchor=(0.65, 0.99), loc=2, borderaxespad=0.)
        
plt.tight_layout()
fig1.savefig(diretorio + '/Imagens/ShapeAnalysis.png', dpi = 300)
plt.show()