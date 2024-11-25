.. ctsmpy documentation master file, created by
   sphinx-quickstart on Tue Jan 23 16:49:22 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyclmuapp: A Python Package for Integration and Execution of Community Land Model Urban (CLMU) in a Containerized Environment
========================================

|DOI| |GitHub| |Docs| |License|

.. |DOI| image:: https://zenodo.org/badge/750479733.svg
  :target: https://zenodo.org/doi/10.5281/zenodo.10710695

.. |GitHub| image:: https://img.shields.io/badge/GitHub-pyclmuapp-brightgreen.svg
   :target: https://github.com/envdes/pyclmuapp

.. |Docs| image:: https://img.shields.io/badge/docs-pyclmuapp-brightgreen.svg
   :target: https://envdes.github.io/pyclmuapp/

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://github.com/envdes/pyclmuapp/blob/main/LICENSE

pyclmuapp: A Python Package for Integration and Execution of Community Land Model Urban (CLMU) in a Containerized Environment

Contributors: `Junjie Yu <https://junjieyu-uom.github.io>`_, `Keith Oleson <https://staff.ucar.edu/users/oleson>`_, `Yuan Sun <https://github.com/YuanSun-UoM>`_, `David Topping <https://research.manchester.ac.uk/en/persons/david.topping>`_, `Zhonghua Zheng <https://zhonghuazheng.com>`_ (zhonghua.zheng@manchester.ac.uk)


.. toctree::
   :maxdepth: 1
   :caption: Overview

   notebooks/overview/overview.md
   notebooks/overview/installation.md

.. toctree::
   :maxdepth: 1
   :caption: Python: warmup

   notebooks/usp/warmup.ipynb

.. toctree::
   :maxdepth: 1
   :caption: Python: examples

   notebooks/usp/example1_usp_basic.ipynb
   notebooks/usp/example2_usp_global_warming.ipynb
   notebooks/usp/example3_usp_adaptation.ipynb

.. toctree::
   :maxdepth: 2
   :caption: Other usage

   notebooks/basic/basic_usage_inter.md
   notebooks/basic/basic_usage_cli.md

.. toctree::
   :maxdepth: 1
   :caption: Python: created input files

   notebooks/own/prepare_forcing_from_era5.ipynb
   notebooks/own/prepare_urbansurf_10evlurb.ipynb

.. toctree::
   :maxdepth: 1
   :caption: Spinup

   notebooks/usp/usp_spinup_mode.ipynb

.. toctree::
   :maxdepth: 1
   :caption: HPC

   notebooks/hpc/HPC.ipynb
   notebooks/hpc/singularity.rst
   

.. toctree::
   :maxdepth: 1
   :caption: Evaluation

   notebooks/val/urban_plumber_usp.ipynb

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   modules.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
