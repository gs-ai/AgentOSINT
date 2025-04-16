import os
import sys
import logging
import shelve
import datetime
import functools
import csv
from distutils.version import StrictVersion
from configobj import ConfigObj
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QMessageBox, QFileDialog, QWidget,
    QVBoxLayout, QTableWidgetItem, QScrollArea, QHBoxLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QMenu
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from yapsy.PluginManager import PluginManagerSingleton
from models.LocationsList import LocationsTableModel
from models.Project import Project
from models.Location import Location
from models.PluginConfigurationListModel import PluginConfigurationListModel
from models.ProjectWizardPluginListModel import ProjectWizardPluginListModel
from models.ProjectWizardSelectedTargetsTable import ProjectWizardSelectedTargetsTable
from models.InputPlugin import InputPlugin
from models.ProjectTree import ProjectNode, LocationsNode, ProjectTreeModel, ProjectTreeNode
from components.PersonProjectWizard import PersonProjectWizard
from components.PluginsConfigurationDialog import PluginsConfigurationDialog
from components.FilterLocationsDateDialog import FilterLocationsDateDialog
from components.FilterLocationsPointDialog import FilterLocationsPointDialog
from components.AboutDialog import AboutDialog
from components.VerifyDeleteDialog import VerifyDeleteDialog
from components.UpdateCheckDialog import UpdateCheckDialog
from utilities import GeneralUtilities
from camoufox import anonymize_request, set_anonymity_level

# Set up logging
logger = logging.getLogger("creepy")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(os.getcwd(), 'creepy_main.log'))
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class AnalyzeProjectThread(QThread):
    locations_found = pyqtSignal(list)

    def __init__(self, project):
        super().__init__()
        self.project = project

    def run(self):
        try:
            logger.info("Starting analysis for project: %s", self.project["name"])
            locations = []
            for target in self.project["targets"]:
                request = anonymize_request({"target": target})
                result = subprocess.run(
                    ["creepy", "--search", request["target"]],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    logger.info("Locations found for target: %s", target)
                    locations.append(result.stdout)
                else:
                    logger.warning("Error analyzing target %s: %s", target, result.stderr)
            self.locations_found.emit(locations)
        except Exception as e:
            logger.error("Analysis failed: %s", e)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creepy Modernized")
        self.setGeometry(100, 100, 800, 600)

        set_anonymity_level("high")

        self.projects = []
        self.current_project = None

        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)
        self.web_view.setUrl(QUrl("https://example-map-view.com"))

    def analyze_project(self, project):
        if not project:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return

        self.current_project = project
        self.analysis_thread = AnalyzeProjectThread(project)
        self.analysis_thread.locations_found.connect(self.display_results)
        self.analysis_thread.start()

    def display_results(self, locations):
        if not locations:
            QMessageBox.information(self, "No Locations", "No locations found for this project.")
            return

        logger.info("Displaying results on the map.")
        for location in locations:
            self.web_view.page().runJavaScript(f"addMarker({location})")

    def load_projects(self):
        projects_dir = os.path.join(os.getcwd(), "projects")
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)

        project_files = [
            os.path.join(projects_dir, f) for f in os.listdir(projects_dir)
            if f.endswith(".db")
        ]

        self.projects = []
        for project_file in project_files:
            try:
                with shelve.open(project_file) as db:
                    self.projects.append(db["project"])
            except Exception as e:
                logger.error("Failed to load project %s: %s", project_file, e)

    def export_project_csv(self, project):
        if not project:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV", os.getcwd(), "CSV Files (*.csv)")
        if not file_name:
            return

        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("Timestamp, Latitude, Longitude, Location Name, Retrieved From, Context\n")
                for loc in project.get("locations", []):
                    f.write(
                        f"{loc['timestamp']}, {loc['latitude']}, {loc['longitude']}, "
                        f"{loc['name']}, {loc['source']}, {loc['context']}\n"
                    )
            logger.info("Project exported to CSV successfully: %s", file_name)
        except Exception as e:
            logger.error("Failed to export project: %s", e)
            QMessageBox.critical(self, "Export Error", "Failed to export project.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
