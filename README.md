# **HARCHIVE**
------------------
![](Harchive_Logo_White.png)


## **About**
<p>Our team at Harchive believes that patients deserve better, and that's why we've built Harchive  - a platform that allows patients to securely and easily access their health records in any hospital they check into. 

Our platform provides a secure, user-friendly solution for managing and accessing medical records anywhere, anytime. 

Here are some of the key features that make us stand out from the crowd
First a patient registers under an insurance scheme and is automatically enrolled into our system and given a unique ID and password."

When the patient checks into an accredited hospital, they only need to provide their ID and password once. After the initial check-in, any of the hospital workers that need the patient's health records only need their ID to access them

For each medical procedure, the health worker in charge of the respective units updates the patient's health records. Health workers can only view or add to the patient's health records, but they can't edit past records to ensure immutability.

The hospital provides medical services to the patient and submits a claim to the insurance company through the platform. The insurance company can access the claim associated with their patients from the platform and use the transaction information to check for any suspicious activity or patterns

With Harchive, patients can easily continue treatment from any accredited hospital by ensuring interoperability between accredited hospitals. Only accredited hospitals can access patient health records from the platform. And every health worker who deals with the patient record has a login that allows them to use the platform under the permission of the hospital they   a third party and access other online health services."</p>



## **API Model Breakdown**

Our API is organized around REST principles. It follows predictable resource-oriented URLs, returns JSON-encoded responses, and uses standard HTTP response codes and verbs.

## **Authentication**

To use our API, you need to authenticate your requests using an API key, which you can obtain by registering for an account on our platform. Once you have an API key, include it in the Authorization header of your requests like this:

```
Authorization: Bearer <your-api-key>
```

## **Endpoints**

Our API exposes the following endpoints:

**User Routes**

POST /user/register

Create's a User

GET /user/all

Returns a list of all users in the system.

GET /user/email/{email}

Returns the user with the specified email.

POST /user/login

Logs a user into the system and returns a JWT token.

GET /user/refresh

Refreshes a user's JWT token.

GET /user/logout

Logs a user out of the system.

## **Insurance Routes**

POST /insurance/admin/register

Creates an insurance admin account.

GET /insurance/admin/all

Returns a list of all insurance admins in the system.

GET /insurance/admin/insuranceID/{insuranceID}

Returns the insurance admin with the specified ID.

POST /insurance/register

Creates an insurance account.

GET /insurance/all

Returns a list of all insurance accounts in the system.

GET /insurance/{insuranceID}

Returns the insurance account with the specified ID.

## **Hospital Routes**

POST /hospital/admin/register

Creates a hospital admin account.

GET /hospital/admin/all

Returns a list of all hospital admins in the system.

GET /hospital/admin/hospitalID/{hospitalID}

Returns the hospital admin with the specified ID.

DELETE /hospital/admin/delete/{hospitalID}

Deletes the hospital admin with the specified ID.

POST /hospital/register

Creates a hospital account.

GET /hospital/all

Returns a list of all hospital accounts in the system.

GET /hospital/{hospitalID}

Returns the hospital account with the specified ID.

POST /hospital/doctor/register

Creates a doctor account.

GET /hospital/doctor/all

Returns a list of all doctor accounts in the system.

GET /hospital/doctor/email/{email}

Returns the doctor account with the specified email.

DELETE /hospital/doctor/delete/{email}

Deletes the doctor account with the specified email.

POST /hospital/checkIn

Checks a patient into the hospital.

DELETE /hospital/checkout

Checks a patient out of the hospital.

## **Patient Routes**

POST /patient/register

Creates a patient account.
GET /patient/all

Returns a list of all the patient accounts in the system.

GET /patient/email/{email}

Returns the patient account with the specified email.

POST /patient/record/add

Creates a patient medical record.

GET /patient/record/all

Returns a list of all patient medical records in the system.

GET /patient/record/nin/{nin}

Returns the patient medical record with the specified National Insurance Number (NIN).

PUT /patient/record/update/{nin}

Updates the patient medical record with the specified NIN.

POST /patient/medication/add/{nin}

Adds a medication to the patient's medical record.

POST /patient/allergy/add/{nin}

Adds an allergy to the patient's medical record.

POST /patient/immunization/add/{nin}

Adds an immunization to the patient's medical record.


POST /patient/transaction/add/{nin}

Adds a transaction to the patient's account.

## **Response Format**

All responses from our API are JSON-encoded. The format of the response depends on the endpoint you're accessing. Typically, the response contains a top-level data field that contains the requested data. If there are any errors, the response contains a top-level error field that contains a message explaining the error.




## **Contributors**
- Hamza Saidu ([Cyberguru1](https://github.com/Cyberguru1))
- Nurudeen Ahmed ([nurvdeen](https://github.com/nurvdeen/t))

