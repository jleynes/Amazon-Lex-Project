import boto3

def lambda_handler(event, context):
    try:
        # Extracts input text and the target language from the Lex event
        input_text = event['sessionState']['intent']['slots']['text']['value']['interpretedValue'].strip()
        language_slot = event['sessionState']['intent']['slots']['language']['value']['interpretedValue']
        
        # Raise an error if no text given
        if not input_text:
            raise ValueError("Input text is empty.")
        
        # Amazon Translate language codes
        language_codes = {
            'French' : 'fr',
            'Japanese' : 'ja',
            'Chinese' : 'zh',
            'Spanish' : 'es',
            'German' : 'de',
            'Norwegian' : 'no'
        }
        
        # Check for ensuring input text is not empty and target language is supported
        if not input_text:
            raise ValueError("Input text is empty.")
        
        if language_slot not in language_codes:
            raise ValueError(f"Unsupported language: {language_slot}")
            
        # Initialize the Amazon Translate client
        translate_client = boto3.client('translate')
        
        # Call Amazon Translate to perform translation
        target_language_code = language_codes[language_slot]
        
        response = translate_client.translate_text(
            Text=input_text,
            SourceLanguageCode='auto', # Auto detect source
            TargetLanguageCode = target_language_code
        )
        
        translated_text = response['TranslatedText']
        
        # Constructing a response for the chatbot with the translated text
        lex_response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "TranslationIntent", #Intent name that was created
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": translated_text
                }
            ]
        }
        
        return lex_response
    
    # Error handling
    except Exception as error:
        error_message = "Lambda execution error: " + str(error)
        print(error_message)
        lex_error_response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "TranslationIntent",
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": error_message
                }
            ]
        }
        return lex_error_response
        
