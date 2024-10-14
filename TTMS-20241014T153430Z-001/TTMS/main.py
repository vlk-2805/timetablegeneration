import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from OneForAll import queries as ofa
import starter as kp
import csv,random
import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
                             QStackedWidget, QMessageBox, QComboBox)
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer, QPointF

class Snowflake:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()
        
    def reset(self):
        self.x = random.uniform(0, self.width)
        self.y = random.uniform(-self.height, 0)
        self.size = random.uniform(2, 5)
        self.speed = random.uniform(2, 4)
        self.opacity = random.uniform(0.5, 1.0)

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.reset()

class Snowfall(QWidget):
    def __init__(self, width, height, num_snowflakes=50):
        super().__init__()
        self.width = width
        self.height = height
        self.snowflakes = [Snowflake(width, height) for _ in range(num_snowflakes)]
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_snowflakes)
        self.timer.start(100)
        
    def update_snowflakes(self):
        for snowflake in self.snowflakes:
            snowflake.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for snowflake in self.snowflakes:
            painter.setPen(QPen(QColor(255, 255, 255, int(snowflake.opacity * 255)), snowflake.size))
            painter.drawPoint(QPointF(snowflake.x, snowflake.y))

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Page")
        self.setGeometry(100, 100, 1500, 900)

        
        self.background_image_path = "assets/mountains.jpg"

        self.users = {}
        with open("assets/TimetableDatabase/CSV/day_1.csv", newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  
            for row in csvreader:
                temp={'password':row[1],'role': row[9]}
                self.users[row[0]] = temp     
  

        self.setup_ui()  

    def setup_ui(self):
        
        pixmap = QPixmap(self.background_image_path)
        brush = QBrush(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

       
        self.create_main_page()
        self.create_student_login_form()
        self.create_staff_login_form()
        self.create_admin_login_form()
        self.create_sign_up_form()

        
        self.snowfall = Snowfall(self.width(), self.height(), num_snowflakes=70)
        self.snowfall.setAttribute(Qt.WA_TransparentForMouseEvents)  
        self.snowfall.setParent(self)
        self.snowfall.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
       
        self.snowfall.resize(self.size())

    def create_main_page(self):
        
        main_page_widget = QWidget()
        main_page_layout = QVBoxLayout(main_page_widget)
        main_page_layout.setAlignment(Qt.AlignCenter)

        # Add heading label
        heading_label = QLabel("𝑻𝒊𝒎𝒆𝒕𝒂𝒃𝒍𝒆 𝑴𝒂𝒏𝒂𝒈𝒆𝒎𝒆𝒏𝒕 𝑺𝒚𝒔𝒕𝒆𝒎")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-weight: bold; font-size: 30pt; color: darkblue;")
        main_page_layout.addWidget(heading_label)

        # Add buttons with smaller widths
        self.create_button(main_page_layout, "Student Login", self.show_student_login, width=120)
        self.create_button(main_page_layout, "Staff Login", self.show_staff_login, width=120)
        self.create_button(main_page_layout, "Admin Login", self.show_admin_login, width=120)
        self.create_button(main_page_layout, "Sign Up", self.show_sign_up, width=120)

        # Add main page widget to stacked widget
        self.stacked_widget.addWidget(main_page_widget)

    def create_button(self, layout, text, func, width=200):
        # Create and style buttons with specified width
        button = QPushButton(text)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 11pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        button.setFixedWidth(width)  # Set fixed width
        button.clicked.connect(func)
        layout.addWidget(button, alignment=Qt.AlignCenter)

    def create_student_login_form(self):
        # Create student login form
        student_form_widget = QWidget()
        student_form_layout = QVBoxLayout(student_form_widget)

        # Add transparent vertical rectangle as background
        transparent_rect_widget = QWidget()
        transparent_rect_layout = QVBoxLayout(transparent_rect_widget)
        transparent_rect_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 15px;")
        transparent_rect_widget.setMinimumHeight(450)
        transparent_rect_widget.setMinimumWidth(250)
        student_form_layout.addWidget(transparent_rect_widget, alignment=Qt.AlignCenter)

        # Add heading label
        heading_label = QLabel("Student Login")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-weight: bold; font-size: 20pt; color: darkblue;")
        transparent_rect_layout.addWidget(heading_label)

        # Add Digital ID label and input
        digital_id_label = QLabel("Digital ID:")
        digital_id_label.setAlignment(Qt.AlignCenter)  # Center-aligned
        digital_id_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(digital_id_label)

        student_id_input = QLineEdit()
        student_id_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(student_id_input)

        # Add password label and input
        password_label = QLabel("Password:")
        password_label.setAlignment(Qt.AlignCenter)  # Center-aligned
        password_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(password_label)

        student_password_input = QLineEdit()
        student_password_input.setEchoMode(QLineEdit.Password)
        student_password_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(student_password_input)

        # Add login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        login_button.clicked.connect(self.student_login)
        transparent_rect_layout.addWidget(login_button)

        # Add forgot password button
        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        forgot_password_button.clicked.connect(self.forgot_password)
        transparent_rect_layout.addWidget(forgot_password_button)

        # Add back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        back_button.clicked.connect(self.show_main_page)
        transparent_rect_layout.addWidget(back_button)

        # Store input fields
        self.student_id_input = student_id_input
        self.student_password_input = student_password_input

        # Add the student form widget to the stacked widget
        self.stacked_widget.addWidget(student_form_widget)

    def create_staff_login_form(self):
        # Create staff login form
        staff_form_widget = QWidget()
        staff_form_layout = QVBoxLayout(staff_form_widget)

        # Add transparent vertical rectangle as background
        transparent_rect_widget = QWidget()
        transparent_rect_layout = QVBoxLayout(transparent_rect_widget)
        transparent_rect_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 15px;")
        transparent_rect_widget.setMinimumHeight(450)
        transparent_rect_widget.setMinimumWidth(250)
        staff_form_layout.addWidget(transparent_rect_widget, alignment=Qt.AlignCenter)

        # Add heading label
        heading_label = QLabel("Staff Login")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-weight: bold; font-size: 20pt; color: darkblue;")
        transparent_rect_layout.addWidget(heading_label)

        # Add Staff ID label and input
        staff_id_label = QLabel("Staff ID:")
        staff_id_label.setAlignment(Qt.AlignCenter)  # Center-aligned
        staff_id_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(staff_id_label)

        staff_id_input = QLineEdit()
        staff_id_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(staff_id_input)

        # Add password label and input
        password_label = QLabel("Password:")
        password_label.setAlignment(Qt.AlignCenter)  # Center-aligned
        password_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(password_label)

        staff_password_input = QLineEdit()
        staff_password_input.setEchoMode(QLineEdit.Password)
        staff_password_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(staff_password_input)

        # Add login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        login_button.clicked.connect(self.staff_login)
        transparent_rect_layout.addWidget(login_button)

        # Add forgot password button
        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        forgot_password_button.clicked.connect(self.forgot_password)
        transparent_rect_layout.addWidget(forgot_password_button)

        # Add back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        back_button.clicked.connect(self.show_main_page)
        transparent_rect_layout.addWidget(back_button)

        # Store input fields
        self.staff_id_input = staff_id_input
        self.staff_password_input = staff_password_input

        # Add the staff form widget to the stacked widget
        self.stacked_widget.addWidget(staff_form_widget)
    def create_admin_login_form(self):
        # Create staff login form
        admin_form_widget = QWidget()
        admin_form_layout = QVBoxLayout(admin_form_widget)

        # Add transparent vertical rectangle as background
        transparent_rect_widget = QWidget()
        transparent_rect_layout = QVBoxLayout(transparent_rect_widget)
        transparent_rect_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 15px;")
        transparent_rect_widget.setMinimumHeight(450)
        transparent_rect_widget.setMinimumWidth(250)
        admin_form_layout.addWidget(transparent_rect_widget, alignment=Qt.AlignCenter)

        # Add heading label
        heading_label = QLabel("Admin Login")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-weight: bold; font-size: 20pt; color: darkblue;")
        transparent_rect_layout.addWidget(heading_label)

        # Add Staff ID label and input
        admin_id_label = QLabel("Admin ID:")
        admin_id_label.setAlignment(Qt.AlignCenter)  
        admin_id_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(admin_id_label)

        admin_id_input = QLineEdit()
        admin_id_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(admin_id_input)

        # Add password label and input
        password_label = QLabel("Password:")
        password_label.setAlignment(Qt.AlignCenter)  
        password_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(password_label)

        admin_password_input = QLineEdit()
        admin_password_input.setEchoMode(QLineEdit.Password)
        admin_password_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(admin_password_input)

        # Add login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        login_button.clicked.connect(self.admin_login)
        transparent_rect_layout.addWidget(login_button)

        # Add forgot password button
        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        forgot_password_button.clicked.connect(self.forgot_password)
        transparent_rect_layout.addWidget(forgot_password_button)

        # Add back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        back_button.clicked.connect(self.show_main_page)
        transparent_rect_layout.addWidget(back_button)

        # Store input fields
        self.admin_id_input = admin_id_input
        self.admin_password_input = admin_password_input

        # Add the staff form widget to the stacked widget
        self.stacked_widget.addWidget(admin_form_widget)

    def create_sign_up_form(self):
        # Create sign up form
        sign_up_form_widget = QWidget()
        sign_up_form_layout = QVBoxLayout(sign_up_form_widget)

        # Add transparent vertical rectangle as background
        transparent_rect_widget = QWidget()
        transparent_rect_layout = QVBoxLayout(transparent_rect_widget)
        transparent_rect_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 15px;")
        transparent_rect_widget.setMinimumHeight(450)
        transparent_rect_widget.setMinimumWidth(250)
        sign_up_form_layout.addWidget(transparent_rect_widget, alignment=Qt.AlignCenter)

        # Add heading label
        heading_label = QLabel("Sign Up")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-weight: bold; font-size: 20pt; color: darkblue;")
        transparent_rect_layout.addWidget(heading_label)

        # Add ID label and input
        digital_id_label = QLabel("ID:")
        digital_id_label.setAlignment(Qt.AlignCenter)
        digital_id_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(digital_id_label)

        digital_id_input = QLineEdit()
        digital_id_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(digital_id_input)

        # Add password label and input
        password_label = QLabel("Password:")
        password_label.setAlignment(Qt.AlignCenter)
        password_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(password_label)

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(password_input)

        # Add role selection label and dropdown
        role_label = QLabel("Role:")
        role_label.setAlignment(Qt.AlignCenter)
        role_label.setStyleSheet("color: darkblue; font-size: 14pt;")
        transparent_rect_layout.addWidget(role_label)

        role_dropdown = QComboBox()
        role_dropdown.addItems(["Student", "Staff","Admin"])
        role_dropdown.setStyleSheet("color: black; border: none; border-bottom: 2px solid black; padding: 5px;")
        transparent_rect_layout.addWidget(role_dropdown)

        # Add sign up button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        sign_up_button.clicked.connect(self.sign_up)
        transparent_rect_layout.addWidget(sign_up_button)

        # Add back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        back_button.clicked.connect(self.show_main_page)
        transparent_rect_layout.addWidget(back_button)

        # Store input fields
        self.sign_up_digital_id_input = digital_id_input ####
        self.sign_up_password_input = password_input
        self.sign_up_role_dropdown = role_dropdown

        # Add the sign up form widget to the stacked widget
        self.stacked_widget.addWidget(sign_up_form_widget)

    def student_login(self):
        student_id = self.student_id_input.text()
        password = self.student_password_input.text()
        self.data={}
        self.data[0]=student_id
        if student_id in self.users and self.users[student_id]["password"] == password:
            response = QMessageBox.information(self, "Login Successful", "Welcome, Student!")
            if response == QMessageBox.Ok:
                self.StudentOptions = QtWidgets.QMainWindow()
                self.ui = Ui_StudentOptions(self.data)
                self.ui.setupUi(self.StudentOptions )
                self.StudentOptions.showMaximized()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Digital ID or password")

    def staff_login(self):
        staff_id = self.staff_id_input.text()
        password = self.staff_password_input.text()
        self.data={}
        self.data[0]=staff_id
        if staff_id in self.users and self.users[staff_id]["password"] == password:
            response = QMessageBox.information(self, "Login Successful", "Welcome, Staff Member!")
            if response == QMessageBox.Ok:
                self.StaffOptions = QtWidgets.QMainWindow()
                self.ui = Ui_StaffOptions(self.data)
                self.ui.setupUi(self.StaffOptions )
                self.StaffOptions.showMaximized()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Staff ID or password")
    def admin_login(self):
        admin_id = self.admin_id_input.text()
        password = self.admin_password_input.text()

        if admin_id in self.users and self.users[admin_id]["password"] == password:
            response = QMessageBox.information(self, "Login Successful", "Welcome, ADMIN!")
            if response == QMessageBox.Ok:
                self.AdminOptions = QtWidgets.QMainWindow()
                self.ui = Ui_AdminOptions()
                self.ui.setupUi(self.AdminOptions)
                self.AdminOptions.showMaximized()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Admin ID or password")

    def forgot_password(self):
        QMessageBox.information(self, "Password Recovery", "Contact Administrator for password recovery", QMessageBox.Ok)

    def sign_up(self):
        digital_id = self.sign_up_digital_id_input.text()
        password = self.sign_up_password_input.text()
        role = self.sign_up_role_dropdown.currentText()

        if digital_id and password:
            self.users[digital_id] = {"password": password, "role": role}
            QMessageBox.information(self, "Sign Up Successful", f"Account created for {role}!")
            self.show_main_page()
        else:
            QMessageBox.warning(self, "Sign Up Failed", "Please fill in all fields.")

    def show_student_login(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_staff_login(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_admin_login(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_sign_up(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_main_page(self):
        self.stacked_widget.setCurrentIndex(0)

class Ui_StudentOptions(object):
    def __init__(self,data):
        self.data = data

    def setupUi(self, StudentOptions):
        self.StudentOptions = StudentOptions
        self.StudentOptions.setObjectName("StudentOptions")
        self.StudentOptions.setGeometry(100, 100, 1500, 900)
        self.centralwidget = QtWidgets.QWidget(StudentOptions)
        self.centralwidget.setObjectName("centralwidget")
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.StudentOptions.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.StudentOptions.setPalette(palette)
        self.StudentOptions.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.setSpacing(25)  
        self.verticalLayout.setContentsMargins(50, 50, 50, 50)
        self.ViewTimeTable = QtWidgets.QPushButton(self.centralwidget)
        self.ViewTimeTable.setGeometry(QtCore.QRect(850,200, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.ViewTimeTable.setFont(font)
        self.ViewTimeTable.setObjectName("ViewTimeTable")
        self.ViewTimeTable.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.ViewTimeTable)
        self.ViewSubjects = QtWidgets.QPushButton(self.centralwidget)
        self.ViewSubjects.setGeometry(QtCore.QRect(850, 320, 141, 41))
        self.ViewSubjects.setFont(font)
        self.ViewSubjects.setObjectName("ViewSubjects")
        self.ViewSubjects.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.ViewSubjects)
        self.GoBack = QtWidgets.QPushButton(self.centralwidget)
        self.GoBack.setGeometry(QtCore.QRect(850, 440, 141, 41))
        self.GoBack.setFont(font)
        self.GoBack.setObjectName("GoBack")
        self.GoBack.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.GoBack)
        self.ViewTimeTable.clicked.connect(self.open_timetable)
        self.ViewSubjects.clicked.connect(self.view_subjects)
        self.GoBack.clicked.connect(self.StudentOptions.close)
        StudentOptions.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StudentOptions)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 988, 21))
        self.menubar.setObjectName("menubar")
        StudentOptions.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StudentOptions)
        self.statusbar.setObjectName("statusbar")
        StudentOptions.setStatusBar(self.statusbar)

        self.retranslateUi(StudentOptions)
        QtCore.QMetaObject.connectSlotsByName(StudentOptions)

    def retranslateUi(self, AdminOptions):
        _translate = QtCore.QCoreApplication.translate
        AdminOptions.setWindowTitle(_translate("AdminOptions", "MainWindow"))
        self.ViewTimeTable.setText(_translate("AdminOptions", "View Timetable"))
        self.ViewSubjects.setText(_translate("AdminOptions", "View Subjects"))
        self.GoBack.setText(_translate("AdminOptions", "Go Back"))

    def view_subjects(self):
        print(self.data[0])
        self.ViewSubject = Ui_ViewSubjects(ofa.tqueries.fetch_subs(self.data[0]))
        self.ViewSubject.showMaximized()
    

    def open_timetable(self):
        self.ViewTimeTable = QtWidgets.QMainWindow()
        self.ui1 = Ui_TimetableOpen(self.data)
        self.ui1.setupUi(self.ViewTimeTable)
        self.ViewTimeTable.showMaximized()

class Ui_StaffOptions(object):
    def __init__(self,data):
        self.data = data

    def setupUi(self, StaffOptions):
        self.StaffOptions = StaffOptions
        self.StaffOptions.setObjectName("StaffOptions")
        self.StaffOptions.setGeometry(100, 100, 1500, 900)
        self.centralwidget = QtWidgets.QWidget(StaffOptions)
        self.centralwidget.setObjectName("centralwidget")
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.StaffOptions.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.StaffOptions.setPalette(palette)
        self.StaffOptions.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.setSpacing(25)  
        self.verticalLayout.setContentsMargins(50, 50, 50, 50)
        self.ViewTimeTable = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.ViewTimeTable.setFont(font)
        self.ViewTimeTable.setObjectName("ViewTimeTable")
        self.ViewTimeTable.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.ViewTimeTable)
        self.ViewClass = QtWidgets.QPushButton(self.centralwidget)
        self.ViewClass.setFont(font)
        self.ViewClass.setObjectName("ViewClass")
        self.ViewClass.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.ViewClass)
        self.GoBack = QtWidgets.QPushButton(self.centralwidget)
        self.GoBack.setFont(font)
        self.GoBack.setObjectName("GoBack")
        self.GoBack.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.GoBack)
        self.ViewTimeTable.clicked.connect(self.open_timetable)
        self.ViewClass.clicked.connect(self.view_class)
        self.GoBack.clicked.connect(self.StaffOptions.close)
        StaffOptions.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StaffOptions)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 988, 21))
        self.menubar.setObjectName("menubar")
        StaffOptions.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StaffOptions)
        self.statusbar.setObjectName("statusbar")
        StaffOptions.setStatusBar(self.statusbar)

        self.retranslateUi(StaffOptions)
        QtCore.QMetaObject.connectSlotsByName(StaffOptions)

    def retranslateUi(self, AdminOptions):
        _translate = QtCore.QCoreApplication.translate
        AdminOptions.setWindowTitle(_translate("AdminOptions", "MainWindow"))
        self.ViewTimeTable.setText(_translate("AdminOptions", "View Timetable"))
        self.ViewClass.setText(_translate("AdminOptions", "View Class"))
        self.GoBack.setText(_translate("AdminOptions", "Go Back"))

    def view_class(self):

        self.ViewClass = Ui_ViewClass(ofa.tqueries.fetch_class(self.data[0]))
        self.ViewClass.showMaximized()
    

    def open_timetable(self):
        self.ViewTimeTable = QtWidgets.QMainWindow()
        self.ui1 = Ui_TimetableOpen(self.data)
        self.ui1.setupUi(self.ViewTimeTable)
        self.ViewTimeTable.showMaximized()
   

