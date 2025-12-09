import plivo

# 1. Credentials provided by Plivo:
AUTH_ID = "1234JJOGRLNZK0ZMZIMM"
AUTH_TOKEN = "1234OWM5NDZlODJmZWFkODE1NjA3OTg0MGFjODI5"

def fetch_plivo_number():
    
    # Initialize the Plivo REST client
    client = plivo.RestClient(AUTH_ID, AUTH_TOKEN)
    
    print("Connecting to Plivo API...")
    try:
        # Call the API to list all numbers
        response = client.numbers.list()

        if response and response['objects']:
            # The first number found is the active number (test number)
            active_number = response['objects'][0]['number']
            print("\n==============================================")
            print(f"SUCCESS! Found active Plivo FROM_NUMBER: {active_number}")
            print("==============================================\n")
            return active_number
        else:
            print("ERROR: No active phone numbers were found on this account.")
            print("Please confirm an active test number is assigned to the API key.")
            return None
            
    except Exception as e:
        print(f"API Error during number fetch: {e}")
        print("Please double-check the Auth ID and Auth Token.")
        return None

if __name__ == "__main__":
    from_number = fetch_plivo_number()
    if from_number:
        print("ACTION.")