<h1 align="center">Rad-Surf: Automated Synthesis of Radiographs and Vertebral Surfaces for Single-View Reconstruction
</h1>

<p  align="center">  

---

###  **Abstract**  
Single-view reconstruction (SVR) enables 3D reconstruction of vertebrae from a single radiograph and is particularly valuable in Minimally Invasive Spine Surgery (MISS), where intraoperative imaging is limited to 2D data obtained from C-arm fluoroscopy. SVR can reduce radiation exposure by avoiding multi-angle imaging. It supports various 3D representations, with mesh-based outputs offering greater memory efficiency and anatomical detail compared to voxel grids. However, SVR remains underexplored due to the lack of paired radiograph–surface datasets.

### ❗ **Problem Statement**  
Although datasets like VerSe, TotalSegmentator, and CTSpine1K offer CT scans with segmentation labels, and others like MedShapeNet and VSD provide surface models, none offer *paired radiographs and meshes* necessary for supervised SVR learning.

### **Method**  
We propose **Rad-Surf**, an automated and generalizable pipeline that:
- Generates **Digitally Reconstructed Radiographs (DRRs)** and surface meshes from CT–segmentation pairs.
- Includes a **Deep Image Prior (DIP)**-based super-resolution enhancement to improve DRR quality.
- Provides post-processing for seamless integration into deep learning-based SVR pipelines.

The generated DRRs were evaluated using:
- Signal-to-Noise Ratio (SNR)
- Contrast-to-Noise Ratio (CNR)
- Entropy
- Edge Sharpness

Additionally, the reconstructed meshes were clinically analyzed based on four vertebral geometric parameters.

### 📊 **Results**  
The **Rad-Surf** dataset for lumbar vertebrae SVR includes:
- **475 unique DRR–mesh pairs**
- **24 diverse DRRs per mesh**
- **Total: 11,400 DRR–mesh pairs**  
The dataset is **open-source** and designed to support robust training of SVR models.

---

### 🧾 **Index Terms**
🔹 Minimally Invasive Spine Surgery (MISS)  
🔹 Single-view Surface Reconstruction (SVR)  
🔹 Digitally Reconstructed Radiograph (DRR)  
🔹 Deep Image Prior (DIP)  
🔹 3D Mesh Reconstruction  
🔹 Dataset Generation  
🔹 Clinical Validation  
🔹 Supervised Learning  

---

