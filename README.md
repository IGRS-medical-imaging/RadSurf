<h1 align="center">Rad-Surf: Automated Synthesis of Radiographs and Vertebral Surfaces for Single-View Reconstruction
</h1>

<p  align="center">  

---

###  `Abstract`  
Single-view reconstruction (SVR) enables 3D reconstruction of vertebrae from a single radiograph and is particularly valuable in Minimally Invasive Spine Surgery (MISS), where intraoperative imaging is limited to 2D data obtained from C-arm fluoroscopy. SVR can reduce radiation exposure by avoiding multi-angle imaging. It supports various 3D representations, with mesh-based outputs offering greater memory efficiency and anatomical detail compared to voxel grids. However, SVR remains underexplored due to the lack of paired radiograph–surface datasets.

###  `Problem Statement`  
Although datasets like VerSe, TotalSegmentator, and CTSpine1K offer CT scans with segmentation labels, and others like MedShapeNet and VSD provide surface models, none offer *paired radiographs and meshes* necessary for supervised SVR learning.

### `Method`  
We propose **Rad-Surf**, an automated and generalizable pipeline that:
- Generates **Digitally Reconstructed Radiographs (DRRs)** and surface meshes from CT–segmentation pairs.
- Includes a **Deep Image Prior (DIP)**-based super-resolution enhancement to improve DRR quality.
- Provides post-processing for seamless integration into deep learning-based SVR pipelines.


###  `Results`  
The **Rad-Surf** dataset for lumbar vertebrae SVR includes:
- **475 unique DRR–mesh pairs**
- **24 diverse DRRs per mesh**
- **Total: 11,400 DRR–mesh pairs**  
The dataset is **open-source** and designed to support robust training of SVR models.

</p>
<h3 > <i>Index Terms</i> </h3> 

  :diamond_shape_with_a_dot_inside: Minimally Invasive Spine Surgery (MISS)
  :diamond_shape_with_a_dot_inside: Single view Surface Reconstruction(SVR)
  :diamond_shape_with_a_dot_inside: Digitally Reconstructed Radiograph (DRR) 
  :diamond_shape_with_a_dot_inside: Deep Image Prior (DIP)
  :diamond_shape_with_a_dot_inside: Dataset Generation 
  :diamond_shape_with_a_dot_inside: Clinical Validation

</div>

</div>

</details>
<h2 align="center">Dataset</h2>
<details>
You can download the dataset from the following link:

🔗 [3DReVert-Dataset](https://drive.google.com/drive/folders/1YBzQlRE8mZOfmKDpoc9omabz6GCIIJbH?usp=sharing) 
Sub-directory-based arrangement:
```
DRR/
├── verse004_segment_20/
│  ├── rendering/
│    ├── 00.png
│    ├── 01.png
│    ├── 02.png
│    └── ...
├──verse005_segment_20/
│   ├── rendering/
│   │   ├── 00.png
│   │   ├── 01.png
│   │   ├── ...
│   │   └── 23.png
├── ...  
│   └── ...
Mesh/
├── verse004_segment_20.stl/..
├── verse005_segment_20.stl/..
├── ...
```
</details>

## <div align="center">Methodology</div>
<p align="center">
  <img src="Methodology_RadSurf.jpg">
</p>
<div align = "center">

:small_orange_diamond: Overview of the Rad-Surf Algorithm: (A) Input CT scan and corresponding segmentation label, (B) DRR rendering and preparation, (C) DRR enhancement using
DIP-based super-resolution, and (D) Mesh rendering and post-processing 
</div>
