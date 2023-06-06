If you don't already have Anaconda Python installed, you can download and
install it from https://anaconda.org. Either Anaconda or Miniconda is fine, but
be sure to install the 64 bit version.

To install the program, open up an Anaconda Python prompt and type:

    conda create -n ncrar-dkm-tools python git
    conda activate ncrar-dkm-tools
	pip install ncrar-dkm-tools

To run the program, open up an Anaconda Python prompt and type:

    conda activate ncrar-dkm-tools
	srm-aggregate

To update the program, type (note the `--upgrade` flag):

	pip install --upgrade ncrar-dkm-tools
