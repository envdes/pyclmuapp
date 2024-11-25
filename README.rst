pyclmuapp: A Python Package for Integration and Execution of Community Land Model Urban (CLMU) in a Containerized Environment
--------------------------------------------------
|doi| |docs| |GitHub| |license| |pepy|

.. |DOI| image:: https://zenodo.org/badge/750479733.svg
  :target: https://zenodo.org/doi/10.5281/zenodo.10710695

.. |GitHub| image:: https://img.shields.io/badge/GitHub-pyclmuapp-brightgreen.svg
   :target: https://github.com/envdes/pyclmuapp

.. |Docs| image:: https://img.shields.io/badge/docs-pyclmuapp-brightgreen.svg
   :target: https://junjieyu-uom.github.io/pyclmuapp/

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://github.com/envdes/pyclmuapp/blob/main/LICENSE
   
.. |pepy| image:: https://static.pepy.tech/personalized-badge/pmcpy?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads
   :target: https://pepy.tech/project/pmcpy

pyclmuapp: A Python Package for Integration and Execution of Community Land Model Urban (CLMU) in a Containerized Environment.

Contributors: `Junjie Yu <https://junjieyu-uom.github.io>`_, `Keith Oleson <https://staff.ucar.edu/users/oleson>`_, `Yuan Sun <https://github.com/YuanSun-UoM>`_, `David Topping <https://research.manchester.ac.uk/en/persons/david.topping>`_, `Zhonghua Zheng <https://zhonghuazheng.com>`_ (zhonghua.zheng@manchester.ac.uk)


**Web interface of pyclmuapp**

.. code-block:: bash

   $ docker pull envdes/pyclmuapp:1.0
   $ docker run --hostname clmu-app -p 8080:7860 envdes/pyclmuapp:1.0
   $ #then open the browser and input the address: http://localhost:8080/


**Python/CLI interface of pyclmuapp**

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

How to use it?
--------------

First, download the Docker (or Singularity). Then, you can use the following command to run the CLMU-App.


.. code-block:: bash

   $ pyclmuapp --has_container False --container_type docker --init True # or singularity

Run the case with the user forcing file and start date. The output file will be saved in the output folder.

Second, you can run the case with the user forcing file and start date. The output file will be saved in the output folder.
The surface data file and domain file are optional, by default, the default surface data file of London is used. Use ``--usr_surfdata`` input the file path.


.. code-block:: bash

   $ pyclmuapp --usr_forcing "inputfolder/usp/CTSM_forcing_London_ERA5_2002_2014.nc" \
   $ --CASE_NAME "basic_test" \
   $ --RUN_STARTDATE "2012-01-01" \
   $ --STOP_OPTION "ndays" \
   $ --STOP_N "15" \


If you are using **Docker**, stop and remove the running container by

.. code-block:: bash

   $ pyclmuapp --has_container True --container_type docker --init False # or singularity


(Optional)

Create your own surface data file.

.. code-block:: bash

   $ pyclmuapp --pyclmuapp_mode get_surfdata \
   $ --lat 51.5074 --lon 0.1278 \
   $ --outputname "surfdata.nc" \
   $ --pct_urban 0,0,100.0 \
   $ --urbsurf "inputfolder/mksrf_urban_0.05x0.05_simyr2000.c120601.nc" \
   $ --soildata "inputfolder/mksrf_soitex.10level.c010119.nc" 

Create your own forcing data file.

.. code-block:: bash

   $ pyclmuapp --pyclmuapp_mode get_forcing \
   $   --lat 51.5 --lon 0.12 --zbot 30 \
   $   --start_year 2012 --end_year 2012 \
   $   --start_month 1 --end_month 1
   $ #will download and save in the default folder `./era5_forcing/`
   $ #the output file will be `./era5_forcing/era5_forcing_51.5_0.12_950_2012_01.nc`

pyclmuapp Input Parameters
===========================

Required
--------

- **usr_forcing/USR_FORCING**: User forcing file, default is ``None``. If you have the domain file, input the file path.
- **run_startdate/RUN_STARTDATE**: Start date, default is ``None``.

Usually Required
----------------

- **strat_tod/START_TOD**: The start time of the day. The default is "00000".
- **stop_option/STOP_OPTION**: Stop option, default is ``ndays``, can be ``nyears``, ``nmonths``, ``ndays``.
- **stop_n/STOP_N**: Stop number, default is ``1``. Case length is STOP_OPTION * STOP_N.
- **pyclmuapp_mode/PYCLMUAPP_MODE**: pyclmuapp mode, default is ``usp``, can be ``script``, ``pts``, ``get_forcing``, ``get_surfdata``.

Optional
--------

**Common:**

- **init/INIT**: If true, only pull(/run) the container. Default is ``False``.
- **pwd/PWD**: Current working directory, default is ``pwd``, can be ``none``. If it is not none, then the input_path, output_path, log_path, scripts_path will be used in pwd or be created. If ``none``, the input_path, output_path, log_path, scripts_path should be provided.
- **container_type/CONTAINER_TYPE**: Container type, default is ``docker``, can be ``singularity``.
- **input_path/INPUT_PATH**: CTSM input path, default is ``None``. The path will be binded to "inputdata" in the container.
- **output_path/OUTPUT_PATH**: CTSM output path, default is ``None``. The path will be binded to "Archive" in the container.
- **log_path/LOG_PATH**: CTSM log path, default is ``None``. The path will be binded to "CaseOutputs" in the container.
- **scripts_path/SCRIPTS_PATH**: CTSM scripts path, default is ``None``. The path will be binded to "/p/scripts" in the container.
- **has_container/HAS_CONTAINER**: Has container, default is ``True``.
- **iflog/IFLOG**: If log, default is ``True``.
- **logfile/LOGFILE**: Log file, default is ``pyclmuapp.log``.

