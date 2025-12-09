import plivo

AUTH_ID = "1234JJOGRLNZK0ZMZIMM"
AUTH_TOKEN = "1234OWM5NDZlODJmZWFkODE1NjA3OTg0MGFjODI5"
FROM_NUMBER = "+911234567890"  # Plivo number (E.164 format: +1555...)
TO_NUMBER = "+911234567890"   # Your cell phone (E.164 format: +1555...)


ANSWER_URL = "https://unbedraggled-feelinglessly-zoe.ngrok-free.dev/ivr_start/"


def trigger_outbound_call():
    client = plivo.RestClient(AUTH_ID, AUTH_TOKEN)
    print(f"Attempting to call {TO_NUMBER}...")
    try:
        response = client.calls.create(
            from_=FROM_NUMBER,
            to_=TO_NUMBER,
            answer_url=ANSWER_URL,
            answer_method='POST'
        )
        print(f"Call initiated successfully. Request UUID: {response['request_uuid']}")
    except Exception as e:
        print(f"Error making call: {e}")

if __name__ == "__main__":
    trigger_outbound_call()