class Ui_AdminOptions(object):
    def setupUi(self, AdminOptions):
        
        self.AdminOptions = AdminOptions
        self.AdminOptions.setObjectName("AdminOptions")
        self.AdminOptions.setGeometry(100, 100, 1500, 900)
        self.centralwidget = QtWidgets.QWidget(AdminOptions)
        self.centralwidget.setObjectName("centralwidget")
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.AdminOptions.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.AdminOptions.setPalette(palette)
        self.AdminOptions.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.setSpacing(25)  
        self.verticalLayout.setContentsMargins(50, 50, 50, 50)
        self.CreateTimeTable = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.CreateTimeTable.setFont(font)
        self.CreateTimeTable.setObjectName("CreateTimeTable")
        self.CreateTimeTable.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.CreateTimeTable)

        self.ModifyStaff = QtWidgets.QPushButton(self.centralwidget)
        self.ModifyStaff.setFont(font)
        self.ModifyStaff.setObjectName("ModifyStaff")
        self.ModifyStaff.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.ModifyStaff)

        self.ViewAvailability = QtWidgets.QPushButton(self.centralwidget)
        self.ViewAvailability.setFont(font)
        self.ViewAvailability.setObjectName("ViewAvailability")
        self.ViewAvailability.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.verticalLayout.addWidget(self.ViewAvailability)
    
        # Connect buttons to methods
        self.CreateTimeTable.clicked.connect(self.open_create_timetable)
        self.ModifyStaff.clicked.connect(self.open_modify_staff)
        self.ViewAvailability.clicked.connect(self.open_view_availability)

        AdminOptions.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdminOptions)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        self.menubar.setObjectName("menubar")
        AdminOptions.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdminOptions)
        self.statusbar.setObjectName("statusbar")
        AdminOptions.setStatusBar(self.statusbar)

        self.retranslateUi(AdminOptions)
        QtCore.QMetaObject.connectSlotsByName(AdminOptions)

    def retranslateUi(self, AdminOptions):
        _translate = QtCore.QCoreApplication.translate
        AdminOptions.setWindowTitle(_translate("AdminOptions", "MainWindow"))
        self.CreateTimeTable.setText(_translate("AdminOptions", "Generate Timetable"))
        self.ModifyStaff.setText(_translate("AdminOptions", "Add Staff"))
        self.ViewAvailability.setText(_translate("AdminOptions", "View Staff Availability"))

    def open_view_availability(self):
        self.StaffAvailability = QtWidgets.QMainWindow()
        self.ui1 = Ui_StaffAvailability()
        self.ui1.setupUi(self.StaffAvailability)
        self.StaffAvailability.showMaximized()
    
    def open_modify_staff(self):
        self.ModifyStaffWindow = QtWidgets.QMainWindow()
        self.ui1 = Ui_AddFaculty()
        self.ui1.setupUi(self.ModifyStaffWindow)
        self.ModifyStaffWindow.showMaximized()

    def open_create_timetable(self):
        self.data = {'LAB':{},'OTHERS':{},'SAME':{}}
        self.ClassSelectionWindow = QtWidgets.QMainWindow()
        self.ui1 = Ui_ClassSelection(self.data)
        self.ui1.setupUi(self.ClassSelectionWindow)
        self.ClassSelectionWindow.showMaximized()

