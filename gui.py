
import sys
from datetime import date
import time
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6 import QtTest
from controller import *

SPECIALIZATIONS_DICTIONARY = {'Anatomical Pathology': 0, 'Anesthesiology': 1, 'Cardiology': 2, 'Cardiovascular/Thoracic Surgery': 3, 'Clinical Immunology/Allergy': 4,
            'Critical Care Medincine': 5, 'Dermatology': 6, 'Diagnostic Radiology': 7, 'Emergency Medicine': 8, 'Endocrinology And Metabolism': 9, 'Family Medicine': 10,
            'Gastroenterology': 11, 'General Internal Medicine': 12, 'General Surgery': 13, 'General/Clinical Pathology': 14, 'Geriatric Medicine': 15, 'Hematology': 16,
            'Medical Biochemistry': 17, 'Medical Genetics': 18, 'Medical Microbiology And Infectious Diseases': 19, 'Medical Oncology': 20, 'Nephrology': 21, 'Neurology': 22,
            'Neurosurgery': 23, 'Nuclear Medicine': 24, 'Obstetrics/Gyenecology': 25, 'Occupational Medicine': 26, 'Opthalmology': 27, 'Orthopedic Surgery': 28, 'Otolaryngology': 29,
            'Pediatrics': 30, 'Physical Medicine And Rehabilitation (PM & R)': 31, 'Plastic Surgery': 32}
            
GENDER_DICTIONARY = {'Male': 0, 'Female': 1, 'Non-Binary': 2}

