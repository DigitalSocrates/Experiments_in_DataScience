""" script to download models """
import os
import sys
import requests
from tqdm import tqdm

CHUNK_SIZE = 1024

if len(sys.argv) != 2:
    print('You must enter the model name as a parameter, \
          e.g.: download_model.py 124M')
    sys.exit(1)

model_name = sys.argv[1]

subdir = os.path.join('models', model_name)
if not os.path.exists(subdir):
    os.makedirs(subdir)
# needed for Windows
subdir = subdir.replace('\\', '/')

# iterates over a list of filenames:
for filename in ['checkpoint', 'encoder.json',
                 'hparams.json',
                 'model.ckpt.data-00000-of-00001',
                 'model.ckpt.index',
                 'model.ckpt.meta', 'vocab.bpe']:
    # For each filename in the list, send an HTTP GET request to a specific URL
    r = requests.get("https://openaipublic.blob.core.windows.net/gpt-2/" +
                     subdir + "/" + filename,
                     stream=True,
                     timeout=60)
    with open(os.path.join(subdir, filename), 'wb') as f:
        # retrieves the file size from the HTTP response headers:
        file_size = int(r.headers["content-length"])
        # open a file for writing in binary mode and downloads
        # the file contents creating progress bars in the command line
        with tqdm(ncols=100, desc="Fetching " + filename,
                  total=file_size,
                  unit_scale=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                # reads a chunk of data from the response
                # and writes it to the local file.
                f.write(chunk)
                progress_bar.update(CHUNK_SIZE)
