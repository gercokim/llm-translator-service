import vertexai
from mock import patch
from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
def test_unexpected_language(mocker):
  mocker.return_value.text = "I don't understand your request"
  content = "Aquí está su primer ejemplo."
  assert translate_content(content) == (True, content)

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
def test_empty_response(mocker):
  mocker.return_value = {}
  content = "Aquí está su primer ejemplo."
  assert translate_content(content) == (True, content)

@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
def test_broken_chat_session(mocker):
  mocker.return_value = {}
  content = "Aquí está su primer ejemplo."
  assert translate_content(content) == (True, content)

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
def test_malformed_response(mocker):
  mocker.return_value.text = "Here is your first example."
  del mocker.return_value.text
  content = "Aquí está su primer ejemplo."
  assert translate_content(content) == (True, content)

@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_broken_model(mocker):
  mocker.return_value = {}
  content = "Aquí está su primer ejemplo."
  assert translate_content(content) == (True, content)
