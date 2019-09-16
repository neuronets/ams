# Automated Meningioma Segmentation

![In-site segmentation results](/images/sample.png) <sub>__Figure__: Example of model outputs on a T1-weighted, contrast-enhanced magnetic resonance image. The structural scan is [available online](http://brainbox.pasteur.fr/mri/?url=https://dl.dropbox.com/sh/71jbelduefu41xs/AAAOa3oh_bVMxdFsmN965kGDa/case_057_2.nii.gz). Runtime on CPU was under 2 minutes.</sub>

```diff
! CAUTION: this tool is not a medical product and is only intended for research purposes.
```

To run using singularity, first pull the image:

```
singularity pull docker://neuronets/ams:latest-gpu
```

You have a few options when running the image. To see them call help.

```
singularity run -B $(pwd):/data -W /data --nv ams_latest-gpu.sif --help
```

Here is an example.

```
singularity run -B $(pwd):/data -W /data --nv ams_latest-gpu.sif T1_001.nii.gz output
```

This will generate two files `output.nii.gz` and `output_orig.nii.gz`. The first is the mask in conformed FreeSurfer space. The second is the mask in the original input space.

### Docker usage example

Instead of singularity with GPU, once can also use docker directly. This is an example with a CPU. Note that the CPU-based run is significantly slower.

```
docker run -it --rm -v $(pwd):/data neuronets/ams:latest-cpu T1_001.nii.gz output
```

The above examples assume there is a file named `T1_001.nii.gz` in `$(pwd)`.

### Docker hub tags

The docker hub tags follow the following naming scheme:

- `master-gpu`: gpu version of current github master
- `latest-gpu`: gpu version of latest release
- `SEMVER-gpu`: gpu version of semantically versioned release

for `cpu` versions replace `gpu` with `cpu`

# nobrainer

This model is based on the nobrainer framework. Transfer learning was applied to learn to label meningiomas from a relatively small dataset. The original model is publicly available and can be found on [nobrainer-models](https://github.com/neuronets/nobrainer-models#3d-u-net).

The pre-trained model can be downloaded via `git-annex`.
