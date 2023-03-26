## Record Db

# create a new medication record instance just an example, use actuall params
```
medication_record = MedicationRecord(medication_type='Aspirin', dosage='100mg', date=date(2022, 1, 1))
```

# create a new record instance that references the medication record and the patient
```
patient = session.query(Patient).filter_by(name='John Doe').first()
record = Record(type='medication', medication_record=medication_record, patient=patient)
```



## Hospital Db/


Here's an example of how to create a Hospital object and add it to the database:

python
```
hospital = Hospital(name='General Hospital')
session.add(hospital)
session.commit()
```
This code creates a new Hospital object with the name "General Hospital" and adds it to the database using the session object. The session.commit() line commits the changes to the database.

To add HospitalWorkers and Doctors to the database, you would use similar code:

python
```
worker = HospitalWorker(name='John Smith', job_title='Nurse', hospital=hospital)
doctor = Doctor(name='Jane Doe', specialization='Cardiology', worker=worker)
session.add(worker)
session.add(doctor)
session.commit()
```
This code creates a new HospitalWorker object with the name "John Smith" and job title "Nurse", and associates it with the Hospital object we created earlier. It also creates a new Doctor object with the name "Jane Doe" and specialization "Cardiology", and associates it with the HospitalWorker object we just created.

You can use the session.query() method to retrieve objects from the database. For example, to retrieve all the HospitalWorkers associated with a particular Hospital, you could do:

python
```
hospital = session.query(Hospital).filter_by(name='General Hospital').first()
workers = hospital.workers
```
This code retrieves the Hospital object with the name "General Hospital" and then retrieves all the associated HospitalWorkers using the workers attribute of the Hospital object.

I hope this helps! Let me know if you have any questions.