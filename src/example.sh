#! bin/bash

# Junjie Yu, Manchester, UK, 2024-06-19
# This is an example script to run pyclmuapp

# =================================================================================================
# Before running this script, please make sure you have installed pyclmuapp and docker/singularity
# You can install pyclmuapp by running: pip install pyclmuapp
# then you can run the following command to check if pyclmuapp is installed successfully:
# $ pyclmuapp -h

# =================================================================================================
# before running this script, you also need to revise the following parameters:
# 1. pwd or input_path, output_path, log_path, scripts_path
# 2. usr_forcing, usr_surfdata
# 3. RUN_STARTDATE, STOP_OPTION, STOP_N, RUN_TYPE,
# 4. lat, lon, zbot, start_year, end_year, start_month, end_month
# 5. pct_urban, urbsurf, soildata

# =================================================================================================
# also you need to download the urban surface data file and soil data file
# The download link is provided in the script
# How to run this script:
# $ bash example.sh --container_type docker --task usp # or get_forcing, get_surfdata, init
# $ bash example.sh --container_type singularity --task usp # or get_forcing, get_surfdata, init
# =================================================================================================

container_type=docker
task=usp
while [[ $# -gt 0 ]]; do
    case "$1" in
        --container_type)
            container_type=$2
            shift 2
            ;;
        --task)
            task=$2
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Start pyclmuapp"
echo "container_type: $container_type"
echo "task: $task"
echo "Start time: $(date)"

if [ $task == "init" ]; then
    pyclmuapp --has_container False --container_type $container_type --init True
fi

if [ $task == "usp" ]; then

    # must revise the 
    # 1. pwd or input_path, output_path, log_path, scripts_path
    # 2. usr_forcing, usr_surfdata
    # 3. RUN_STARTDATE, STOP_OPTION, STOP_N, RUN_TYPE,
    pyclmuapp \
        --pwd $PWD \
        --container_type $container_type \
        --iflog True \
        --logfile "pyclmuapp.log" \
        --usr_forcing "inputfolder/usp/CTSM_forcing_London_ERA5_2002_2014.nc" \
        --usr_surfdata "inputfolder/usp/CTSM_surfdata_London_urban_0.05x0.05.nc" \
        --RUN_STARTDATE "2012-01-01" \
        --STOP_OPTION "ndays" \
        --STOP_N "15" \
        --RUN_TYPE "coldstart" \
        --hist_type "GRID" \
        --hist_nhtfrq "1" \
        --hist_mfilt "1000000000" \
        --output_prefix "_clm.nc" \
        --CASE_NAME "pyclmuapp" \
        --run_type "coldstart" \
        --run_refcase "None" \
        --run_refdate "None" 
fi

if [ $task == "get_forcing" ]; then
    # revise the lat, lon, zbot, start_year, end_year, start_month, end_month
    pyclmuapp \
        --pyclmuapp_mode get_forcing \
        --lat 51.5074 --lon 0.1278 --zbot 30 \
        --start_year 2012 --end_year 2012 \
        --start_month 1 --end_month 12
fi


if [ $task == "get_surfdata" ]; then
    # revise the lat, lon, pct_urban, urbsurf, soildata
    pyclmuapp \
        --pyclmuapp_mode get_surfdata \
        --lat 51.5074 --lon 0.1278 \
        --outputname "surfdata.nc" \
        --pct_urban 0,0,100.0 \
        --urbsurf "inputfolder/mksrf_urban_0.05x0.05_simyr2000.c120601.nc" \
        --soildata "inputfolder/mksrf_soitex.10level.c010119.nc"
fi
# how to download the urban surface data file: 
#wget --no-check-certificate -O {soildata_name} \
#    https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_soitex.10level.c010119.nc
#wget --no-check-certificate -O {urbsurf_name} \
#    https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_urban_0.05x0.05_simyr2000.c120601.nc


