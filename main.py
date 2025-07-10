from PyQt6.QtWidgets import QApplication,QMainWindow,QComboBox,QScrollArea,QSizePolicy,QStackedWidget,QSplashScreen, QGraphicsDropShadowEffect,QLabel,QHBoxLayout,QMenuBar, QLineEdit, QGridLayout, QWidget, QGroupBox, QPushButton, QVBoxLayout,QMessageBox
from PyQt6 import QtCore
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import  Qt,QUrl, QByteArray
from PyQt6.QtGui import QFont, QPixmap, QColor,QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import functions, matplotlib.pyplot as plt
import numpy as np   # Import the function
import requests
import os, time
from datetime import date, timedelta
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from dotenv import load_dotenv

      
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setGeometry(550, 300, 500, 450)
        self.setMinimumSize(300,300)
        self.setStyleSheet('background-color: white')
        self.drop_down = QComboBox()
        self.drop_down.addItems(['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sept','Oct','Nov','Dec'])
        
        self.gb= QGroupBox()
        # Create the layout
        layout = QGridLayout()
        income=QLabel("Income", self)
        self.incomeText = QLineEdit()
        self.incomeText.setPlaceholderText("0")
        layout.addWidget(income,0,0)
        layout.addWidget(self.incomeText,0,1)
        layout.addWidget(self.drop_down,0,2)

        # Initialize a dictionary to store items as keys and QLineEdit as values
        self.data = {"Rent": 0, "Groceries": 0, "Bills": 0}

# Iterate through the dictionary
        for index, item in enumerate(self.data):
                label = QLabel(f"{item}")  # Create QLabel for the key
                line_edit = QLineEdit()    # Create QLineEdit for the value
                line_edit.setPlaceholderText("0")

    # Update the dictionary with the QLineEdit object
                self.data[item] = line_edit

    # Add widgets to the layout
                layout.addWidget(label, index + 1, 0)
                layout.addWidget(line_edit, index + 1, 1)

        
        button = QPushButton("Submit",self)
        self.answer=QLabel(self)
        save = QPushButton("Save",self)
        button.clicked.connect(lambda: (functions.process(self)))
        save.clicked.connect(lambda: (functions.update_table(self,table)))
        save.setMaximumWidth(100)
       
        
        
        layout.addWidget(button, 6, 0)
        layout.addWidget(save, 6, 1)
        layout.addWidget(self.answer,6,2)
        
       
      
        self.gb.setLayout(layout)
        self.gb.setStyleSheet("QGroupBox { border: none;  }")  # Remove border
        update_button = QPushButton("update",self)
        pie_button = QPushButton("Pie Chart",self)
        
        bar_button = QPushButton("Bar Graph",self)
        
         # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        labels=self.data.keys()
        length=len(self.data)
        x=[100/length]*length
        self.curr_graph="pie"
       

    # Create a pie chart
        axes = self.figure.add_subplot(111)
        axes.pie(x, labels=labels) 
         # Adjust the height to make it look better
        self.chart_layout = QVBoxLayout()
       
        self.chart_layout.addWidget(self.canvas)
        
        update_button.clicked.connect(lambda:functions.chart(self)) 
        pie_button.clicked.connect(lambda:functions.pie_chart(self)) 
        bar_button.clicked.connect(lambda:functions.bar_chart(self)) 
        self.chart_layout.addWidget(update_button)
        self.chart_layout.addWidget(pie_button)
        self.chart_layout.addWidget(bar_button)


        self.chart_group_box= QGroupBox()
        self.chart_group_box.setLayout(self.chart_layout)
        self.menu = QMenuBar()
        self.menu_layout= QHBoxLayout()
        self.menu_layout.addWidget(self.menu)
        
        

    def closeEvent(self, event):
        # Create a confirmation dialog
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Exit")
                msg_box.setText("Are you sure you want to exit?")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
       
                reply= msg_box.exec()
                if reply == QMessageBox.StandardButton.Yes:
                     event.accept()  # Accept the close event
                else:
                     event.ignore() 
        


