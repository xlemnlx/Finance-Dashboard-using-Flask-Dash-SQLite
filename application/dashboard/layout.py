from .functions import main, dropdown_list
from dash import Dash, html, dcc
from dash_bootstrap_components import Row, Col

def init_layout(app: Dash):
    
    _, df_income, df_expense, _, _, _ = main()
    
    # Create Dash Layout
    app.layout = html.Header(children=[
        html.Nav(children=[
            html.A(children="Dashboard", href="/dashboard/", className="header_nav"),
            html.A(children="Home", href="/", className="header_nav"),
            html.A(children="About Me", href="/about_me", className="header_nav")
        ])
    ]), html.Div(id="dash_main_div", children=[
        html.H1(children="Finance Dashboard"),
        Row(html.Div(className="dash_inner_div_l2", children=[
            Col(html.Div(children=[
                Col(html.P(children="Filter by Year:")),
                Col(dcc.Dropdown(dropdown_list(df_income, all=True), dropdown_list(df_income)[-1], id="pie_income_selector"))
                ])),
            Col(html.Div(children=[
                Col(html.P(children="Filter by Year:")),
                Col(dcc.Dropdown(dropdown_list(df_expense, all=True), dropdown_list(df_expense)[-1], id="pie_expense_selector"))
                ])),
        ])),
        Row(html.Div(className="dash_inner_div_l1", id="pie_charts", children=[
            Col(dcc.Graph(id="pie_income_content")),
            Col(dcc.Graph(id="pie_expense_content"))
        ])),
        Row(html.Br()), # CURRENTLY HERE
        Row(html.Div(className="dash_inner_div_l2", children=[
            Col(html.Div(children=[
                Col(html.P(children="Filter by Year:")),
                Col(dcc.Dropdown(dropdown_list(df_income, all=True), dropdown_list(df_income)[-1], id="line_income_selector"))
                ])),
            Col(html.Div(children=[
                Col(html.P(children="Filter by Year:")),
                Col(dcc.Dropdown(dropdown_list(df_expense, all=True), dropdown_list(df_expense)[-1], id="line_expense_selector"))
                ])),
        ])),
        Row(html.Div(className="dash_inner_div_l1", id="line_charts", children=[
            Col(dcc.Graph(id="line_income_content")),
            Col(dcc.Graph(id="line_expense_content"))
        ])),
        Row(html.Br()),
        Row(html.Div(className="dash_inner_div_l2", children=[
            Col(html.Div(children=[
                Col(html.P(children="Filter by Year:")),
                Col(dcc.Dropdown(dropdown_list(df_income), dropdown_list(df_income)[-1], id="bar_income_selector"))
                ])),
            Col(html.Div(children=[
                Col(html.P(children="Filter by Year:")),
                Col(dcc.Dropdown(dropdown_list(df_expense), dropdown_list(df_expense)[-1], id="bar_expense_selector"))
                ])),
        ])),
        Row(html.Div(className="dash_inner_div_l1", id="bar_plots", children=[
            Col(dcc.Graph(id="bar_income_content")),
            Col(dcc.Graph(id="bar_expense_content"))
        ]))
    ]), html.Footer(children=[
        html.Div(className="my_links", children=[
            html.H1(children="My links:"),
            html.Nav(children=[
                html.A(children="GitHub", href="https://github.com/xlemnlx", target="_blank", className="footer_nav"),
                html.A(children="LinkedIn", href="https://www.linkedin.com/in/emmanuel-darca-35822b211/", target="_blank", className="footer_nav"),
                html.A(children="E-mail", href="mailto:eman.darca86@gmail.com", className="footer_nav")
            ])
        ])
    ])