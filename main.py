import sys
import os
diretorio = os.getcwd()
sys.path.append(diretorio + '/Modules')

from CropVol import CropVol
from DetAtMap import DetAtMap
from FilterElements import FilterElements
from CropSUF import CropSUF
from CropSUF_w import CropSUF_w
from Settings import Settings
from ZoneAnalysis_REGION import ZoneAnalysis_REGION
from ZoneAnalysis_FULL import ZoneAnalysis_FULL
from VolumeAnalysisPLOT import VolumeAnalysisPLOT
from TopographyAnalysis import TopographyAnalysis
from PlotTOPO import PlotTOPO
from ATDETAnalysis import ATDETAnalysis
from ShapeAnalysis import ShapeAnalysis
from ShapeAnalysisPLOT import ShapeAnalysisPLOT

settingsDic = Settings()
#CropVol(settingsDic)
#DetAtMap(settingsDic)
#FilterElements(settingsDic)
#ZoneAnalysis_REGION(settingsDic)
#ZoneAnalysis_FULL(settingsDic)
#VolumeAnalysisPLOT(settingsDic)
#ATDETAnalysis(settingsDic)
ShapeAnalysis(settingsDic)
#ShapeAnalysisPLOT(settingsDic)

#if settingsDic['TopoMODE_input'].lower() == 'yes':
    #CropSUF(settingsDic)
    #CropSUF_w(settingsDic)
    #TopographyAnalysis(settingsDic)
    #PlotTOPO()