class Ui_ClassSelection(object):
    def __init__(self, data):
        self.data = data

    def setupUi(self, ClassSelection):
        self.ClassSelection = ClassSelection
        self.ClassSelection.setObjectName("ClassSelection")
        self.ClassSelection.setGeometry(100, 100, 1500, 900)
        
        self.centralwidget = QtWidgets.QWidget(ClassSelection)
        self.centralwidget.setObjectName("centralwidget")
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.ClassSelection.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.ClassSelection.setPalette(palette)
        self.ClassSelection.setAutoFillBackground(True)

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.setSpacing(30)
        self.mainLayout.setContentsMargins(50, 50, 50, 50) 

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(30)

        
        labelFont = QtGui.QFont()
        labelFont.setPointSize(14)  

        semesterLabel = QtWidgets.QLabel("Choose Semester:")
        semesterLabel.setFont(labelFont)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("""
        QComboBox{
            color: black;
            font-size: 10pt;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }           
        """)
        self.formLayout.addRow(semesterLabel, self.comboBox)

        sectionLabel = QtWidgets.QLabel("Choose Section:")
        sectionLabel.setFont(labelFont)
        self.comboBox_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.setStyleSheet("""
        QComboBox{
            color: black;
            font-size: 10pt;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }
        """)
        self.formLayout.addRow(sectionLabel, self.comboBox_1)

        lectureHallLabel = QtWidgets.QLabel("Choose Lecture Hall:")
        lectureHallLabel.setFont(labelFont)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setStyleSheet("""
        QComboBox{
            color: black;
            font-size: 10pt;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }           
        """)
        self.formLayout.addRow(lectureHallLabel, self.comboBox_2)

        labRoomLabel = QtWidgets.QLabel("Choose Lab Room:")
        labRoomLabel.setFont(labelFont)
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.setStyleSheet("""
        QComboBox{
            color: black;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }
        """)
        self.formLayout.addRow(labRoomLabel, self.comboBox_3)

        # Add form layout to the main layout
        self.mainLayout.addLayout(self.formLayout)

        # Create and add the "NEXT" button
        self.movenext = QtWidgets.QPushButton(self.centralwidget)
        self.movenext.setObjectName("movenext")
        self.movenext.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.mainLayout.addWidget(self.movenext, alignment=QtCore.Qt.AlignCenter)

        for i in range(1,9):
            self.comboBox.addItem(str(i))
        for cl in ofa.cqueries.fetch():
            self.comboBox_1.addItem(cl)
        for lh in ofa.rqueries.fetch_lh():
            self.comboBox_2.addItem(lh)
        for lab in ofa.rqueries.fetch_lab():
            self.comboBox_3.addItem(lab)
            
        ClassSelection.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(ClassSelection)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 753, 21))
        self.menubar.setObjectName("menubar")
        ClassSelection.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(ClassSelection)
        self.statusbar.setObjectName("statusbar")
        ClassSelection.setStatusBar(self.statusbar)
        
        self.retranslateUi(ClassSelection)
        QtCore.QMetaObject.connectSlotsByName(ClassSelection)
        
        # Initialize data
        self.data[0] = self.comboBox_1.currentText()
        self.data[1] = self.comboBox_2.currentText()
        self.data[2] = self.comboBox_3.currentText()
        self.data[3]  = self.comboBox.currentText()

        # Connect signals
        self.movenext.clicked.connect(self.on_movenext_clicked)

    def retranslateUi(self, ClassSelection):
        _translate = QtCore.QCoreApplication.translate
        ClassSelection.setWindowTitle(_translate("ClassSelection", "MainWindow"))
        self.movenext.setText(_translate("ClassSelection", "NEXT"))

    def on_movenext_clicked(self):
        self.ClassSelection.close()
        self.data[0] = self.comboBox_1.currentText()
        self.data[1] = self.comboBox_2.currentText()
        self.data[2] = self.comboBox_3.currentText()
        self.data[3]  = self.comboBox.currentText()
        self.openSubjectSelectionWindow()

    def openSubjectSelectionWindow(self):
        self.subjectWindow = QtWidgets.QMainWindow()
        self.ui = Ui_SubjectSelection(self.data)
        self.ui.setupUi(self.subjectWindow)
        self.subjectWindow.showMaximized()


