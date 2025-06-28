# import os
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim
# import shutil
# from skimage.io import imread
# from PIL import Image
# from tqdm import tqdm
# from torch.cuda.amp import GradScaler, autocast
# from torch.utils.checkpoint import checkpoint

# # Configuration
# torch.backends.cudnn.benchmark = True
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# class ResNetBlock(nn.Module):
#     def __init__(self, in_channels, out_channels, stride=1):
#         super().__init__()
#         self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
#         self.bn1 = nn.BatchNorm2d(out_channels)
#         self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
#         self.bn2 = nn.BatchNorm2d(out_channels)
#         self.relu = nn.ReLU(inplace=True)
#         self.downsample = nn.Sequential(
#             nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
#             nn.BatchNorm2d(out_channels),
#         ) if stride != 1 or in_channels != out_channels else None

#     def forward(self, x):
#         return checkpoint(self._forward_impl, x, use_reentrant=False)
    
#     def _forward_impl(self, x):
#         identity = x
#         out = self.conv1(x)
#         out = self.bn1(out)
#         out = self.relu(out)
#         out = self.conv2(out)
#         out = self.bn2(out)
#         if self.downsample is not None:
#             identity = self.downsample(x)
#         out += identity
#         return self.relu(out)

# class EfficientDIP(nn.Module):
#     def __init__(self, num_channels=64):
#         super().__init__()
#         self.upsample = nn.Upsample(size=(224, 224), mode='bilinear', align_corners=True)
#         self.conv_in = nn.Conv2d(1, num_channels, 3, padding=1)
#         self.res_blocks = nn.Sequential(*[ResNetBlock(num_channels, num_channels) for _ in range(12)])
#         self.conv_out = nn.Conv2d(num_channels, 1, 3, padding=1)

#     def forward(self, x):
#         x = self.upsample(x)
#         x = self.conv_in(x)
#         x = self.res_blocks(x)
#         return self.conv_out(x)

# def process_image(image_path):
#     # Load and preprocess
#     img = imread(image_path).astype(np.float32)
#     img = np.mean(img, axis=-1) if img.ndim == 3 else img
    
#     # Create tensors
#     LR_tensor = torch.tensor(img, device=device).unsqueeze(0).unsqueeze(0)
#     upsampled_LR = torch.nn.functional.interpolate(LR_tensor, size=(224, 224), mode='bilinear', align_corners=True)
    
#     # Model and optimizer per image
#     model = EfficientDIP().to(device)
#     optimizer = optim.SGD(model.parameters(), lr=1e-3, momentum=0.9, fused=True)
#     scaler = GradScaler()
    
#     # Training setup
#     noise = 0.01 * torch.randn_like(LR_tensor, device=device)
#     best_output = None
#     best_loss = float('inf')
    
#     # Mixed precision training
#     for epoch in range(800):  # Reduced epochs with better convergence
#         optimizer.zero_grad(set_to_none=True)
        
#         with autocast(device_type='cuda'):
#             output = model(noise)
#             loss = nn.L1Loss()(output, upsampled_LR)
            
#         scaler.scale(loss).backward()
#         scaler.step(optimizer)
#         scaler.update()
        
#         if loss < best_loss:
#             best_loss = loss.item()
#             with torch.no_grad():
#                 best_output = output.float().cpu().numpy()
                
#         if epoch % 100 == 0:
#             torch.cuda.empty_cache()

#     # Post-process
#     sr_image = (best_output[0,0] - best_output.min()) / (best_output.ptp() + 1e-7)
#     return Image.fromarray((sr_image * 255).astype(np.uint8))

# def batch_process_images(input_root, output_root):
#     for subdir, _, files in os.walk(input_root):
#         if "rendering" in subdir:
#             output_dir = os.path.join(output_root, os.path.relpath(subdir, input_root))
#             os.makedirs(output_dir, exist_ok=True)
            
#             for file in tqdm([f for f in files if f.lower().endswith(('.png','.jpg','.jpeg'))], 
#                            desc=f"Processing {os.path.basename(subdir)}"):
#                 try:
#                     result = process_image(os.path.join(subdir, file))
#                     result.convert("L").save(os.path.join(output_dir, file))
#                 except RuntimeError as e:
#                     if 'CUDA out of memory' in str(e):
#                         torch.cuda.empty_cache()
#                         result = process_image(os.path.join(subdir, file))  # Retry once
#                         result.convert("L").save(os.path.join(output_dir, file))

# def move_images_to_sorted(source_root, sorted_root):
#     for subdir, _, files in os.walk(source_root):
#         if "rendering" in subdir:
#             sorted_dir = os.path.join(sorted_root, os.path.relpath(subdir, source_root))
#             os.makedirs(sorted_dir, exist_ok=True)
#             for img in [f for f in files if f.lower().endswith(('.png','.jpg','.jpeg','.bmp','.tiff'))][:23]:
#                 shutil.copy2(os.path.join(subdir, img), os.path.join(sorted_dir, img))

# if __name__ == "__main__":
#     input_folder = r"D:\ShapeNetV1Renderings\ShapeNetV1Renderings\02691156"
#     output_folder = r"D:\DIP_TRY\deep_image_prior\super_resolved"
#     sorted_folder = r"D:\DIP_TRY\deep_image_prior\sorted_after_sr"
    
#     print("=== Starting Optimized Pipeline ===")
#     batch_process_images(input_folder, output_folder)
#     move_images_to_sorted(output_folder, sorted_folder)
#     print("=== Pipeline Completed ===")

