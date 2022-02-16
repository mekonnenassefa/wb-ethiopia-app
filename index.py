from dash import dcc, html, Input, Output



# Connect to main app.py file
from app import app
from app import server


# Connect to your app pages
from apps import ethiopia, eastafrica
#from apps.data_scripts import return_figures


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H1('World Bank Dashboard for Ethiopia', style={"textAlign": "center"}),
        dcc.Link('Ethiopia  | ', href='/apps/ethiopia'),
        dcc.Link('East Africa', href='/apps/eastafrica'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/ethiopia':
        return ethiopia.layout
    if pathname == '/apps/eastafrica':
        return eastafrica.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)