# pyclmuapp -h
#usage: pyclmuapp [-h] [--version] [--init INIT] [--pwd PWD] [--container_type CONTAINER_TYPE] [--input_path INPUT_PATH]
#                 [--output_path OUTPUT_PATH] [--log_path LOG_PATH] [--scripts_path SCRIPTS_PATH] [--pyclmuapp_mode PYCLMUAPP_MODE]
#                 [--has_container HAS_CONTAINER] [--usr_domain USR_DOMAIN] [--usr_forcing USR_FORCING] [--usr_surfdata USR_SURFDATA]
#                 [--output_prefix OUTPUT_PREFIX] [--case_name CASE_NAME] [--run_startdate RUN_STARTDATE] [--stop_option STOP_OPTION]
#                 [--stop_n STOP_N] [--run_type RUN_TYPE] [--run_refcase RUN_REFCASE] [--run_refdate RUN_REFDATE] [--iflog IFLOG]
#                 [--logfile LOGFILE] [--hist_type HIST_TYPE] [--hist_nhtfrq HIST_NHTFRQ] [--hist_mfilt HIST_MFILT] [--clean CLEAN]
#                 [--surf_var SURF_VAR] [--surf_action SURF_ACTION] [--forcing_var FORCING_VAR] [--forcing_action FORCING_ACTION] [--script SCRIPT]
#                 [--urbsurf URBSURF] [--soildata SOILDATA] [--pct_urban PCT_URBAN] [--lat LAT] [--lon LON] [--outputname OUTPUTNAME] [--zbot ZBOT]
#                 [--start_year START_YEAR] [--end_year END_YEAR] [--start_month START_MONTH] [--end_month END_MONTH]
#
#pyclmuapp command line tool.
#
#options:
#  -h, --help            show this help message and exit
#  --version, -v         show program's version number and exit
#  --init INIT           Init pyclmuapp, default is False
#  --pwd PWD             Param for usp and script. Current working directory, default is pwd, can be none. If is not none, the the input_path,
#                        output_path, log_path, scripts_path will be used in pwd or be created. If none, the input_path, output_path, log_path,
#                        scripts_path should be provided.
#  --container_type CONTAINER_TYPE
#                        Param for usp and script. Container type, default is docker, can be singularity
#  --input_path INPUT_PATH
#                        Param for usp and script. CTSM input path, default is None. The path will be binded to "inputdata" in container
#  --output_path OUTPUT_PATH
#                        Param for usp and script. CTSM output path, default is None. The path will be binded to "Archive" in container
#  --log_path LOG_PATH   Param for usp and script. CTSM log path, default is None. The path will be binded to "CaseOutputs" in container
#  --scripts_path SCRIPTS_PATH
#                        Param for usp and script. CTSM scripts path, default is None. The path will be binded to "/p/scripts" in container
#  --pyclmuapp_mode PYCLMUAPP_MODE
#                        pyclmuapp mode, default is usp, can be script, pts, get_forcing, get_surfdata
#  --has_container HAS_CONTAINER
#                        Param for usp and script. Has container, default is True
#  --usr_domain USR_DOMAIN
#                        Param for usp. User domain file, default is None
#  --usr_forcing USR_FORCING
#                        Param for usp. User forcing file, default is None
#  --usr_surfdata USR_SURFDATA
#                        Param for usp. User surface data file, default is None
#  --output_prefix OUTPUT_PREFIX
#                        Param for usp. Output file name prefix, default is _clm.nc, is used to generate the output file of pyclmuapp
#  --case_name CASE_NAME
#                        Param for usp. Case name, default is usp_case
#  --run_startdate RUN_STARTDATE
#                        Param for usp. Start date, default is None
#  --stop_option STOP_OPTION
#                        Param for usp. Stop option, default is ndays, can be nyears, nmonths, ndays
#  --stop_n STOP_N       Param for usp. Stop number, default is 1
#  --run_type RUN_TYPE   Param for usp. Run type, default is coldstart, can be branch
#  --run_refcase RUN_REFCASE
#                        Param for usp. Reference case, default is None
#  --run_refdate RUN_REFDATE
#                        Param for usp. Reference date, default is None
#  --iflog IFLOG         Param for usp and script. If log, default is True
#  --logfile LOGFILE     Param for usp and script. Log file, default is pyclmuapp.log
#  --hist_type HIST_TYPE
#                        Param for usp. ouput type. Can be GRID, LAND, COLS, default is GRID
#  --hist_nhtfrq HIST_NHTFRQ
#                        Param for usp. History file frequency, default is 1 (ouput each time step)
#  --hist_mfilt HIST_MFILT
#                        Param for usp. each history file will include mfilt time steps, default is 1000000000
#  --clean CLEAN         Param for usp. Clean, default is False
#  --surf_var SURF_VAR   Param for usp. Surface variable, default is None. Can be one/some (use ','(withou space to seperate each)) of
#                        'CANYON_HWR', 'HT_ROOF','THICK_ROOF','THICK_WALL','WTLUNIT_ROOF','WTROAD_PERV','WIND_HGT_CANYON','NLEV_IMPROAD','TK_ROOF',
#                        'TK_WALL','TK_IMPROAD','CV_ROOF','CV_WALL','CV_IMPROAD','EM_IMPROAD','EM_PERROAD','EM_ROOF','EM_WALL','ALB_IMPROAD_DIR','A
#                        LB_IMPROAD_DIF','ALB_PERROAD_DIR','ALB_PERROAD_DIF','ALB_ROOF_DIR','ALB_ROOF_DIF','ALB_WALL_DIR','ALB_WALL_DIF','T_BUILDIN
#                        G_MIN'
#  --surf_action SURF_ACTION
#                        Param for usp. Surface action, default is None. The number is same as surf_var with "," seperated (not ", ")
#  --forcing_var FORCING_VAR
#                        'Param for usp. Forcing variable, default is None. Can be one/some (use ','(withou space to seperate each)) of
#                        'Prectmms','Wind','LWdown','PSurf','Qair','Tair','SWdown'
#  --forcing_action FORCING_ACTION
#                        Param for usp. Forcing action, default is None. The number is same as forcing_var with "," seperated (not ", ")
#  --script SCRIPT       Param for script. Script file in container, default is None
#  --urbsurf URBSURF     Param for get_surfdata. Urban surface data file, default is None. Here to download the urban surface data file:
#                        https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_urban_0.05x0.05_simyr2000.c120601.nc
#  --soildata SOILDATA   Param for get_surfdata. Soil data file, default is None. Here to download the soil data file: https://svn-ccsm-
#                        inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_soitex.10level.c010119.nc
#  --pct_urban PCT_URBAN
#                        Param for get_surfdata. Percentage of urban land use in each density class, sum should be 100, default is [0,0,100.0]
#  --lat LAT             Param for get_surfdata and get_forcing. Latitude of the urban area, default is None
#  --lon LON             Param for get_surfdata and get_forcing. Longitude of the urban area, default is None
#  --outputname OUTPUTNAME
#                        Param for get_surfdata. Output file name, default is surfdata.nc
#  --zbot ZBOT           Param for get_forcing. zbot, default is 30 meters
#  --start_year START_YEAR
#                        Param for get_forcing. Start year, default is 2012
#  --end_year END_YEAR   Param for get_forcing. End year, default is 2012
#  --start_month START_MONTH
#                        Param for get_forcing. Start month, default is 1
#  --end_month END_MONTH
#                        Param for get_forcing. End month, default is 12
#
#For any question, contact yjj1997@live.cn