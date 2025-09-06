import boto3

def lambda_handler(event, context):
    try:
        # Capture slots
        slots = event['sessionState']['intent']['slots']
        input_text = slots['Text']['value']['interpretedValue'].strip()
        language_slot = slots['Language']['value']['interpretedValue']

        if not input_text:
            raise ValueError("Input text is empty.")

        # Supported language codes
        language_codes = {
            'French': 'fr',
            'Japanese': 'ja',
            'Chinese': 'zh',
            'Spanish': 'es',
            'German': 'de',
            'Norwegian': 'no'
        }

        if language_slot not in language_codes:
            raise ValueError(f"Unsupported language: {language_slot}")

        target_language_code = language_codes[language_slot]

        # Call Amazon Translate
        translate_client = boto3.client('translate')
        response = translate_client.translate_text(
            Text=input_text,
            SourceLanguageCode='auto',
            TargetLanguageCode=target_language_code
        )

        translated_text = response['TranslatedText']

        # Ask user if they'd like to continue (loop back to text slot)
        lex_response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "Text"
                },
                "intent": {
                    "name": "translationIntent",
                    "state": "InProgress",
                    "slots": {
                        "Text": None,
                        "Language": {
                            "value": {
                                "interpretedValue": language_slot
                            }
                        }
                    }
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"✅ Translated: {translated_text}\n\nYou can enter another phrase to translate."
                }
            ]
        }

        return lex_response

    except Exception as error:
        error_message = "Lambda execution error: " + str(error)
        print(error_message)
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "translationIntent",
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
