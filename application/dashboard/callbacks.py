from .functions import main
from dash import callback, Output, Input, Dash
import plotly.express as px

def init_callbacks(app: Dash):
    
    _, df_income, df_expense, _, df_val_con_income, df_val_con_expense = main()
    
    @app.callback(
        Output("pie_income_content", "figure"),
        Input("pie_income_selector" , "value")
    )
    def pie_income(value):
        if value == "All":
            pie_income_fig = px.pie(df_income, labels="transact_sub_type", values="money", names="transact_sub_type", color="transact_sub_type")
            pie_income_fig.update_traces(hovertemplate="%{label}: <br>Amount: $%{value}", textinfo="value")
            pie_income_fig.update_layout(title="Overall income overview.", legend=dict(title="Income Source", bgcolor="LightBlue"))
        else:
            dff_income = df_income[df_income["year"] == value]
            pie_income_fig = px.pie(dff_income, labels="transact_sub_type", values="money", names="transact_sub_type", color="transact_sub_type")
            pie_income_fig.update_traces(hovertemplate="%{label}: <br>Amount: $%{value}", textinfo="value")
            pie_income_fig.update_layout(title=f"Income overview for the year: {value}", legend=dict(title="Income Source", bgcolor="LightBlue"))
        return pie_income_fig
    
    @app.callback(
        Output("pie_expense_content", "figure"),
        Input("pie_expense_selector" , "value")
    )
    def pie_expense(value):
        if value == "All":
            pie_expense_fig = px.pie(df_expense, labels="transact_sub_type", values="money", names="transact_sub_type", color="transact_sub_type")
            pie_expense_fig.update_traces(hovertemplate="%{label}: <br>Amount: $%{value}", textinfo="value")
            pie_expense_fig.update_layout(title="Overall expenses overview", legend=dict(title="Expenses Source", bgcolor="LightBlue"))
        else:
            dff_expense = df_expense[df_expense["year"] == value]
            pie_expense_fig = px.pie(dff_expense, labels="transact_sub_type", values="money", names="transact_sub_type", color="transact_sub_type")
            pie_expense_fig.update_traces(hovertemplate="%{label}: <br>Amount: $%{value}", textinfo="value")
            pie_expense_fig.update_layout(title=f"Expenses overview for the year: {value}", legend=dict(title="Expenses Source", bgcolor="LightBlue"))
        return pie_expense_fig
    
    @app.callback(
        Output("line_income_content", "figure"),
        Input("line_income_selector", "value")
    )
    def line_income(value):
        if value == "All":
            line_income_fig = px.line(df_val_con_income, x="month", y="total_amount", color="sub_type", title="Overall income overview.")
            line_income_fig.update_layout(legend=dict(title="Expenses Source", bgcolor="LightBlue"))
            line_income_fig.update_traces(hovertemplate="Month: %{x} <br>Amount: $%{y}")
            line_income_fig.update_xaxes(title_text="Months")
            line_income_fig.update_yaxes(title_text="Amount")
        else:
            dff_con_income = df_val_con_income[df_val_con_income["year"] == value]
            line_income_fig = px.line(dff_con_income, x="month", y="total_amount", color="sub_type", title=f"Income overview for the year: {value}")
            line_income_fig.update_layout(legend=dict(title="Expenses Source", bgcolor="LightBlue"))
            line_income_fig.update_traces(hovertemplate="Month: %{x} <br>Amount: $%{y}")
            line_income_fig.update_xaxes(title_text="Months")
            line_income_fig.update_yaxes(title_text="Amount")
        return line_income_fig
    
    @app.callback(
        Output("line_expense_content", "figure"),
        Input("line_expense_selector", "value")
    )
    def line_expense(value):
        if value == "All":
            line_expense_fig = px.line(df_val_con_expense, x="month", y="total_amount", color="sub_type", title="Overall expenses overview")
            line_expense_fig.update_layout(legend=dict(title="Expenses Source", bgcolor="LightBlue"))
            line_expense_fig.update_traces(hovertemplate="Month: %{x} <br>Amount: $%{y}")
            line_expense_fig.update_xaxes(title_text="Months")
            line_expense_fig.update_yaxes(title_text="Amount")
        else:
            dff_con_expense = df_val_con_expense[df_val_con_expense["year"] == value]
            line_expense_fig = px.line(dff_con_expense, x="month", y="total_amount", color="sub_type", title=f"Expenses overview for the year: {value}")
            line_expense_fig.update_layout(legend=dict(title="Expenses Source", bgcolor="LightBlue"))
            line_expense_fig.update_traces(hovertemplate="Month: %{x} <br>Amount: $%{y}")
            line_expense_fig.update_xaxes(title_text="Months")
            line_expense_fig.update_yaxes(title_text="Amount")
        return line_expense_fig
    
    @app.callback(
        Output("bar_income_content", "figure"),
        Input("bar_income_selector" , "value")
    )
    def bar_income(value):
        dff_income = df_val_con_income[df_val_con_income["year"] == value]
        bar_income_fig = px.bar(dff_income, x="month", y="total_amount", color="sub_type", text_auto=True)
        bar_income_fig.update_layout(xaxis_title="Months", yaxis_title="Amount", title=f"Income overview for the year: {value}", legend=dict(title="Income Source", bgcolor="LightBlue"))
        bar_income_fig.update_traces(hovertemplate="Month: %{x} <br>Amount: $%{y}")
        return bar_income_fig
    
    @app.callback(
        Output("bar_expense_content", "figure"),
        Input("bar_expense_selector" , "value")
    )
    def bar_expense(value):
        dff_expense = df_val_con_expense[df_val_con_expense["year"] == value]
        bar_expense_fig = px.bar(dff_expense, x="month", y="total_amount", color="sub_type", text_auto=True)
        bar_expense_fig.update_layout(xaxis_title="Months", yaxis_title="Amount", title=f"Expenses overview for the year: {value}", legend=dict(title="Expenses Source", bgcolor="LightBlue"))
        bar_expense_fig.update_traces(hovertemplate="Month: %{x} <br>Amount: $%{y}")
        return bar_expense_fig