class MainWindow(QMainWindow):
    def __init__(self):
        '''Initializer for the main window'''
        super().__init__()
        uic.loadUi('DMShome.ui', self)
        self.addDoctorWidgetsSetup()
        self.modifyDoctorWidgetsSetup()
        self.addPatientWidgetsSetup()
        self.modifyPatientWidgetsSetup()

    def qLabelStringChangeWait(self, label_name: QLabel, new_text: str, wait_time: float = 1500):
        '''Waits the specified amount of time before changing the QLabel'''
        QtTest.QTest.qWait(wait_time)
        label_name.setText(new_text)

    def clearAddDoctorFieldsAfterAdding(self, first_name: QLabel, last_name: QLabel, phone_number: QLabel, email: QLabel, age: QSpinBox, gender: QComboBox, address: QLabel,\
        specialization: QComboBox, years_of_experience: QSpinBox):
        '''This function will clear / reset the fields of the add doctor tab.'''
        self.clearPersonInfoFields(first_name, last_name, phone_number, email, age, gender, address)
        specialization.setCurrentIndex(-1)
        years_of_experience.setValue(0)

    def clearAddPatientFieldsAfterAdding(self, first_name: QLabel, last_name: QLabel, phone_number: QLabel, email: QLabel, age: QSpinBox, gender: QComboBox, address: QLabel):
        '''This function will clear the fields of the add patient tab'''
        self.clearPersonInfoFields(first_name, last_name, phone_number, email, age, gender, address)

    def clearPersonInfoFields(self, first_name: QLabel, last_name: QLabel, phone_number: QLabel, email: QLabel, age: QSpinBox, gender: QComboBox, address: QLabel):
        '''This function is called when the clearAddPatientFieldsAfterAdding or clearAddDoctorFieldsAfterAdding and contains the common information between them'''
        first_name.setText('')
        last_name.setText('')
        phone_number.setText('')
        email.setText('')
        age.setValue(0)
        gender.setCurrentIndex(-1)
        address.setText('')

    def populateOrRefreshModifyTabInformation(self, dictionary: dict, dictionary_reference: str, id: QLabel, first_name: QLabel, last_name: QLabel, phone_number: QLabel, email: QLabel, age: QSpinBox,\
        gender: QComboBox, address: QLabel):
        '''This function is called when the the fields need to be populated or updated to reflect the current doctor/patient selection, and contains the common information between them.
         In the controller module, get patient or doctor info by id functions return a dictionary, that's the dictionary parameter. The dictionary reference is the function will be able to
         change the text in the id field to the correct text'''
        
        id.setText(str(dictionary[f"{dictionary_reference}Id"]))
        first_name.setText(dictionary['firstName'])
        last_name.setText(dictionary['lastName'])
        phone_number.setText(dictionary['phoneNumber'])
        email.setText(dictionary['email'])
        age.setValue(dictionary['age'])
        gender.setCurrentIndex(GENDER_DICTIONARY[dictionary['gender']])
        address.setText(dictionary['address'])

    def refreshModifyTab(self, tab_refernce: str):
        '''This function takes a tab reference as a string and uses the combo box names to clear their data and refresh it'''
        if tab_refernce == 'doctor':
            self.doctorNameComboBoxModifyTab.clear()
            colNames, rows = getDoctorIdsAndNames()
            row_counter = 0
            for row in rows:
                row_counter += 1

            if row_counter != 0:
                for row in rows:
                    self.doctorNameComboBoxModifyTab.addItem(row[1], userData = row[0])
            else:
                pass

        elif tab_refernce == 'patient':
            self.patientNameComboBoxModifyTab.clear()
            colNames, rows = getPatientIdsAndNames()
            row_counter = 0
            for row in rows:
                row_counter += 1

            if row_counter != 0:
                for row in rows:
                    self.patientNameComboBoxModifyTab.addItem(row[1], userData = row[0])
            else:
                pass

    def addDoctorWidgetsSetup(self):
        '''This function initializes all variables that will later need to be accessed in the Add Doctor Tab'''
        
        self.firstNameInputAddDoctorTab = self.findChild(QLineEdit, 'firstNameInputAddDoctorTab')
        self.lastNameInputAddDoctorTab = self.findChild(QLineEdit, 'lastNameInputAddDoctorTab')
        self.phoneNumberInputAddDoctorTab = self.findChild(QLineEdit, 'phoneNumberInputAddDoctorTab')
        self.emailInputAddDoctorTab = self.findChild(QLineEdit, 'emailInputAddDoctorTab')
        self.ageSelectorAddDoctorTab = self.findChild(QSpinBox, 'ageSelectorAddDoctorTab')
        self.genderSelectorAddDoctorTab = self.findChild(QComboBox, 'genderSelectorAddDoctorTab')
        self.addressInputAddDoctorTab = self.findChild(QLineEdit, 'addressInputAddDoctorTab')
        self.specializationSelectorAddDoctorTab = self.findChild(QComboBox, 'specializationSelectorAddDoctorTab')
        self.yearsOfExperienceSelectorAddDoctorTab = self.findChild(QSpinBox, 'yearsOfExperienceSelectorAddDoctorTab')

        self.addDoctorButton = self.findChild(QPushButton, 'addDoctorButton')
        self.addDoctorButton.clicked.connect(self.addDoctorButtonHandler)

        self.addDoctorFeedback = self.findChild(QLabel, 'addDoctorFeedback')

    def addDoctorButtonHandler(self):
        '''This function will read all the data from the gui variables defined in the addDoctorWidgetsSetup function and call the add_doctor function with the read data'''
        try:
            first_name = self.firstNameInputAddDoctorTab.text()
            last_name = self.lastNameInputAddDoctorTab.text()
            phone_number = self.phoneNumberInputAddDoctorTab.text()
            email = self.emailInputAddDoctorTab.text()
            age = int(self.ageSelectorAddDoctorTab.cleanText())
            gender = self.genderSelectorAddDoctorTab.currentIndex()
            if gender == 0:
                gender = 'Male'
            elif gender == 1:
                gender = 'Female'
            elif gender == 2:
                gender = 'Non-Binary'
            address = self.addressInputAddDoctorTab.text()
            specialization = self.specializationSelectorAddDoctorTab.currentText()
            years_of_experience = int(self.yearsOfExperienceSelectorAddDoctorTab.cleanText())
            result = add_doctor(first_name, last_name, phone_number, email, age, gender, address, specialization, years_of_experience)
            if result == 1:
                self.qLabelStringChangeWait(self.addDoctorFeedback, 'Sucessfully Added', 200)
                self.qLabelStringChangeWait(self.addDoctorFeedback, "", 1500)
                self.clearAddDoctorFieldsAfterAdding(self.firstNameInputAddDoctorTab, self.lastNameInputAddDoctorTab, self.phoneNumberInputAddDoctorTab, self.emailInputAddDoctorTab,\
                    self.ageSelectorAddDoctorTab, self.genderSelectorAddDoctorTab, self.addressInputAddDoctorTab, self.specializationSelectorAddDoctorTab, self.yearsOfExperienceSelectorAddDoctorTab)
                self.refreshModifyTab('doctor')
            elif result == 0:
                self.qLabelStringChangeWait(self.addDoctorFeedback, 'Failure', 200)
                self.qLabelStringChangeWait(self.addDoctorFeedback, "", 3000)
        except Exception as e:
            print(e)

    def modifyDoctorWidgetsSetup(self):
        '''This function initializes all variables that will later need to be accessed in the Modify Doctor Tab'''

        # initializing all objects
        self.doctorNameComboBoxModifyTab = self.findChild(QComboBox, 'doctorNameComboBoxModifyTab')
        self.doctorIdLineEditReadOnlyModifyTab = self.findChild(QLineEdit, 'doctorIdLineEditReadOnlyModifyTab')
        self.doctorFirstNameLineEditModifyTab = self.findChild(QLineEdit, 'doctorFirstNameLineEditModifyTab')
        self.doctorLastNameLineEditModifyTab = self.findChild(QLineEdit, 'doctorLastNameLineEditModifyTab')
        self.doctorPhoneNumberLineEditModifyTab = self.findChild(QLineEdit, 'doctorPhoneNumberLineEditModifyTab')
        self.doctorEmailLineEditModifyTab = self.findChild(QLineEdit, 'doctorEmailLineEditModifyTab')
        self.doctorAgeSelectorModifyTab = self.findChild(QSpinBox, 'doctorAgeSelectorModifyTab')
        self.doctorGenderSelectorModifyTab = self.findChild(QComboBox, 'doctorGenderSelectorModifyTab')
        self.doctorAddressLineEditModifyTab = self.findChild(QLineEdit, 'doctorAddressLineEditModifyTab')
        self.specializationSelectorModifyDoctorTab = self.findChild(QComboBox, 'specializationSelectorModifyDoctorTab')
        self.yearsOfExperienceSelectorModifyTab = self.findChild(QSpinBox, 'yearsOfExperienceSelectorModifyTab')

        self.doctorSaveChangesButton = self.findChild(QPushButton, 'doctorSaveChangesButton')
        self.doctorSaveChangesButton.clicked.connect(self.doctorSaveChangesButtonHandler)

        self.doctorDeleteButton = self.findChild(QPushButton, 'doctorDeleteButton')
        self.doctorDeleteButton.clicked.connect(self.doctorDeleteButtonHandler)

        self.modifyDoctorTabFeedbackLabel = self.findChild(QLabel, 'modifyDoctorTabFeedbackLabel')

        # the following conditional will allow the program to continue to run if no doctors currently exist

        # this section will populate the combo box with all doctor names
        colNames, rows = getDoctorIdsAndNames()
        row_counter = 0
        for row in rows:
            row_counter += 1
        
        if row_counter != 0:
            for row in rows:
                self.doctorNameComboBoxModifyTab.addItem(row[1], userData = row[0]) # row[1] is the first and last name concatonation
        else:
            pass

        self.populateOrRefreshAllDoctorInformation(getDoctorInfoById(rows[0][0]))

        self.doctorNameComboBoxModifyTab.currentIndexChanged.connect(self.doctorNameComboBoxModifyTabCurrentIndexChangedHandler)

    def doctorNameComboBoxModifyTabCurrentIndexChangedHandler(self):
        '''This function will call the populateOrRefreshAllDoctorInformation whenever the current doctor selection / index changes.'''
        try:
            docId = self.doctorNameComboBoxModifyTab.currentData()
            self.populateOrRefreshAllDoctorInformation(getDoctorInfoById(docId))
        except Exception as e:
            print(e)

    def populateOrRefreshAllDoctorInformation(self, docInfo):
        '''This function will populate all the fields in the Modify Doctor tab with the information of the currently selected doctor'''

        self.populateOrRefreshModifyTabInformation(docInfo, 'doctor', self.doctorIdLineEditReadOnlyModifyTab, self.doctorFirstNameLineEditModifyTab,\
            self.doctorLastNameLineEditModifyTab, self.doctorPhoneNumberLineEditModifyTab, self.doctorEmailLineEditModifyTab, self.doctorAgeSelectorModifyTab,\
                self.doctorGenderSelectorModifyTab, self.doctorAddressLineEditModifyTab)

        self.specializationSelectorModifyDoctorTab.setCurrentIndex(SPECIALIZATIONS_DICTIONARY[docInfo['specialization']])
        self.yearsOfExperienceSelectorModifyTab.setValue(docInfo['yearsOfExperience'])
        
    def doctorSaveChangesButtonHandler(self):
        '''This function will read all the data from the gui variables defined in the modifyDoctorWidgetsSetup function and call the modify_doctor function with the read data'''
        try:
            doctor_id = self.doctorIdLineEditReadOnlyModifyTab.text()
            first_name = self.doctorFirstNameLineEditModifyTab.text()
            last_name = self.doctorLastNameLineEditModifyTab.text()
            phone_number = self.doctorPhoneNumberLineEditModifyTab.text()
            email = self.doctorEmailLineEditModifyTab.text()
            age = int(self.doctorAgeSelectorModifyTab.cleanText())
            gender = self.doctorGenderSelectorModifyTab.currentText()
            address = self.doctorAddressLineEditModifyTab.text()
            specialization = self.specializationSelectorModifyDoctorTab.currentText()
            years_of_experience = int(self.yearsOfExperienceSelectorModifyTab.cleanText())
            result = modify_doctor(doctor_id = doctor_id, first_name = first_name, last_name = last_name
            , phone_number = phone_number, email = email, age = age, gender = gender, address = address, specialization = specialization, years_of_experience = years_of_experience)
            if result == 1:
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, 'Changes Saved', 200)
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, "", 1500)
                self.refreshModifyTab('doctor')
            elif result == 0:
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, 'Failure', 200)
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, "", 3000)
        except Exception as e:
            print(e)

    def doctorDeleteButtonHandler(self):
        '''This function will read the current selected doctors ID and pass the argument into and then call the delete_doctor function'''
        try:
            doctor_id = int(self.doctorIdLineEditReadOnlyModifyTab.text())
            result = delete_doctor(doctor_id = doctor_id)
            if result == 1:
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, "Doctor Successfully Deleted", 200)
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, "", 1500)
                self.refreshModifyTab('doctor')
            elif result == 0:
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, "Failure", 200)
                self.qLabelStringChangeWait(self.modifyDoctorTabFeedbackLabel, "", 3000)
        except Exception as e:
            print(e)
    
        
    def addPatientWidgetsSetup(self):
        '''This function initializes all variables that will later need to be accessed in the Add Patient Tab'''
        self.firstNameInputAddPatientTab = self.findChild(QLineEdit, 'firstNameInputAddPatientTab')
        self.lastNameInputAddPatientTab = self.findChild(QLineEdit, 'lastNameInputAddPatientTab')
        self.phoneNumberInputAddPatientTab = self.findChild(QLineEdit, 'phoneNumberInputAddPatientTab')
        self.emailInputAddPatientTab = self.findChild(QLineEdit, 'emailInputAddPatientTab')
        self.ageSelectorAddPatientTab = self.findChild(QSpinBox, 'ageSelectorAddPatientTab')
        self.genderSelectorAddPatientTab = self.findChild(QComboBox, 'genderSelectorAddPatientTab')
        self.addressInputAddPatientTab = self.findChild(QLineEdit, 'addressInputAddPatientTab')

        self.addPatientButton = self.findChild(QPushButton, 'addPatientButton')
        self.addPatientButton.clicked.connect(self.addPatientButtonHandler)


        self.addPatientFeedback = self.findChild(QLabel, 'addPatientFeedback')
        

    def addPatientButtonHandler(self):
        '''This function will read all the data from the gui variables defined in the addPatientWidgetsSetup function and call the add_patient function with the read data'''
        try:
            first_name = self.firstNameInputAddPatientTab.text()
            last_name = self.lastNameInputAddPatientTab.text()
            phone_number = self.phoneNumberInputAddPatientTab.text()
            email = self.emailInputAddPatientTab.text()
            age = int(self.ageSelectorAddPatientTab.cleanText())
            gender = self.genderSelectorAddPatientTab.currentIndex()
            if gender == 0:
                gender = 'Male'
            elif gender == 1:
                gender = 'Female'
            elif gender == 2:
                gender = 'Non-Binary'
            address = self.addressInputAddPatientTab.text()
            result = add_patient(first_name, last_name, phone_number, email, age, gender, address)
            if result == 1:
                self.qLabelStringChangeWait(self.addPatientFeedback, "Patient Added", 200)
                self.qLabelStringChangeWait(self.addPatientFeedback, "", 1500)
                self.clearAddPatientFieldsAfterAdding(self.firstNameInputAddPatientTab, self.lastNameInputAddPatientTab, self.phoneNumberInputAddPatientTab,\
                    self.emailInputAddPatientTab, self.ageSelectorAddPatientTab, self.genderSelectorAddPatientTab, self.addressInputAddPatientTab)
                self.refreshModifyTab('patient')
            elif result == 0:
                self.qLabelStringChangeWait(self.addPatientFeedback, "Failure", 200)
                self.qLabelStringChangeWait(self.addPatientFeedback, "", 3000)
        except Exception as e:
            print(e)

    def modifyPatientWidgetsSetup(self):
        '''This function initializes all variables that will later need to be accessed in the Modify Patient Tab'''

        # initializing all objects
        self.patientNameComboBoxModifyTab = self.findChild(QComboBox, 'patientNameComboBoxModifyTab')
        self.patientIdLineEditReadOnlyModifyTab = self.findChild(QLineEdit, 'patientIdLineEditReadOnlyModifyTab')
        self.patientFirstNameLineEditModifyTab = self.findChild(QLineEdit, 'patientFirstNameLineEditModifyTab')
        self.patientLastNameLineEditModifyTab = self.findChild(QLineEdit, 'patientLastNameLineEditModifyTab')
        self.patientPhoneNumberLineEditModifyTab = self.findChild(QLineEdit, 'patientPhoneNumberLineEditModifyTab')
        self.patientEmailLineEditModifyTab = self.findChild(QLineEdit, 'patientEmailLineEditModifyTab')
        self.patientAgeSelectorModifyTab = self.findChild(QSpinBox, 'patientAgeSelectorModifyTab')
        self.patientGenderSelectorModifyTab = self.findChild(QComboBox, 'patientGenderSelectorModifyTab')
        self.patientAddressLineEditModifyTab = self.findChild(QLineEdit, 'patientAddressLineEditModifyTab')

        self.patientdoctorSaveChangesButton = self.findChild(QPushButton, 'patientSaveChangesButton')
        self.patientdoctorSaveChangesButton.clicked.connect(self.patientSaveChangesButtonHandler)

        self.patientDeletePatientButton = self.findChild(QPushButton, 'patientDeleteButton')
        self.patientDeletePatientButton.clicked.connect(self.patientDeleteButtonHandler)

        self.modifyPatientTabFeedbackLabel = self.findChild(QLabel, 'modifyPatientTabFeedbackLabel')
    

        # the following conditional will allow the program to continue to run if no doctors currently exist
        # this section will populate the combo box with all patient names
        colNames, rows = getPatientIdsAndNames()
        row_counter = 0
        for row in rows:
            row_counter += 1
        
        if row_counter != 0:
            for row in rows:
                self.patientNameComboBoxModifyTab.addItem(row[1], userData = row[0])
        else:
            pass

        self.populateOrRefreshModifyTabInformation(getPatientInfoById(rows[0][0]),  'patient', self.patientIdLineEditReadOnlyModifyTab, self.patientFirstNameLineEditModifyTab,\
                self.patientLastNameLineEditModifyTab, self.patientPhoneNumberLineEditModifyTab, self.patientEmailLineEditModifyTab, self.patientAgeSelectorModifyTab, self.patientGenderSelectorModifyTab,\
                    self.patientAddressLineEditModifyTab) # rows[0][0] is the patient id 
        self.patientNameComboBoxModifyTab.currentIndexChanged.connect(self.patientNameComboBoxModifyTabCurrentIndexChangedHandler)

    def patientNameComboBoxModifyTabCurrentIndexChangedHandler(self):
        '''This function is called whenever the current patient selection / index is changed'''
        try:
            patientId = self.patientNameComboBoxModifyTab.currentData()
            self.populateOrRefreshModifyTabInformation(getPatientInfoById(patientId), 'patient', self.patientIdLineEditReadOnlyModifyTab, self.patientFirstNameLineEditModifyTab,\
                self.patientLastNameLineEditModifyTab, self.patientPhoneNumberLineEditModifyTab, self.patientEmailLineEditModifyTab, self.patientAgeSelectorModifyTab, self.patientGenderSelectorModifyTab,\
                    self.patientAddressLineEditModifyTab)
        except Exception as e:
            print(e)

    def patientSaveChangesButtonHandler(self):
        '''This function will read all the data from the gui variables defined in the modifyPatientWidgetsSetup function and call the modify_patient function with the read data'''
        try:
            patient_id = self.patientIdLineEditReadOnlyModifyTab.text()
            first_name = self.patientFirstNameLineEditModifyTab.text()
            last_name = self.patientLastNameLineEditModifyTab.text()
            phone_number = self.patientPhoneNumberLineEditModifyTab.text()
            email = self.patientEmailLineEditModifyTab.text()
            age = int(self.patientAgeSelectorModifyTab.cleanText())
            gender = self.patientGenderSelectorModifyTab.currentText()
            address = self.patientAddressLineEditModifyTab.text()
            result = modify_patient(patient_id = patient_id, first_name = first_name, last_name = last_name\
            , phone_number = phone_number, email = email, age = age, gender = gender, address = address)
            if result == 1:
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, 'Changes Saved', 200)
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, "", 1500)
                self.refreshModifyTab('patient')
            elif result == 0:
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, 'Failure', 200)
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, "", 3000)
        except Exception as e:
            print(e)
    
    def patientDeleteButtonHandler(self):
        '''This function will read the current selected patients ID and pass the argument into and then call the delete_patient function'''
        try:
            patient_id = int(self.patientIdLineEditReadOnlyModifyTab.text())
            result = delete_patient(patient_id = patient_id)
            if result == 1:
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, "Patient Successfully Deleted", 200)
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, "", 1500)
                self.refreshModifyTab('patient')
            elif result == 0:
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, "Failure", 200)
                self.qLabelStringChangeWait(self.modifyPatientTabFeedbackLabel, "", 3000)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    # argv is what accesses the command line
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()