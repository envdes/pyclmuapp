# encoding: utf-8
# Author: Junjie Yu, 2024-5-18
# Description: interface for CLMU-App

# pyclmuapp/infer.py

from pyclmuapp import usp_clmu, get_forcing
from pyclmuapp._cli import _main_usp, get_pypars, check_file, _main_create_surfdata
from fake_forcing.fake_forcing import get_fake_forcing_ncs, dist, future_scenario, forcing_vars
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gradio as gr
import pandas as pd
import xarray as xr
import os



def dict_to_args(args_dict):
    args = []
    for key, value in args_dict.items():
        key_arg = f"--{key}"
        args.extend((key_arg, str(value)))
    return args

def plotting(ds, fig, label):
    
    label_dict = {
        "original": 'O',
        "modify_forcing": 'MF',
        "modify_surf": 'MS',
        "modify_surf_forcing": 'MFS'
    }
    
    #ds = ds.isel(lndgrid=0)
    
    dim = ds['TSA'].dims[-1]
    
    if dim == 'gridcell':
        ds = ds.isel({dim:0})
    elif dim == 'column':
        for col in ds[dim]:
            if ds['cols1d_itype_col'].sel({dim:col}).values == 71:
                print(col)
                break
        ds = ds.isel({dim:col})
    elif dim == 'landunit':
        for lu in ds[dim]:
            if ds['land1d_ityplunit'].sel({dim:lu}).values == 9:
                print(lu)
                break
        ds = ds.isel({dim:lu})
    else:
        print("No such dimension")
    
    fig.add_trace(
        go.Scatter(x=ds['time'],
                   y=ds['TSA'], 
                   mode='lines', 
                   name=label_dict[label]),
        row=1, col=1)
    fig.update_xaxes(title_text="Time", row=1, col=1)
    fig.update_yaxes(title_text=ds['TSA'].attrs['long_name'], row=1, col=1)

    
    ds_usp_hour = ds['TSA'].groupby('time.hour')
    mean = ds_usp_hour.mean('time')
    var = ds_usp_hour.var('time')
    
    fig.add_trace(
        go.Scatter(x=mean['hour'],
                   y=mean, 
                   mode='lines', 
                   name=label_dict[label]+'-mean'),
        row=2, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text=ds['TSA'].attrs['long_name'], row=2, col=1)
    
    return fig

def plot_forcing(ds):
    ds = ds.isel(x=0, y=0)
    fig = make_subplots(rows=8, cols=1)
    forcing_vars = ['SWdown', 'LWdown', 'Qair', 'Tair', 'Wind', 'Prectmms', 'PSurf', 'Zbot']
    unit = ['W/m2', 'W/m2', 'kg/kg', 'K', 'm/s', 'mm/s', 'Pa', 'm']
    for i, var in enumerate(forcing_vars, start=1):
        fig.add_trace(
            go.Scatter(x=ds['time'],
                       y=ds[var], 
                       mode='lines'),
                       #name=var,
            row=i, col=1)
        fig.update_yaxes(title_text=var+' ('+unit[i-1]+')', row=i, col=1)
    
    fig.update_layout(height=1200, width=800, title_text="Forcing variables")
    return fig


