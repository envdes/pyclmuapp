
# Junjie Yu, 2024-02-06, Mancheser UK
#------------------------------------------------------------------------------
# This script is used to run CESM2 via python

import os
import xarray as xr
import numpy as np
from typing import Union, List, Dict
import time
import gc

def get_urban_params(urban_ds: Union[xr.Dataset, str],
                     soil_ds: Union[xr.Dataset, str],
                     lat: float, 
                     lon: float,
                     template: Union[xr.Dataset, str] = os.path.join(os.path.dirname(__file__), "usp", "surfdata.nc"),
                     PTC_URBAN: list = [0,0,100],
                     outputname: str = "surfdata.nc"
                     ) -> xr.Dataset:
    
    """
    Get the urban parameters.
    
    Args:
        urban_ds (xr.Dataset or str): the urban dataset
        soil_ds (xr.Dataset or str): the soil dataset
        template (xr.Dataset or str, optional): the template dataset
        lat (float): latitude of interest point
        lon (float): longitude of interest point
        PTC_URBAN (list, optional): The percentage of urban. Defaults to [0,0,100].
            0. TBD urban, 1. HD urban, 2. MD urban
        outputname (str, optional): the output file name. Defaults to "surfdata.nc".
        
    Returns:
        xr.Dataset: the modified template dataset
    """
    
    if lon > 180:
        lon = lon - 360
    
    if isinstance(urban_ds, str):
        urban_ds = xr.open_dataset(urban_ds)
    if isinstance(template, str):
        template = xr.open_dataset(template)

    urban = urban_ds.assign_coords(lat=urban_ds.LAT, lon=urban_ds.LON).sel(lat=lat, lon=lon, method='nearest')
    urban =  urban.sel(region=(urban.REGION_ID.values-1)) # to make region_id start from 0
    urban['ALB_ROOF_DIF'] = urban['ALB_ROOF'].sel(numsolar=0)
    urban['ALB_ROOF_DIR'] = urban['ALB_ROOF'].sel(numsolar=1)
    urban['ALB_WALL_DIF'] = urban['ALB_WALL'].sel(numsolar=0)
    urban['ALB_WALL_DIR'] = urban['ALB_WALL'].sel(numsolar=1)
    urban['ALB_IMPROAD_DIF'] = urban['ALB_IMPROAD'].sel(numsolar=0)
    urban['ALB_IMPROAD_DIR'] = urban['ALB_IMPROAD'].sel(numsolar=1)
    urban['ALB_PERROAD_DIF'] = urban['ALB_PERROAD'].sel(numsolar=0)
    urban['ALB_PERROAD_DIR'] = urban['ALB_PERROAD'].sel(numsolar=1)
    
    # Set the urban parameters
    for v1 in urban.variables:
        for v2 in template.variables:
            if v1 == v2:
                #print(f"Setting {v1} to {v2}")
                #print(template[v2].loc[dict(lsmlat=float(template['lsmlat'].values), lsmlon=float(template['lsmlon'].values))].shape)
                #print(urban[v1].shape)
                try:
                    lsmlat = float(template['lsmlat'].values)
                    lsmlon = float(template['lsmlon'].values)
                except: 
                    lsmlat = template['lsmlat'].values.item()
                    lsmlon = template['lsmlon'].values.item()
                
                template[v2].loc[dict(lsmlat=lsmlat, lsmlon=lsmlon)] = urban[v1].values
                if v2 == 'LONGXY':
                    if template[v2].loc[dict(lsmlat=lsmlat, lsmlon=lsmlon)] < 0:
                        template[v2].loc[dict(lsmlat=lsmlat, lsmlon=lsmlon)] = template[v2].loc[dict(lsmlat=lsmlat, lsmlon=lsmlon)].values + 360
                template[v2] = template[v2].fillna(0)
    template['URBAN_REGION_ID'].loc[dict(lsmlat=lsmlat, lsmlon=lsmlon)] = urban['REGION_ID'].values
    template['PCT_URBAN'].values[:, 0, 0] = np.array(PTC_URBAN)
    
    sand, clay = get_soil_params(soil_ds, lat, lon)
    
    template['PCT_SAND'].values[:, 0, 0] = sand
    template['PCT_CLAY'].values[:, 0, 0] = clay
    
    template.to_netcdf(outputname)
                
    return  template


