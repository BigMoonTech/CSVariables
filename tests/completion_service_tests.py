from sqlalchemy import null
from tests.test_client import flask_app
from unittest.mock import patch
import openai

from src.services.completion_service import (
    validated_openai_response
)

FAKE_COMPLETION = {
    "id": "cmpl-test_id",
    "object": "text_completion",
    "created": 1589478378,
    "model": "text-davinci-002",
    "choices": [
        {
            "text": "\n\nThis is a test",
            "index": 0,
            "logprobs": null,
            "finish_reason": "length"
        }
    ],
    "usage": {
        "prompt_tokens": 5,
        "completion_tokens": 6,
        "total_tokens": 11
    }
}


def test_validated_openai_response_returns_dict_with_good_api_key():
    """
    This test will fail if the API key is not set in the environment.
    Warning: actually calls the OpenAI API.

    :return: None
    """
    with flask_app.app_context():
        good_api_key = flask_app.config['OPENAI_API_KEY']
        openai.api_key = good_api_key
        completion = validated_openai_response("test")
        assert isinstance(completion, dict)


def test_validated_openai_response_returns_msg_with_bad_api_key():
    bad_api_key = 'bad_key'
    openai.api_key = bad_api_key
    completion = validated_openai_response("test")
    assert "openai authentication" in completion


def test_validated_openai_response_returns_msg_with_request_timeout():
    with patch('openai.Completion.create') as mock_create:
        mock_create.side_effect = openai.error.Timeout
        completion = validated_openai_response("test")
        assert "timed out" in completion


def test_integration_add_completion_to_db(client):
    with flask_app.app_context():
        patch_target = "src.services.completion_service.validated_openai_response"
        with patch(patch_target) as mock_response:
            mock_response.return_value = FAKE_COMPLETION

            from src.services.completion_service import add_completion_to_db, get_completion_by_completion_id
            add_completion_to_db(mock_response.return_value, "test prompt", user_id="test user")
            assert get_completion_by_completion_id("cmpl-test_id") is not None


def test_integration_add_completion_to_db_returns_false_with_bad_key(client):
    with flask_app.app_context():
        patch_target = "src.services.completion_service.validated_openai_response"
        with patch(patch_target) as mock_response:
            mock_response.return_value = {}
            from src.services.completion_service import add_completion_to_db
            assert not add_completion_to_db(mock_response.return_value, "test prompt", user_id="test user")


def test_integration_add_completion_to_db_returns_false_with_duplicate_completion(client):
    with flask_app.app_context():
        patch_target = "src.services.completion_service.validated_openai_response"
        with patch(patch_target) as mock_response:
            mock_response.return_value = FAKE_COMPLETION

            from src.services.completion_service import add_completion_to_db
            add_completion_to_db(mock_response.return_value, "test prompt", user_id="test user")
            assert not add_completion_to_db(mock_response.return_value, "test prompt", user_id="test user")


def test_integration_get_completion_by_completion_id(client):
    with flask_app.app_context():
        patch_target = "src.services.completion_service.validated_openai_response"
        with patch(patch_target) as mock_response:
            mock_response.return_value = FAKE_COMPLETION

            from src.services.completion_service import add_completion_to_db, get_completion_by_completion_id
            from src.db_models.completions import Completion

            add_completion_to_db(mock_response.return_value, "test prompt", user_id="test user")
            completion = get_completion_by_completion_id("cmpl-test_id")
            assert completion is not None
            assert type(completion) == Completion