class Ui_SubjectSelection(object):
    def __init__(self, data):
        self.data = data

    def setupUi(self, SubjectSelection):
        self.SubjectSelection = SubjectSelection
        self.SubjectSelection.setObjectName("SubjectSelection")
        self.SubjectSelection.setGeometry(100, 100, 1500, 900)
        
        self.centralwidget = QtWidgets.QWidget(SubjectSelection)
        self.centralwidget.setObjectName("centralwidget")
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.SubjectSelection.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.SubjectSelection.setPalette(palette)
        self.SubjectSelection.setAutoFillBackground(True)

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setContentsMargins(50, 50, 50, 50)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(20)

        # Create and add labels with increased font size
        labelFont = QtGui.QFont()
        labelFont.setPointSize(12)  # Set the font size as desired

        typeLabel = QtWidgets.QLabel("Choose Type:")
        typeLabel.setFont(labelFont)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("""
        QComboBox{
            color: black;
            font-size: 13pt;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }           
        """)
        self.formLayout.addRow(typeLabel, self.comboBox)

        courseLabel = QtWidgets.QLabel("Choose Course:")
        courseLabel.setFont(labelFont)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setStyleSheet("""
        QComboBox{
            color: black;
            font-size: 13pt;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }
        """)
        self.formLayout.addRow(courseLabel, self.comboBox_2)

        staffLabel = QtWidgets.QLabel("Choose Staff:")
        staffLabel.setFont(labelFont)
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.setStyleSheet("""
        QComboBox{
            color: black;
            font-size: 13pt;
        }
        QComboBox QAbstractItemView{
            color: white;
            background-color :black;
        }
        """)
        self.formLayout.addRow(staffLabel, self.comboBox_3)

        # Add form layout to the main layout
        self.mainLayout.addLayout(self.formLayout)

        # Create and add the "Add Faculty" button
        self.AddFaculty = QtWidgets.QPushButton(self.centralwidget)
        self.AddFaculty.setObjectName("AddFaculty")
        self.AddFaculty.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 13pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.mainLayout.addWidget(self.AddFaculty, alignment=QtCore.Qt.AlignCenter)

        # Create and add the "Generate Timetable" button
        self.GenerateTimetable = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateTimetable.setObjectName("GenerateTimetable")
        self.GenerateTimetable.setEnabled(False)
        self.GenerateTimetable.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 13pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.mainLayout.addWidget(self.GenerateTimetable, alignment=QtCore.Qt.AlignCenter)

        SubjectSelection.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(SubjectSelection)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        self.menubar.setObjectName("menubar")
        SubjectSelection.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(SubjectSelection)
        self.statusbar.setObjectName("statusbar")
        SubjectSelection.setStatusBar(self.statusbar)

        self.retranslateUi(SubjectSelection)
        QtCore.QMetaObject.connectSlotsByName(SubjectSelection)
        
        # Initialize data
        self.comboBox.addItem("LAB", ofa.subqueries.fetch_labs(self.data[3]))
        self.comboBox.addItem("OTHERS", ofa.subqueries.fetch_others(self.data[3]))
        self.comboBox.addItem("SAME", ofa.subqueries.fetch_same(self.data[3]))
        
        
        # Connect signals
        self.comboBox.currentIndexChanged.connect(self.indexChanged1)
        self.comboBox_2.currentIndexChanged.connect(self.indexChanged2)
        self.indexChanged1(self.comboBox.currentIndex())
        self.AddFaculty.clicked.connect(lambda: self.addFaculty(self.comboBox, self.comboBox_2, self.comboBox_3))
        self.GenerateTimetable.clicked.connect(self.open_timetable_window)

    def retranslateUi(self, SubjectSelection):
        _translate = QtCore.QCoreApplication.translate
        SubjectSelection.setWindowTitle(_translate("SubjectSelection", "MainWindow"))
        self.AddFaculty.setText(_translate("SubjectSelection", "Add Faculty"))
        self.GenerateTimetable.setText(_translate("SubjectSelection", "Generate Timetable"))

    def indexChanged1(self, index):
        self.comboBox_2.clear()
        data = self.comboBox.itemData(index)
        if data is not None:
            for item in data:
                self.comboBox_2.addItem(item)

    def indexChanged2(self):
        self.comboBox_3.clear()
        data = ofa.squeries.most_free(ofa.subqueries.which_dept(self.comboBox_2.currentText()),6)
        if data is not None:
            for item in data:
                self.comboBox_3.addItem(item)


    def addFaculty(self, combo1, combo2, combo3):
        if combo1.currentText() == "LAB":
            room = self.data[2]
        else:
            room = self.data[1]
        key = combo1.currentText()
        inner_dict = {combo2.currentText(): [combo3.currentText(), room, self.data[0],ofa.subqueries.recommended_hrs(combo2.currentText())]}
        self.data[key].update(inner_dict)
        combo2.removeItem(combo2.currentIndex())
        if combo2.count() == 0:
            combo1.removeItem(combo1.currentIndex())
        if combo1.count() == 0:
            self.GenerateTimetable.setEnabled(True)


    def open_timetable_window(self):
        k=0
        while True:
            print(k)
            k+=1
            cid = self.data[0]
            print("Data passed to kp.pkp:", self.data, cid) 
            #ofa.restart()
            if k==15:
                QMessageBox.information(self.SubjectSelection, "Invalid Input", "Try different input \nAllocation with the following choices is not possible")
                ofa.restart()
                self.SubjectSelection.close()
                break
            if ((kp.pkp(self.data, cid) == 1 )):
                print("kp.pkp returned 1") 
                self.SubjectSelection.close()
                self.openTimetableWindow()
                break 

            else:
                ofa.restart()
                print("Try  - _ - again")  # Debug print statement
   

    def openTimetableWindow(self):
        self.TimetabletWindow = QtWidgets.QMainWindow()
        self.ui = Ui_TimetableOpen(self.data)
        self.ui.setupUi(self.TimetabletWindow)
        self.TimetabletWindow.showMaximized()

