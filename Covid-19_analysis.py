confirmed_link = “https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv”
confirmed = pd.read_csv(confirmed_link)
confirmed.columns
confirmed.info()
confirmed.head()
# moving the columns into rows using dataframe’s melt function
confirmed = confirmed.melt(id_vars=[‘Province/State’, ‘Country/Region’, ‘Lat’, ‘Long’], var_name=”Date”, value_name=”Confirmed”)
#drop unnecessary columns
confirmed = confirmed.drop([‘Province/State’,’Lat’,’Long’],axis=1)

# for some countries there are multiple rows since the province data was populated, we need # to group by country and date after the province col
droppedconfirmed = confirmed.groupby([‘Country/Region’,’Date’]).sum()
confirmed = confirmed.reset_index()

# Update the Country column to match with the world
dataframeconfirmed[‘Country’] = confirmed[‘Country/Region’].map(country_map)
confirmed.loc[~confirmed[‘Country’].notnull(), ‘Country’] = confirmed.loc[~confirmed[‘Country’].notnull(), ‘Country/Region’]
confirmed

world = gpd.read_file(gpd.datasets.get_path(‘naturalearth_lowres’))
world

#Generating the Static Chloropleth map
country_map = {‘Bosnia and Herzegovina’:’Bosnia and Herz.’
, ‘Central African Republic’:’Central African Rep.’
, “Cote d’Ivoire”:”Côte d’Ivoire”
, ‘Dominican Republic’:’Dominican Rep.’
, ‘Equatorial Guinea’:’Eq. Guinea’
, ‘Eswatini’:’eSwatini’
, ‘South Sudan’:’S. Sudan’
, ‘Taiwan*’:’Taiwan’
, ‘US’:’United States of America’
, ‘Western Sahara’:’W. Sahara’}

cdf[‘Country’] = cdf[‘Country/Region’].map(country_map)
cdf.loc[~cdf[‘Country’].notnull(), ‘Country’] = cdf.loc[~cdf[‘Country’].notnull(), ‘Country/Region’]

#since we cannot plot time series choropleths in GeoPandas directly, we will just take one day into a temporary dataframe
confirmed20 = confirmed[confirmed[‘Date’]==’6/20/20′]
#A merged data frame is generated based on confirmed20 and world GeoPandas dataframe
cworld = world.merge(confirmed20,how= ‘left’,left_on=’name’,right_on=’Country’)
cworld = cworld[world.name!=”Antarctica”]
cworld.Confirmed = cworld.Confirmed.fillna(0)

#finally generate the choropleth map
#Generate the choropleth map using gdf plot function on the Confirmed columnfig = cworld.plot(column=’Confirmed’,cmap=’cool’,figsize=(18,10), legend = True
            ,legend_kwds={‘label’: “No of Confirmed COVID-19”,
                          ‘orientation’: “horizontal”})
#removing axis ticks
plt.axis(‘off’)#Add the title
plt.title(“Confirmed COVID-19 cases per Country”)
plt.show()


#Time series analysis 
mergedworld = pd.DataFrame()
for i in confirmed.Date.unique():
    mergetemp=world.merge(confirmed[confirmed.Date==i],left_on=’name’ ,right_on=’Country’,how=’left’)
    mergedworld = mergedworld.append(mergetemp)
    
def worldplot(date):
    mergedworld[mergedworld.Date==date[0]].plot(column=’Confirmed’,figsize=(20,9), legend = True) 


interact(worldplot,date=selection_range_slider)






