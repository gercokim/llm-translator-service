from google.cloud import aiplatform
import subprocess
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


PROJECT_ID = "nodebb-417100"
subprocess.run(['gcloud', 'config', 'set', 'project', PROJECT_ID,])

aiplatform.init(
    project=PROJECT_ID,
    location='us-central1'
)

def translate_content(content: str) -> tuple[bool, str]:
    context1 = "You are an English translator that translates text to English. Ensure that every response is only in English. Reply with an empty string if given unintelligible text"
    context2 = "You reply with true if the given text is made up of valid English words, false otherwise."
    parameters = {
            "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
            "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        }
    #try:
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat(context=context1)
    response1 = chat.send_message(content, **parameters)
    chat = chat_model.start_chat(context=context2)
    response2 = chat.send_message(content, **parameters)
    b1 = "true" in response2.text or "True" in response2.text
    b2 = "false" in response2.text or "False" in response2.text
    if not b1 and not b2:
        return (b1, "I was unable to answer your request")
    return (b1, response1.text)
    #except Exception as e:
        #return (False, "I was unable to answer your request")

print(translate_content('Aquí está su primer ejemplo.'))
