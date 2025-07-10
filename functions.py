from PyQt6.QtWidgets import QApplication, QMainWindow,  QLabel, QLineEdit, QGridLayout, QWidget, QGroupBox, QPushButton, QTableWidget,QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt, QUrl, QByteArray
from PyQt6.QtGui import QFont, QPixmap, QColor,QImage



def process(window):
    try:
        # Initialize a dictionary to store numeric values from QLineEdit widgets
        total=0

        # Convert empty values to "0" and validate each entry
        for key, line_edit in window.data.items():
            # Get text from the QLineEdit widget
            value = line_edit.text()
            if not value:  # Set empty fields to "0"
                value = "0"
             # Convert to float and validate
            value = float(value)
            if value < 0:  # Validate for negative numbers
                window.answer.setText("Do not write negative numbers")
                return
           
            # Update the data dictionary with validated numeric values
            total+= value

        # Retrieve income and validate it
        income = window.incomeText.text()
        if not income:  # Set empty income to "0"
            window.answer.setText("Enter amount in income")
            return
        income = float(income)
        if income < 0:  # Validate income for negative numbers
            window.answer.setText("Do not write negative numbers")
            return

        # Sum all spending values in the dictionary
        

        # Calculate savings and display
        savings = income - total
        window.answer.setText(f"Savings: {savings}")

    except ValueError:
        # Handle invalid inputs (e.g., non-numeric values)
        window.answer.setText("Please enter valid numbers")



def convert(window):
    array = []
    for line_edit in window.data.values():
        num = line_edit.text()  # Get text from each QLineEdit
        if not num:  # If empty, set it to "0"
            num = "0"
        
        num = float(num)  # Convert to float
        array.append(num)
    return array

def chart(window):
    if not is_valid(window):
        window.answer.setText("Invalid data provided")
        return
    if window.curr_graph=="pie":
        pie_chart(window)
    else:
        bar_chart(window)

def pie_chart(window):
    if not is_valid(window):
        window.answer.setText("Invalid data provided")
        return
    
    window.figure.clear()
    window.curr_graph="pie"

    x = convert(window)
    labels = list(window.data.keys())

   
    axes = window.figure.add_subplot(111)
    axes.pie(x, labels=labels, autopct='%1.1f%%')

    window.canvas.draw()


        
def is_valid(window):
    for i in window.data.values():
        if i is None or i.text() == "":
            return False
        try:
            value = float(i.text())
            if value == 0:
                return False
            if value<0:
                return False
        except ValueError:
            return False
    return True

def bar_chart(window):
    if not is_valid(window):
        window.answer.setText("Invalid data provided")
        return
    window.figure.clear()
    window.curr_graph="bar"
    x = convert(window)
    labels = list(window.data.keys())
    window.axes = window.figure.add_subplot(111)
    window.axes.bar(labels, x)
    window.axes.set_xlabel("Expenses")
    window.axes.set_ylabel("Values")
    
 
    window.canvas.draw()


def table(window):
    table=QTableWidget()
    year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    table.setRowCount(len(year)+1)
    table.setColumnCount(len(window.data)+3)
    table.setVerticalHeaderLabels(year)

    table.setHorizontalHeaderLabels(window.data.keys())
    
    for i in range(13):
        for j in range(len(window.data)+3):  # Assuming 3 columns (0, 1, 2)
            item = QTableWidgetItem("0.0")
            # Disable editing for the item
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(i, j, item)
    table.setHorizontalHeaderItem(3, QTableWidgetItem("Income"))
    table.setHorizontalHeaderItem(4, QTableWidgetItem("Expenses"))
    table.setHorizontalHeaderItem(5, QTableWidgetItem("Savings"))
    table.setVerticalHeaderItem(12, QTableWidgetItem("Total"))
    


    return table
'''
def update_table(window,table):
    array= convert(window)
    expenses=0
    for i in range(len(array)):
        expenses+=array[i]
        table.setItem(window.drop_down.currentIndex(), i, QTableWidgetItem(str(array[i])))  # Set key
   
    table.setItem(0, 4, QTableWidgetItem(str(expenses))) 
    #table.setItem(12, 4, QTableWidgetItem(str(total_expenses)))  # Set key
'''
def update_table(window,table):
    array= convert(window)
    expenses= 0
    total_expenses= 0

    col=4
    for i in range(len(array)):
            expenses+=array[i]
            table.setItem(window.drop_down.currentIndex(), i, QTableWidgetItem(str(array[i]))) 
            table.setItem(window.drop_down.currentIndex(), col, QTableWidgetItem(str(expenses))) 

    for row in range(table.rowCount()-1):
        item = table.item(row, col)  # Retrieves the item
        text_value = item.text() 
        total_expenses+= float(text_value)
        
    table.setItem(12, col, QTableWidgetItem(str(total_expenses))) 


