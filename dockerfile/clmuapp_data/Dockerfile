# escape=`

# Description: Dockerfile for the clmuapp application
# Author: Junjie Yu, 2024-05-23, The University of Manchester
FROM envdes/clmu-app:1.0

LABEL `
    org.label-schema.schema-version="1.0" `
    org.label-schema.name="clmuapp with input data" `
    org.label-schema.version="1" `
    org.label-schema.build-date="20231125" `
    clm.version.major="5" `
    clm.env.compiler="GCC" `
    clm.env.compiler.version="9.3.1" `
    clm.env.mpi="OpenMPI" `
    clm.env.mpi.version="4.0.2-1" `
    clm.env.cmake.version="3.18" `
    clm.env.pnetcdf.version="1.12.3" `
    clm.env.netcdf-c.version="4.7.0-2" `
    clm.env.netcdf-fortran.version="4.5.2-3" `
    clm.env.esmf.version="8.0.1" `
    clm.env.python.version="3.7.9" `
    clm.env.svn.version="1.12" ` 
    clm.os.version="Fedora 31" 

USER root
WORKDIR /root

# must copy one file by one file, otherwise the inut data will be redownloaded
COPY ./inputfolder/atm/cam/chem/trop_mozart/emis/megan21_emis_factors_78pft_c20161108.nc /p/scratch/CESMDATAROOT/inputdata/atm/cam/chem/trop_mozart/emis/megan21_emis_factors_78pft_c20161108.nc

# the aerosoldep_WACCM.ensmean_monthly_hist_1849-2015_0.9x1.25_CMIP6_c180926.nc has been selected only include the 2000 year
# by Python Xarray, so the file size is smaller than the original file
# original file: 5.8G, selected file: 36 M
COPY ./inputfolder/atm/cam/chem/trop_mozart_aero/aero/aerosoldep_WACCM.ensmean_monthly_hist_1849-2015_0.9x1.25_CMIP6_c180926.nc /p/scratch/CESMDATAROOT/inputdata/atm/cam/chem/trop_mozart_aero/aero/aerosoldep_WACCM.ensmean_monthly_hist_1849-2015_0.9x1.25_CMIP6_c180926.nc
COPY ./inputfolder/atm/datm7/topo_forcing/topodata_0.9x1.25_USGS_070110_stream_c151201.nc /p/scratch/CESMDATAROOT/inputdata/atm/datm7/topo_forcing/topodata_0.9x1.25_USGS_070110_stream_c151201.nc
COPY ./inputfolder/lnd/clm2/paramdata/clm5_params.c171117.nc /p/scratch/CESMDATAROOT/inputdata/lnd/clm2/paramdata/clm5_params.c171117.nc
COPY ./inputfolder/lnd/clm2/snicardata/snicar_drdt_bst_fit_60_c070416.nc /p/scratch/CESMDATAROOT/inputdata/lnd/clm2/snicardata/snicar_drdt_bst_fit_60_c070416.nc
COPY ./inputfolder/lnd/clm2/snicardata/snicar_optics_5bnd_c090915.nc /p/scratch/CESMDATAROOT/inputdata/lnd/clm2/snicardata/snicar_optics_5bnd_c090915.nc
COPY ./inputfolder/lnd/clm2/urbandata/CLM50_tbuildmax_Oleson_2016_0.9x1.25_simyr1849-2106_c160923.nc /p/scratch/CESMDATAROOT/inputdata/lnd/clm2/urbandata/CLM50_tbuildmax_Oleson_2016_0.9x1.25_simyr1849-2106_c160923.nc

USER root
WORKDIR /root
CMD ["/bin/bash","-l"]