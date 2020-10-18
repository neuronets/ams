# Automated Meningioma Segmentation

![In-site segmentation results](/images/sample.png) <sub>__Figure__: Example of model outputs on a T1-weighted, contrast-enhanced magnetic resonance image. The structural scan is [available online](http://brainbox.pasteur.fr/mri/?url=https://dl.dropbox.com/sh/71jbelduefu41xs/AAAOa3oh_bVMxdFsmN965kGDa/case_057_2.nii.gz). Runtime on CPU was under 2 minutes.</sub>

```diff
! CAUTION: this tool is not a medical product and is only intended for research purposes. !
```

## Requirements for use

- Input data should be gadolinium contrast-enhanced T1-weighted magnetic resonance images. The model was trained and evaluated on this type of data.
- CPU or, optionally, GPU
  - Runtime will be much faster when a GPU is available. Please see the Singularity usage example below for running the model on a GPU.

## Singularity usage example

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

## Docker usage example

Instead of singularity with GPU, once can also use Docker directly. This is an example with a CPU. Note that the CPU-based run is significantly slower.

```
docker run -it --rm -v $(pwd):/data --user 1000:1000 neuronets/ams:latest-cpu T1_001.nii.gz output
```

The above examples assume there is a file named `T1_001.nii.gz` in the working directory. The option `--user 1000:1000` runs the container with user ID 1000 and group ID 1000. This will prevent the created files from being owned by root. Replace the IDs with your own IDs. On Unix-like systems, one can use `id -u` and `id -g` to get user ID and group ID, respectively.

### DockerHub tags

The DockerHub tags follow the following naming scheme:

- `master-gpu`: gpu version of current GitHub master
- `latest-gpu`: gpu version of latest release
- `SEMVER-gpu`: gpu version of semantically versioned release

for `cpu` versions replace `gpu` with `cpu`

# nobrainer

This model is based on the nobrainer framework. Transfer learning was applied to learn to label meningiomas from a relatively small dataset. The original model is publicly available and can be found on [neuronets/trained-models](https://github.com/neuronets/trained-models#3d-u-net).

The pre-trained model can be downloaded via `git-annex`.
