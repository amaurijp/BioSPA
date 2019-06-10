import matplotlib.pyplot as plt
import os
import MODImpExp
import numpy as np

diretorio=os.getcwd()

fileSalist_BACt1=open(diretorio+'/SUFAdjusted' + '/WithBAC_SaList_t1.txt', 'r')
DataSalist_BACt1=np.array(MODImpExp.ConvertStrTOData(fileSalist_BACt1, ','))
fileSalist_BACt1.close()

fileSalist_BACt2=open(diretorio+'/SUFAdjusted' + '/WithBAC_SaList_t2.txt', 'r')
DataSalist_BACt2=np.array(MODImpExp.ConvertStrTOData(fileSalist_BACt2, ','))
fileSalist_BACt2.close()

fileSqlist_BACt1=open(diretorio+'/SUFAdjusted' + '/WithBAC_SqList_t1.txt', 'r')
DataSqlist_BACt1=np.array(MODImpExp.ConvertStrTOData(fileSqlist_BACt1, ','))
fileSqlist_BACt1.close()

fileSqlist_BACt2=open(diretorio+'/SUFAdjusted' + '/WithBAC_SqList_t2.txt', 'r')
DataSqlist_BACt2=np.array(MODImpExp.ConvertStrTOData(fileSqlist_BACt2, ','))
fileSqlist_BACt2.close()

fileSsKlist_BACt1=open(diretorio+'/SUFAdjusted' + '/WithBAC_SsKList_t1.txt', 'r')
DataSsKlist_BACt1=np.array(MODImpExp.ConvertStrTOData(fileSsKlist_BACt1, ','))
fileSsKlist_BACt1.close()

fileSsKlist_BACt2=open(diretorio+'/SUFAdjusted' + '/WithBAC_SsKList_t2.txt', 'r')
DataSsKlist_BACt2=np.array(MODImpExp.ConvertStrTOData(fileSsKlist_BACt2, ','))
fileSsKlist_BACt2.close()


fileSalist_SUFt1=open(diretorio+'/SUFAdjusted' + '/WithoutBAC_SaList_t1.txt', 'r')
DataSalist_SUFt1=np.array(MODImpExp.ConvertStrTOData(fileSalist_SUFt1, ','))
fileSalist_SUFt1.close()

fileSqlist_SUFt1=open(diretorio+'/SUFAdjusted' + '/WithoutBAC_SqList_t1.txt', 'r')
DataSqlist_SUFt1=np.array(MODImpExp.ConvertStrTOData(fileSqlist_SUFt1, ','))
fileSqlist_SUFt1.close()

fileSsKlist_SUFt1=open(diretorio+'/SUFAdjusted' + '/WithoutBAC_SsKList_t1.txt', 'r')
DataSsKlist_SUFt1=np.array(MODImpExp.ConvertStrTOData(fileSsKlist_SUFt1, ','))
fileSsKlist_SUFt1.close()



fig1=plt.figure(figsize=(14, 10), facecolor='w', edgecolor='k') 
g1_1=plt.subplot2grid((3,5),(0,0),rowspan=1,colspan=3)
#g1_1.set_title('Sa values',fontsize=16)
g1_1.set_ylabel('Sa ($\\mu$m)', fontsize=16)
g1_1.set_xlabel('Area ($\\mu$$m^2$)', fontsize=16)
g1_1.set_ylim(-1,10)
g1_1.set_xlim(0,120)
g1_1.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_1.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)

g1_2=plt.subplot2grid((3,5),(1,0),rowspan=1,colspan=3)
#g1_2.set_title('Sq values',fontsize=16)
g1_2.set_ylabel('Sq ($\\mu$m)', fontsize=16)
g1_2.set_xlabel('Area ($\\mu$$m^2$)', fontsize=16)
g1_2.set_ylim(-1,11)
g1_2.set_xlim(0,120)
g1_2.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_2.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)

g1_3=plt.subplot2grid((3,5),(2,0),rowspan=1,colspan=3)
#g1_3.set_title('Ssk values',fontsize=16)
g1_3.set_ylabel('Ssk', fontsize=16)
g1_3.set_xlabel('Area ($\\mu$$m^2$)', fontsize=16)
g1_3.set_ylim(-15,55)
g1_3.set_xlim(0,120)
g1_3.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_3.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)

g1_4=plt.subplot2grid((3,5),(0,3),rowspan=1,colspan=1)
g1_4.set_ylabel('Norm. Frequency', fontsize=16)
g1_4.set_xlabel('Sa values', fontsize=16)
g1_4.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_4.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)
g1_4.set_xlim(0,3)

g1_5=plt.subplot2grid((3,5),(0,4),rowspan=1,colspan=1)
g1_5.set_ylabel('Norm. Frequency', fontsize=16)
g1_5.set_xlabel('Sa values', fontsize=16)
g1_5.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_5.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)
g1_5.set_xlim(0,3)

g1_6=plt.subplot2grid((3,5),(1,3),rowspan=1,colspan=1)
g1_6.set_ylabel('Norm. Frequency', fontsize=16)
g1_6.set_xlabel('Sq values', fontsize=16)
g1_6.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_6.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)
g1_6.set_xlim(0,5)

g1_7=plt.subplot2grid((3,5),(1,4),rowspan=1,colspan=1)
g1_7.set_ylabel('Norm. Frequency', fontsize=16)
g1_7.set_xlabel('Sq values', fontsize=16)
g1_7.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_7.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)
g1_7.set_xlim(0,5)

g1_8=plt.subplot2grid((3,5),(2,3),rowspan=1,colspan=1)
g1_8.set_ylabel('Norm. Frequency', fontsize=16)
g1_8.set_xlabel('Ssk values', fontsize=16)
g1_8.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_8.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)
g1_8.set_xlim(-10,10)