class Ui_ViewClass(QMainWindow):
    def __init__(self, data):
        super().__init__()

        # Set the title and size of the window
        self.setWindowTitle("Dynamic Table")
        self.setGeometry(100, 100, 1500, 900)

        # Create the main widget and layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        # Add a title label
        self.title_label = QLabel("Subject Table")
        self.title_label.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Create the table
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                border: 2px solid #dcdcdc;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
            QTableWidget::item {
                padding: 10px;
                border-right: 1px solid #dcdcdc;
                color: #333333;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #87cefa;
                color: black;
            }
        """)
        self.layout.addWidget(self.table_widget)

        # Set the main widget as the central widget of the window
        self.setCentralWidget(self.main_widget)

        # Populate the table with data
        self.populate_table(data)

        # Add a refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFont(QtGui.QFont('Arial', 12))
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #4682b4;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5a9bd3;
            }
        """)
        self.refresh_button.clicked.connect(lambda: self.populate_table(data))
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        self.layout.addLayout(button_layout)

    def populate_table(self, data):
        # Set the number of columns
        self.table_widget.setColumnCount(4)

        # Set the column headers
        self.table_widget.setHorizontalHeaderLabels(["S.No", "Class ID", "Class Name","Subject ID"])

        # Set the number of rows
        self.table_widget.setRowCount(len(data))

        # Populate the table with data
        for row_index, row_data in enumerate(data):
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_index + 1)))
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row_data[0]))
            self.table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(row_data[1]))
            self.table_widget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(row_data[2]))


        # Set column width and header style
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4682b4;
                color: white;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                padding: 5px;
            }
        """)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(True)
        self.table_widget.setGridStyle(Qt.SolidLine)

class  Ui_StaffAvailability(object):
    def setupUi(self, StaffAvailability):
        self.StaffAvailability= StaffAvailability
        StaffAvailability.setObjectName("StaffAvailability")
        StaffAvailability.setGeometry(100, 100, 1500, 900)
        StaffAvailability.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        StaffAvailability.setAutoFillBackground(False)
        StaffAvailability.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(StaffAvailability)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.StaffAvailability.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.StaffAvailability.setPalette(palette)
        self.StaffAvailability.setAutoFillBackground(True)

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.setSpacing(30)
        self.mainLayout.setContentsMargins(500, 50, 600, 50) 

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(30)

        self.StaffName = QtWidgets.QLabel(self.StaffAvailability)
        self.StaffName.setStyleSheet("QLabel {font-size : 12px; color:black;}")
        self.StaffName.setObjectName("StaffName")
        self.StaffName.setFont(font)

        self.DeptName = QtWidgets.QLabel(self.StaffAvailability)
        self.DeptName.setStyleSheet("QLabel {font-size : 12px; color:black;}")
        self.DeptName.setObjectName("DeptName")
        self.DeptName.setFont(font)

        self.StaffName_3 = QtWidgets.QLabel(self.StaffAvailability)
        self.StaffName_3.setObjectName("StaffName_3")
        self.StaffName_3.setStyleSheet("QLabel {font-size : 12px; color:black;}")

        self.lineEdit = QtWidgets.QLineEdit(self.StaffAvailability)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.addRow(self.StaffName, self.lineEdit)

        self.comboBox = QtWidgets.QComboBox(self.StaffAvailability)
        self.comboBox.setGeometry(QtCore.QRect(180, 80, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setStyleSheet("""
        QComboBox{
            color: black;
        }
        QComboBox QAbstractItemView{
            color: white;
        
            background-color :black;
        }
        """)
        self.formLayout.addRow(self.DeptName, self.comboBox)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.StaffAvailability)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.addRow(self.StaffName_3, self.lineEdit_2)
        self.mainLayout.addLayout(self.formLayout)

        self.Add = QtWidgets.QPushButton(self.StaffAvailability)
        self.Add.setCheckable(True)
        self.Add.setChecked(False)
        self.Add.setObjectName("Search")
        self.Add.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 9pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.mainLayout.addWidget(self.Add, alignment=QtCore.Qt.AlignCenter)

        StaffAvailability.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StaffAvailability)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1338, 21))
        self.menubar.setObjectName("menubar")
        StaffAvailability.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StaffAvailability)
        self.statusbar.setObjectName("statusbar")
        StaffAvailability.setStatusBar(self.statusbar)
        QtWidgets.QPushButton.setEnabled(self.Add, False)
        if(self.comboBox.currentIndexChanged):
            QtWidgets.QPushButton.setEnabled(self.Add, True)
            self.Add.clicked.connect(self.viewredirect)
        self.retranslateUi(StaffAvailability)
        QtCore.QMetaObject.connectSlotsByName(StaffAvailability)
        
    def viewredirect(self):
        self.staff_name=self.lineEdit.text()
        self.staff_id=self.lineEdit_2.text()
        self.dept_name=self.comboBox.currentText()
        self.StaffAvailability.close()
        self.StaffAvailabilityOpen = QtWidgets.QMainWindow()
        self.ui1 = Ui_StaffAvailabilityOpen(self.dept_name+self.staff_id)
        self.ui1.setupUi(self.StaffAvailabilityOpen)
        self.StaffAvailabilityOpen.showMaximized()
        

    def retranslateUi(self, AddFaculty):
        _translate = QtCore.QCoreApplication.translate
        AddFaculty.setWindowTitle(_translate("AddFaculty", "MainWindow"))
        self.StaffName.setText(_translate("AddFaculty", "Enter Staff Name"))
        self.DeptName.setText(_translate("AddFaculty", "Enter Department Name"))
        self.StaffName_3.setText(_translate("AddFaculty", "Enter Staff ID"))
        self.comboBox.setItemText(0, _translate("AddFaculty", "CSE"))
        self.comboBox.setItemText(1, _translate("AddFaculty", "IT"))
        self.comboBox.setItemText(2, _translate("AddFaculty", "ECE"))
        self.comboBox.setItemText(3, _translate("AddFaculty", "EEE"))
        self.comboBox.setItemText(4, _translate("AddFaculty", "MECH"))
        self.comboBox.setItemText(5, _translate("AddFaculty", "CIVIL"))
        self.comboBox.setItemText(6, _translate("AddFaculty", "BME"))
        self.comboBox.setItemText(7, _translate("AddFaculty", "CHEM"))
        self.comboBox.setItemText(8, _translate("AddFaculty", "ENG"))
        self.comboBox.setItemText(9, _translate("AddFaculty", "PHY"))
        self.comboBox.setItemText(10, _translate("AddFaculty", "MATH"))
        self.Add.setText(_translate("AddFaculty", "Search"))

class Ui_ViewSubjects(QMainWindow):
    def __init__(self, data):
        super().__init__()

        # Set the title and size of the window
        self.setWindowTitle("Dynamic Table")
        self.setGeometry(100, 100, 800, 600)

        # Create the main widget and layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        # Add a title label
        self.title_label = QLabel("Subject Table")
        self.title_label.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Create the table
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                border: 2px solid #dcdcdc;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
            QTableWidget::item {
                padding: 10px;
                border-right: 1px solid #dcdcdc;
                color: #333333;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #87cefa;
                color: black;
            }
        """)
        self.layout.addWidget(self.table_widget)

        # Set the main widget as the central widget of the window
        self.setCentralWidget(self.main_widget)

        # Populate the table with data
        self.populate_table(data)

        # Add a refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFont(QtGui.QFont('Arial', 12))
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #4682b4;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5a9bd3;
            }
        """)
        self.refresh_button.clicked.connect(lambda: self.populate_table(data))
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        self.layout.addLayout(button_layout)

    def populate_table(self, data):
        # Set the number of columns
        self.table_widget.setColumnCount(4)

        # Set the column headers
        self.table_widget.setHorizontalHeaderLabels(["S.No", "Subject Code", "Subject Name","Staff ID"])

        # Set the number of rows
        self.table_widget.setRowCount(len(data))

        # Populate the table with data
        for row_index, row_data in enumerate(data):
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_index + 1)))
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row_data[0]))
            self.table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(row_data[1]))
            self.table_widget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(row_data[2]))

        # Set column width and header style
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4682b4;
                color: white;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                padding: 5px;
            }
        """)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(True)
        self.table_widget.setGridStyle(Qt.SolidLine)


