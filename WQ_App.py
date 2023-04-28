from PyQt5.QtWidgets import *
from designe import Ui_MainWindow
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PropAlgo import graph
from PyQt5 import QtWidgets
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")

class My_GuI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("QW-App")

        self.horizontalLayout = QtWidgets.QVBoxLayout(self.ui.frame)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.horizontalLayout.addWidget(self.canvas)

        self.ui.pushButton_save_data.clicked.connect(self.on_pushButton_clicked_save_data)

        self.ui.pushButton_test.clicked.connect(self.on_pushButton_clicked_canvas)

    def on_pushButton_clicked_canvas(self):
        index = self.ui.comboBox_test.currentIndex()
        if index == 0:
            self.plotOnCanvas_pH()
        elif index == 1:
            self.plotOnCanvas_Ox()
        elif index == 2:
            self.plotOnCanvas_Cl()
        else:
            self.plotOnCanvas_Trub()

    def on_pushButton_clicked_save_data(self):
        index = self.ui.comboBox_test.currentIndex()
        if index == 0:
            self.saveData_pH()
        elif index == 1:
            self.saveData_Ox()
        elif index == 2:
            self.saveData_Cl()
        else:
            self.saveData_Trub()

    def saveData_pH(self):

        cluster = MongoClient(
            f"mongodb+srv://{USERNAME}:"+PASSWORD+"@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["database"]
        collection = db["pH"]

        data_pH_value = \
            {"pH": float(self.ui.lineEdit_Value.text()),
             "time_stamp": pd.to_datetime(self.ui.lineEdit_Date.text())}
        collection.insert_one(data_pH_value)
        self.ui.lineEdit_Value.clear()
        self.ui.lineEdit_Date.clear()

    def saveData_Ox(self):

        cluster = MongoClient(
            f"mongodb+srv://{USERNAME}:"+PASSWORD+"@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["database"]
        collection = db["Ox"]

        data_Ox_value = \
            {"Dissolved Oxygen": float(self.ui.lineEdit_Value.text()),
             "time_stamp": pd.to_datetime(self.ui.lineEdit_Date.text())}
        collection.insert_one(data_Ox_value)
        self.ui.lineEdit_Value.clear()
        self.ui.lineEdit_Date.clear()

    def saveData_Cl(self):

        cluster = MongoClient(
            f"mongodb+srv://{USERNAME}:"+PASSWORD+"@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["database"]
        collection = db["Cl"]

        data_Cl_value = \
            {"Chlorine": float(self.ui.lineEdit_Value.text()),
             "time_stamp": pd.to_datetime(self.ui.lineEdit_Date.text())}
        collection.insert_one(data_Cl_value)
        self.ui.lineEdit_Value.clear()
        self.ui.lineEdit_Date.clear()

    def saveData_Trub(self):

        cluster = MongoClient(
            f"mongodb+srv://{USERNAME}:"+PASSWORD+"@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["database"]
        collection = db["Turb"]

        data_Trub_value = \
            {"Turbidity": float(self.ui.lineEdit_Value.text()),
             "time_stamp": pd.to_datetime(self.ui.lineEdit_Date.text())}
        collection.insert_one(data_Trub_value)
        self.ui.lineEdit_Value.clear()
        self.ui.lineEdit_Date.clear()

    def plotOnCanvas_pH(self):
        self.figure.clear()
        index = self.ui.comboBox_Algo.currentIndex()
        if index == 0:
            df = graph(0)
            x = df.loc[:, "ds"]
            y = df.loc[:, "fact"]
            anomaly = df.loc[:, "anomaly"]
            plt.scatter(x[anomaly == 0], y[anomaly == 0], color='black', label='Normal')
            plt.scatter(x[anomaly != 0], y[anomaly != 0], color='red', label='Anomaly')

            plt.xlabel('Time')
            plt.ylabel('Ph')
            plt.legend()

        self.canvas.draw()

    def plotOnCanvas_Ox(self):
        self.figure.clear()
        index = self.ui.comboBox_Algo.currentIndex()
        if index == 0:
            df = graph(1)
            x = df.loc[:, "ds"]
            y = df.loc[:, "fact"]
            anomaly = df.loc[:, "anomaly"]
            plt.scatter(x[anomaly == 0], y[anomaly == 0], color='black', label='Normal')
            plt.scatter(x[anomaly != 0], y[anomaly != 0], color='red', label='Anomaly')

            plt.xlabel('Time')
            plt.ylabel('Ox')
            plt.legend()

        self.canvas.draw()

    def plotOnCanvas_Cl(self):
        self.figure.clear()
        index = self.ui.comboBox_Algo.currentIndex()
        if index == 0:
            df = graph(2)
            x = df.loc[:, "ds"]
            y = df.loc[:, "fact"]
            anomaly = df.loc[:, "anomaly"]
            plt.scatter(x[anomaly == 0], y[anomaly == 0], color='black', label='Normal')
            plt.scatter(x[anomaly != 0], y[anomaly != 0], color='red', label='Anomaly')

            plt.xlabel('Time')
            plt.ylabel('Cl')
            plt.legend()

        self.canvas.draw()

    def plotOnCanvas_Trub(self):
        self.figure.clear()
        index = self.ui.comboBox_Algo.currentIndex()
        if index == 0:
            df = graph(3)
            x = df.loc[:, "ds"]
            y = df.loc[:, "fact"]
            anomaly = df.loc[:, "anomaly"]
            plt.scatter(x[anomaly == 0], y[anomaly == 0], color='black', label='Normal')
            plt.scatter(x[anomaly != 0], y[anomaly != 0], color='red', label='Anomaly')

            plt.xlabel('Time')
            plt.ylabel('Trub')
            plt.legend()

        self.canvas.draw()

app = QApplication([])
mygui = My_GuI()
mygui.show()
app.exec_()