g1_9=plt.subplot2grid((3,5),(2,4),rowspan=1,colspan=1)
g1_9.set_ylabel('Norm. Frequency', fontsize=16)
g1_9.set_xlabel('Ssk values', fontsize=16)
g1_9.tick_params(axis="y", colors='k', labelsize=15, width=1.5,length=3.5)
g1_9.tick_params(axis="x", colors='k', labelsize=15, width=1.5,length=3.5)
g1_9.set_xlim(-10,10)

g1_1.scatter(np.array(DataSalist_SUFt1)[:,1], np.array(DataSalist_SUFt1)[:,2], color='y', alpha=0.3, label='non colonized areas (n.c.a)')
g1_1.scatter(np.array(DataSalist_BACt1)[:,1], np.array(DataSalist_BACt1)[:,2], color='r', alpha=0.4, label='initial attachment ($t_0$)')
g1_1.scatter(np.array(DataSalist_BACt2)[:,1], np.array(DataSalist_BACt2)[:,2], color='b', alpha=0.3, label='after the flow (flow)')
g1_1.legend(bbox_to_anchor=(0.42, 0.95), loc=2, borderaxespad=0., ncol=1, fontsize=16)

g1_2.scatter(np.array(DataSqlist_SUFt1)[:,1], np.array(DataSqlist_SUFt1)[:,2], color='tab:gray', alpha=0.3, label='non colonized areas (n.c.a)')
g1_2.scatter(np.array(DataSqlist_BACt1)[:,1], np.array(DataSqlist_BACt1)[:,2], color='m', alpha=0.4, label='initial attachment ($t_0$)')
g1_2.scatter(np.array(DataSqlist_BACt2)[:,1], np.array(DataSqlist_BACt2)[:,2], color='c', alpha=0.6, label='after the flow (flow)')
g1_2.legend(bbox_to_anchor=(0.42, 0.95), loc=2, borderaxespad=0., ncol=1, fontsize=16)

g1_3.scatter(np.array(DataSsKlist_SUFt1)[:,1], np.array(DataSsKlist_SUFt1)[:,2], color='g', alpha=0.3, label='non colonized areas (n.c.a)')
g1_3.scatter(np.array(DataSsKlist_BACt1)[:,1], np.array(DataSsKlist_BACt1)[:,2], color='k', alpha=0.5, label='initial attachment ($t_0$)')
g1_3.scatter(np.array(DataSsKlist_BACt2)[:,1], np.array(DataSsKlist_BACt2)[:,2], color='r', alpha=0.3, label='after the flow (flow)')
g1_3.legend(bbox_to_anchor=(0.42, 0.95), loc=2, borderaxespad=0., ncol=1, fontsize=16)

g1_4.hist(np.array(DataSalist_SUFt1)[:,2], bins=40, normed=True, color='y', alpha=0.3, label='n.c.a.')
g1_4.hist(np.array(DataSalist_BACt1)[:,2], bins=40, normed=True, color='r', alpha=0.3, label='$t_0$')
g1_4.legend(bbox_to_anchor=(0.3, 0.95), loc=2, borderaxespad=0., mode='expand', ncol=1, fontsize=13)

g1_5.hist(np.array(DataSalist_BACt1)[:,2], bins=40, normed=True, color='r', alpha=0.3, label='$t_0$')
g1_5.hist(np.array(DataSalist_BACt2)[:,2], bins=40, normed=True, color='b', alpha=0.3, label='flow')
g1_5.legend(bbox_to_anchor=(0.3, 0.95), loc=2, borderaxespad=0., mode='expand', ncol=1, fontsize=13)

g1_6.hist(np.array(DataSqlist_SUFt1)[:,2], bins=40, normed=True, color='tab:gray', alpha=0.3, label='n.c.a.')
g1_6.hist(np.array(DataSqlist_BACt1)[:,2], bins=40, normed=True, color='m', alpha=0.3, label='$t_0$')
g1_6.legend(bbox_to_anchor=(0.3, 0.95), loc=2, borderaxespad=0., mode='expand', ncol=1, fontsize=13)

g1_7.hist(np.array(DataSqlist_BACt1)[:,2], bins=40, normed=True, color='m', alpha=0.3, label='$t_0$')
g1_7.hist(np.array(DataSqlist_BACt2)[:,2], bins=40, normed=True, color='c', alpha=0.3, label='flow')
g1_7.legend(bbox_to_anchor=(0.3, 0.95), loc=2, borderaxespad=0., mode='expand', ncol=1, fontsize=13)

g1_8.hist(np.array(DataSsKlist_SUFt1)[:,2], bins=40, normed=True, color='g', alpha=0.3, label='n.c.a.')
g1_8.hist(np.array(DataSsKlist_BACt1)[:,2], bins=40, normed=True, color='k', alpha=0.3, label='flow')
g1_8.legend(bbox_to_anchor=(0.2, 0.95), loc=2, borderaxespad=0., ncol=1, fontsize=13)

g1_9.hist(np.array(DataSsKlist_BACt1)[:,2], bins=40, normed=True, color='k', alpha=0.3, label='$t_0$')
g1_9.hist(np.array(DataSsKlist_BACt2)[:,2], bins=40, normed=True, color='r', alpha=0.3, label='flow')
g1_9.legend(bbox_to_anchor=(0.2, 0.95), loc=2, borderaxespad=0., ncol=1, fontsize=13)


plt.tight_layout(pad=2, h_pad=None, w_pad=None)
fig1.savefig(diretorio + '/Imagens/TopoAnalysis.png', dpi = 300)
plt.show()
