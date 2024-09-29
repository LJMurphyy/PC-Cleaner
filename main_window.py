import sys
from pathlib import Path
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QWidget, QListWidget, QListWidgetItem, QLabel, 
                               QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget)
import cleaner


class MainWidget(QWidget):
    _menu_items = ['Main Menu', 'Downloads Cleaner']

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setWindowTitle("Cleaner")

        # Create Title Bar
        self.title_widget = self.title_widget_creator()
        # self.title_widget.setFixedHeight(75) 

        # Create and Configure Menu Widget
        self.menu_widget = self.menu_widget_creator()
        self.menu_widget.setFixedWidth(300)
        self.menu_widget.currentItemChanged.connect(self.on_item_selected)

        # Manage Pages
        self.stacked_widget = QStackedWidget()

        # Create pages
        self.main_menu_page = self.create_main_menu_page()
        self.downloads_cleaner_page = self.create_downloads_cleaner_page()
        
        self.stacked_widget.addWidget(self.main_menu_page)
        self.stacked_widget.addWidget(self.downloads_cleaner_page)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.title_widget)

        # Content Layout
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.addWidget(self.menu_widget)
        self.content_layout.addWidget(self.stacked_widget)

        self.main_layout.addLayout(self.content_layout)

        self.setLayout(self.main_layout)

    def title_widget_creator(self):
        title_widget = QWidget()
        title_widget.setStyleSheet("""
            background-color: #D6D6D6;
        """)

        layout = QHBoxLayout(title_widget)

        image_logo = QPixmap("content/cleaner_logo_crosses.png")
        logo_label = QLabel()
        logo_label.setPixmap(image_logo)

        title_label = QLabel("Cleaner")
        title_label.setStyleSheet("""
            color: #000000;
            font-size: 24px;
        """)

        
        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        return title_widget


    def menu_widget_creator(self):
        # Create the menu widget
        menu_widget = QListWidget()
        for item in self._menu_items:
            new_item = QListWidgetItem(item)
            new_item.setTextAlignment(Qt.AlignCenter)
            menu_widget.addItem(new_item)

        menu_widget.setStyleSheet("""
            QListWidget {
                color: #000000;
                background-color: #D6D6D6;
                border: none;
                font-size: 16px;
            }

            QListWidget::item {
                height: 50px;
                width: 40px;
            }

            QListWidget::item:selected {
                background-color: #0099ff;
                border: none;
            }
            """)

        return menu_widget

    def create_main_menu_page(self):
        # Main menu page layout
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("This is a scalable automation program that cleans the downloads directory")
        # label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 20px;
        """)

        layout.addWidget(label)
        
        return page

    def create_downloads_cleaner_page(self):
        # Downloads cleaner page layout
        page = QWidget()
        layout = QVBoxLayout(page)
        self.downloads_button = QPushButton("Run")
        self.downloads_button.setStyleSheet("""
            QPushButton {
                background-color: white; 
                color: #000000; 
                border: 2px solid #0099ff;
                border-radius: 5px;
                font-size: 20px;
                padding: 15px 25px;
                height: 50px;
                          
            }
            QPushButton:hover {
                background-color: #0099ff;
                color: #ffffff;
            }
            """)
        self.downloads_button.clicked.connect(self.downloads_cleanup)
        label = QLabel("Sort all files in the Downloads directory into directores \naccording to the file extenstion")
        label.setStyleSheet("""
            font-size: 20px;
        """)

        

        layout.addWidget(label)
        layout.addWidget(self.downloads_button)
        return page

    @QtCore.Slot()
    def on_item_selected(self, current, previous):
        if current:
            selected_item = current.text()
            if selected_item == "Main Menu":
                self.stacked_widget.setCurrentWidget(self.main_menu_page)
            elif selected_item == "Downloads Cleaner":
                self.stacked_widget.setCurrentWidget(self.downloads_cleaner_page)
            # Handle other items if needed

    @QtCore.Slot()
    def downloads_cleanup(self):
        home_directory = Path.home()
        source = home_directory / "Downloads"

        clean_directory = cleaner.DownloadsCleaner(source)
        clean_directory.set_directories()
        clean_directory.clean_directory()

if __name__ == "__main__":
    app = QApplication()

    window = MainWidget()
    window.setStyleSheet("""
        background-color: #FFFFFF;
        color: #000000;
        """)
    
    window.resize(800, 600)

    window.show()
    sys.exit(app.exec())
