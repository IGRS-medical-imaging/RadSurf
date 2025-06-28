import os
import time
import ScreenCapture

# Define parameters
viewNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLViewNode")
outputDir = "D:/DRR_batch3/"

file_name_prefix = "verse557"  # Change this as needed

# Rotation settings
rotationInterval = 30  # Degrees per step
totalRotation = 360
yawSteps = (totalRotation // rotationInterval)  # 12 steps (0° → 330°)
pitchSteps = (totalRotation // rotationInterval)  # 12 steps

# Define rotation sequences
rotationSequence = [
    ("Yaw", yawSteps + 1),  # Rotate Yaw (0° → 330° → 360° → back to 0° naturally)
    ("Pitch", pitchSteps)   # Rotate Pitch (0° → 330°)
]


# Define the capture function
def capture3dViewRotation(viewNode, outputDir):
    """
    Capture screenshots of the 3D view while rotating:
    1. Yaw forward (0° to 360°, ensuring it returns to 0°)
    2. Pitch forward (0° to 330°)
    """

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Get the view renderer
    layoutManager = slicer.app.layoutManager()
    renderView = None
    for threeDViewIndex in range(layoutManager.threeDViewCount):
        threeDWidget = layoutManager.threeDWidget(threeDViewIndex)
        if threeDWidget.mrmlViewNode() == viewNode:
            renderView = threeDWidget.threeDView()
            break
    if not renderView:
        raise ValueError("View node not found")

    # Capture images for each rotation type
    for rotationAxis, numSteps in rotationSequence:
        renderView.setPitchRollYawIncrement(0)  # Reset rotation increment

        if rotationAxis == "Yaw":
            renderView.yawDirection = renderView.YawRight
        elif rotationAxis == "Pitch":
            renderView.pitchDirection = renderView.PitchUp

        for i in range(numSteps):
            # Rotate the view
            if rotationAxis == "Yaw":
                renderView.yaw()
            elif rotationAxis == "Pitch":
                renderView.pitch()

            renderView.forceRender()

            # Calculate current rotation angle
            angle_rotated = (i * rotationInterval) % 360  # Ensure it loops back to 0°

            # Construct filename
            screenshotFilename = os.path.join(
                outputDir, f"L3_{file_name_prefix}_{rotationAxis.lower()}_{angle_rotated:03d}.png"
            )

            # Capture and save the image
            ScreenCapture.ScreenCaptureLogic().captureImageFromView(renderView, screenshotFilename)

            # Set the rotation increment for the next step
            renderView.setPitchRollYawIncrement(-rotationInterval)

            print(f"Saved: {screenshotFilename}")

    print("Rotation capture complete!")


# Run the function
start_time = time.time()
capture3dViewRotation(viewNode, outputDir)
end_time = time.time()
print(f"Execution Time: {end_time - start_time:.2f} seconds")