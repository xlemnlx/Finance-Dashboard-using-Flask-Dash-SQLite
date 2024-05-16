from .dashboard.functions import main
from datetime import datetime
import pandas as pd
import sqlite3
import os

def datetime_formatter() -> tuple:
    """datetime formatter and generator.

    Returns:
        tuple: formatted_datetime: str, current_datetime: datetime
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    
    return formatted_datetime, current_datetime

def path_generator() -> tuple[str, str, str, str, str]:
    """Outputs the dynamic paths.

    Returns:
        tuple[str, str, str, str, str]: [base_path, db_path, backup_path, backup_folder, backup_file_name]
    """
    formatted_datetime, _ = datetime_formatter()
    
    db_file_name = "finance.db"
    backup_file_name = f"db_backup_{formatted_datetime}.csv"
    
    base_path = os.path.dirname(__file__)
    
    db_path_folder = os.path.join(base_path, "static", "db")
    db_path = os.path.join(db_path_folder, db_file_name)
    
    backup_folder = os.path.join(base_path, "..", "backups", "output_files")
    backup_path = os.path.join(backup_folder, backup_file_name)
    
    return base_path, db_path, backup_path, backup_folder, backup_file_name

def date_fixer(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Removes the time in the datetime since its just "00:00:00.0000"

    Args:
        dataframe (pd.DataFrame): raw dataframe

    Returns:
        pd.DataFrame: fixed dataframe
    """
    cleaned_table: list = []
    
    for _, row in dataframe.iterrows():
        current_date: str = row["transact_date"]
        
        if len(current_date) == 10:
            cleaned_table.append(row.to_dict())
        else:
            extracted_date = current_date.split(" ")[0]
            row["transact_date"] = extracted_date
            
            cleaned_table.append(row.to_dict())
    
    df_fixed = pd.DataFrame(cleaned_table)
    df_fixed["transact_date"] = pd.to_datetime(df_fixed["transact_date"], format="%Y-%m-%d")
    
    return df_fixed

def string_formatter(file_name: str, creation_date: str) -> tuple[str, str]:
    """Formats the string to the desired format.

    Args:
        file_name (str): File name with extension included
        creation_date (str): Full date and time with decimals.

    Returns:
        tuple[str, str]: File name with extensions removed.\n\tFull date and time with decimals removed.
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
    formatted_name = str(file_name.split(".csv")[0])
    
    original_date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_obj = datetime.strptime(creation_date, original_date_format)
    desired_date_format = "%Y%m%d-%H%M%S"
    desired_date_str = date_obj.strftime(desired_date_format)
    
    filter_month = desired_date_str[4:6]
    if filter_month in month_dict:
        month_str = month_dict[filter_month]
    formatted_date = f"{month_str} {desired_date_str[6:8]}, {desired_date_str[:4]} - {desired_date_str[9:]}"
    
    return formatted_name, formatted_date

def backup_list() -> list: 
    """Retrieves the list of backup file names, date created, and user remarks. 

    Returns:
        list: backup file names, date created, and user remarks as dict inside a list.
    """
    _, db_path, _, _, _ = path_generator()
    file_list: list = []
    
    try:
        conn = sqlite3.connect(db_path)
        select_query = "SELECT backup_name, backup_date, note FROM backup_table;"
        df = pd.read_sql(select_query, conn)
        
        for _, row in df.iterrows():
            row_filename: str = row["backup_name"]
            row_date: str = row["backup_date"]
            
            formatted_name, formatted_date = string_formatter(row_filename, row_date)
            
            row["backup_name"] = formatted_name
            row["backup_date"] = formatted_date
            
            file_list.append(row.to_dict())
    except Exception as e:
        print(f"Something is wrong with the select statement.\nMake sure that the table exists.\nError: {type(e).__name__}")
        return file_list # returns an empty list.
    finally:
        conn.close
    
    return file_list

def export_sql_to_csv(note: str) -> None:
    """Creates new table if not exists for listing the backup file names, date created, and remarks.
    Then it creates a CSV file to the backup folder.
    
    Args:
        note (str): Remarks from the user.
    """
    base_path, db_path, backup_path, _, backup_file_name = path_generator()
    _, current_datetime = datetime_formatter()
    
    try:
        
        conn = sqlite3.connect(db_path)
        
        backup_table_schema = f"{base_path}/static/schema/backup_table_creation.sql"
        with open(backup_table_schema) as f:
            conn.executescript(f.read())
        
        select_query = "SELECT * FROM finance__table;"
        df = pd.read_sql(select_query, conn)
        
        cursor = conn.cursor()
        insert_query = "INSERT INTO backup_table (backup_name, backup_date, note) VALUES (?, ?, ?);"
        cursor.execute(insert_query, (backup_file_name, current_datetime, note))
        conn.commit()
        
        print(f"Successfully created a backup. File name: {backup_file_name}")
        
    except Exception as e:
        print(f"Error: {type(e).__name__}")
    finally:
        conn.close()
    
    try:
        df_fixed = date_fixer(df)
        df_fixed.to_csv(backup_path, index=False)
    except Exception as e:
        print(f"There is some error exporting the dataframe to a csv file. Error: {type(e).__name__}")

def import_csv_to_sql(file_name: str) -> None:
    """Restores the data of the database table using the csv backup file that the user picked. 

    Args:
        file_name (str): file name of the csv file to be use to restore the data of the database table.
    """
    base_path, db_path, _, backup_folder, _ = path_generator()
    
    try:
        
        conn = sqlite3.connect(db_path)
        
        finance_table_schema = f"{base_path}/static/schema/finance__table_creation.sql"
        with open (finance_table_schema) as f:
            conn.executescript(f.read())
        
        backup_filename_path = f"{backup_folder}/{file_name}"
        df = pd.read_csv(backup_filename_path)
        
        df.to_sql("finance__table", conn, if_exists="append", index=False)
        
        print(f"Successfully restored the database using {file_name}.")
        
    except Exception as e:
        print(f"Error: {type(e).__name__}")
    finally:
        conn.close()

def amount_values() -> dict:
    """Sums up value for Income and Expense, substract them, and insert to a dictionary. To be displayed in the index.

    Returns:
        dict: keys: "savings", "income", "expense"
    """
    _, _, _, df_con, _, _ = main()

    income: int = 0
    expense: int = 0

    for _, row in df_con.iterrows():
        
        handler = row["main_type"]
        money: int = 0
        
        if handler == "Income":
            money = int(row["total_amount"])
            income += money
        else:
            money = int(row["total_amount"])
            expense += money

    current_savings: str = str(income - expense)
    total_income: str = str(income)
    total_expense: str = str(expense)

    amount_dict: dict = {"savings" : current_savings, "income" : total_income, "expense" : total_expense}
    formatted_amount_dict: dict = {}

    for key, amount in amount_dict.items():
        rev_amount = amount[::-1]
        if len(rev_amount) > 3:
            fix_format: list = []
            count: int = 1
            for num in rev_amount:
                fix_format.append(num)
                if count == 3 or count == 6:
                    fix_format.append(",")
                count += 1
            rev_fix_amount = "".join(fix_format)
            fix_amount = rev_fix_amount[::-1]
            formatted_amount_dict[key] = fix_amount
    
    return formatted_amount_dict