class Ui_AddFaculty(object):
    def setupUi(self, AddFaculty):
        AddFaculty.setObjectName("AddFaculty")
        AddFaculty.setGeometry(100, 100, 1500, 900)
        AddFaculty.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        AddFaculty.setAutoFillBackground(False)
        AddFaculty.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.AddFaculty= AddFaculty
        self.centralwidget = QtWidgets.QWidget(AddFaculty)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        pixmap = QPixmap("assets/mountains.jpg")
        brush = QBrush(pixmap.scaled(self.AddFaculty.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.AddFaculty.setPalette(palette)
        self.AddFaculty.setAutoFillBackground(True)

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.setSpacing(30)
        self.mainLayout.setContentsMargins(500, 50, 600, 50) 

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(30)

        self.StaffName = QtWidgets.QLabel(self.AddFaculty)
        self.StaffName.setStyleSheet("QLabel {font-size : 14px; color:black;}")
        self.StaffName.setObjectName("StaffName")
        self.StaffName.setFont(font)

        self.DeptName = QtWidgets.QLabel(self.AddFaculty)
        self.DeptName.setStyleSheet("QLabel {font-size : 14px; color:black;}")
        self.DeptName.setObjectName("DeptName")
        self.DeptName.setFont(font)

        self.StaffName_3 = QtWidgets.QLabel(self.AddFaculty)
        self.StaffName_3.setObjectName("StaffName_3")
        self.StaffName_3.setStyleSheet("QLabel {font-size : 14px; color:black;}")

        self.lineEdit = QtWidgets.QLineEdit(self.AddFaculty)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.addRow(self.StaffName, self.lineEdit)

        self.comboBox = QtWidgets.QComboBox(self.AddFaculty)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setStyleSheet("""
        QComboBox{
            color: black;
        }
        QComboBox QAbstractItemView{
            color: white;
        
            background-color :black;
        }
        """)
        self.formLayout.addRow(self.DeptName, self.comboBox)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.AddFaculty)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.addRow(self.StaffName_3, self.lineEdit_2)
        self.mainLayout.addLayout(self.formLayout)

        self.Add = QtWidgets.QPushButton(self.AddFaculty)
        self.Add.setCheckable(True)
        self.Add.setChecked(False)
        self.Add.setObjectName("Search")
        self.Add.setStyleSheet(
            """
            QPushButton {
                background-color: lightblue;
                color: black;
                border-radius: 15px;
                font-size: 14pt;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: darkblue;
                color: white;
            }
            """
        )
        self.mainLayout.addWidget(self.Add, alignment=QtCore.Qt.AlignCenter)

        AddFaculty.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AddFaculty)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1338, 21))
        self.menubar.setObjectName("menubar")
        AddFaculty.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AddFaculty)
        self.statusbar.setObjectName("statusbar")
        AddFaculty.setStatusBar(self.statusbar)
        QtWidgets.QPushButton.setEnabled(self.Add, False)
        if(self.comboBox.currentIndexChanged):
            QtWidgets.QPushButton.setEnabled(self.Add, True)
            self.Add.clicked.connect(self.adredirect)
        self.retranslateUi(AddFaculty)
        QtCore.QMetaObject.connectSlotsByName(AddFaculty)
        
    def adredirect(self):
        self.staff_name=self.lineEdit.text()
        self.staff_id=self.lineEdit_2.text()
        self.dept_name=self.comboBox.currentText()
        print(self.staff_name,self.staff_id,self.dept_name)
        ofa.squeries.add_staff(self.staff_name,self.staff_id,self.dept_name)
        QMessageBox.information(self.AddFaculty, "Success", "Addition of staff done!")
        self.AddFaculty.close()
        

    def retranslateUi(self, AddFaculty):
        _translate = QtCore.QCoreApplication.translate
        AddFaculty.setWindowTitle(_translate("AddFaculty", "MainWindow"))
        self.StaffName.setText(_translate("AddFaculty", "Enter Staff Name"))
        self.DeptName.setText(_translate("AddFaculty", "Enter Department Name"))
        self.StaffName_3.setText(_translate("AddFaculty", "Enter Staff ID "))
        self.comboBox.setItemText(0, _translate("AddFaculty", "CSE"))
        self.comboBox.setItemText(1, _translate("AddFaculty", "IT"))
        self.comboBox.setItemText(2, _translate("AddFaculty", "ECE"))
        self.comboBox.setItemText(3, _translate("AddFaculty", "EEE"))
        self.comboBox.setItemText(4, _translate("AddFaculty", "MECH"))
        self.comboBox.setItemText(5, _translate("AddFaculty", "CIVIL"))
        self.comboBox.setItemText(6, _translate("AddFaculty", "BME"))
        self.comboBox.setItemText(7, _translate("AddFaculty", "CHEM"))
        self.comboBox.setItemText(8, _translate("AddFaculty", "ENG"))
        self.comboBox.setItemText(9, _translate("AddFaculty", "PHY"))
        self.comboBox.setItemText(10, _translate("AddFaculty", "MATH"))
        self.Add.setText(_translate("AddFaculty", "Add"))