def get_soil_params(ds: Union [xr.Dataset, xr.DataArray, str],
                    lat: float = 51.508965,
                    lon: float = -0.118092) -> tuple:
    
    """
    Get the soil parameters.
    
    Args:
        ds (xr.Dataset or xr.DataArray or str): the soil dataset
        lat (float): latitude of interest point
        lon (float): longitude of interest point
    
    Returns:
        tuple: sand and clay content from the soil dataset
    """
    
    if isinstance(ds, str):
        ds = xr.open_dataset(ds)
    
    ds = ds.assign_coords(lat=ds.LAT, lon=ds.LON)

    lat_soil = lat
    lon_soil = lon

    search_range = 180/21600  # 0.008333333333333333

    while True:
        found_point = False  # flag to indicate if a suitable point is found
        for lat_offset in [0, 1 , -1]:
            for lon_offset in [0, 1, -1]:
                # calculate new latitude and longitude
                new_lat = lat_soil + lat_offset * search_range
                new_lon = lon_soil + lon_offset * search_range
                
                # select the nearest point
                dd = ds.sel(lat=new_lat, lon=new_lon, method='nearest')
                sand = dd['PCT_SAND'].sel(max_value_mapunit=int(dd['MAPUNITS'].values)).values
                clay = dd['PCT_CLAY'].sel(max_value_mapunit=int(dd['MAPUNITS'].values)).values
                
                # check if the point is suitable
                if not (np.all(sand == 0) or np.all(clay == 0)):
                    found_point = True
                    lat_soil = new_lat
                    lon_soil = new_lon
                    break  #  break the inner loop
            # break the outer loop
            if found_point:
                print(f'Found suitable point at lat: {lat_soil}, lon: {lon_soil}')
                break  # break the outer loop
        # break the while loop
        if found_point:
            print(f'Found suitable point at lat: {lat_soil}, lon: {lon_soil}')
            break  # break the while loop
        else:
            print('No suitable point found in the search range, expanding search range.')
            search_range += 180/21600  # expand the search range by 0.008333333333333333

    return sand, clay


