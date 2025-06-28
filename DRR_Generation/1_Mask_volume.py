import slicer
import vtk
import os
import re
import numpy as np
import time

# Start the timer
start_time = time.time()

# Root directory containing folders with CT and segmentation files
root_dir = "D:/03_training_VERSE2020/"  # Replace with your root directory
output_directory = "D:/02_training_VERSE2020/test_mask"  # Replace with your desired output directory

# Target segment label (L4 vertebra)
for i in range(20,25):
    target_segment_label = f"Segment_{i}"


    # Function to find the CT and segmentation files in each folder
    def find_nii_files(folder_path):
        ct_file = None
        seg_file = None

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".nii.gz"):
                if re.search(r'seg', file_name, re.IGNORECASE):  # Looking for "seg" in the filename
                    seg_file = os.path.join(folder_path, file_name)
                else: 
                    ct_file = os.path.join(folder_path, file_name)

        return ct_file, seg_file

    # Process each folder
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        
        if os.path.isdir(folder_path):
            ct_file, seg_file = find_nii_files(folder_path)
            
            if not ct_file or not seg_file:
                print(f"Skipping folder {folder_name}, missing CT or segmentation file.")
                continue

            print(f"Processing CT file: {ct_file}, Segmentation file: {seg_file}")
            
            # Load the volume (CT)
            volume_node = slicer.util.loadVolume(ct_file)
            
            # Load the segmentation
            segmentation_node = slicer.util.loadSegmentation(seg_file)

            # Get the Subject Hierarchy node
            sh_node = slicer.mrmlScene.GetSubjectHierarchyNode()
            segmentation_item_id = sh_node.GetItemByDataNode(segmentation_node)
            segmentation_data_node = sh_node.GetItemDataNode(segmentation_item_id)

            # Check if the segmentation contains "Segment_23" (L4 vertebra)
            segment_id = segmentation_data_node.GetSegmentation().GetSegmentIdBySegmentName(target_segment_label)
            
            if not segment_id:
                print(f"Skipping folder {folder_name}, as it does not contain {target_segment_label}.")
                slicer.mrmlScene.RemoveNode(volume_node)
                slicer.mrmlScene.RemoveNode(segmentation_node)
                continue

            # Create a labelmap volume node for the specified segment
            # Create a labelmap volume node for the specified segment
            labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")
            slicer.modules.segmentations.logic().ExportSegmentsToLabelmapNode(segmentation_node, [segment_id], labelmapVolumeNode, volume_node)


            # Masking
            voxels = slicer.util.arrayFromVolume(volume_node)
            mask = slicer.util.arrayFromVolume(labelmapVolumeNode)
            maskedVoxels = np.copy(voxels)  # we don't want to modify the original volume
            maskedVoxels[mask == 0] = 0

            # Write masked volume to a new volume node
            maskedVolumeNode = slicer.modules.volumes.logic().CloneVolume(volume_node, "Masked")
            slicer.util.updateVolumeFromArray(maskedVolumeNode, maskedVoxels)

            # Save the masked volume
            file_name_prefix = f'{os.path.basename(seg_file).split("_")[0]}_{target_segment_label}.nii'
            output_file_path = os.path.join(output_directory, file_name_prefix)
            slicer.util.saveNode(maskedVolumeNode, output_file_path)
            print(f"Saved masked volume to {output_file_path}")

            # Remove the volume and segmentation nodes from the scene after processing
            slicer.mrmlScene.RemoveNode(volume_node)
            slicer.mrmlScene.RemoveNode(segmentation_node)
            slicer.mrmlScene.RemoveNode(labelmapVolumeNode)
            slicer.mrmlScene.RemoveNode(maskedVolumeNode)

end_time = time.time()
# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Script executed in {elapsed_time:.2f} seconds.")
print("Batch processing complete.")

'''
import os
start_angle = 0
end_angle = 360
increment = 90

output_directory = "D:/SIT/tmp/Verse04"

# Get the volume node (the actual CT volume used for rendering)
volume_node = slicer.util.getNode('Masked Volume')  # Replace with your actual volume node name

for angle in range(start_angle, end_angle, increment):
    # Create a new transform node for each rotation
    transform_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode')

    # Apply the transform to the volume node (not the volume rendering node)
    volume_node.SetAndObserveTransformNodeID(transform_node.GetID())

    # Create the rotation matrix
    transform_matrix = vtk.vtkTransform()
    transform_matrix.RotateZ(angle)

    # Apply the transformation to the transform node
    transform_node.SetMatrixTransformToParent(transform_matrix.GetMatrix())

    # Define the file name for the DRR image
    file_name_prefix = f'DRR_Rotated_{angle}_deg'
    export_dir = os.path.join(output_directory, file_name_prefix)

    # Make sure the output directory exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # Render the DRR
    slicer.app.processEvents()  # Ensure all events are processed before capturing

    # Capture a screenshot of the 3D view (to save the DRR)
    threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()  # Get the 3D view
    screenshot_path = os.path.join(export_dir, f'DRR_{angle}_deg.png')
    
    # Capture the screenshot of the 3D view and save it
    slicer.util.captureImageFromView(threeDView, screenshot_path)

    # Harden the transform for the volume node if needed
    slicer.vtkSlicerTransformLogic().hardenTransform(volume_node)

    print(f"Saved DRR screenshot at {angle} degrees to {screenshot_path}")
'''


