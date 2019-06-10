import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
from skimage import io
import MODImpExp

diretorio=os.getcwd()

def VolAnalysis(ExperimentNumber,
                ImportRootFolderBAC,
                ImportRootFolderEPS,
                FirstStack=1,LastStack=2,
                initialTimePoint=0,
                timeinterval=30,
                ZStep=1,
                XYField=[100,100],
                RawImageDefinition=[500,500],
                RegionAnalysis=False,
                FirstRegion=1,Lastregion=2,
                SmutansRadius=0.5, #em microns
                Max_a_FitError=0.3,
                Max_b_FitError=0.5,
                
                p0_THR_val1=3,
                p0_THR_val2=20,
                
                Det_TopoXVol_relation=False,
                StackToFindRelation=1): #dado em celulas bacterianas

    StackList=list(range(FirstStack,LastStack+1))
    
    #Definindo a função de ajuste
    def expFunc1(x, a, b):
        return(v0 + (a * (x ** b)))
    
    def expFunc2(x, b):
        return(v0 + (x ** b))
    
    def linearFunc(x, a, b):
        return(a + x * b)
    
    if RegionAnalysis == False:
        #Figura 1
        fig1=plt.figure(figsize=(6, 8), facecolor='w', edgecolor='k') 
        g1=plt.subplot2grid((2,1),(0,0),rowspan=1,colspan=1)

        plt.subplots_adjust(wspace=0.5, hspace=0)
        
        #Grafico da curva de crescimento
        g1.set_title('1.0% Sucrose' ,fontsize=16)
        g1.set_ylabel('Growth ($\\mu$$m^3$ / $\\mu$$m^2$)', labelpad=5, fontsize=16)
        g1.tick_params(axis="y", labelleft='on', left='on', labelright='off', right='off', colors='k', width=1.5,length=3.5, labelsize=15)
        g1.tick_params(axis="x",colors='k', width=1.5,length=3.5, labelsize=15)
        g1.grid(True, color='k', linestyle='-', linewidth=0.4, alpha=0.2)

        g1_1=plt.subplot2grid((2,1),(1,0),rowspan=1,colspan=1)
        g1_1.set_xlabel('Time (min)', labelpad=5, fontsize=16)
        g1_1ylabel=g1_1.set_ylabel('Surface occupation (%-$\\mu$$m^2$)', labelpad=5, fontsize=16)   
        g1_1.yaxis.set_label_position("right")
        g1_1ylabel.set_color("r")
        g1_1.tick_params(axis="y", labelleft='off', left='off', labelright='on', right='on', colors='r', width=1.5, length=3.5, labelsize=15)
        g1_1.tick_params(axis="x", bottom='on', colors='k', width=1.5,length=3.5, labelsize=15)
        g1_1.grid(True, color='k', linestyle='-', linewidth=0.4, alpha=0.2)
        
        VoxelVal = ZStep * (XYField[0]/RawImageDefinition[0]) * (XYField[1]/RawImageDefinition[1])
        
        BACarealist=[]
        EPSarealist=[]
        
        BACyVolumeValsList=[]
        EPSyVolumeValsList=[]
        xTimeValsList=[]
        
        time=initialTimePoint
        for stackNumber in StackList:
            with open(diretorio + ImportRootFolderBAC + '/FullVolume_t' + str(stackNumber) + '.txt', 'r') as VolValBACa:
                VolValBAC = (int(VolValBACa.read()) * VoxelVal) / (XYField[0] * XYField[1])
           
            BACyVolumeValsList.append(VolValBAC)
            
            VolValBACa.close()
                        
            with open(diretorio + ImportRootFolderEPS + '/FullVolume_t' + str(stackNumber) + '.txt', 'r') as VolValEPSa:
                VolValEPS = (int(VolValEPSa.read()) * VoxelVal) / (XYField[0] * XYField[1])
           
            EPSyVolumeValsList.append(VolValEPS)
            
            VolValEPSa.close()
            
            ProjectImageBAC=io.imread(diretorio + '/Binarized/bac/ImageJ/t' + str(stackNumber) + '/ZProjection.png')
            ProjectImageBACN=np.where(ProjectImageBAC > 0, 1, 0)
            ProjectImageEPS=io.imread(diretorio + '/Binarized/EPS_THR2/ImageJ/t' + str(stackNumber) + '/ZProjection.png')
            ProjectImageEPSN=np.where(ProjectImageEPS > 0, 1, 0)
            
            BACarealist.append(100 * ProjectImageBACN.sum()/(RawImageDefinition[0]*RawImageDefinition[1]))
            EPSarealist.append(100 * ProjectImageEPSN.sum()/(RawImageDefinition[0]*RawImageDefinition[1]))
            
            xTimeValsList.append(time)            
            time += timeinterval            

            
        try:
            v0 = BACyVolumeValsList[0]
            #v0 = 0
            
            VOLBACbestVals, VOLBACCoVar = curve_fit(expFunc1, 
                                        np.array(xTimeValsList), 
                                        np.array(BACyVolumeValsList),
                                        bounds=(
                                        (0, 0),
                                        (100, 5)))
            
            VOLEPSbestVals, VOLEPSCoVar = curve_fit(expFunc1, 
                                        np.array(xTimeValsList), 
                                        np.array(EPSyVolumeValsList),
                                        bounds=(
                                        (0, 0),
                                        (100, 5)))
            
            VOLBACpar_a=VOLBACbestVals[0]
            VOLBACpar_b=VOLBACbestVals[1]
            #VOLBACpar_c=VOLBACbestVals[2]
            
            VOLEPSpar_a=VOLEPSbestVals[0]
            VOLEPSpar_b=VOLEPSbestVals[1]
            #VOLEPSpar_c=VOLEPSbestVals[2]
            
            
            AREABACbestVals, AREABACCoVar = curve_fit(expFunc1, 
                                        np.array(xTimeValsList), 
                                        np.array(BACarealist),
                                        bounds=(
                                        (0, 0),
                                        (100, 5)))
            
            AREAEPSbestVals, AREAEPSCoVar = curve_fit(linearFunc, 
                                        np.array(xTimeValsList), 
                                        np.array(EPSarealist),
                                        bounds=(
                                        (0, 0),
                                        (1, 5)))
            
            AREABACpar_a=AREABACbestVals[0]
            AREABACpar_b=AREABACbestVals[1]
            #AREABACpar_c=AREABACbestVals[2]
            
            AREAEPSpar_a=AREAEPSbestVals[0]
            AREAEPSpar_b=AREAEPSbestVals[1]
            #AREAEPSpar_c=AREAEPSbestVals[2]
            
            
            
            # Plotando grafico da volume
            g1.plot(xTimeValsList, [expFunc1(val, VOLBACpar_a, VOLBACpar_b,) for val in xTimeValsList], color='g', alpha=0.5, label='Bacteria V(t [min]) = a . $t^b$' + ' (a=' + str(VOLBACpar_a.round(10)) + ', b=' + str(VOLBACpar_b.round(2)) + ')')
            g1.scatter(xTimeValsList, BACyVolumeValsList, color='k', alpha=0.3)
            g1.plot(xTimeValsList, [expFunc1(val, VOLEPSpar_a, VOLEPSpar_b) for val in xTimeValsList], color='r', alpha=0.5, label='EPS V(t [min]) = a . $t^b$' + ' (a=' + str(VOLEPSpar_a.round(6)) + ', b=' + str(VOLEPSpar_b.round(4)) + ')')
            g1.scatter(xTimeValsList, EPSyVolumeValsList, color='k', alpha=0.3)
            
            g1.legend(bbox_to_anchor=(0.03, 0.98), loc=2, borderaxespad=0., fontsize=16)
            
            g1.spines["right"].set_visible(False)
            g1.spines["left"].set_visible(True)
            g1.spines["left"].set_color("k")
            g1.spines["left"].set_linewidth(1.5)
            g1.spines["left"].set_bounds(0, 5)
            g1.spines["top"].set_visible(False)
            g1.spines["bottom"].set_visible(True)
            g1.spines["bottom"].set_linewidth(1.5)
            g1.spines["bottom"].set_bounds(30,511)
            
            g1.set_xticks(list(np.arange(initialTimePoint, xTimeValsList[-1]+1, int(max(xTimeValsList)/9))))
            g1.set_xlim(0,520)
            g1.set_yticks(list(np.arange(0, 5, round(5/4, 1))))
            g1.set_ylim(-0.5,7)
            
            #Desenhar uma linha para separar os gráficos (não está sendo usada)
            #g1.axhline(y=360000,color="k",linewidth=1,alpha=0)


            # Plotando grafico da area
            g1_1.plot(xTimeValsList, [expFunc1(val, AREABACpar_a, AREABACpar_b) for val in xTimeValsList], color="b", alpha=0.5, label='Bacteria S(t [min]) = c+a.$t^b$' + ' (a=' + str(AREABACpar_a.round(5)) + ', b=' + str(AREABACpar_b.round(2)) + ')')
            g1_1.scatter(xTimeValsList, BACarealist, color="k", alpha=0.3)
            g1_1.plot(xTimeValsList, [linearFunc(val, AREAEPSpar_a, AREAEPSpar_b) for val in xTimeValsList], color="r", alpha=0.5, label='EPS S(t [min]) = a + b. t' + ' (a=' + str(AREAEPSpar_a.round(14)) + ', b=' + str(AREAEPSpar_b.round(4)) + ')')            
            g1_1.scatter(xTimeValsList, EPSarealist, color="k", alpha=0.3)
            
            g1_1.legend(bbox_to_anchor=(0.03, 0.98), loc=2, borderaxespad=0., fontsize=16)
            
            g1_1.spines["left"].set_visible(False)
            g1_1.spines["right"].set_visible(True)
            g1_1.spines["right"].set_color('r')
            g1_1.spines["right"].set_linewidth(1.5)
            g1_1.spines["right"].set_bounds(0,100)
            g1_1.spines["top"].set_visible(False)
            g1_1.spines["bottom"].set_visible(True)
            g1_1.spines["bottom"].set_linewidth(1.5)
            g1_1.spines["bottom"].set_bounds(20,511)
            
            g1_1.set_xticks(list(np.arange(initialTimePoint, xTimeValsList[-1]+1, int(max(xTimeValsList)/9))))
            g1_1.set_xlim(0,520)
            g1_1.set_yticks(list(np.arange(0,100+1,int(100/5))))
            g1_1.set_ylim(-8, 140)
            
            plt.tight_layout()
            fig1.savefig(diretorio + '/Imagens/VolumeCurveFull.png', dpi = 300)
            plt.show() 
            
        except RuntimeError:
            pass            
        
    
    if RegionAnalysis == True:        
        RegionList=list(range(FirstRegion,Lastregion+1))
    
        #Figura 1
        fig1=plt.figure(figsize=(11, 15), facecolor='w', edgecolor='k') 
        g1_1=plt.subplot2grid((12,10),(0,0),rowspan=3,colspan=4) # Histograma t0 and t420 min
        g1_1.set_title('Volume distribution for bacteria',fontsize=16)
        g1_1.set_xlabel('Volume value ($\\mu$$m^3$)', fontsize=16)
        g1_1.set_ylabel('Frequency', fontsize=16)
        g1_1.tick_params(width=2, length=3.5, labelsize=16)        
        
        g1_2=plt.subplot2grid((12,10),(0,4),rowspan=3,colspan=6) # Volume (microns^3) X Time
        g1_2.set_title('Colony growth curves',fontsize=16)
        g1_2.set_xlabel('Time (min)', fontsize=16)
        g1_2.set_ylabel('Volume ($\\mu$$m^3$)', fontsize=16)
        g1_2.tick_params(width=2, length=3.5, labelsize=16)        
        
        g1_3a=plt.subplot2grid((12,10),(3,0),rowspan=3,colspan=3) # Histograma do valor de a
        g1_3a.set_title('V(t) = $v_0$ + a . $t^b$',fontsize=16)
        g1_3a.set_xlabel('a value', fontsize=16)
        g1_3a.set_ylabel('Frequency', fontsize=16)
        g1_3a.tick_params(width=2, length=3.5, labelsize=16)
        
        g1_3b=plt.subplot2grid((12,10),(3,3),rowspan=3,colspan=3)# Histograma do valor de b
        g1_3b.set_title('V(t) = $v_0$ + a . $t^b$',fontsize=16)
        g1_3b.set_xlabel('b value', fontsize=16)
        g1_3b.set_ylabel('Frequency', fontsize=16)
        g1_3b.tick_params(width=2, length=3.5, labelsize=16)

        g1_4=plt.subplot2grid((12,10),(3,6),rowspan=3,colspan=4) # Histrograma do número de celula dos colonizadores
        g1_4.set_title('Colonizers cell number ($P_0$)',fontsize=16)
        g1_4.set_xlabel('Cell number', fontsize=16)
        g1_4.set_ylabel('Frequency', fontsize=16)  
        g1_4.tick_params(width=2, length=3.5, labelsize=16)
        
        g1_5=plt.subplot2grid((12,10),(6,0),rowspan=3,colspan=5) # Scatter grafico de Numero de celula inicial (p0) X Exp a
        g1_5.set_xlabel('$P_0$ (cell number)', fontsize=16)
        g1_5.set_ylabel('a value', fontsize=16)  
        g1_5.tick_params(width=2, length=3.5, labelsize=16)
        g1_5.set_ylim(-0.00005,0.0005)

        g1_6=plt.subplot2grid((12,10),(6,5),rowspan=3,colspan=5) # Scatter grafico de Numero de celula inicial (p0) X Exp b
        g1_6.set_xlabel('$P_0$ (cell number)', fontsize=16)
        g1_6.set_ylabel('b value', fontsize=16)  
        g1_6.tick_params(width=2, length=3.5, labelsize=16)
        
        g1_7=plt.subplot2grid((12,10),(9,0),rowspan=3,colspan=5) # Scatter grafico de Numero de celula inicial (p0) X Volume final
        g1_7.set_xlabel('$P_0$ (cell number)', fontsize=16)
        g1_7.set_ylabel('$V_{420}$ ($\\mu$$m^3$)', fontsize=16)  
        g1_7.tick_params(width=2, length=3.5, labelsize=16)
        g1_7.set_yscale('log')
        
        g1_8=plt.subplot2grid((12,10),(9,5),rowspan=3,colspan=5)
        g1_8.set_xlabel('$V_0$  ($\\mu$$m^3$)', fontsize=16)
        g1_8.set_ylabel('$V_{420}$  ($\\mu$$m^3$)', fontsize=16)
        g1_8.tick_params(width=2, length=3.5, labelsize=16)
        
        
        plt.tight_layout()

        
        #Figura 2
        fig2=plt.figure(figsize=(6, 6), facecolor='w', edgecolor='k')
        g2_1=plt.subplot2grid((2,1),(0,0),rowspan=1,colspan=1)
        g2_2=plt.subplot2grid((2,1),(1,0),rowspan=1,colspan=1)
        
        #Grafico do desvio padrão dos parametros fitados: valores de volume em microns
        g2_1.set_title('Fit Parameters STD (sigma) for a', fontsize=16)
        g2_1.set_xlabel('Colony number', fontsize=16)
        g2_1.set_ylabel('Value', fontsize=16)
        g2_1.set_ylim(-0.0001,0.0009)
        g2_1.tick_params(width=1.5,length=3.5, labelsize=13)

        #Grafico do desvio padrão dos parametros fitados: valores de volume normalizados por celula
        g2_2.set_title('Fit Parameters STD (sigma) for b', fontsize=16)
        g2_2.set_xlabel('Colony number', fontsize=16)
        g2_2.set_ylabel('Value', fontsize=16)
        g2_2.tick_params(width=1.5,length=3.5, labelsize=13)
    
        plt.tight_layout(pad=2)


        # PLot dos fittings feitos com threshold
        fig3=plt.figure(figsize=(13, 13), facecolor='w', edgecolor='k') 
        g3_1=plt.subplot2grid((3,3),(0,0),rowspan=1,colspan=1) # Volume (microns^3) X Time para threshold 1        
        g3_1.set_title('$P_0$ < ' + str(int(p0_THR_val1)) + ' bacteria',fontsize=16)
        g3_1.set_xlabel('Time (min)', fontsize=16)
        g3_1.set_ylabel('Volume ($\\mu$$m^3$)', fontsize=16)
        g3_1.tick_params(width=2, length=3.5, labelsize=16)
        #g1_8.set_ylim(0, 1800)

        g3_2=plt.subplot2grid((3,3),(1,0),rowspan=1,colspan=1) # Volume (microns^3) X Time para threshold 2        
        g3_2.set_title(str(int(p0_THR_val1)) + '< $P_0$ < ' + str(int(p0_THR_val2)) + ' bacteria',fontsize=16)
        g3_2.set_xlabel('Time (min)', fontsize=16)
        g3_2.set_ylabel('Volume ($\\mu$$m^3$)', fontsize=16) 
        g3_2.tick_params(width=2, length=3.5, labelsize=16)
        #g1_9.set_ylim(0, 1800)
        
        g3_3=plt.subplot2grid((3,3),(2,0),rowspan=1,colspan=1) # Volume (microns^3) X Time para threshold 3        
        g3_3.set_title('$P_0$ > ' + str(int(p0_THR_val2)) + ' bacteria',fontsize=16)
        g3_3.set_xlabel('Time (min)', fontsize=16)
        g3_3.set_ylabel('Volume ($\\mu$$m^3$)', fontsize=16) 
        g3_3.tick_params(width=2, length=3.5, labelsize=16)
        #g1_9.set_ylim(0, 1800)
        
        g3_4=plt.subplot2grid((3,3),(0,1),rowspan=1,colspan=1) # Histrograma dos valores de a para threshold 1 
        g3_4.set_title('V(t) = $v_0$ + a . $t^b$',fontsize=16)
        g3_4.set_ylabel('Frequency', fontsize=16)
        g3_4.set_xlabel('Value', fontsize=16)    
        g3_4.tick_params(width=2, length=3.5, labelsize=16)    
        
        g3_5=plt.subplot2grid((3,3),(1,1),rowspan=1,colspan=1) # Histrograma dos valores de a para threshold 2        
        g3_5.set_ylabel('Frequency', fontsize=16)
        g3_5.set_xlabel('Value', fontsize=16)
        g3_5.tick_params(width=2, length=3.5, labelsize=16)

        g3_6=plt.subplot2grid((3,3),(2,1),rowspan=1,colspan=1) # Histrograma dos valores de a para threshold 3
        g3_6.set_ylabel('Frequency', fontsize=16)
        g3_6.set_xlabel('Value', fontsize=16)
        g3_6.tick_params(width=2, length=3.5, labelsize=16)

        g3_7=plt.subplot2grid((3,3),(0,2),rowspan=1,colspan=1) # Histrograma dos valores de b para threshold 1 
        g3_7.set_title('V(t) = $v_0$ + a . $t^b$',fontsize=16)
        g3_7.set_ylabel('Frequency', fontsize=16)
        g3_7.set_xlabel('Value', fontsize=16)
        g3_7.tick_params(width=2, length=3.5, labelsize=16)
        
        g3_8=plt.subplot2grid((3,3),(1,2),rowspan=1,colspan=1) # Histrograma dos valores de b para threshold 2
        g3_8.set_ylabel('Frequency', fontsize=16)
        g3_8.set_xlabel('Value', fontsize=16)
        g3_8.tick_params(width=2, length=3.5, labelsize=16)

        g3_9=plt.subplot2grid((3,3),(2,2),rowspan=1,colspan=1) # Histrograma dos valores de b para threshold 2
        g3_9.set_ylabel('Frequency', fontsize=16)
        g3_9.set_xlabel('Value', fontsize=16)
        g3_9.tick_params(width=2, length=3.5, labelsize=16)

        plt.tight_layout()

        # Plot das curvas não fitadas
        fig4=plt.figure(figsize=(20, 4), facecolor='w', edgecolor='k') 
        g4_1=plt.subplot2grid((1,3),(0,0),rowspan=1,colspan=1)
        g4_1.set_xlabel('Time (min)', fontsize=16)
        g4_1.set_ylabel('Volume ($\\mu$$m^3$)', fontsize=16)
        g4_1.tick_params(width=2, length=3.5, labelsize=16)
        
        g4_2=plt.subplot2grid((1,3),(0,1),rowspan=1,colspan=1)
        
        g4_3=plt.subplot2grid((1,3),(0,2),rowspan=1,colspan=1)
        g3_3.set_title('Non-fitted elements',fontsize=16)
        g4_3.set_ylabel('Frequency', fontsize=16)
        g4_3.set_xlabel('$P_{420}$', fontsize=16)
        g4_3.tick_params(width=2, length=3.5, labelsize=16)

        plt.tight_layout()


        BACExpAList_1=[]
        BACExpBList_1=[]
        BACExpAList_N=[]
        BACExpBList_N=[]
        BACVolList_p0=[]
         
        BACCoVarAList_1=[]
        BACCoVarBList_1=[]
        BACCoVarAList_N=[]
        BACCoVarBList_N=[]        
    
        BACExpAList_p0_1=[]
        BACExpAList_p0_2=[]
        BACExpAList_p0_3=[]        
        BACExpBList_p0_1=[]
        BACExpBList_p0_2=[]
        BACExpBList_p0_3=[]
    
        BACMinVolList=[]
        BACMinVolList_fitted_p0=[]
        BACMaxVolList=[]
        NoFitBacMinMax = []
        
        VoxelVal = ZStep * (XYField[0]/RawImageDefinition[0]) * (XYField[1]/RawImageDefinition[1])
        
        BACRegionPlotList_1=[]
        BACRegionPlotList_N=[]

        fittedPerc_1 = 0
        fittedPerc_N = 0
        
        NonFittedlist=[]
        
        for regionN in RegionList:
            xTimeValsList=[]
            
            BACyVolumeValsList_1=[]
            BACyVolumeValsList_N=[]
            EPSyVolumeValsList=[]
            
            time=initialTimePoint
            
            for stackNumber in StackList:
                
                # Valores de volume de BAC
                with open(diretorio + ImportRootFolderBAC + '/Region' + str(regionN) + '/Volume_t' + str(stackNumber) + '.txt', 'r') as VolValBACa:
                    VolValBACb = int(VolValBACa.read())
                    
                BACyVolumeValsList_1.append(VolValBACb * VoxelVal)               
                BACyVolumeValsList_N.append(VolValBACb * VoxelVal)
                
                VolValBACa.close()

                # Valores de volume de EPS
                with open(diretorio + ImportRootFolderEPS + '/Region' + str(regionN) + '/Volume_t' + str(stackNumber) + '.txt', 'r') as VolValEPSa:
                    VolValEPS=int(VolValEPSa.read()) * VoxelVal
               
                EPSyVolumeValsList.append(VolValEPS)
                
                VolValEPSa.close()
                
                
                xTimeValsList.append(time)            
                time += timeinterval

            
            BACMinVolList.append(BACyVolumeValsList_1[0])
            
            if int(BACyVolumeValsList_1[0] / ((4/3)* np.pi * (SmutansRadius ** 3))) != 0:
                BACVolList_p0.append(int(BACyVolumeValsList_1[0] / ((4/3)* np.pi * (SmutansRadius ** 3))))
            else:
                BACVolList_p0.append(1)
            
            BACMaxVolList.append(BACyVolumeValsList_1[-1])

            BACyVolumeValsArray_1=np.array(BACyVolumeValsList_1)            
            BACyVolumeValsArray_N=np.array(BACyVolumeValsList_N)
            
            xTimeValsArray=np.array(xTimeValsList)
            
            
            # Fitting dos valores de volume RAW (so fitara elementos que quintuplicaram de tamanho)         
            if BACyVolumeValsList_1[-1] >= (BACyVolumeValsList_1[0] + (BACyVolumeValsList_1[0] * 5)):
            
                try:
                    v0 = BACyVolumeValsList_1[0]
                    
                    BACbestVals_1, BACCoVar_1 = curve_fit(expFunc1, 
                                                xTimeValsArray, 
                                                BACyVolumeValsArray_1,
                                                bounds=(
                                                (0, 0),
                                                (1, 5)))
                
                    if BACCoVar_1[1, 1]**(1/2) <= Max_b_FitError and BACCoVar_1[0, 0]**(1/2) <= Max_a_FitError:
                        
                        fittedPerc_1 += 1
                        
                        BACpar_a_1=BACbestVals_1[0]
                        BACpar_b_1=BACbestVals_1[1]
                        
                        BACExpAList_1.append(BACpar_a_1)
                        BACExpBList_1.append(BACpar_b_1)
                        
                        BACpar_CoVarA_1=BACCoVar_1[0, 0]**(1/2)
                        BACpar_CoVarB_1=BACCoVar_1[1, 1]**(1/2)
                        
                        BACCoVarAList_1.append(BACpar_CoVarA_1)
                        BACCoVarBList_1.append(BACpar_CoVarB_1)
                        
                        BACRegionPlotList_1.append(regionN)
                        
                        
                        if int(BACyVolumeValsList_1[0] / ((4/3)* np.pi * (SmutansRadius ** 3))) != 0:
                            BACMinVolList_fitted_p0.append(int(BACyVolumeValsList_1[0] / ((4/3)* np.pi * (SmutansRadius ** 3))))
                        else:
                            BACMinVolList_fitted_p0.append(1)
                                    
                        
                        #Grafico da curva de crescimento bacteriano     
                        g1_2.scatter(xTimeValsList, BACyVolumeValsList_1, color='0.75', alpha=0.5)
                        g1_2.plot(xTimeValsList, [expFunc1(val, BACpar_a_1, BACpar_b_1) for val in xTimeValsList], color='r', alpha=0.2)
                        
                    else:
                        NonFittedlist.append(BACyVolumeValsList_1[-1])
                        
                        g4_1.scatter(xTimeValsList, BACyVolumeValsList_1, color='b', alpha=0.5)
                        g1_8.scatter(BACyVolumeValsList_1[0], BACyVolumeValsList_1[-1], color='k', alpha=0.5)                    
                        NoFitBacMinMax.append([BACyVolumeValsList_1[0],BACyVolumeValsList_1[-1]])
                        pass
                        
                except RuntimeError:
                    NonFittedlist.append(BACyVolumeValsList_1[-1])
                    
                    g4_1.scatter(xTimeValsList, BACyVolumeValsList_1, color='b', alpha=0.5)
                    g1_8.scatter(BACyVolumeValsList_1[0], BACyVolumeValsList_1[-1], color='k', alpha=0.5)                 
                    NoFitBacMinMax.append([BACyVolumeValsList_1[0],BACyVolumeValsList_1[-1]])
                    pass
            else:
                NonFittedlist.append(BACyVolumeValsList_1[-1])
                
                g4_1.scatter(xTimeValsList, BACyVolumeValsList_1, color='b', alpha=0.5)
                g1_8.scatter(BACyVolumeValsList_1[0], BACyVolumeValsList_1[-1], color='k', alpha=0.5) 
                NoFitBacMinMax.append([BACyVolumeValsList_1[0],BACyVolumeValsList_1[-1]])
                pass                 
            
            
            # Fitting dos valores de volume normalizados
            try:
                v0 = BACyVolumeValsList_N[0]
                
                BACbestVals_N, BACCoVar_N = curve_fit(expFunc1, 
                                            xTimeValsArray, 
                                            BACyVolumeValsArray_N,
                                            bounds=(
                                            (0, 0),
                                            (1, 5)))
            
                if BACCoVar_N[1, 1]**(1/2) <= Max_b_FitError and BACCoVar_N[0, 0]**(1/2) <= Max_a_FitError:
                    
                    fittedPerc_N += 1
                    
                    BACpar_a_N=BACbestVals_N[0]
                    BACpar_b_N=BACbestVals_N[1]
                    
                    BACExpAList_N.append(BACpar_a_N)
                    BACExpBList_N.append(BACpar_b_N)
                    
                    BACpar_CoVarA_N=BACCoVar_N[0, 0]**(1/2)
                    BACpar_CoVarB_N=BACCoVar_N[1, 1]**(1/2)
                    
                    BACCoVarAList_N.append(BACpar_CoVarA_N)
                    BACCoVarBList_N.append(BACpar_CoVarB_N)
                    
                    BACRegionPlotList_N.append(regionN)
                        
                    if int(BACyVolumeValsList_N[0] / ((4/3)* np.pi * (SmutansRadius ** 3))) < p0_THR_val1:
                        BACExpAList_p0_1.append(BACpar_a_N)
                        BACExpBList_p0_1.append(BACpar_b_N)
                        
                        g3_1.scatter(xTimeValsList, BACyVolumeValsList_N, color='0.75', alpha=0.5)
                        g3_1.plot(xTimeValsList, [expFunc1(val, BACpar_a_N, BACpar_b_N) for val in xTimeValsList], color='c', alpha=0.3)
                                    
                    elif p0_THR_val1 < int(BACyVolumeValsList_N[0] / ((4/3)* np.pi * (SmutansRadius ** 3))) < p0_THR_val2 :
                        BACExpAList_p0_2.append(BACpar_a_N)
                        BACExpBList_p0_2.append(BACpar_b_N)
                        
                        g3_2.scatter(xTimeValsList, BACyVolumeValsList_N, color='0.75', alpha=0.5)
                        g3_2.plot(xTimeValsList, [expFunc1(val, BACpar_a_N, BACpar_b_N) for val in xTimeValsList], color='c', alpha=0.3)

                    elif int(BACyVolumeValsList_N[0] / ((4/3)* np.pi * (SmutansRadius ** 3))) > p0_THR_val2 :
                        BACExpAList_p0_3.append(BACpar_a_N)
                        BACExpBList_p0_3.append(BACpar_b_N)
                        
                        g3_3.scatter(xTimeValsList, BACyVolumeValsList_N, color='0.75', alpha=0.5)
                        g3_3.plot(xTimeValsList, [expFunc1(val, BACpar_a_N, BACpar_b_N) for val in xTimeValsList], color='c', alpha=0.3)
                    
                else:
                    pass
                    
            except RuntimeError:
                pass
            
       
        # Histograma t0 and t420 min
        g1_1.hist(BACMaxVolList, log=True, range=(0,500), color='salmon', alpha=0.3, label='t=420 min')
        g1_1.hist(BACMinVolList, log=True, range=(0,500), color='k', alpha=0.3, label='$t_0$')
        g1_1.legend(bbox_to_anchor=(0.3, 0.6, 1., .102), loc=3, borderaxespad=0., fontsize=16)
        
        # Histograma de valores de b
        g1_3a.hist(BACExpAList_1, bins=6, log=True, range=(0, 0.003), color='b', alpha=0.3, label='a')
        g1_3b.hist(BACExpBList_1, bins=7, log=True, range=(0, 5), color='g', alpha=0.3, label='b')        

        # Histograma de valores de p0 (populacao inicial de bacteria)
        g1_4.hist(BACVolList_p0, bins=7, log=True, color='k', alpha=0.3) 
    
        #Plot de Numero de celula inicial X Exp a
        g1_5.scatter(BACMinVolList_fitted_p0, BACExpAList_1, color='b', alpha=0.3)
        g1_5.axhline(y=np.percentile(np.array(BACExpAList_1), 25), color='k',linewidth=2, linestyle='-', alpha=0.4)
        g1_5.axhline(y=np.percentile(np.array(BACExpAList_1), 50), color="r",linewidth=2, linestyle='-', alpha=0.4)
        g1_5.axhline(y=np.percentile(np.array(BACExpAList_1), 75), color='k',linewidth=2, linestyle='-', alpha=0.4)
        
        print('\n\n A mediana da constante a eh ', np.median(np.array(BACExpAList_1)))
        
        #Plot de Numero de celula inicial X Exp b        
        g1_6.scatter(BACMinVolList_fitted_p0, BACExpBList_1, color='g', alpha=0.3)
        g1_6.axhline(y=np.percentile(np.array(BACExpBList_1), 25), color='k',linewidth=2, linestyle='-', alpha=0.4)
        g1_6.axhline(y=np.percentile(np.array(BACExpBList_1), 50), color="r",linewidth=2, linestyle='-', alpha=0.4)
        g1_6.axhline(y=np.percentile(np.array(BACExpBList_1), 75), color='k',linewidth=2, linestyle='-', alpha=0.4)
        print('\n\n A mediana da constante b eh ', np.median(np.array(BACExpBList_1)))

        #Plot de Numero de celula inicial X Volume final
        g1_7.scatter(BACVolList_p0, BACMaxVolList, color='m', alpha=0.3)


        if Det_TopoXVol_relation == True:

            # Grafico             
            g4_2.set_title('Roughness influence', fontsize=16)
            g4_2.set_xlabel('Sa ($\\mu$m)', fontsize=16)
            g4_2.set_ylabel('Volume ($\\mu$$m^3$)', fontsize=16)
            g4_2.tick_params(width=1.5,length=3.5, labelsize=13)
        
            fileSalist_BACt=open(diretorio+'/SUFAdjusted' + '/WithBAC_SaList_t' + str(StackToFindRelation) + '.txt', 'r')
            DataSalist_BACt=np.array(MODImpExp.ConvertStrTOData(fileSalist_BACt, ','))
            fileSalist_BACt.close()
            
            g4_2.scatter(DataSalist_BACt[:,2], DataSalist_BACt[:,3], color='k', alpha=0.5,)


        #Grafico do desvio padrão dos parametros fitados
        g2_1.scatter(BACRegionPlotList_1, BACCoVarAList_1 , color='b', alpha=0.5, label='$\\sigma$ a')
        g2_2.scatter(BACRegionPlotList_1, BACCoVarBList_1 , color='r', alpha=0.5, label='$\\sigma$ b')
        
        # Histrograma dos valores de a para threshold 1 
        g3_4.hist(BACExpAList_p0_1, bins=10, log=True, range=(0, 12), color='b', alpha=0.5, label='a')
        g3_4.legend(bbox_to_anchor=(0.7, 0.55, 1., .102), loc=3, borderaxespad=0., fontsize=16)

        # Histrograma dos valores de a para threshold 2 
        g3_5.hist(BACExpAList_p0_2, bins=10, log=True, range=(0, 12), color='b', alpha=0.5, label='a')
        g3_5.legend(bbox_to_anchor=(0.7, 0.55, 1., .102), loc=3, borderaxespad=0., fontsize=16)

        # Histrograma dos valores de a para threshold 3 
        g3_6.hist(BACExpAList_p0_3, bins=10, log=True, range=(0, 12), color='b', alpha=0.5, label='a')
        g3_6.legend(bbox_to_anchor=(0.7, 0.55, 1., .102), loc=3, borderaxespad=0., fontsize=16)

        # Histrograma dos valores de b para threshold 1 
        g3_7.hist(BACExpBList_p0_1, bins=10, log=True, range=(1,5), color='g', alpha=0.5, label='b')
        g3_7.legend(bbox_to_anchor=(0.7, 0.55, 1., .102), loc=3, borderaxespad=0., fontsize=16)

        # Histrograma dos valores de b para threshold 2 
        g3_8.hist(BACExpBList_p0_2, bins=10, log=True, range=(1,5), color='g', alpha=0.5, label='b')
        g3_8.legend(bbox_to_anchor=(0.7, 0.55, 1., .102), loc=3, borderaxespad=0., fontsize=16)
        
        # Histrograma dos valores de b para threshold 3
        g3_9.hist(BACExpBList_p0_3, bins=10, log=True, range=(1,5), color='g', alpha=0.5, label='b')
        g3_9.legend(bbox_to_anchor=(0.7, 0.55, 1., .102), loc=3, borderaxespad=0.)        
         
        
        # Histograma para os valores de volume de curvas nao fitadas
        g4_3.hist([(val / ((4/3)* np.pi * (SmutansRadius ** 3))) for val in NonFittedlist], bins=20, range=(0,100), color='m', alpha=0.5, label='b')
        
        #salvando
        fig1.savefig(diretorio + '/Imagens/Fitting1.png', dpi = 300)
        fig2.savefig(diretorio + '/Imagens/Fitting2.png', dpi = 300)
        fig3.savefig(diretorio + '/Imagens/Fitting3.png', dpi = 300)
        fig4.savefig(diretorio + '/Imagens/Fitting4.png', dpi = 300)
        
        plt.show()
        
        print('\n\n\n Foram fitados ', fittedPerc_1,' dos ', len(RegionList),'presentes.\n')
        print('(', fittedPerc_1/len(RegionList) * 100,'%)')
        
        print('\n\n O valor medio de a eh:\n', np.mean(np.array(BACExpAList_1)), ' (', np.std(np.array(BACExpAList_1)), ')')
        print('\n\n O valor medio de b eh:\n', np.mean(np.array(BACExpBList_1)), ' (', np.std(np.array(BACExpBList_1)), ')')
        
        print('\n\n\n Foram fitados ', fittedPerc_N,' dos ', len(RegionList),'presentes (p0 em offset).\n')
        print('(', fittedPerc_N/len(RegionList) * 100,'%)')

        
        List_singlecells = []
        List_cluster = []
        List_aggregates = []
        List_microcolonies = []
        
        for Number in list(range(len(BACVolList_p0))):
            if BACVolList_p0[Number] <= 5:
                List_singlecells.append(1)
            if 5 < BACVolList_p0[Number] <= 50:
                List_cluster.append(1)
            if 50 < BACVolList_p0[Number] <= 300:
                List_aggregates.append(1)
            if BACVolList_p0[Number] > 300:
                List_microcolonies.append(1)
                
        print('\n\n Distribuição dos volumes do colonizadores\n')
        print('\n\n Single Cells, ', len(List_singlecells), ' unidades', '(', len(List_singlecells)/len(BACVolList_p0) * 100, '%) \n')
        print('\n\n Cluster, ', len(List_cluster), ' unidades', '(', len(List_cluster)/len(BACVolList_p0) * 100, '%) \n')
        print('\n\n Aggregates, ', len(List_aggregates), ' unidades', '(', len(List_aggregates)/len(BACVolList_p0) * 100, '%) \n')
        print('\n\n Microcolonies, ', len(List_microcolonies), ' unidades', '(', len(List_microcolonies)/len(BACVolList_p0) * 100, '%) \n')
        
        print('\n\n Total de colonizadores =', len(BACVolList_p0))
        
        #Export txt P0_X_ExpB
        file1=open('/media/Storage/Image_proc/P0_X_ExpB_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACMinVolList_fitted_p0))):
            file1.write('[' + str(BACMinVolList_fitted_p0[Number]) + ', ' + str(BACExpBList_1[Number]) + ']' + '\n')
        file1.close()

        #Export txt P0_X_ExpA
        file2=open('/media/Storage/Image_proc/P0_X_ExpA_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACMinVolList_fitted_p0))):
            file2.write('[' + str(BACMinVolList_fitted_p0[Number]) + ', ' + str(BACExpAList_1[Number]) + ']' + '\n')
        file2.close()
        
        #Export txt ExpA histogram        
        file3=open('/media/Storage/Image_proc/ExpA_Values_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACExpAList_1))):
            file3.write(str(BACExpAList_1[Number]) + '\n')
        file3.close()
        
        #Export txt ExpB histogram        
        file4=open('/media/Storage/Image_proc/ExpB_Values_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACExpBList_1))):
            file4.write(str(BACExpBList_1[Number]) + '\n')
        file4.close()
        
        #Export txt P0_X_Volume Final (420 min)
        file5=open('/media/Storage/Image_proc/P0_X_BacFinalVol_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACVolList_p0))):
            file5.write('[' + str(BACVolList_p0[Number]) + ', ' + str(BACMaxVolList[Number]) + ']' + '\n')
        file5.close()
        
        #Export txt Volume Inicial_X_Volume Final (420 min) para os dados não fitados
        file6=open('/media/Storage/Image_proc/NoFIT_V0_X_BacFinalVol_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(NoFitBacMinMax))):
            file6.write(str(NoFitBacMinMax[Number]) + '\n')
        file6.close()
        
        #Export txt Volume Inicial_X_Volume Final (420 min) para os dados não fitados
        file7=open('/media/Storage/Image_proc/p0_Values_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACVolList_p0))):
            file7.write(str(BACVolList_p0[Number]) + '\n')
        file7.close()        

        file8=open('/media/Storage/Image_proc/BACMinVol_X_MaxVol_' + str(ExperimentNumber) + '.txt', 'w')
        for Number in list(range(len(BACMinVolList))):
            file8.write('[' + str(BACMinVolList[Number]) + ', ' + str(BACMaxVolList[Number]) + ']' + '\n')
        file8.close()
