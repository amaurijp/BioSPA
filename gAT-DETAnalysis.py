import numpy as np
import os
from skimage import io
import matplotlib.pyplot as plt

diretorio=os.getcwd()

MapField=[319.45,319.45] # [DeltaX, DelatY] in microns
MaxTimePoint=15
TimeInterval=30


ATData=io.imread(diretorio + '/Imagens/TimeAnalysis_AT.png')
ATticks=[]
for point in list(np.arange(0,255+1,255/MaxTimePoint)):
    if point <= ATData.max():
        ATticks.append(int((point/255)*(TimeInterval*MaxTimePoint)))
    else:
        break

DETData=io.imread(diretorio + '/Imagens/TimeAnalysis_DeT.png')
DETticks=[]
for point in list(np.arange(0,255+1,255/MaxTimePoint)):
    if point <= DETData.max():
        DETticks.append(int((point/255)*(TimeInterval*MaxTimePoint)))
    else:
        break

fig1=plt.figure(figsize=(20, 14), dpi=100, facecolor='w', edgecolor='k')

#Attachement map
map1=plt.subplot2grid((1,2),(0,1),rowspan=1,colspan=1)
map1.set_title('Bacteria attachment and growth map',fontsize=10)
map1.tick_params(which='both',
                 bottom='off', labelbottom='on',
                 top='off', labeltop='off',
                 left='off', labelleft='on', 
                 right='off', labelright='off',
                 labelsize='9')

map1.set_xlabel('$\\mu$m')
map1.set_xticks([0,int(len(ATData[0])/2),len(ATData[0])])
map1.set_xticklabels([str(0), str(int(MapField[0]/2)), str(int(MapField[0]))])
map1.set_yticks([0,int(len(ATData)/2),len(ATData)])
map1.set_yticklabels([str(int(MapField[1])), str(int(MapField[1]/2)), str(0)])

map1axi=map1.imshow(ATData, cmap='Spectral')

Colbar1=fig1.colorbar(map1axi, fraction=0.156, pad=0.08, orientation='horizontal')
Colbar1.set_label('Time (min)', fontsize=10)
Colbar1.set_ticks(list(np.arange(0,max(ATticks)+1,(255/(MaxTimePoint+1.5)))))
Colbar1.set_ticklabels(['']+[str(i) for i in ATticks])


#Detachement map
map2=plt.subplot2grid((1,2),(0,0),rowspan=1,colspan=1)
map2.set_title('Bacteria Detachment map',fontsize=10)
map2.tick_params(which='both',
                 bottom='on', labelbottom='on',
                 top='off', labeltop='off',
                 left='on', labelleft='on', 
                 right='off', labelright='off',
                 labelsize='9')

map2.set_xlabel('$\\mu$m')
map2.set_xticks([0,int(len(DETData[0])/2),len(DETData[0])])
map2.set_xticklabels([str(0), str(int(MapField[0]/2)), str(int(MapField[0]))])
map2.set_yticks([0,int(len(DETData)/2),len(DETData)])
map2.set_yticklabels([str(int(MapField[1])), str(int(MapField[1]/2)), str(0)])

map2axi=map2.imshow(DETData, cmap='coolwarm')

Colbar2=fig1.colorbar(map2axi, fraction=0.156, pad=0.08, orientation='horizontal')
Colbar2.set_label('Time (min)', fontsize=10)
Colbar2.set_ticks(list(np.arange(0,DETData.max()+1,(255/MaxTimePoint))))
Colbar2.set_ticklabels(['']+[str(i) for i in DETticks[1:]])

print('O maior valor de contraste encontrado no ATMap eh ', ATData.max(), ' min \n')
print('O ultimo evento encontrado no ATMap se da em ', ATData.max()/255*(TimeInterval*MaxTimePoint), ' min \n')

print('O maior valor de contraste encontrado no ATMap eh ', DETData.max(), ' min \n')
print('O ultimo evento encontrado no DetMap se da em ', DETData.max()/255*(TimeInterval*MaxTimePoint), ' min \n')

plt.tight_layout()
fig1.savefig(diretorio + '/Imagens/TimeColonization.png')
plt.show()