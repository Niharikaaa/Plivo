from flask import Flask, request, make_response, url_for
from plivo import plivoxml 

app = Flask(__name__)

# --- CONFIGURATION ---
AUDIO_URL = "https://s3.amazonaws.com/plivocloud/Trumpet.mp3"
ASSOCIATE_NUMBER = "+911234567890"

# --- HELPER: FORCE ABSOLUTE URLS ---
def get_absolute_url(endpoint):
    """Generates the full https://ngrok... URL for a given endpoint function name."""
    return url_for(endpoint, _external=True)

@app.route('/ivr_start/', methods=['POST', 'GET']) 
def ivr_start():
    print("--- RECEIVED CALL AT /ivr_start/ ---")
    
    response = plivoxml.ResponseElement()

    response.add(
        plivoxml.SpeakElement("Welcome to Inspire Works. Press 1 for English or press 2 for Spanish.")
    )

    action_url = get_absolute_url('ivr_level_2_menu')

    get_input = plivoxml.GetInputElement(
        action=action_url, 
        method='POST',
        input_type='dtmf', 
        num_digits=1,
        redirect=True
    )
    
    response.add(get_input)
    response.add(plivoxml.SpeakElement("No input received. Goodbye.")) 

    return create_plivo_response(response)


@app.route('/level_2/', methods=['POST']) 
def ivr_level_2_menu():
    print("--- RECEIVED INPUT AT /level_2/ ---")
    digits = request.form.get('Digits')
    response = plivoxml.ResponseElement()
    
    # Handle invalid input
    if digits not in ['1', '2']:
        response.add(plivoxml.SpeakElement("Invalid entry. Starting over."))
        response.add(plivoxml.RedirectElement(get_absolute_url('ivr_start'))) 
        return create_plivo_response(response)

    # Set Language
    language = "en" if digits == '1' else "es"
    print(f"User selected language: {language}")

    if language == "en":
        prompt = "Press 1 to play a short audio message. Press 2 to connect to a live associate."
    else:
        prompt = "Pulse 1 para escuchar un mensaje. Pulse 2 para hablar con un asociado."

    # CHANGE 3: Build Action URL manually to include query params
    base_action = get_absolute_url('ivr_action')
    next_action_url = f"{base_action}?lang={language}"
    
    # Speak first, then wait for input
    response.add(plivoxml.SpeakElement(prompt))

    get_input = plivoxml.GetInputElement(
        action=next_action_url,
        method='POST',
        input_type='dtmf',
        num_digits=1,
        redirect=True
    )
    
    response.add(get_input)
    response.add(plivoxml.SpeakElement("No input received. Starting over."))
    response.add(plivoxml.RedirectElement(get_absolute_url('ivr_start')))
    
    return create_plivo_response(response)


@app.route('/ivr_action', methods=['POST'])
def ivr_action():
    print("--- EXECUTING FINAL ACTION ---")
    digits = request.form.get('Digits')
    language = request.args.get('lang', 'en') 
    response = plivoxml.ResponseElement()

    if digits == '1':
        # Action: Play Audio
        msg = "Playing the message now." if language == "en" else "Reproduciendo el mensaje ahora."
        response.add(plivoxml.SpeakElement(msg))
        response.add(plivoxml.PlayElement(AUDIO_URL))
    elif digits == '2':
        # Action: Forward to Associate
        msg = "Connecting you now." if language == "en" else "Conectando ahora."
        response.add(plivoxml.SpeakElement(msg))
        dial = plivoxml.DialElement()
        dial.add(plivoxml.NumberElement(ASSOCIATE_NUMBER))
        response.add(dial)
    else:
        response.add(plivoxml.SpeakElement("Invalid selection. Goodbye."))

    return create_plivo_response(response)


def create_plivo_response(response_element):
    xml_string = response_element.to_string()
    # DEBUG: Print the XML to verify the Absolute URLs
    print(f"GENERATED XML:\n{xml_string}")
    
    resp = make_response(xml_string)
    resp.headers['Content-Type'] = 'text/xml'
    return resp

@app.route('/answer', methods=['POST', 'GET'])
def answer_handler():
    return '', 200

if __name__ == '__main__':
    # Ensure this port matches your Ngrok command
    app.run(host='0.0.0.0', port=8080, debug=True)