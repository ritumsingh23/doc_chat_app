import requests

# Replace these with your actual credentials
client_id = "cf2c3e78-abc9-4517-bccb-3c834e159f6f"
client_secret = "your_client_secret"

# Base URL for EPIC's FHIR API (replace with the actual URL)
fhir_base_url = "https://epic-fhir-test-api.example.com"

# Authentication endpoint for EPIC's FHIR API
token_url = f"{fhir_base_url}/oauth2/token"

# API endpoint to retrieve patient data
patient_url = f"{fhir_base_url}/Patient"

def get_access_token():
    # Request an access token using client credentials
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to get access token")

def get_patient_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(patient_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get patient data")

if __name__ == "__main__":
    access_token = get_access_token()
    patient_data = get_patient_data(access_token)
    print(patient_data)