**For PYCLMUAPP_MODE = usp:**

- **usr_domain/USR_DOMAIN**: User domain file, default is ``None``. If you have the domain file, input the file path.
- **usr_surfdata/USR_SURFDATA**: User surface data file, default is ``None``. If you have the domain file, input the file path.
- **output_prefix/OUTPUT_PREFIX**: Output file name prefix, default is ``_clm.nc``, used to generate the output file of pyclmuapp.
- **case_name/CASE_NAME**: Case name, default is ``usp_case``.
- **hist_type/HIST_TYPE**: Param for usp. ouput type. Can be GRID, LAND, COLS, default is GRID
- **hist_nhtfrq/HIST_NHTFRQ**: Param for usp. History file frequency, default is 1 (ouput each time step)
- **hist_mfilt/HIST_MFILT**: Param for usp. each history file will include mfilt time steps, default is 1000000000
- **var_add/VAR_ADD**: Additional variables of urban, default is ``TSA_U``.
- **claen/CLAEN**: Clean, default is ``False``. If ``True``, will clean the case files.
- **surf_var/SURF_VAR**: Param for usp. Surface variable, default is None. Can be one/some (use ','(withou space to seperate each)) of 'CANYON_HWR', 'HT_ROOF','THICK_ROOF','THICK_WALL',' WTLUNIT_ROOF','WTROAD_PERV','WIND_HGT_CANYON','NLEV_IM PROAD','TK_ROOF','TK_WALL','TK_IMPROAD','CV_ROOF','CV_ WALL','CV_IMPROAD','EM_IMPROAD','EM_PERROAD','EM_ROOF' ,'EM_WALL','ALB_IMPROAD_DIR','ALB_IMPROAD_DIF','ALB_PERROAD_DIR','ALB_PERROAD_DIF','ALB_ROOF_DIR','ALB_ROOF_DIF','ALB_WALL_DIR','ALB_WALL_DIF','T_BUILDING_MIN'.
- **surf_action/SURF_ACTION**: Param for usp. Surface action, default is None. The number is same as surf_var with "," seperated (not ", ").
- **forcing_var/FORCING_VAR**: Param for usp. Forcing variable, default is None. Can be one/some (use ','(withou space to seperate each)) of 'Prectmms','Wind','LWdown','PSurf','Qair','Tair','S Wdown'.
- **forcing_action/FORCING_ACTION**: Param for usp. Forcing action, default is None. The number is same as forcing_var with "," seperated (not ", ").
- **urban_hac/URBAN_HAC**: The flag to turn on the urban HAC. The default is "ON_WASTEHEAT". valid_values="OFF","ON","ON_WASTEHEAT".

**For PYCLMUAPP_MODE = usp and RUN_TYPE = branch:**

- **run_type/RUN_TYPE**: Run type, default is ``coldstart``, can be ``branch``.
- **run_refcase/RUN_REFCASE**: Reference case, default is ``None``.
- **run_refdate/RUN_REFDATE**: Reference date, default is ``None``.
- **run_reftod/RUN_REFTOD**: Reference time of the day, default is 00000. Need to be provided when the RUN_TYPE is "branch".

**For PYCLMUAPP_MODE = script:**

- **script/SCRIPT**: Script file in the container, default is ``None``.

**For PYCLMUAPP_MODE = get_surfdata and get_forcing**

- **urbsurf/URBSURF**: Param for get_surfdata. Urban surface data file, default is ``None``. Here to download the urban surface data file: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_urban_0.05x0.05_simyr2000.c120601.nc.
- **soildata/SOILDATA**: Param for get_surfdata. Soil data file, default is ``None``. Here to download the soil data file: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_soitex.10level.c010119.nc.
- **pct_urban/PCT_URBAN**:  Param for get_surfdata. Percentage of urban land use in each density class, sum should be 100, default is 0,0,100.0.
- **lat/LAT**: Param for get_surfdata and get_forcing. Latitude of the urban area, default is ``None``.
- **lon/LON**: Param for get_surfdata and get_forcing. Longitude of the urban area, default is ``None``.
- **outputname/OUTPUTNAME**: Param for get_surfdata. Output file name, default is surfdata.nc
- **zbot/ZBOT**: Param for get_forcing. Zbot, default is 30 meters.
- **start_year/START_YEAR**: Param for get_forcing. Start year, default is 2012.
- **end_year/END_YEAR**: Param for get_forcing. End year, default is 2012.
- **start_month/START_MONT**: Param for get_forcing. Start month, default is 1.
- **end_month/END_MONTH**: Param for get_forcing. End month, default is 12.

Please check `online documentation <https://junjieyu-uom.github.io/pyclmuapp/>`_ for more information.

How to ask for help
-------------------
The `GitHub issue tracker <https://junjieyu-uom.github.io/pyclmuapp/issues>`_ is the primary place for bug reports. 