def _gr_main_usp(
                 case_name,
                 usr_surfdata,
                 usr_forcing,
                 run_startdate,
                 stop_option,
                 stop_n,
                 surf_var,
                 surf_action,
                 forcing_var,
                 forcing_action,
                 urban_hac,
                 run_type,
                 run_refcase,
                 run_refdate,
                 run_reftod,
                 #var_add,
                 hist_type,
                 hist_nhtfrq,
                 hist_mfilt,
                 logfile,
                 clean
                 ):
    
    print(surf_var, surf_action)

    surf_var = ','.join(surf_var)
    forcing_var = ','.join(forcing_var)
    print(surf_var)

    if usr_surfdata is None:
        raise ValueError("Please upload the urban surface data file")
    
    if usr_forcing is None:
        raise ValueError("Please upload the forcing data file")

    gr_l = {
        "usr_surfdata": usr_surfdata.name,
        "usr_forcing": usr_forcing.name,
        "case_name": case_name,
        "run_startdate": run_startdate,
        "stop_option": stop_option,
        "stop_n": stop_n,
        "surf_var": surf_var,
        "surf_action": surf_action,
        "forcing_var": forcing_var,
        "forcing_action": forcing_action,
        "urban_hac": urban_hac,
        "run_type": run_type,
        "run_refcase": run_refcase,
        "run_refdate": run_refdate,
        "run_reftod": run_reftod,
        #"var_add": var_add,
        "hist_type": hist_type,
        "hist_nhtfrq": hist_nhtfrq,
        "hist_mfilt": hist_mfilt,
        "logfile": logfile,
        "clean": str(clean),
        "pyclmuapp_mode": "usp",

    }


    gr_l = dict_to_args(gr_l)

    gr_l = get_pypars(gr_l=gr_l)

    usp = usp_clmu(
            pwd=None,
            input_path="/p/clmuapp",
            output_path="/p/scratch/CESMDATAROOT/Archive",
            log_path="/p/scratch/CESMDATAROOT/CaseOutputs",
            scripts_path = "/p/scripts",
            container_type='docker_in')

    print(gr_l)
    ouptut = _main_usp(gr_l, usp)

    #fig, axs = plt.subplots(2, 1, figsize=(8, 6))
    
    fig = make_subplots(rows=2, cols=1)

    for label, ds_name in ouptut.items():
        ds = usp.nc_view(ds_name[0])
        fig = plotting(ds, fig, label)

    
    ouptutfiles = []
    for key, value in ouptut.items():
        ouptutfiles.extend(iter(value))
    #ouptut = gr_l
    
    if clean:
        usp.clean_usp()
        usp.case_clean(case_name=case_name)
    
    return ouptut, ouptutfiles, fig
    
def _gr_main_create_forcing(
    start_year, end_year, start_month, end_month, lat, lon, zbot, source,
    cdsid, cdsapikey):
    
    if source == 'cds':
        command = """cat <<EOF > ~/.cdsapirc
        url: {url}
        key: {uid}:{apikey}
        EOF""".format(url='https://cds.climate.copernicus.eu/api/v2',
                        uid=cdsid,
                        apikey=cdsapikey)
        
        os.system(command)
    
    
    outputname=get_forcing(
        start_year=int(start_year),
        end_year=int(end_year),
        start_month=int(start_month),
        end_month=int(end_month),
        lat=float(lat),
        lon=float(lon),
        zbot=float(zbot),
        source=source,
    )
    
    ds = xr.open_dataset(outputname)
    
    fig = plot_forcing(ds)
    
    return outputname, fig
    
def _gr_main_create_surfdata(
                    lat,
                    lon,
                    pct_urban,
                    outputname):

    # https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_soitex.10level.c010119.nc
    soildata = os.path.join('/p/scratch/CESMDATAROOT/inputdata', 'mksrf_soitex.10level.c010119.nc')
    if not os.path.exists(soildata):
        os.system(f'wget --no-check-certificate -O {soildata} https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_soitex.10level.c010119.nc')
    
    urbsurf = os.path.join('/p/scratch/CESMDATAROOT/inputdata', 'mksrf_urban_0.05x0.05_simyr2000.c170724.nc')
    
    # https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_urban_0.05x0.05_simyr2000.c170724.nc
    if not os.path.exists(urbsurf):
        os.system(f'wget --no-check-certificate -O {urbsurf} https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/mksrf_urban_0.05x0.05_simyr2000.c170724.nc')
        
    gr_l = {
            "urbsurf": urbsurf,
            "soildata": soildata,
            "lat": lat,
            "lon": lon,
            "pct_urban": pct_urban,
            "outputname": outputname,
        }
    gr_l = dict_to_args(gr_l)
    
    gr_l = get_pypars(gr_l=gr_l)
        
    return _main_create_surfdata(gr_l)
        
    