class Ui_TimetableOpen(object):
    def __init__(self, data):
        self.data = data

    def setupUi(self, TimetableOpen):
        self.TimetableOpen = TimetableOpen
        TimetableOpen.setObjectName("TimetableOpen")
        TimetableOpen.setGeometry(100, 100, 1500, 900)  # Set initial size
        self.centralwidget = QtWidgets.QWidget(TimetableOpen)
        self.centralwidget.setObjectName("centralwidget")
        self.timetable = QtWidgets.QTableWidget(self.centralwidget)
        self.timetable.setGeometry(QtCore.QRect(0, 0, 1375, 650))
        self.timetable.setGridStyle(QtCore.Qt.SolidLine)
        self.timetable.setRowCount(6)
        self.timetable.setColumnCount(8)
        self.timetable.setObjectName("timetable")

        # Resize policies
        self.timetable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.timetable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Example: Fetch timetable data
        data = ofa.tqueries.fetch_timetable(self.data[0])
        fhours = ["P&T", "ICELL", "Library", "Mentor", "PED", "Project(IFSP)"]

        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(cell))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFont(QtGui.QFont("Arial", 12))
                if cell=="0":
                    item = QtWidgets.QTableWidgetItem("Free")
                    item.setBackground(QtGui.QColor(40, 198, 40))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFont(QtGui.QFont("Arial", 12))
                # Setting different background colors based on cell content
                elif cell in ['', '8:00 AM - 8:50 AM', '8:50 AM - 9:40 AM', '10:00 AM - 10:50 AM', '10:50 AM - 11:40 AM', '12:45 PM - 1:35 PM', '1:35 PM - 2:25 PM', '2:50 PM - 3:40 PM', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                    item.setBackground(QtGui.QColor(154, 210, 227))
                elif ofa.subqueries.is_lab(cell):
                    item.setBackground(QtGui.QColor(18, 198, 201))
                elif cell in fhours:
                    item.setBackground(QtGui.QColor(40, 198, 40))
                else:
                    item.setBackground(QtGui.QColor(18, 137, 201))

                self.timetable.setItem(i, j, item)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 650, 161, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Continue")
        self.pushButton_2.setStyleSheet("background-color: lightblue; color: white; font-size: 14px; border-radius: 5px;")
        self.pushButton_2.clicked.connect(self.connect_continue)

        TimetableOpen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TimetableOpen)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1800, 21))
        self.menubar.setObjectName("menubar")
        TimetableOpen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TimetableOpen)
        self.statusbar.setObjectName("statusbar")
        TimetableOpen.setStatusBar(self.statusbar)

        self.retranslateUi(TimetableOpen)
        QtCore.QMetaObject.connectSlotsByName(TimetableOpen)

    def connect_continue(self):
        ofa.updatecsv()
        self.TimetableOpen.close()

    def retranslateUi(self, TimetableOpen):
        _translate = QtCore.QCoreApplication.translate
        TimetableOpen.setWindowTitle(_translate("TimetableOpen", "Timetable"))