class News(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("News"))
        todays = date.today()
        yesterday = date.today() - timedelta(days=1)
        month = todays.strftime("%B")
        day = todays.day
        date_title=QLabel()
        date_title.setText(f'{month} {day}')
        layout.addWidget(date_title)
        load_dotenv()

        api = os.environ.get('api')
        # Get today's date
        
        url = f"https://newsapi.org/v2/everything?q=finance%20AND%20investment&language=en&from={todays}&to={yesterday}&sortBy=publishedAt&apiKey={api}"
                
        response = requests.get(url)
        data =response.json()
        articles = data.get("articles")
        
        news_list=QVBoxLayout()
        
        main=QGroupBox()
        main.setLayout(news_list)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main)
        layout.addWidget(scroll_area)  
        main.setStyleSheet("QGroupBox { border: none;  }")

        

       # if response.status_code != 200:
        #        print(f"Error: {response.status_code}, {response.text}")

        if not articles:
              label = QLabel("No Articles Found")
              label.setStyleSheet("""
                color: lightgrey;         
                font-size: 30px;   
                font-weight: bold;   
                margin: 50px;               
              """)
              
              news_list.addWidget(label)
              
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.on_image_loaded)

        for index, article in enumerate(articles):
             title = article.get('title', 'No title available')
             description = article.get('description', 'No description available')
             news_url =article.get('url')
             image_url = article.get('urlToImage')  # Get the image URL

             if not description:  # Check if description is None or empty
                   description = 'No description available'
             elif len(description)>200:
                   description= description[:240]+ "...."
             
             box = QGroupBox()
             self.headline=QGridLayout()
            
             
             
             topic = QLabel(title)
             topic.setFont(QFont("Times New Roman", 18))
             summary = QLabel(f'{description} <a href="{news_url}">See more</a>')
             summary.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
             summary.setOpenExternalLinks(True)
             summary.setWordWrap(True)
             topic.setWordWrap(True)
             summary.setMinimumHeight(200)
             summary.setFont(QFont("Times New Roman", 12))
             box.setMaximumWidth(900)

             topicAndSummary= QVBoxLayout()
             topicAndSummary.addWidget(topic)
             topicAndSummary.addWidget(summary)
             self.container=QWidget()
             self.container.setLayout(topicAndSummary)
             self.headline.addWidget(self.container,0,0)
             if image_url:
                #summary.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

                topic.setAlignment(Qt.AlignmentFlag.AlignLeft)
                summary.setAlignment(Qt.AlignmentFlag.AlignLeft)
                image_label = QLabel()
                image_label.setMaximumWidth(230)
                self.headline.addWidget(image_label,0,1)
                image_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                request = QNetworkRequest(QUrl(image_url))
                reply = self.manager.get(request)
                reply.image_label = image_label
               # reply.article_index = index
             else:
                self.container.setMaximumWidth(850)
            

             
             self.headline.setContentsMargins(20, 10, 10, 10)  # Adds margins around the layout
             



             box.setLayout(self.headline)
             
             shadow = QGraphicsDropShadowEffect()
             shadow.setBlurRadius(10)  # Softness of the shadow
             shadow.setColor(QColor(0, 0, 0, 50))  # Semi-transparent black shadow
             shadow.setOffset(1, 1)  # Shadow offset to make it appear around the border

             box.setGraphicsEffect(shadow)
            
             news_list.addWidget(box)
        
             
        
        menu=QMenuBar()
        layout.addWidget(menu)
        menu.setStyleSheet('background-color: blue')
        news_action = menu.addAction("News")
        home_action = menu.addAction("Home") 
        # Connect Acdions
        home_action.triggered.connect(lambda: stacked.setCurrentWidget(central_widget))

        news_action.triggered.connect(lambda: stacked.setCurrentWidget(news))
        self.setLayout(layout)  
    def on_image_loaded(self, reply):
        image_data = reply.readAll()
        image = QImage()
        image.loadFromData(image_data)

        label = getattr(reply, 'image_label', None)

        if not image.isNull():
            
            pixmap = QPixmap.fromImage(image).scaled(
                220, 190, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            

            if label:
                label.setPixmap(pixmap)
            
        reply.deleteLater()
       




app = QApplication([])


  # Simulate loading
window = Window()
    # Initialize main window

    # Close splash screen

    # Close splash screen

table = functions.table(window)

# Create the central widget
central_widget = QWidget()
main= QGridLayout()
        
main.addWidget(window.gb, 1,0)
main.addWidget(window.chart_group_box,1,1)
main.addLayout(window.menu_layout,2,0,1,2)
main.addWidget(table, 3,0)

        # Set the layout for the central widget
central_widget.setLayout(main)
central_widget.setStyleSheet('background-color: rgba(255,255,255,0.5);')

stacked = QStackedWidget()
news= News()
stacked.addWidget(news)
stacked.addWidget(central_widget)

news_action = window.menu.addAction("News")
home_action = window.menu.addAction("Home")
stacked.setCurrentWidget(central_widget)
        # Connect Acdions
home_action.triggered.connect(lambda: stacked.setCurrentWidget(central_widget))

news_action.triggered.connect(lambda: stacked.setCurrentWidget(news))
        # Set the central widget for QMainWindow
window.setCentralWidget(stacked)


window.show()

app.exec()
