# Medical-Clinic-GUI

This project is the development of a graphical user interface (GUI) for a Medical Clinic System, following a Model-View-Controller (MVC) design pattern. The system has been developed in phases, starting with a model implementation and a file layer to ensure persistence of user data. The second phase involved a command-line interface (CLI) prototype, and now the final phase is focused on integrating a GUI for a user-friendly experience.

Key Features:
User Interface (UI): The GUI will be designed using the PyQt6 framework and will feature a main window where users can interact with the system. The ClinicGUI class will serve as the main interface for patient and note management.

User Stories: The system includes several user stories that must be implemented in the GUI:

Log in / Log out,
Search patient,
Create, update, delete, and list patients in a QTableView widget
Choose current patient,
Create, update, delete, and list notes in a QPlainTextEdit widget
Retrieve patient and note records in their respective widgets,
Data Management: The system maintains patient records and associated notes, and provides functionalities to manipulate and retrieve these records, all while ensuring data consistency.

MVC Design: The GUI serves as the "view" in the MVC pattern, while the controller interacts with the model, handling user inputs and updating the view accordingly.

Modularization: The code is organized in different modules, with the GUI code placed under the clinic/gui subdirectory and other related code in their respective directories, ensuring clean separation of concerns.

Manual Testing: While automated tests are assumed to pass, manual testing will be primarily used to verify that the system works as expected, especially for the GUI interactions and data persistence.