class Ui_StaffAvailabilityOpen(object):
    def __init__(self,staff_id):
        self.staff_id = staff_id

    def setupUi(self, StaffAvailabilityOpen):
        StaffAvailabilityOpen.setObjectName("StaffAvailabilityOpen")
        StaffAvailabilityOpen.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(StaffAvailabilityOpen)
        self.centralwidget.setObjectName("centralwidget")
        self.timetable = QtWidgets.QTableWidget(self.centralwidget)
        self.timetable.setGeometry(QtCore.QRect(0, 10, 1450, 600))
        self.timetable.setAutoFillBackground(True)
        self.timetable.setGridStyle(QtCore.Qt.SolidLine)
        self.timetable.setRowCount(6)
        self.timetable.setColumnCount(8)
        self.timetable.setObjectName("timetable")
        self.timetable.horizontalHeader().setVisible(False)
        self.timetable.horizontalHeader().setCascadingSectionResizes(False)
        self.timetable.verticalHeader().setVisible(False)
        data=ofa.tqueries.fetch_timetable(self.staff_id)
        for i, row in enumerate(data):
            self.timetable.setRowHeight(i,100)
            for j, cell in enumerate(row):
                if cell in ['', '8:00 AM - 8:50 AM', '8:50 AM - 9:40 AM', '10:00 AM - 10:50 AM', '10:50 AM - 11:40 AM', '12:45 PM - 1:35 PM','1:35 PM - 2:25 PM','2:50 PM - 3:40 PM','Monday','Tuesday','Wednesday','Thursday','Friday'] :
                    item = QtWidgets.QTableWidgetItem(str(cell))
                    item.setBackground(QtGui.QColor(154, 210, 227))
                    self.timetable.setColumnWidth(j,105)
                    item.setTextAlignment(QtCore.Qt.AlignCenter) 
                    self.timetable.setItem(i, j, item)
                else:
                    if cell=="0":
                        self.timetable.setColumnWidth(j,180)
                        item = QtWidgets.QTableWidgetItem("Available")
                        item.setBackground(QtGui.QColor(0, 205, 0))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.timetable.setItem(i, j, item)
                    else:
                        self.timetable.setColumnWidth(j,180)
                        item = QtWidgets.QTableWidgetItem("Occupied")
                        item.setBackground(QtGui.QColor(205, 0, 0))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.timetable.setItem(i, j, item)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(565, 645, 161, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(StaffAvailabilityOpen.close)
        StaffAvailabilityOpen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StaffAvailabilityOpen)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1255, 21))
        self.menubar.setObjectName("menubar")
        StaffAvailabilityOpen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StaffAvailabilityOpen)
        self.statusbar.setObjectName("statusbar")
        StaffAvailabilityOpen.setStatusBar(self.statusbar)
        self.retranslateUi(StaffAvailabilityOpen)
        QtCore.QMetaObject.connectSlotsByName(StaffAvailabilityOpen)

    def retranslateUi(self, TimetableOpen):
        _translate = QtCore.QCoreApplication.translate
        TimetableOpen.setWindowTitle(_translate("StaffAvailabilityOpen", "MainWindow"))
        self.pushButton_2.setText(_translate("StaffAvailabilityOpen", "Continue"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.AdminOptionsWindow = QtWidgets.QMainWindow()
        self.ui = Ui_AdminOptions()
        self.ui.setupUi(self.AdminOptionsWindow)
        self.AdminOptionsWindow.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_page = MainPage()
    main_page.showMaximized()
    sys.exit(app.exec_())


    