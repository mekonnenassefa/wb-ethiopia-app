import pandas as pd
import plotly.graph_objects as go
from app import app


def cleandata(dataset, keepcolumns = ['Country Name', '1990', '2021'], value_variables = ['1990', '2021']):
    """Clean world bank data for a visualizaiton dashboard
    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file
    Args:
        dataset (str): name of the csv data file
    Returns:
        None
    """
    df = pd.read_csv(dataset, skiprows=4)

    # Keep only the columns of interest (years and country name)
    df = df[keepcolumns]

    eastafrica = ['Ethiopia', 'Kenya', 'Eritrea', 'Somalia', 'South Sudan', 'Dijibouti', 'South Africa', 'Sudan']
    df = df[df['Country Name'].isin(eastafrica)]

    # melt year columns  and convert year to date time
    df_melt = df.melt(id_vars='Country Name', value_vars = value_variables)
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt

def return_figures():
    """Creates four plotly visualizations
    Args:
        None
    Returns:
        list (dict): list containing the four plotly visualizations
    """

  # first chart plots arable land from 1990 to 2021 in top 10 economies
  # as a line chart

    graph_one = []
    df = cleandata('./data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3603754.csv')
    df.columns = ['country','year','gdp']
    df.sort_values('gdp', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()

    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].gdp.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Change in Hectares Arable Land <br> per Person 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'GDP'),
                )

# second chart plots ararble land for 2015 as a bar chart
    graph_two = []
    df = cleandata('./data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3603754.csv')
    df.columns = ['country','year','']
    df.sort_values('hectaresarablelandperperson', ascending=False, inplace=True)
    df = df[df['year'] == 2015]

    graph_two.append(
      go.Bar(
      x = df.country.tolist(),
      y = df.hectaresarablelandperperson.tolist(),
      )
    )

    layout_two = dict(title = 'Hectares Arable Land per Person in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Hectares per person'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df = cleandata('./data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3603754.csv')
    df.columns = ['country', 'year', 'percentrural']
    df.sort_values('percentrural', ascending=False, inplace=True)
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].percentrural.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_three = dict(title = 'Change in Rural Population <br> (Percent of Total Population)',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'Percent'),
                )

# fourth chart shows rural population vs arable land
    graph_four = []

    valuevariables = [str(x) for x in range(1995, 2016)]
    keepcolumns = [str(x) for x in range(1995, 2016)]
    keepcolumns.insert(0, 'Country Name')

    df_one = cleandata('./data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3603754.csv', keepcolumns, valuevariables)
    df_two = cleandata('./data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_3603754.csv', keepcolumns, valuevariables)

    df_one.columns = ['country', 'year', 'variable']
    df_two.columns = ['country', 'year', 'variable']

    df = df_one.merge(df_two, on=['country', 'year'])

    for country in countrylist:
      x_val = df[df['country'] == country].variable_x.tolist()
      y_val = df[df['country'] == country].variable_y.tolist()
      year = df[df['country'] == country].year.tolist()
      country_label = df[df['country'] == country].country.tolist()

      text = []
      for country, year in zip(country_label, year):
          text.append(str(country) + ' ' + str(year))

      graph_four.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'markers',
          text = text,
          name = country,
          textposition = 'top center'
          )
      )

    layout_four = dict(title = 'Rural Population versus <br> Forested Area (Square Km) 1990-2015',
                xaxis = dict(title = 'Rural Population'),
                yaxis = dict(title = 'Forest Area (square km)'),
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures