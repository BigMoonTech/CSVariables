from typing import Optional, Union

import openai
import sqlalchemy.exc as exc
from openai.error import AuthenticationError, APIError, APIConnectionError, InvalidRequestError, OpenAIError, Timeout

import src.db_models.db_session as db_session
from src.db_models.completions import Completion
from openai import Completion as aiCompletion
from src.helpers import bad_words


def add_completion_to_db(completion_data: dict,
                         prompt: str,
                         ip_id: Union[str, None] = None,
                         user_id: Union[str, None] = None) -> bool:
    """
    Add a completion to the database and return True if successful.

    :param completion_data: a dictionary of completion data
    :param prompt: the prompt that was used to generate the completion
    :param ip_id: the ip id of the user if they are not registered
    :param user_id: the uuid of the user if they are registered
    :return: True if successful, False if not
    """
    try:
        completion = Completion()
        completion.completion_id = completion_data['id']
        completion.model = completion_data['model']
        completion.prompt_text = prompt
        completion.response_text = get_choices_text(completion_data)
        completion.finish_reason = get_choices_finish_reason(completion_data)
        completion.prompt_tokens = get_usage_prompt_tokens(completion_data)
        completion.completion_tokens = get_usage_completion_tokens(completion_data)
        completion.total_tokens = get_usage_total_tokens(completion_data)

        if user_id:
            completion.user_id = user_id
        else:
            completion.ip_id = ip_id

        session = db_session.create_session()

        # check if completion already exists and catch the IntegrityError if for some reason it does
        try:
            session.add(completion)
            session.commit()
            session.close()
            return True
        except exc.IntegrityError:
            session.rollback()
            session.close()
            return False

    # if any of the getters raise a KeyError then return False
    except KeyError:
        return False


def call_openai(prompt: str, max_tokens: int = 250) -> Optional[aiCompletion]:
    """ Make a completion """
    completion = aiCompletion.create(
        model="text-davinci-002",
        prompt=f"Computer Science Tutor: I am a computer science tutor.\nYou: I have a variable that stores a dictionary about bird data, like species, wingspan, and so on. Should I name it bird_dictionary?\nComputer Science Tutor: When naming variables, keep them concise and descriptive. Also, a variable name should be independent from its data type, so it should not contain the word dictionary or dict. Consider naming it bird instead, or perhaps bird_data.\nYou: {prompt}",
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["You:"]
    )

    return completion


def validated_openai_response(prompt: Union[str, None] = None) -> Union[dict, str]:
    """
    Validate the response from the OpenAI API. If the response is valid, return it.

    :param prompt: The prompt to call the OpenAI API with
    :return: The response dictionary or None
    """

    if not prompt:
        return 'You must provide a prompt.'

    try:
        completion_created = call_openai(prompt)
        if not completion_created:
            return "An error occurred while contacting OpenAI."
        return completion_created.to_dict()

    except AuthenticationError:
        return 'Error with openai authentication.'
    except APIError:
        return 'APIError raised'
    except APIConnectionError:
        return 'There was an error communicating with the OpenAI API. Please try again later.'
    except InvalidRequestError:
        return 'InvalidRequestError raised'
    except openai.error.RateLimitError:
        return "RateLimitError raised: We've hit the OpenAI API rate limit. Please try again later."
    except Timeout:
        return 'Request timed out. Please try again later.'
    except OpenAIError:
        return 'An unknown error occurred. Please try again later.'


def get_choices_text(completion: dict) -> str:
    """ Get the completion text from the api response """
    return completion['choices'][0]['text']


def get_choices_finish_reason(completion: dict) -> str:
    """ Get the finish reason from the api response """
    return completion['choices'][0]['finish_reason']


def get_usage_prompt_tokens(completion: dict) -> int:
    """ Get the prompt tokens from the api response """
    return completion['usage']['prompt_tokens']


def get_usage_completion_tokens(completion: dict) -> int:
    """ Get the completion tokens from the api response """
    return completion['usage']['completion_tokens']


def get_usage_total_tokens(completion: dict) -> int:
    """ Get the total tokens from the api response """
    return completion['usage']['total_tokens']


def valid_prompt_len(prompt: str) -> Union[bool, str]:
    """ Validate the completion prompt """
    return False if len(prompt) > 200 else True


def has_no_profanity(prompt: str) -> bool:
    """ Return False if the prompt contains a bad word """

    banned_words = bad_words.get_bad_words()
    return False if any(word in banned_words for word in prompt.split()) else True


def get_completion_by_completion_id(completion_id: str) -> Optional[Completion]:
    """ Get a completion by completion id """
    if not completion_id:
        return None

    session = db_session.create_session()
    completion = session.query(Completion).filter(Completion.completion_id == completion_id).first()
    session.close()

    if not completion:
        return None

    return completion


def get_all_completions() -> list[Completion]:
    """ Get all completions """
    session = db_session.create_session()
    return session.query(Completion).all()


def get_completions_by_uuid(user_id: str = None) -> Optional[list[Completion]]:
    """ Get all completions by user id """
    if user_id is None:
        return None

    session = db_session.create_session()
    completions = session.query(Completion).filter(Completion.user_id == user_id).all()
    session.close()

    # todo - move this to the template instead of doing it here because I don't really like the look of the fake table
    # These completions are shown in a user's history table, so if they don't have any I want to show a fake one
    if len(completions) == 0:
        return create_empty_completion()

    return completions


def create_empty_completion() -> list[Completion]:
    """ A fake completion for a new user's empty Dashboard """

    completion = Completion()
    completion.id = 0
    completion.completion_id = 'No Data'
    completion.prompt_text = 'No Data'
    completion.response_text = 'No Data'
    completion.total_tokens = 0
    return [completion]