# defing the interface

sur_vars = ['CANYON_HWR', 'HT_ROOF','THICK_ROOF','THICK_WALL','WTLUNIT_ROOF',
'WTROAD_PERV','WIND_HGT_CANYON','NLEV_IMPROAD',
'TK_ROOF','TK_WALL','TK_IMPROAD','CV_ROOF','CV_WALL','CV_IMPROAD',
'EM_IMPROAD','EM_PERROAD','EM_ROOF','EM_WALL',
'ALB_IMPROAD_DIR','ALB_IMPROAD_DIF','ALB_PERROAD_DIR','ALB_PERROAD_DIF',
'ALB_ROOF_DIR','ALB_ROOF_DIF','ALB_WALL_DIR','ALB_WALL_DIF','T_BUILDING_MIN']

forcing_vars = [
"Prectmms","Wind","LWdown","PSurf","Qair","Tair","SWdown"
]

interface_usp = gr.Interface(fn=_gr_main_usp,
                            inputs=[
                         gr.Textbox(label="Case name", value="pyclmuapp"),
                         gr.File(label="Urban surface data"),
                         gr.File(label="CLM forcing data"),
                         gr.Textbox(label="Run start date", value="2012-08-08"),
                         gr.Radio(label="Stop option", choices=["ndays", "nmonths", "nyears"], value="ndays"),
                         gr.Number(label="Stop_n (case lenth = Stop option * Stop_n)", value=1),
                            ],
                        outputs=[gr.Textbox(label="Output files"),
                                 gr.Files(label="Output files"),
                                 gr.Plot(label="Urban air temperature")
                                 ],
                        additional_inputs = [
                            gr.CheckboxGroup(choices=sur_vars, label="surf_var: the urban variables to modify", value=None),
                            gr.Textbox(label="surf_action (the number is same as surf_var with ',' seperated (not ', '))", value=0),
                            gr.CheckboxGroup(choices=forcing_vars, label="forcing_var: the forcing variables to modify", value=None),
                            gr.Textbox(label="forcing_action (the number is same as forcing_var with ',' seperated (not ', '))", value=0),
                            gr.Textbox(label="urban_hac", value="ON"),
                            gr.Textbox(label="run_type", value="coldstart"),
                            gr.Textbox(label="run_refcase", value="None"),
                            gr.Textbox(label="run_refdate", value="None"),
                            gr.Textbox(label="run_reftod", value="None"),
                            #gr.Textbox(label="var_add", value="TSA_U"),
                            gr.Textbox(label="hist_type", value="GRID"),
                            gr.Textbox(label="hist_nhtfrq", value="1"),
                            gr.Textbox(label="hist_mfilt", value="1000000000"),
                            gr.Textbox(label="logfile", value="pyclmuapp.log"),
                            gr.Checkbox(label="case clean (if clean the file after simulations)", value=False),
                        ],
                        theme='Soft'
                        )

interface_create_forcing = gr.Interface(fn=_gr_main_create_forcing,
                            inputs=[
                            gr.Textbox(label="Start year", value="2012"),
                            gr.Textbox(label="End year", value="2012"),
                            gr.Textbox(label="Start month", value="01"),
                            gr.Textbox(label="End month", value="12"),
                            gr.Textbox(label="Latitude", value="53.4808"),
                            gr.Textbox(label="Longitude", value="-2.2426"),
                            gr.Textbox(label="Zbot (m)", value="30"),
                            gr.Radio(label="Source", choices=["cds", "arco-era5"], value="cds"),
                            gr.Textbox(label="CDS API UID", value=""),
                            gr.Textbox(label="CDS API key", value=""),
                            ],
                            outputs=[gr.File(label="Output file"),
                                    gr.Plot(label="Forcing variables")
                                        ],
                            theme='Soft'
                            )

interface_create_surfdata = gr.Interface(fn=_gr_main_create_surfdata,
                            inputs=[
                            gr.Textbox(label="Latitude", value="53.4808"),
                            gr.Textbox(label="Longitude", value="-2.2426"),
                            gr.Textbox(label="Percentage of urban land use in each density class, sum should be 100, default is [0,0,100.0]", value="0,0,100.0"),
                            gr.Textbox(label="Output name", value="surfdata.nc"),
                                ],
                            outputs=[gr.File(label="Output file")],
                            theme='Soft'
                            )
    
# get_fake_forcing_ncs(dist, '2012-01-01', 'nyears', 1, ouput_nc='data/forcing.nc')['Qair'].plot(label='fake')
def get_fake(_dist, start_date, stop_option, stop_n, Zbot, ouput_nc):
    
    if _dist is None:
        _dist = dist
    else:
        _dist = pd.read_csv(_dist.name)
    ds = get_fake_forcing_ncs(_dist, start_date, stop_option, stop_n, Zbot, ouput_nc)
    
    fig = plot_forcing(ds)
    
    return os.path.abspath(ouput_nc), fig

def clean_files(usp, case_name, era5_files,cache_files):
    
    if usp is not None:
        os.system(f"rm -rf /p/scratch/CESMDATAROOT/inputdata/usp")

    if case_name is not None:
        case_name = case_name.split(";")
        for case in case_name:
            os.system(f"rm -rf /p/scratch/CESMDATAROOT/CaseOutputs/{case}")
            os.system(f"rm -rf /p/scripts/{case}")
            
    if era5_files is not None:
        os.system(f"rm -rf era5_data")
    
    if cache_files is not None:
        os.system(f"rm -rf cache")
        os.system(f"rm -rf /p/scratch/CESMDATAROOT/Archive/logs/*")
        os.system(f"rm -rf /p/scratch/CESMDATAROOT/Archive/rest/*")
        os.system(f"rm -rf /p/scratch/CESMDATAROOT/Archive/lnd/hist/*")
        
    return "Files cleaned"

interface_fake_forcing = gr.Interface(fn=get_fake,
                            inputs=[
                            gr.File(label="Distribution file", value=None),
                            gr.Textbox(label="Start date", value="2012-01-01"),
                            gr.Radio(label="Stop option", choices=["ndays", "nmonths", "nyears"], value="ndays"),
                            gr.Number(label="Stop_n (case lenth = Stop option * Stop_n)", value=1),
                            gr.Number(label="Zbot/meters, observational height", value=30),
                            gr.Textbox(label="Output name", value="forcing.nc"),
                                ],
                            outputs=[gr.File(label="Output file"),
                                    gr.Plot(label="Forcing variables")
                                        ],
                            theme='Soft'
                            )   

interface_clean_files = gr.Interface(fn=clean_files,
                            inputs=[
                            gr.Checkbox(label="Clean USP files", value=False),
                            gr.Textbox(label="Case name. If case more than 2, use ; (without space) to split them", value=""),
                            gr.Checkbox(label="Clean era5 files", value=False),
                            gr.Checkbox(label="Clean cache files", value=False),
                                ],
                            outputs=[gr.Textbox(label="Output message")],
                            theme='Soft'
                            )

tabbed_interface = gr.TabbedInterface([interface_usp, interface_create_forcing, 
                                       interface_create_surfdata, interface_fake_forcing,
                                       interface_clean_files],
                                      ["USP", "Create forcing from ERA5", 
                                       "Create surfdata", "Create fake forcing",
                                       "Clean files"])

def main():
    tabbed_interface.launch(server_name="0.0.0.0")
    
    
if __name__ == "__main__":
    main()
