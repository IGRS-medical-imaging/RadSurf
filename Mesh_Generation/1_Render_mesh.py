import slicer
import vtk
import os
import re
import time

# Start the timer
start_time = time.time()

# Root directory containing folders with CT and segmentation files
root_dir = "D:/02_training"  # Replace with your root directory
output_directory = "D:/mesh_test/"  # Replace with your desired output directory

file_format = "STL"
lps = True
size_scale = 1.0
merge = False

for i in range(24,25):
    target_segment_label = f"Segment_{i}"

    # Function to find the CT and segmentation files in each folder
    def find_nii_files(folder_path):
        ct_file = None
        seg_file = None

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".nii.gz"):
                if re.search(r'seg', file_name, re.IGNORECASE):  # Looking for "CT" in the filename
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

            segment_ids = vtk.vtkStringArray()
            segment_ids.InsertNextValue(segment_id)

            # Define the file name for the STL
            file_name_prefix = f'{os.path.basename(seg_file).split("_")[0]}_{target_segment_label}'
            export_dir = os.path.join(output_directory, file_name_prefix)

            # Make sure the output directory exists
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            # Export the segment to STL file
            success = slicer.modules.segmentations.logic().ExportSegmentsClosedSurfaceRepresentationToFiles(
                export_dir,
                segmentation_node,
                segment_ids,
                file_format,
                lps,
                size_scale,
                merge
            )

            if not success:
                print(f"Failed to export {file_name_prefix}")

            # Remove the volume and segmentation nodes from the scene after processing
            slicer.mrmlScene.RemoveNode(volume_node)
            slicer.mrmlScene.RemoveNode(segmentation_node)

end_time = time.time()
# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Script executed in {elapsed_time:.2f} seconds.")
print("Batch processing and STL export complete.")


