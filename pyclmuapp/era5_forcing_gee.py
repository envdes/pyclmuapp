
try:
    import ee
except ImportError:
    raise ImportError("The 'ee' module is required. Please install the Earth Engine Python API with 'pip install earthengine-api'.")

import pandas as pd
import xarray as xr
import numpy as np
from typing import Union    
import datetime
import os
from datetime import date

def get_era5_ee(ee, lat, lon, start_YY_MM, end_YY_MM):
    
    """
    
    "The function `get_era5_ee` retrieves ERA5 weather data for a specific location and time range using Google Earth Engine."

    Args:
        ee (module): The Google Earth Engine module.
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
        start_YY_MM (str): The start date in 'YYYY-MM-DD' format.
        end_YY_MM (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        xarray.Dataset: The ERA5 weather data.
    """

    # =================  Get ERA5 variable data  =================
    variables = [
    'u_component_of_wind_10m', 
    'v_component_of_wind_10m', 
    'dewpoint_temperature_2m',
    'temperature_2m',
    'surface_pressure',
    'surface_solar_radiation_downwards',
    'surface_thermal_radiation_downwards',
    'total_precipitation',
    'forecast_surface_roughness'
    ]

    era5_var_dict = {
    'u_component_of_wind_10m': 'u10',
    'v_component_of_wind_10m': 'v10',
    'dewpoint_temperature_2m': 'd2m',
    'temperature_2m': 't2m',
    'surface_pressure': 'sp',
    'surface_solar_radiation_downwards': 'ssrd',
    'surface_thermal_radiation_downwards': 'strd',
    'total_precipitation': 'tp',
    'forecast_surface_roughness': 'fsr'
    }
    # ================= Get ERA5 variable data =================
    
    point = ee.Geometry.Point([lon, lat])
    
    dataset = (ee.ImageCollection('ECMWF/ERA5/HOURLY')
           .filter(ee.Filter.date(start_YY_MM, end_YY_MM))
           .select(variables))
    
    time_series = dataset.getRegion(point, 1000).getInfo()

    headers = time_series[0]
    data = time_series[1:]
    df = pd.DataFrame(data, columns=headers).rename(columns=era5_var_dict).drop(columns=['id'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df.set_index('time')
    df = df.sort_index()
    ds = df.to_xarray()
    return ds

def era5_to_forcing(
                    single: Union[str, xr.Dataset], 
                    zbot: int = 30,
                    lapse_rate: int = 0.006
                    ):
    
    """
    "The function `era5_to_forcing` takes in two xarray Datasets `pres` and `single`, latitude `lat`, longitude `lon`, 
    and an optional `pressure` parameter with a default value of 950."
    
    Args:
        single (xarray.Dataset, str): The single level data.
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
        zbot (int, float): The bottom level of the forcing data.
        outputfile (str): The path to save the forcing data.
        lapse_rate (int, float): The lapse rate of the forcing data. default is 0.006, from Pritchard et al. (GRL, 35, 2008) of CTSM 

    Returns:
        xarray.Dataset: The forcing data.
    """

    
    #-------------------Constants-------------------
    SHR_CONST_BOLTZ   = 1.38065e-23  # Boltzmann's constant ~ J/K/molecule
    SHR_CONST_AVOGAD  = 6.02214e26   # Avogadro's number ~ molecules/kmole
    SHR_CONST_RGAS    = SHR_CONST_AVOGAD*SHR_CONST_BOLTZ       # Universal gas constant ~ J/K/kmole
    SHR_CONST_MWDAIR  = 28.966       # molecular weight dry air ~ kg/kmole
    SHR_CONST_MWWV    = 18.016       # molecular weight water vapor
    SHR_CONST_RDAIR   = SHR_CONST_RGAS/SHR_CONST_MWDAIR        # Dry air gas constant     ~ J/K/kg
    SHR_CONST_G       = 9.80616      # acceleration of gravity ~ m/s^2

    rair              = SHR_CONST_RDAIR
    grav              = SHR_CONST_G
    # Pritchard et al. (GRL, 35, 2008) use 0.006
    #lapse_rate = 0.006 # https://github.com/ESCOMP/CTSM/blob/a9433779f0ae499d60ad118d2ec331628f0eaaa8/bld/namelist_files/namelist_defaults_ctsm.xml#L197
    
    
    # costants for saturation vapor pressure for Qair
    a0 =  6.11213476
    a1 =  0.444007856
    a2 =  0.143064234e-01
    a3 =  0.264461437e-03
    a4 =  0.305903558e-05
    a5 =  0.196237241e-07
    a6 =  0.892344772e-10
    a7 = -0.373208410e-12
    a8 =  0.209339997e-15

    c0 =  6.11123516
    c1 =  0.503109514
    c2 =  0.188369801e-01
    c3 =  0.420547422e-03
    c4 =  0.614396778e-05
    c5 =  0.602780717e-07
    c6 =  0.387940929e-09
    c7 =  0.149436277e-11
    c8 =  0.262655803e-14
    # -------------------Constants-------------------
    
    #tbot_c = tbot_g-lapse_rate*(hsurf_c-hsurf_g)
    #Hbot  = rair*0.5*(tbot_g+tbot_c)/grav
    #pbot_c = pbot_g*np.exp(-(hsurf_c-hsurf_g)/Hbot)
    
    single['Tair'] = single['t2m']/1.0
    single['Tair'] = single['Tair'] - lapse_rate * (zbot - 2.0)
    single['Tair'].attrs['units'] = 'K'
    single['Tair'].attrs['long_name'] = 'Air temperature'
    
    Hbot = rair * single['Tair'] / grav
    single['PSurf'] = single['sp']/1.0
    single['PSurf'] = single['PSurf'] * np.exp(-(zbot - 2.0) / Hbot)
    single['PSurf'].attrs['units'] = 'Pa'
    single['PSurf'].attrs['long_name'] = 'Surface pressure at 950 hPa'

    single['Wind'] = (single['u10']**2 + single['v10']**2)**0.5
    # ref: https://doi.org/10.5194/essd-14-5157-2022
    single['Wind'] = single['Wind'] * (np.log(zbot / single['fsr']) / np.log(10 / single['fsr']))
    #single['Wind'] = single['Wind'] * (xr.ufuncs.log(2 / single['fsr']) / xr.ufuncs.log(10 / single['fsr']))
    single['Wind'] = single['Wind'].assign_attrs(units='m/s')
    single['Wind'] = single['Wind'].assign_attrs(long_name='Wind speed')

    # ref1: https://github.com/ESCOMP/CTSM/blob/75b34d2d8770461e3e28cee973a39f1737de091d/doc/source/tech_note/Land-Only_Mode/CLM50_Tech_Note_Land-Only_Mode.rst#L113
    # ref2: https://journals.ametsoc.org/view/journals/apme/57/6/jamc-d-17-0334.1.xml
    # ref3: https://github.com/ESCOMP/CTSM/blob/75b34d2d8770461e3e28cee973a39f1737de091d/src/biogeophys/QSatMod.F90
    # Reference:  Polynomial approximations from:
    #             Piotr J. Flatau, et al.,1992:  Polynomial fits to saturation
    #             vapor pressure.  Journal of Applied Meteorology, 31, 1507-1513.
    lapse_rate_dew = 1.8/1000 # ref: https://commons.erau.edu/cgi/viewcontent.cgi?article=1374&context=ijaaa
    # DPLR of moist air at temperature of 20oC (293 K) and dew point of 12oC(285 K) has RH of approximately 60%. 
    # DP-depression D is 8oC (8 K). Using Eq. (38), whileneglecting specific humidity contribution, 
    # DPLR yields about 0.546 K/1,000 ft (1.8 K/km). Thisis valid result as measured DPLRs are normally in the range 1.6-2.0 K/km or 0.50 to 0.6 K/1,000ft.
    # for simple, we use lapse_rate_dew = 1.8/1000, which is the middle of the range.
    # also: Pilot’s Handbook of Aeronautical Knowledge : "When lifted, ... the dew point temperature decreases at a rate of 1 °F per 1,000 feet."
    # ~ 0.555556 K/1000 ft or 1.8 K/km.
    # ref: https://www.faa.gov/sites/faa.gov/files/14_phak_ch12.pdf
    # pdf is in src/CLMU_literatures/14_phak_ch12.pdf
    single['d2m'] = single['d2m'] - 273.15 - lapse_rate_dew * (zbot - 2.0)
    # es_water
    single['es_water'] = a0 + single['d2m']*(a1 + single['d2m']*(a2 + single['d2m']*(a3 + single['d2m']*(a4 
            + single['d2m']*(a5 + single['d2m']*(a6 + single['d2m']*(a7 + single['d2m']*a8)))))))
    single['es_water'] = single['es_water'] * 100
    # es_ice
    single['es_ice'] = c0 + single['d2m']*(c1 + single['d2m']*(c2 + single['d2m']*(c3 + single['d2m']*(c4 
            + single['d2m']*(c5 + single['d2m']*(c6 + single['d2m']*(c7 + single['d2m']*c8)))))))
    single['es_ice'] = single['es_ice'] * 100   
    # es 
    single['es'] = xr.where(single['d2m'] >= 0, single['es_water'],single['es_ice'])
    # Qair
    single['Qair'] = 0.622 * single['es'] / (single['PSurf'] - (1 - 0.622) * single['es'])
    single['Qair'] = single['Qair'].where(single['Qair'] > 0, 1e-16)
    single['Qair'].attrs['units'] = 'kg/kg'
    single['Qair'].attrs['long_name'] = 'Specific humidity'
    
    single['Zbot'] = single['sp'] /1.0
    single['Zbot'].values = np.ones(single['Zbot'].shape) * zbot
    single['Zbot'].attrs['units'] = 'm'
    single['Zbot'].attrs['long_name'] = 'Geopotential height'
    
    single['SWdown'] = single['ssrd']/ 3600 
    single['SWdown'] = single['SWdown'].where(single['SWdown'] > 0, 1e-16)
    single['SWdown'].attrs['units'] = 'W/m^2'
    single['SWdown'].attrs['long_name'] = 'Surface solar radiation downwards'
    single['LWdown'] = single['strd']/ 3600 
    single['LWdown'] = single['LWdown'].where(single['LWdown'] > 0, 1e-16)
    single['LWdown'].attrs['units'] = 'W/m^2'
    single['LWdown'].attrs['long_name'] = 'Surface thermal radiation downwards'
    
    single['Prectmms'] = single['tp'] * 1000 / 3600
    single['Prectmms'] = single['Prectmms'].where(single['Prectmms'] > 0, 1e-16)
    single['Prectmms'].attrs['units'] = 'mm/s'
    single['Prectmms'].attrs['long_name'] = 'Total precipitation'
    for var in ['PSurf', 'Qair', 'Wind', 'Tair', 'Zbot', 'SWdown', 'LWdown', 'Prectmms']:
        single[var] = single[var].assign_attrs(_FillValue=1.e36)
    single['x'] = 1
    single['y'] = 1
    single = single.assign_coords(x=1,y=1)
    for var in single.data_vars:
        single[var] = single[var].expand_dims('x',axis=1).expand_dims('y',axis=1)
        
    del single['latitude'], single['longitude'], single['d2m'], \
        single['sp'], single['ssrd'], single['strd'], single['tp'], \
        single['u10'], single['v10'], single['fsr'], \
        single['t2m'], single['es_water'], single['es_ice'], single['es']
    
    #single.to_netcdf(outputfile)
    return single


def month_chunks(start_date: str, end_date: str):
    y, m, d = map(int, start_date.split('-'))
    Y, M, D = map(int, end_date.split('-'))
    cur = date(y, m, 1)
    end = date(Y, M, 1)

    chunks = []
    while cur <= end:
        if cur.month == 12:
            nxt = date(cur.year + 1, 1, 1)
        else:
            nxt = date(cur.year, cur.month + 1, 1)
        s = cur.isoformat()
        e = min(nxt, date(Y, M, D)).isoformat() if cur.year == Y and cur.month == M else nxt.isoformat()
        chunks.append((s, e))
        cur = nxt
    return chunks

def gee_era5s_to_forcing(ee, lat, lon, start_date, end_date, zbot=30, outputfile='./forcing.nc'):

    print(f'Get ERA5 data from {start_date} to {end_date} for ({lat}, {lon})')

    chunks = month_chunks(start_date, end_date)
    
    datasets = []
    for s, e in chunks:
        print(f'  - {s} ~ {e}')
        ds = get_era5_ee(ee, lat, lon, s, e)
        datasets.append(ds)
    ds_all = xr.concat(datasets, dim='time')
    ds_all = ds_all.sortby('time')
    ds_forcing = era5_to_forcing(ds_all, zbot=zbot)
    if os.path.exists(outputfile):
        os.remove(outputfile)
    ds_forcing.to_netcdf(outputfile)
    return ds_forcing

if __name__ == '__main__':
    ee.Authenticate()   # 弹出授权
    ee.Initialize()
    lat, lon = 39.9, 116.4
    start_date = '2018-01-15'
    end_date = '2020-03-20'
    zbot = 30
    outputfile = './forcing_gee.nc'
    ds_forcing = gee_era5s_to_forcing(ee, lat, lon, start_date, end_date, zbot=zbot, outputfile=outputfile)
    print(ds_forcing)