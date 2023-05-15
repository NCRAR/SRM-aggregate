If you don't already have Anaconda Python installed, you can download and
install it from https://anaconda.org. Either Anaconda or Miniconda is fine, but
be sure to install the 64 bit version.

To install the prgoram, open up an Anaconda Python prompt and type:

    conda create -n srm-aggregate python git
    conda activate srm-aggregate
	pip install srm-aggregate@git+https://github.com/NCRAR/srm-aggregate.git

To run the program, open up an Anaconda Python prompt and type:

    conda activate srm-aggregate
	srm-aggregate

To update the program, type (note the `--upgrade` flag):

	pip install --upgrade srm-aggregate @ git+https://github.com/NCRAR/srm-aggregate.git
