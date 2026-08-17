# CV and 3D Vision pipeline positioning

## Canonical pipeline

Use the smallest applicable subset:

1. **Input**: monocular/multi-view RGB, panorama/ERP, RGB-D, LiDAR, video, text, or latent input.
2. **Camera / pose**: intrinsics, extrinsics, calibration, SfM, tracking, or pose-free estimation.
3. **Preprocessing / features**: enhancement, matching, encoders, depth/normal priors, masks, or segmentation.
4. **Representation**: point cloud, voxels, mesh, radiance field, 3D Gaussians, triplanes, implicit surfaces, or hybrids.
5. **Initialization**: SfM points, random primitives, feed-forward prediction, depth back-projection, or learned anchors.
6. **Optimization / update**: per-scene training, densification/pruning, bundle adjustment, deformation, continual update, or feed-forward refinement.
7. **Rendering / rasterization**: ray marching, volume rendering, splatting, projection, visibility, blending, filtering, or shading.
8. **Loss / supervision**: photometric, geometric, perceptual, regularization, semantic, or temporal objectives.
9. **Output**: geometry, novel views, depth, semantics, camera pose, editable assets, or generated content.
10. **Evaluation**: protocol, datasets, splits, metrics, cost, and failure cases.

For each paper, produce a delta such as:

```text
Input: reused
Camera/Pose: reused
Representation: changed
Initialization: reused
Optimization: changed
Rendering/Rasterization: changed
Loss: changed
Output: novel-view rendering, not metric geometry
```

## Task boundary

Do not collapse these goals:

- **Geometry reconstruction**: estimates measurable surfaces, points, depth, normals, poses, or occupancy.
- **Novel-view rendering**: synthesizes images from new viewpoints; representation may not yield trustworthy geometry.
- **Feed-forward prediction**: predicts a representation or scene state without per-scene optimization, though optional refinement may follow.
- **Generative 3D**: creates plausible assets or scenes from priors; plausibility is not recovery of the observed real geometry.
- **Editing / continual update**: modifies or maintains a scene representation; dynamic rendering alone does not prove persistent real-scene updating.

State the paper's primary deliverable before comparing it with another method.

## Metric boundary

### Geometry evidence

Use accuracy, completeness, precision/recall/F-score at a stated threshold, Chamfer distance, depth error, normal error, pose error, or surface distance. Check alignment, scale, visibility masks, and evaluation region.

### Rendering evidence

Use PSNR, SSIM, LPIPS, perceptual/user studies, and view-dependent quality. These do not by themselves prove geometry.

### Efficiency evidence

Use train time, inference/render FPS, memory, model size, primitive count, and preprocessing time only with comparable hardware and resolution.

### Prediction/generation evidence

Use task-specific accuracy, consistency, diversity, fidelity, or distributional metrics. Do not treat attractive samples as reconstruction accuracy.

## Special checks

- **Panorama**: distinguish 360-degree coverage from translational parallax; a single-center panorama usually needs depth, layout, or generative priors for 3D.
- **3DGS**: identify changes to primitive parameters, initialization, densification/pruning, projection/covariance, sorting/blending, shading, losses, and training schedule.
- **NeRF**: identify encoder/field, sampling, integration, proposal networks, scene contraction, pose handling, and supervision.
- **Mesh-Gaussian hybrids**: state whether the mesh is the native representation, a constraint, or a post-hoc extraction; connected does not imply watertight or manifold.
- **Dynamic scenes**: separate deformation/canonical modeling, time conditioning, tracking, and persistent updates across acquisition epochs.

## Fair comparison checklist

Before saying A outperforms B, check:

- same task and output;
- same dataset, split, and image resolution;
- same camera assumptions and input count;
- comparable training budget and initialization;
- same metric implementation and masks;
- comparable hardware for speed/memory;
- official versus reimplemented baseline;
- geometry versus rendering evidence.

If any condition fails, describe the comparison as indicative rather than controlled.