def get_forcing(start_year :int, 
                end_year: int, 
                start_month: int, end_month: int,
                lat: float, lon: float, zbot: float,
                source: str = 'cds'
                ):
    
    """
    get the forcing data from the era5 dataset
    
    Args:
        start_year (int): the start year
        end_year (int): the end year
        start_month (int): the start month
        end_month (int): the end month
        lat (float): latitude of interest point
        lon (float): longitude of interest point
        zbot (float): the bottom level height
        source (str): the source of the data, can be "cds", "arco-era5", "era5-land-ts", "gee"
            "cds": download data from the Copernicus Climate Data Store (CDS) using the CDS API
            "arco-era5": download data from the ARCO ERA5 dataset
            "era5-land-ts": download data from the ERA5-Land Time Series dataset
            "gee": download data from the Google Earth Engine (GEE) using the GEE API
    Returns:
        xr.Dataset: the forcing dataset
    """
    
    if source == "cds":
        from pyclmuapp.era5_forcing import era5_to_forcing, era5_download
        import xarray as xr
        era5_list = []
        # from 2002 to 2014
        years = range(start_year, end_year+1)
        # download data from January to December
        months = range(start_month, end_month+1)
        if not os.path.exists('./era5_data'):
            os.makedirs('./era5_data', exist_ok=True)
            os.makedirs('./era5_data/era5_single', exist_ok=True)
        outputfile='era5_data/era5_forcing_{lat}_{lon}_{zbot}_{year}_{month}.nc'
        for year in years:
            
            if start_year == end_year:
                months = range(start_month, end_month+1)
            elif year == end_year:
                months = range(1, end_month+1)
            elif year == start_year:
                months = range(start_month, 13)
            else:
                months = range(1, 13)
                
            for month in months:
                single = era5_download(year=year, month=month,
                                            lat=lat, lon=lon, outputfolder='./era5_data/era5_single')
                # Convert ERA5 data to CLM forcing
                forcing = era5_to_forcing(single=single, 
                                        lat=lat, lon=lon, zbot=zbot,)
                era5_list.append(forcing)
                
            #for month in months:
            #    single = era5_download(year=year, month=month,
            #                                lat=lat, lon=lon, outputfolder='./era5_data')
            #    # Convert ERA5 data to CLM forcing
            #    forcing = era5_to_forcing(single=single, 
            #                            lat=lat, lon=lon, zbot=zbot,
            #                            outputfile=outputfile.format(lat=lat, lon=lon, 
            #                                                        zbot=zbot, year=year, 
            #                                                        month=str(month).zfill(2)))
            #    ds = xr.open_dataset(outputfile.format(lat=lat, lon=lon, 
            #                                        zbot=zbot, year=year, 
            #                                        month=str(month).zfill(2)))
            #    era5_list.append(ds)
        era5 = xr.concat(era5_list, dim='time').sortby('time')
        outfile = f'era5_data/era5_forcing_{lat}_{lon}_{zbot}_{start_year}_{start_month}_{end_year}_{end_month}.nc'
        if os.path.exists(outfile):
            os.remove(outfile)
        era5.to_netcdf(outfile)
        result = os.path.join(os.getcwd(), outfile)

    elif source == "arco-era5":
        if not os.path.exists('./era5_data'):
            os.makedirs('./era5_data', exist_ok=True)
        outfile = f'era5_data/arco_era5_forcing_{lat}_{lon}_{zbot}_{start_year}_{start_month}_{end_year}_{end_month}.nc'
        from pyclmuapp.era5_forcing import arco_era5_to_forcing
        if os.path.exists(outfile):
            print(f"The forcing file {outfile} already exists.")
        else:
            arco_era5_to_forcing(lat=lat, lon=lon, zbot=zbot, 
                                start_year=start_year, end_year=end_year, 
                                start_month=start_month, end_month=end_month, outputfile=outfile)
        result = os.path.join(os.getcwd(), outfile)
        
    elif source == "era5-land-ts":
        from pyclmuapp.era_forcing import workflow_era5s_to_forcing
        if not os.path.exists('./era5_data'):
            os.makedirs('./era5_data', exist_ok=True)
        outfile = f'era5_data/era5_land_ts_forcing_{lat}_{lon}_{zbot}_{start_year}_{start_month}_{end_year}_{end_month}.nc'
        if os.path.exists(outfile):
            print(f"The forcing file {outfile} already exists.")
        else:
            start_date = f"{start_year}-{str(start_month).zfill(2)}-01"
            if end_month == 12:
                end_date = f"{end_year+1}-01-01"
            else:
                end_date = f"{end_year}-{str(end_month+1).zfill(2)}-01"
            outputfile = f'era5_data/era5_land_ts_forcing_{lat}_{lon}_{zbot}_{start_year}_{start_month}_{end_year}_{end_month}.nc'
            workflow_era5s_to_forcing(lat, lon, start_date, end_date, zbot=zbot, outputfile=outputfile)
        result = os.path.join(os.getcwd(), outfile)
        
    elif source == "gee":
        from pyclmuapp.era5_forcing_gee import gee_era5s_to_forcing
        try:
            import ee
        except ImportError:
            raise ImportError("The 'ee' module is required. Please install the Earth Engine Python API with 'pip install earthengine-api'.")

        ee.Authenticate()   # 弹出授权
        ee.Initialize()

        start_date = f'{start_year}-{str(start_month).zfill(2)}-01'
        if end_month == 12:
            end_date = f'{end_year+1}-01-01'
        else:
            end_date = f'{end_year}-{str(end_month+1).zfill(2)}-01'
        if not os.path.exists('./era5_data'):
            os.makedirs('./era5_data', exist_ok=True)
        outputfile = f'era5_data/era5_gee_forcing_{lat}_{lon}_{zbot}_{start_year}_{start_month}_{end_year}_{end_month}.nc'
        ds_forcing = gee_era5s_to_forcing(ee, lat, lon, start_date, end_date, zbot=zbot, outputfile=outputfile)
        result = os.path.join(os.getcwd(), outputfile)
    else:
        raise ValueError("The source is not supported. Please choose from 'cds', 'arco-era5', 'era5-land-ts', 'gee'.")
    return result