# tinydrive
a tool to download, compress, and re-upload your files google drive files.

# installation

## asdf

I use [asdf-vm](https://asdf-vm.com/), which makes it super easy to use the same 
version of python as me (see `.tool-versions`). If you don't, make sure you're on python `3.13.5`.

## Google Cloud

since I don't want to share my private credentials for this project and I can't 
be bothered to host this myself (yet), you'll have to create your own Google Cloud 
project.

to do this, follow the [Python quickstart](https://developers.google.com/workspace/drive/api/quickstart/python)
up until the "Install the Google client library" section.

## virtual environment

now, you'll need to create a new virtual environment using `venv`:

```bash
python -m venv .venv
```

and activate it (if you're on bash) using:

```bash
source ./.venv/bin/activate
```

## requirements

finally, after activating your virtual environment, install all requirements using:

```bash
pip install -r requirements.txt
```

# usage 

idk yet :)
