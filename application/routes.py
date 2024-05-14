"""Routes for parent Flask app"""
from flask import render_template, redirect, request
from flask import current_app as server
from . import db
from .utilities import backup_list, export_sql_to_csv, import_csv_to_sql
from .models import Finance_Table
from datetime import datetime
from time import sleep


@server.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        main_type = request.form["main_type"]
        if main_type == "Income":
            sub_type = request.form["income_sub_type"]
        elif main_type == "Expense":
            sub_type = request.form["expense_sub_type"]
        else:
            print(main_type)
        transact_amount = request.form["amount"]
        transact_note = request.form["note"]
        
        
        try:
            select_date_str = request.form["select_date"]
            select_date = datetime.strptime(select_date_str, "%Y-%m-%d")
        except Exception as e:
            print(f"Invalid date format. Please use YYYY-MM-DD.\nError: {type(e).__name__}")
        
        new_transact = Finance_Table(transact_type=main_type, 
                                     transact_sub_type=sub_type, 
                                     transact_date=select_date, 
                                     money=transact_amount, 
                                     note=transact_note) # type: ignore
        
        try:
            db.session.add(new_transact)
            db.session.commit()
        except Exception as e:
            print(f"There was an issue adding your transaction. Error: {type(e).__name__}")
        finally:
            db.session.close()
            return redirect("/")
        
    else:
        transact = Finance_Table.query.order_by(Finance_Table.transact_date).all()
        return render_template("index.html", transact=transact)

@server.route("/delete/<int:transact_id>")
def delete(transact_id):
    transact_to_delete = Finance_Table.query.get_or_404(transact_id)
    
    try:
        db.session.delete(transact_to_delete)
        db.session.commit()
    except Exception as e:
        print(f"There was a problem deleting that transaction data. Error: {type(e).__name__}")
    finally:
        db.session.close()
        return redirect("/")

@server.route("/update/<int:transact_id>", methods=["GET", "POST"])
def update(transact_id):
    transact_to_update = Finance_Table.query.get_or_404(transact_id)
    
    if request.method == "POST":
        transact_to_update.money = request.form["amount"]
        transact_to_update.note = request.form["note"]
        
        try:
            select_date = request.form["select_date"]
            transact_to_update.transact_date = datetime.strptime(select_date, "%Y-%m-%d")
        except Exception as e:
            print(f"Invalid date format. Please use YYYY-MM-DD. Error: {type(e).__name__}")
        
        try:
            db.session.commit()
        except Exception as e:
            print(f"There was a problem updating the selected transaction data. Error: {type(e).__name__}")
        finally:
            db.session.close()
            return redirect("/")
    else:
        return render_template("update.html", transact=transact_to_update)

@server.route("/confirm_backup", methods=["POST"])
def confirm_backup():
    if request.method == "POST":
        try:
            backup_note = request.form["backup_note"]
            if backup_note != "":
                export_sql_to_csv(backup_note)
                print("Backup has been created!")
        except Exception as e:
            print(f"Make sure that the function is working properly. Error: {type(e).__name__}")
        finally:
            return redirect("/")
    else:
        return redirect("/")

@server.route("/backup_list")
def get_backup_list():
    try:
        file_list: list =  backup_list()
    except Exception as e:
        file_list: list = [] # Set the list to an empty list so that it will still render the template. Just without the backup lists.
        print(f"Make sure that the function is working properly. Error: {type(e).__name__}")
    finally:
        return render_template("file_selection.html", file_list=file_list)

@server.route("/load_backup", methods=["POST"])
def load_backup():
    if request.method == "POST":
        try:
            file_name = request.form["selected_button"]
            full_file_name = f"{file_name}.csv"
            import_csv_to_sql(full_file_name)
            sleep(3)
        except Exception as e:
            print(f"The selected file does not exist. Error: {type(e).__name__}")
        finally:
            return redirect("/")
    else:
        return redirect("/")

@server.route("/about_me")
def about_me():
    return render_template("about_me.html")

