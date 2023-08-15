import os
import numpy as np
import xarray as xr

# read grib
# URL: https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{date}%2F{hour}%2Fatmos&file=gfs.t{hour}z.pgrb2.0p25.f000&var_HGT=on&var_MSLET=on&var_SPFH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&lev_2_m_above_ground=on&lev_10_m_above_ground=on&lev_1000_mb=on&lev_925_mb=on&lev_850_mb=on&lev_700_mb=on&lev_600_mb=on&lev_500_mb=on&lev_400_mb=on&lev_300_mb=on&lev_250_mb=on&lev_200_mb=on&lev_150_mb=on&lev_100_mb=on&lev_50_mb=on&lev_mean_sea_level=on&subregion=&toplat=90&leftlon=0&rightlon=360&bottomlat=-90
tdata = xr.open_dataset('gfs.pgrb2.0p25.f000', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2}})
wdata = xr.open_dataset('gfs.pgrb2.0p25.f000', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 10}})
mdata = xr.open_dataset('gfs.pgrb2.0p25.f000', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'meanSea'}})
upper = xr.open_dataset('gfs.pgrb2.0p25.f000', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'isobaricInhPa'}})

# grib2npy
# surface data
surface_data = np.zeros((4, 721, 1440), dtype=np.float32)
surface_data[0] = mdata['mslet'][::-1,:].data.astype(np.float32)
surface_data[1] = wdata['u10'][::-1,:].data.astype(np.float32)
surface_data[2] = wdata['v10'][::-1,:].data.astype(np.float32)
surface_data[3] = tdata['t2m'][::-1,:].data.astype(np.float32)
np.save(os.path.join('input_surface.npy'), surface_data)

# upper air data
upper_data = np.zeros((5, 13, 721, 1440), dtype=np.float32)
upper_data[0] = (upper.variables['gh'][:,::-1,:].data * 9.80665).astype(np.float32)
upper_data[1] = upper.variables['q'][:,::-1,:].data.astype(np.float32)
upper_data[2] = upper.variables['t'][:,::-1,:].data.astype(np.float32)
upper_data[3] = upper.variables['u'][:,::-1,:].data.astype(np.float32)
upper_data[4] = upper.variables['v'][:,::-1,:].data.astype(np.float32)
np.save(os.path.join('input_upper.npy'), upper_data)
