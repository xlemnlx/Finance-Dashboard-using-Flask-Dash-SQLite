from os.path import dirname, join
from sqlite3 import connect
import pandas as pd

def db_location() -> str:
    """Returns the path for the database

    Returns:
        str: path to the database.
    """
    base_folder = dirname(__file__)
    db_path = join(base_folder, "..", "static", "db", "finance.db")
    
    return db_path

def date_fixer(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Parse the dates from the raw dataframe and returns three dataframe.

    Args:
        dataframe (pd.DataFrame): raw dataframe

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Returns a three dataframe.
        \n\t\tOne - All data.
        \n\t\tTwo - Filtered to Income only.
        \n\t\tThree - Filtered to Expense only.
    """
    cleaned_table: list = []
    month_list: list = []
    year_list: list = []
    arranged_columns = ["transact_id", 
                        "transact_type", 
                        "transact_sub_type", 
                        "transact_date", 
                        "month", "year", 
                        "money", "note"]
    
    for _, row in dataframe.iterrows():
        current_date: str = row["transact_date"]
        
        if len(current_date) == 10:
            month, year = month_year_adder(current_date)
            month_list.append(month)
            year_list.append(int(year))
            
            cleaned_table.append(row.to_dict())
        else:
            extracted_date = current_date.split(" ")[0]
            row["transact_date"] = extracted_date
            
            month, year = month_year_adder(extracted_date)
            month_list.append(month)
            year_list.append(int(year))
            
            cleaned_table.append(row.to_dict())
    
    df_handler = pd.DataFrame(cleaned_table)
    df_handler["month"] = month_list
    df_handler["year"] = year_list
    df_handler["transact_date"] = pd.to_datetime(df_handler["transact_date"], format="%Y-%m-%d")
    df_arranged_columns = df_handler[arranged_columns]
    df_date_fix = df_arranged_columns.set_index("transact_id")
    
    df_income = df_date_fix[df_date_fix["transact_type"] == "Income"]
    df_expense = df_date_fix[df_date_fix["transact_type"] == "Expense"]
    
    return df_date_fix, df_income, df_expense

def sql_to_df() -> pd.DataFrame:
    """Loads the table to a dataframe

    Returns:
        pd.DataFrame: the finance table of the database
    """
    db_path = db_location()
    
    try:
        conn = connect(db_path)
        select_statement = "SELECT * FROM finance__table"
        df_raw = pd.read_sql(select_statement, conn)
    except Exception as e:
        print(f"Something is wrong to the database or the table. Error: {type(e).__name__}")
    finally:
        conn.close()
    
    return df_raw

def month_year_adder(date: str) -> tuple[str, str]:
    """Extracts the month and year data from the full date data.

    Args:
        date (str): full date format.

    Returns:
        tuple[str, str]: month and year.
    """
    month_dict = {
        "01" : "January",
        "02" : "February",
        "03" : "March",
        "04" : "April",
        "05" : "May",
        "06" : "June",
        "07" : "July",
        "08" : "August",
        "09" : "September",
        "10" : "October",
        "11" : "November",
        "12" : "December",
    }
    
    month_num = date.split("-")[1]
    year = date.split("-")[0]
    
    if month_num in month_dict:
        month = month_dict[month_num]
    
    return month, year

def month_reordering_list(month_unordered: list) -> list:
    """Returns a list in which it arrange the Months from Jan. -> Dec from the list as its argument.

    Args:
        month_unordered (list): unordered list of months available.

    Returns:
        list: ordered list of months available.
    """
    month_ordered: list = []
    
    month_based = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    for month in month_based:
        if month in month_unordered:
            month_ordered.append(month)
    
    return month_ordered

def df_value_consolidator(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Creates a dataframe where the values are added up for the sub-type the reoccurring within the same month and year. Example: Groceries.
       Returns three dataframes. One is all of the data, while the other two are filtered between Income and Expense.

    Args:
        dataframe (pd.DataFrame): Insert here the df_fixed.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: df_val_con, df_val_con_income, df_val_con_expense
    """
    value_consolidated_list: list = []
    
    year_list: list = list(dataframe["year"].unique())
    year_arr = sorted(year_list)
    
    for year in year_arr:
        
        df_year: pd.DataFrame = dataframe[dataframe["year"] == year]
        month_unordered: list = list(df_year["month"].unique())
        
        month_ordered: list = month_reordering_list(month_unordered)
        
        for month in month_ordered:
            
            df_month: pd.DataFrame = df_year[df_year["month"] == month]
            
            total_income_fulltime: int = 0
            total_income_freelance: int = 0
            total_expense_groceries: int = 0
            total_expense_bills: int = 0
            total_expense_leisure: int = 0
            
            for _, row in df_month.iterrows():
                
                main_type = row["transact_type"]
                sub_type = row["transact_sub_type"]
                amount = row["money"]
                
                if main_type == "Income":
                    
                    if sub_type == "Full-time Job":
                        total_income_fulltime += int(amount)
                    else: # Freelancing
                        total_income_freelance += int(amount)
                    
                else: # Expense
                    
                    if sub_type == "Groceries":
                        total_expense_groceries += int(amount)
                    elif sub_type == "Bills":
                        total_expense_bills += int(amount)
                    else: # Leisure
                        total_expense_leisure += int(amount)
            
            value_consolidated_list.append({"main_type" : "Income", "sub_type" : "Full-time Job", "month" : month, "year" : year, "total_amount" : total_income_fulltime})
            value_consolidated_list.append({"main_type" : "Income", "sub_type" : "Freelancing", "month" : month, "year" : year, "total_amount" : total_income_freelance})
            value_consolidated_list.append({"main_type" : "Expense", "sub_type" : "Groceries", "month" : month, "year" : year, "total_amount" : total_expense_groceries})
            value_consolidated_list.append({"main_type" : "Expense", "sub_type" : "Bills", "month" : month, "year" : year, "total_amount" : total_expense_bills})
            value_consolidated_list.append({"main_type" : "Expense", "sub_type" : "Leisure", "month" : month, "year" : year, "total_amount" : total_expense_leisure})
    
    df_value_consolidated = pd.DataFrame(value_consolidated_list)
    
    df_val_con = df_value_consolidated[df_value_consolidated["total_amount"] != 0]
    
    df_val_con_income = df_value_consolidated[df_value_consolidated["main_type"] == "Income"]
    df_val_con_expense = df_value_consolidated[df_value_consolidated["main_type"] == "Expense"]
    
    return df_val_con, df_val_con_income, df_val_con_expense

def dropdown_list(dataframe: pd.DataFrame, all=False) -> list:
    """Return a list that contains the year to used as dropdown items.

    Args:
        dataframe (pd.DataFrame): dataframe where the year is to be extract
        all (bool, optional): Defaults to False. If set to true, it add a "All" to the dropdown item where there will be no filtering for the year.

    Returns:
        list: a list that contains the year to used as dropdown items.
    """
    if all is False:
        selector_list: list = sorted(list(dataframe["year"].unique()))
    else:
        selector_list: list = ["All"] + sorted(list(dataframe["year"].unique()))
    
    return selector_list

def main() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Just runs the three function so that in the other files, this just needs to be run.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: dataframes - df_fixed, df_income, df_expense, df_val_con, df_val_con_income, df_val_con_expense
    """
    df_raw = sql_to_df()
    df_fixed, df_income, df_expense = date_fixer(df_raw)
    df_val_con, df_val_con_income, df_val_con_expense = df_value_consolidator(df_fixed)
    
    return df_fixed, df_income, df_expense, df_val_con, df_val_con_income, df_val_con_expense

