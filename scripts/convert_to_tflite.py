"""Convert a Keras model (in hdf5) to TFLite."""

import tempfile
import tensorflow as tf

def convert(inpath, outpath):
    with tempfile.TemporaryDirectory() as tmp_saved_model_dir:
        # Keras hdf5 to savedmodel.
        model = tf.keras.models.load_model(in_path, compile=False)
        model.save(tmp_saved_model_dir.name)
        # Convert the model.
        converter = tf.lite.TFLiteConverter.from_saved_model(tmp_saved_model_dir.name)
        tflite_model = converter.convert()
        # Save the model.
        with open(out_path, 'wb') as f:
            f.write(tflite_model)

if __name__ == "__main__":
    import sys

    try:
        inpath = sys.argv[1]
        outpath = sys.argv[2]
    except IndexError:
        print("usage: python convert.py HDF5_PATH TFLITE_PATH")
        sys.exit(1)
    convert(inpath, outpath)
