import slicer
import os
import ScreenCapture
#import time

#start_time = time.time()
volumeNode = slicer.util.loadVolume(r"D:\02_training_VERSE2020\verse005_Segment_24.nii")
#Render Volume
logic = slicer.modules.volumerendering.logic()
volumeNode = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')
displayNode = logic.CreateVolumeRenderingDisplayNode()
displayNode.UnRegister(logic)
slicer.mrmlScene.AddNode(displayNode)
volumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
logic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)

volRenWidget = slicer.modules.volumerendering.widgetRepresentation()
volumePropertyNode = displayNode.GetVolumePropertyNode()
volumePropertyNodeWidget = slicer.util.findChild(volRenWidget, 'VolumePropertyNodeWidget')
volumePropertyNodeWidget.setMRMLVolumePropertyNode(volumePropertyNode)
preset = logic.GetPresetByName('CT-X-ray')
volumePropertyNode.Copy(preset)
# Adjust the transfer function
volumePropertyNodeWidget.moveAllPoints(205, 0, False)

# #centre view in 3D
layoutManager = slicer.app.layoutManager()
threeDView = layoutManager.threeDWidget(0).threeDView()
threeDView.resetFocalPoint()

#end_time = time.time()
# Calculate and print the elapsed time
##print(f"Script executed in {elapsed_time:.2f} seconds.")

