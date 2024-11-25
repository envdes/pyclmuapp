import cartopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

def plotmap(x,y,c, ax, title, camp='CMRmap'):


    ax.set_extent([-180,180,-60,75],crs=ccrs.PlateCarree())
    ax.coastlines(zorder=5, linewidth=0.3)
    ax.add_feature(cartopy.feature.LAND, facecolor='lightgray', edgecolor='black', linewidth=0.3, zorder=0)
    ax.add_feature(cartopy.feature.OCEAN, facecolor='whitesmoke',zorder=0)
    ax.add_feature(cartopy.feature.LAKES, facecolor='none',edgecolor='black',
                linewidth=0.3,zorder=5)
    ax.add_feature(cartopy.feature.BORDERS,
                facecolor='none',
                edgecolor='black',
                linewidth=0.3,zorder=5)

    g = ax.gridlines(color='grey', linestyle='--', draw_labels=False,zorder=4)
    g.xlocator = mticker.FixedLocator([-90, 0, 90])
    lon_formatter = LongitudeFormatter()#zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    p = ax.scatter(x=x, y=y, transform=ccrs.PlateCarree(), c=c, cmap=camp, s=50, alpha=0.8, zorder=10)
    cbar = plt.colorbar(p, ax=ax,
                        orientation="vertical",
                        fraction=0.20,
                        shrink=0.90,
                        pad=0.02,
                        aspect=30,
                        extend="both")
    cbar.ax.set_title(title, fontsize=10)