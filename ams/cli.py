from pathlib import Path
import subprocess
import tempfile
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import click
import etelemetry
import nibabel as nib
import nobrainer
import numpy as np
import tensorflow as tf

from ams import __version__

_REQUIRED_SHAPE = (256, 256, 256)
_BLOCK_SHAPE = (128, 128, 128)

_here = Path(__file__).parent
_default_model = _here / 'meningioma_T1wc_128iso_v1.h5'


@click.command()
@click.argument('infile')
@click.argument('outprefix')
@click.option('-b', '--batch-size', type=int, default=1, help='Batch size during prediction.')
@click.option('-t', '--threshold', type=float, default=0.3, help='Threshold for binarization of predictions.')
# @click.option('-m', '--model-file', type=click.Path(exists=True), default=_default_model, help='Path to Keras model.')
@click.version_option(version=__version__)
def predict(*, infile, outprefix, batch_size, threshold):
    """Segment meningiomas in a 3D T1-weighted contrast-enhanced MRI using a trained deep neural network.

    CAUTION: this tool is not a medical product and is only intended for research purposes.

    The predictions are saved to OUTPREFIX_* with the same extension as the input file.

    If you encounter out-of-memory issues, use a lower batch size value.
    """

    msg = "CAUTION: this tool is not a medical product and is only intended for research purposes."
    msg = '\n' + '*' * len(msg) + '\n' + msg + '\n' + '*' * len(msg) + '\n'
    click.echo(click.style(msg, fg='red'))

    try:
        latest = etelemetry.get_project("neuronets/kwyk")
    except RuntimeError as e:
        print("Could not check for version updates: ", e)
    else:
        if latest and 'version' in latest:
            print("Your version: {0} Latest version: {1}".format(
                __version__, latest["version"]))

    _orig_infile = infile

    if infile.lower().endswith('.nii.gz'):
        outfile_ext = '.nii.gz'
    else:
        outfile_ext = Path(infile).suffix

    outfile = "{}{}".format(outprefix, outfile_ext)
    outfile_orig = "{}_orig{}".format(outprefix, outfile_ext)

    img = nib.load(infile)
    ndim = len(img.shape)
    if ndim != 3:
        raise ValueError("Input volume must have three dimensions but got {}.".format(ndim))
    if img.shape != _REQUIRED_SHAPE:
        tmp = tempfile.NamedTemporaryFile(suffix='.nii.gz')
        print("++ Conforming volume to 1mm^3 voxels and size 256x256x256.")
        _conform(infile, tmp.name)
        infile = tmp.name
    else:
        tmp = None

    # Load and preprocess MRI.
    img = nib.load(infile)
    x = nobrainer.io.read_volume(infile, dtype='float32')
    x = nobrainer.volume.standardize_numpy(x)
    x = nobrainer.volume.to_blocks_numpy(x, _BLOCK_SHAPE)
    x = x[..., None]  # Add grayscale channel.

    # Run forward pass of model.
    model = tf.keras.models.load_model(_default_model, compile=False)
    y_ = model.predict(x, batch_size=batch_size, verbose=1)
    y_ = np.squeeze(y_, axis=-1)

    # Binarize probabilities and combine into volume.
    y_ = (y_ > threshold).astype(np.uint8)
    y_ = nobrainer.volume.from_blocks_numpy(y_, _REQUIRED_SHAPE)
    y_img = nib.Nifti1Image(y_, affine=img.affine, header=img.header)
    y_img.header.set_data_dtype(np.uint8)

    nib.save(y_img, outfile)

    # Reslice only if we conformed.
    if tmp is not None:
        print("++ Reslicing into original volume space.")
        _reslice(input=outfile, output=outfile_orig, reference=_orig_infile, labels=True)


def _conform(input, output):
    """Conform volume using FreeSurfer."""
    subprocess.run(['mri_convert', '--conform', input, output], check=True)
    return output


def _reslice(input, output, reference, labels=False):
    """Reslice volume using FreeSurfer."""
    if labels:
        subprocess.run(['mri_convert', '-rl', reference, '-rt', 'nearest', '-ns', '1',
                        input, output],
                       check=True)
    else:
        subprocess.run(['mri_convert', '-rl', reference, input, output], check=True)
    return output
