<h1 align="center">Rad-Surf: Automated Synthesis of Radiographs and Vertebral Surfaces for Single-View Reconstruction
</h1>

<p  align="center">  

---

**Rad-Surf** is an automated pipeline designed for single-view 3D vertebra reconstruction in Minimally Invasive Spine Surgery (MISS), where only 2D radiographs are available intraoperatively. Unlike existing datasets that lack paired radiograph–surface data, Rad-Surf generates high-quality Digitally Reconstructed Radiographs (DRRs), point clouds, and surface meshes from CT–segmentation pairs. The dataset is made open source and designed to support robust models.[RadSurf-Dataset](https://drive.google.com/drive/folders/1YBzQlRE8mZOfmKDpoc9omabz6GCIIJbH?usp=sharing) 

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
<summary><b>Rad-Surf Dataset Overview</b></summary>

The **Rad-Surf** dataset for lumbar vertebrae single-view reconstruction includes:  
- **475 unique DRR–mesh pairs**  
- **24 DRRs per mesh**  
- **Total: 11,400 DRR–mesh pairs**  


You can download the dataset from the following link:

🔗 [RadSurf-Dataset](https://drive.google.com/drive/folders/1YBzQlRE8mZOfmKDpoc9omabz6GCIIJbH?usp=sharing) 
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
