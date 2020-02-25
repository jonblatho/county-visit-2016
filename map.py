import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

# Set up the figure
fig = plt.figure(figsize=(12,8))
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
ax.set_extent([-120, -72.5, 22, 50], ccrs.Geodetic())
ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)

# Set up colormap
ticks = [-1, -0.2, 0, 0.2, 1]
colors = [(0,0,0.6), (0,0,0.6), (0,0,0.8), (0,0,1), (0.7,0,0.7), (1,0,0), (0.8,0,0), (0.6,0,0), (0.6,0,0)]
cmap = mpl.colors.LinearSegmentedColormap.from_list('colors', colors, N=200)
norm = mpl.colors.Normalize(vmin=-40, vmax=40)
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='horizontal', extend='both', format='%.0f%%', fraction=0.09, pad=0, shrink=0.4)
cbar.set_label("Trump 2016 margin")

# Visited counties
visited = ['29095', '29037', '29083', '29167', '29077', '29109', '29097', '29145', '29119', '29043',
           '29209', '29213', '29225', '29229', '29067', '29153', '29091', '29149', '29203', '29215',
           '29105', '29029', '29131', '29051', '29019', '29510', '29189', '29071', '29055', '29161',
           '29187', '29093', '29179', '29035', '29023', '29207', '29201', '29143', '29133', '29185', # Missouri
           '40003', '40053', '40035', '40115', '40041', '40097', '40143', '40037', '40119', '40103',
           '40047', '40093', '40011', '40017', '40087', '40027', '40109', '40083', '40081', '40125',
           '40133', '40107', '40111', '40091', '40101', '40135', '40131', # Oklahoma
           '05007', '05143', '05033', '05131', '05087', '05015', '05009', '05005', '05049', '05135',
           '05075', '05031', '05111', '05035', # Arkansas
           '47157', '47047', '47075', '47113', '47077', '47039', '47005', '47085', '47081', '47043',
           '47125', '47021', '47147', '47037', '47189', '47159', '47141', '47035', '47145', '47105',
           '47093', '47155', '47089', '47063', '47059', '47179', '47163', # Tennessee
           '21007', '21145', '21157', '21139', '21143', '21033', '21047', '21221', # Kentucky
           '51191', '51173', '51197', '51155', '51121', '51161', '51023', '51163', '51015', '51790',
           '51165', '51750', '51660', '51171', '51187', '51061', '51107', '51153', '51059', '51600',
           '51510', '51013', '51520', # Virginia
           '01003', '01097', # Alabama
           '11001', # Washington, D.C.
           '12033', # Florida
           '28033', '28137', '28107', '28161', '28043', '28015', '28007', '28159', '28099', '28101',
           '28075', '28023', '28153', '28041', # Mississippi
           '37119', # North Carolina
           '17003', # Illinois
           '45041', '45067', '45051' # South Carolina
           ]

# Process election data
file = open('countypres_2016.csv', 'r')
lines = file.readlines()[1:] # Skip header
results = [line.split(',') for line in lines]
visited_results = dict()
for fips_code in visited:
    # Reformat FIPS code to remove leading 0 for state FIPS codes below 10
    if fips_code[0] == '0':
        fips_code = fips_code[1:]

    # Find results for each FIPS code
    county_results = [result for result in results if result[4] == fips_code]
    clinton_result = [result for result in county_results if result[6] == "Hillary Clinton"][0]
    trump_result = [result for result in county_results if result[6] == "Donald Trump"][0]
    margin = (int(trump_result[8]) - int(clinton_result[8]))/int(trump_result[9])

    # Now reset FIPS codes to add back the leading 0 and store results in the dictionary
    if len(fips_code) == 4:
        fips_code = '0' + fips_code
    visited_results[fips_code] = margin

# Draw counties
counties = shpreader.Reader('us_counties_20m.shp').records()
for county in counties:
    fips_code = county.attributes["STATEFP"] + county.attributes["COUNTYFP"]
    if fips_code not in visited:
        ax.add_geometries([county.geometry], ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor=(0,0,0,0.2), linewidth=0.5)
    else:
        ax.add_geometries([county.geometry], ccrs.PlateCarree(), facecolor=cmap(norm(visited_results[fips_code]*100)), edgecolor=(0,0,0,0.2), linewidth=0.5)

# Draw state borders atop counties
shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='50m', category='cultural', name=shapename)
states = shpreader.Reader(states_shp).records()

for state in states:
    if state.attributes['iso_a2'] == 'US':
        ax.add_geometries([state.geometry], ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor='black')

# Label with my username and save the plot
plt.annotate('@jonblatho', xy=(0.93, 0.01), xycoords='figure fraction', annotation_clip=False, size=10, alpha=0.5)
plt.savefig('map.png')
