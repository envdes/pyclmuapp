pyclmuapp on HPC: Python
================
Docker are not always available on HPC. Singularity is a container software usually employed in **HPC** (High performance computer). It provides a mechanism to run containers where containers can be used to package entire scientific workflows, software and libraries, and even data. Ref: https://ri.itservices.manchester.ac.uk/csf3/software/applications/singularity/

A quick look for python scripts of pyclmuapp ``singularity`` mode. 

Note! We recommend to use the ``singularity`` mode on HPC, and install `pyclmuapp` from source code (There is some configuration changed, which is not upadted to Pypi).

**Note**: must download the image in current directory first before running the command.

.. code-block:: bash

    pyclmuapp --has_container False --container_type singularity --init True


.. code-block:: python

    from pyclmuapp import usp_clmu
    
    # initialize
    o = usp_clmu(container_type='singularity')  # important to define the container_type. The default is docker
    
    # the clmu-app_1.0.sif image will be download from docker hub at the current work dir.
    # o.docker(cmd="pull", cmdlogfile="None",)  # This will pull the image from the docker hub if you not have a local image

    # other parameters are available, see the Python API documentation
    # no need to o.docker(cmd="run") for singularity
    # then same as usually
    o.check_surf_data()
    o.check_domain_data()
    o.check_forcing_data(
        usr_forcing="provided_forcing_netcdf_file.nc")
    
    original = o.run(
        ouptname="_clm.nc",
        case_name="usp_case",
        RUN_STARTDATE="2012-08-08",
        STOP_OPTION="ndays",
        STOP_N="10",
        iflog=True,
        logfile="log.log",
        crun_type="usp-exec"  #
    )
    print(original)


How to run the python in HPC?
-----------------------------
HPC usually uses batch system like 
- Manchester csf3 (The Computational Shared Facility 3) : https://ri.itservices.manchester.ac.uk/csf3/batch/
- UK ARHCER2 : https://docs.archer2.ac.uk/user-guide/scheduler/

A quick look for Manchester csf3 batch scripts, e.g., named as job_pyclmuapp.sh

.. code-block:: bash

    #!/bin/bash --login
    #$ -cwd
    #$ -pe smp.pe 2
    # activate conda env
    source activate pyclmuapp
    python your_python_script_path.py


Then submit to the batch system by

.. code-block:: bash

    qsub job_pyclmuapp.sh


.. note::

    ``singularity`` mode is slightly different from ``docker`` mode. The image is usually downloaded from docker hub at the current work dir.