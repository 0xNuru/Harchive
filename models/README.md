# create a new medication record instance
```
medication_record = MedicationRecord(medication_type='Aspirin', dosage='100mg', date=date(2022, 1, 1))
```

# create a new record instance that references the medication record and the patient
```
patient = session.query(Patient).filter_by(name='John Doe').first()
record = Record(type='medication', medication_record=medication_record, patient=patient)
```