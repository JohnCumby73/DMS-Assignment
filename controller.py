from mySqlFunctions import executeQueryAndCommit, executeQueryAndReturnResult

def add_doctor(first_name: str, last_name: str, phone_number: str, email: str, age: int, gender: str, address: str, specialization: str, years_of_experience: int):
    '''This function builds an sql statement from the arguments it is passed and calls the executeQueryAndCommit function'''

    sql = f"INSERT INTO doctor_management_system.doctor (first_name, last_name, phone_number, email, age, gender, address, specialization, years_of_experience) VALUES ('{first_name}',\
    '{last_name}', '{phone_number}', '{email}', '{age}', '{gender}', '{address}', '{specialization}', '{years_of_experience}');"
    return executeQueryAndCommit(sql)

def modify_doctor(doctor_id: int, first_name: str, last_name: str, phone_number: str, email: str, age: int, gender: str, address: str, specialization: str, years_of_experience: int):
    '''This function builds an sql statement from the arguments it is passed and calles the executeQueryAndCommit function'''
    sql = f"UPDATE doctor SET first_name = '{first_name}', last_name = '{last_name}', phone_number = '{phone_number}', email = '{email}',\
    age = '{age}', gender = '{gender}', address = '{address}', specialization = '{specialization}', years_of_experience = '{years_of_experience}' WHERE doctor_id = '{doctor_id}';"
    return executeQueryAndCommit(sql)

def delete_doctor(doctor_id: int):
    '''This function builds an sql statement from the arguments it is passed and calls the executeQueryAndCommit function'''

    sql = f"DELETE FROM doctor WHERE doctor_id = {doctor_id}"
    return executeQueryAndCommit(sql)

def getDoctorIdsAndNames():
    '''This function will return a tuple and the first one is all column names, and the second one is a list of tuples of the retrieved rows'''

    sql = f"SELECT doctor_id, concat(first_name, ' ', last_name) as 'Doctor Name' FROM doctor;"
    return executeQueryAndReturnResult(sql)

def getDoctorInfoById(doctor_id) -> dict:
    '''This function will return a dictionary of all the information of the doctor retrived by the doctor id'''

    sql = f"SELECT * FROM doctor_management_system.doctor WHERE doctor_id = {doctor_id};"
    doctorInfo = executeQueryAndReturnResult(sql)[1][0]  
    data = {'doctorId': doctorInfo[0], 'firstName': doctorInfo[1], 'lastName': doctorInfo[2], 'phoneNumber': doctorInfo[3], 'email': doctorInfo[4],
     'age': doctorInfo[5], 'gender': doctorInfo[6], 'address': doctorInfo[7], 'specialization': doctorInfo[8], 'yearsOfExperience': doctorInfo[9]}
    return data

# ------------------------------------------------------------------------------------------------- Patient Functions -------------------------------------------------------------------------------------------------------------

def add_patient(first_name: str, last_name: str, phone_number: str, email: str, age: int, gender: str, address: str):
    '''This function builds an sql statement from the arguments it is passed and calls the executeQueryAndCommit function'''

    sql = f"INSERT INTO doctor_management_system.patient (first_name, last_name, phone_number, email, age, gender, address) VALUES ('{first_name}', '{last_name}', '{phone_number}', '{email}', '{age}', '{gender}', '{address}');"
    return executeQueryAndCommit(sql)

def modify_patient(patient_id: int, first_name: str, last_name: str, phone_number: str, email: str, age: int, gender: str, address: str):
    '''This function builds an sql statement from the arguments it is passed and calls the executeQueryAndCommit function'''

    sql = f"UPDATE patient SET first_name = '{first_name}', last_name = '{last_name}', phone_number = '{phone_number}', email = '{email}', age = '{age}', gender = '{gender}', address = '{address}'\
        WHERE patient_id = {patient_id};"
    return executeQueryAndCommit(sql)

def delete_patient(patient_id: int):
    '''This function builds an sql statement from the arguments it is passed and calls the executeQueryAndCommit function'''

    sql = f"DELETE FROM patient WHERE patient_id = {patient_id}"
    return executeQueryAndCommit(sql)

def getPatientIdsAndNames():
    '''This function will return a tuple where the first one is all column names, and the second one is a list of tuples of the retrieved rows'''

    sql = f"SELECT patient_id, concat(first_name, ' ', last_name) as 'Patient Name' FROM patient;"
    return executeQueryAndReturnResult(sql)

def getPatientInfoById(patient_id) -> dict:
    ''''This function will return a dictionary of all the information of the doctor retrived by the doctor id'''

    sql = f"SELECT * FROM doctor_management_system.patient WHERE patient_id = {patient_id};"
    patientInfo = executeQueryAndReturnResult(sql)[1][0]
    data = {'patientId': patientInfo[0], 'firstName': patientInfo[1], 'lastName': patientInfo[2], 'phoneNumber': patientInfo[3], 'email': patientInfo[4],
     'age': patientInfo[5], 'gender': patientInfo[6], 'address': patientInfo[7]}
    return data
    
