pyclmuapp: A Python Package for Integration and Execution of Community Land Model Urban (CLMU) in a Containerized Environment
-----------------------------------------------------------------------------------------------------------------------------
|docs| |GitHub| |license| 

.. |GitHub| image:: https://img.shields.io/badge/GitHub-pyclmuapp-brightgreen.svg
   :target: https://github.com/envdes/pyclmuapp

.. |Docs| image:: https://img.shields.io/badge/docs-pyclmuapp-brightgreen.svg
   :target: https://envdes.github.io/pyclmuapp/

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://github.com/envdes/pyclmuapp/blob/main/LICENSE

pyclmuapp: A Python Package for Integration and Execution of Community Land Model Urban (CLMU) in a Containerized Environment.

Contributors: `Junjie Yu <https://junjieyu-uom.github.io>`_, `Keith Oleson <https://staff.ucar.edu/users/oleson>`_, `Yuan Sun <https://github.com/YuanSun-UoM>`_, `David Topping <https://research.manchester.ac.uk/en/persons/david.topping>`_, `Zhonghua Zheng <https://zhonghuazheng.com>`_ (zhonghua.zheng@manchester.ac.uk)


**Python interface of pyclmuapp**

Installation
------------
Step 1: create an environment::

    $ conda create -n pyclmuapp python=3.8
    $ conda activate pyclmuapp
    $ conda install -c conda-forge numpy pandas xarray haversine netcdf4 nc-time-axis

Step 2: install using pip::

    $ pip install pyclmuapp

(optional) install from source:: 

    $ git clone https://github.com/envdes/pyclmuapp.git
    $ cd pyclmuapp
    $ python setup.py pyclmuapp


Please check `online documentation <https://envdes.github.io/pyclmuapp/>`_ for more information.

How to ask for help
-------------------
The `GitHub issue tracker <https://github.com/envdes/pyclmuapp/issues>`_ is the primary place for bug reports. 
