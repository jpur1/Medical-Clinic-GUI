# Medical-Clinic-GUI

This project is the development of a graphical user interface (GUI) for a Medical Clinic System, following a **Model-View-Controller (MVC)** design pattern. The system has been developed in phases: 

1. **Phase 1**: Model implementation and a file layer to ensure persistence of user data.  
2. **Phase 2**: Command-line interface (CLI) prototype.  
3. **Phase 3**: Integration of a GUI for a user-friendly experience.  

## Key Features

### User Interface (UI)
- Designed using the **PyQt6** framework.
- Features a main window for system interaction.
- The `ClinicGUI` class serves as the main interface for managing patients and notes.

### User Stories
The system includes several user stories implemented in the GUI:
- **Log in / Log out**  
- **Search patient**  
- **Manage patients**: Create, update, delete, and list patients using a `QTableView` widget.  
- **Choose current patient**  
- **Manage notes**: Create, update, delete, and list notes in a `QPlainTextEdit` widget.  
- **Data retrieval**: Display patient and note records in their respective widgets.  

### Data Management
- Maintains patient records and associated notes.  
- Provides functionality for manipulating and retrieving records while ensuring data consistency.  

### MVC Design
- The GUI acts as the **View** in the MVC pattern.  
- The Controller handles user inputs and updates the View by interacting with the Model.

### Modularization
- Code is organized into modules for a clean separation of concerns.  
- GUI code resides in the `clinic/gui` subdirectory.  
- Other related code is placed in their respective directories.  

### Manual Testing
- Manual testing ensures proper functionality of GUI interactions and data persistence.  
- While automated tests are assumed to pass, the focus is on verifying real-world usability.
