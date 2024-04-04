import vertexai
from mock import patch
from src.translator import translate_content


class MockObject():
  def __init__(self, text):
    self.text = text

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatModel')
@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_llm_normal_response(mocker_pretrained, mocker_model, mocker_chat, mocker_session, mocker_msg):
  mocker_msg.side_effect = [MockObject("This is a Chinese message"), MockObject("False")]
  mocker_session().send_message = mocker_chat.return_value
  mocker_chat.return_value = mocker_session
  mocker_model().start_chat = mocker_chat
  mocker_pretrained.return_value = mocker_model
  is_english, translated_content = translate_content("这是一条中文消息")
  assert is_english == False
  assert translated_content == "This is a Chinese message" 

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatModel')
@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_llm_gibberish_response(mocker_pretrained, mocker_model, mocker_chat, mocker_session, mocker_msg):
  mocker_msg.return_value.text = "asdlfkjq;lejq"
  mocker_session().send_message = mocker_msg
  mocker_chat.return_value = mocker_session
  mocker_model().start_chat = mocker_chat
  mocker_pretrained.return_value = mocker_model
  assert translate_content("Aquí está su primer ejemplo.") == (False, "I was unable to answer your request") 

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatModel')
@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_unexpected_language(mocker_pretrained, mocker_model, mocker_chat, mocker_session, mocker_msg):
  # we mock the model's response to return a random message
  mocker_msg.return_value.text = "I don't understand your request"
  mocker_session().send_message = mocker_msg
  mocker_chat.return_value = mocker_session
  mocker_model().start_chat = mocker_chat
  mocker_pretrained.return_value = mocker_model
  # TODO assert the expected behavior
  assert translate_content("Aquí está su primer ejemplo.") == (False, "I was unable to answer your request")

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatModel')
@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_empty_response(mocker_pretrained, mocker_model, mocker_chat, mocker_session, mocker_msg):
  mocker_msg.return_value = {}
  mocker_session().send_message = mocker_msg
  mocker_chat.return_value = mocker_session
  mocker_model().start_chat = mocker_chat
  mocker_pretrained.return_value = mocker_model
  assert translate_content("Aquí está su primer ejemplo.") == (False, "I was unable to answer your request")

@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatModel')
@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_broken_chat_session(mocker_pretrained, mocker_model, mocker_chat):
  mocker_chat.return_value = {}
  mocker_model().start_chat = mocker_chat
  mocker_pretrained.return_value = mocker_model
  assert translate_content("Aquí está su primer ejemplo.") == (False, "I was unable to answer your request")

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models._PreviewChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatModel')
@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_malformed_response(mocker_pretrained, mocker_model, mocker_chat, mocker_session, mocker_msg):
  mocker_msg.return_value.text = "Here is your first example."
  mocker_session().send_message = mocker_msg
  mocker_chat.return_value = mocker_session
  mocker_model().start_chat = mocker_chat
  mocker_pretrained.return_value = mocker_model
  del mocker_msg.return_value.text
  assert translate_content("Aquí está su primer ejemplo.") == (False, "I was unable to answer your request")

@patch('vertexai.preview.language_models._PreviewChatModel.from_pretrained')
def test_broken_model(mocker):
  mocker.return_value = {}
  assert translate_content("Aquí está su primer ejemplo.") == (False, "I was unable to answer your request")
