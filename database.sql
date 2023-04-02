DROP DATABASE IF EXISTS doctor_management_system;
CREATE DATABASE doctor_management_system;
USE doctor_management_system;
CREATE TABLE patient (
	patient_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR (50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL
);
USE doctor_management_system;
CREATE TABLE doctor (
	doctor_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR (50) NOT NULL,
    email VARCHAR (50) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    specialization VARCHAR(50) NOT NULL,
    years_of_experience INT NOT NULL
);

	


    
    
	