import pytest
from unittest.mock import MagicMock
from agent_logic import get_base64_image, get_technical_analysis
from anthropic_investment_agent_streamlit import main as streamlit_main

def test_get_base64_image():
    # Create a dummy image data
    image_data = b'test_image_data'

    # Expected base64 string
    expected_base64 = "data:image/jpeg;base64,dGVzdF9pbWFnZV9kYXRh"

    # Call the function
    result = get_base64_image(image_data)

    # Assert the result
    assert result == expected_base64

def test_get_technical_analysis(mocker):
    # Mock the Anthropic client
    mock_client = MagicMock()

    # Mock the response from the API
    mock_response = MagicMock()
    mock_response.content = [MagicMock()]
    mock_response.content[0].text = "Technical analysis result"
    mock_client.messages.create.return_value = mock_response

    # Dummy image data
    image_data = b'test_image_data'

    # Call the function with the mocked client
    result = get_technical_analysis(mock_client, image_data)

    # Assert the result
    assert result == "Technical analysis result"

    # Assert that the create method was called with the correct arguments
    mock_client.messages.create.assert_called_once()

def test_streamlit_app_no_api_key(mocker):
    """Test the Streamlit app when no API key is provided."""
    mocker.patch('streamlit.text_input', return_value=None)
    mock_title = mocker.patch('streamlit.title')
    mock_set_page_config = mocker.patch('streamlit.set_page_config')
    mock_file_uploader = mocker.patch('streamlit.file_uploader')

    streamlit_main()

    mock_set_page_config.assert_called_once_with(page_title="Crypto Technical and On-Chain Analysis", page_icon="📊")
    mock_title.assert_called_once_with("Crypto Technical and On-Chain Analysis")
    mock_file_uploader.assert_not_called()

def test_streamlit_app_with_api_key_no_file(mocker):
    """Test the Streamlit app with an API key but no file uploaded."""
    mocker.patch('streamlit.set_page_config')
    mocker.patch('streamlit.title')
    mocker.patch('streamlit.text_input', return_value='fake_api_key')
    mocker.patch('streamlit.file_uploader', return_value=None)
    mocker.patch('anthropic_investment_agent_streamlit.anthropic.Anthropic')
    mock_get_analysis = mocker.patch('anthropic_investment_agent_streamlit.get_technical_analysis')

    streamlit_main()

    mock_get_analysis.assert_not_called()

def test_streamlit_app_with_api_key_and_file(mocker):
    """Test the Streamlit app with an API key and an uploaded file."""
    mocker.patch('streamlit.set_page_config')
    mocker.patch('streamlit.title')
    mocker.patch('streamlit.text_input', return_value='fake_api_key')
    mock_uploaded_file = MagicMock()
    mock_uploaded_file.getvalue.return_value = b'fake_image_data'
    mocker.patch('streamlit.file_uploader', return_value=mock_uploaded_file)
    mock_markdown = mocker.patch('streamlit.markdown')
    mock_write = mocker.patch('streamlit.write')

    mocker.patch('anthropic_investment_agent_streamlit.get_base64_image', return_value='data:image/jpeg;base64,fake_base64_string')
    mocker.patch('anthropic_investment_agent_streamlit.get_technical_analysis', return_value='fake_analysis')

    mocker.patch('anthropic_investment_agent_streamlit.anthropic.Anthropic')

    streamlit_main()

    mock_markdown.assert_called_once_with('<img src="data:image/jpeg;base64,fake_base64_string" width="500">', unsafe_allow_html=True)
    mock_write.assert_any_call("### Technical Analysis Summary")
    mock_write.assert_any_call("fake_analysis")
