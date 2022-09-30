from typing import Optional, Union
import src.db_models.db_session as db_session
from src.db_models.completions import Completion
from openai import Completion as aiCompletion
from src.helpers import bad_words


def add_completion_to_db(resp: dict, prompt: str, ip_id: str = None, user_id: str = None):
    """ Add a completion to the database """

    completion = Completion()
    completion.completion_id = resp['id']
    completion.model = resp['model']
    completion.prompt_text = prompt
    completion.response_text = get_choices_text(resp)
    completion.finish_reason = get_choices_finish_reason(resp)
    completion.prompt_tokens = get_usage_prompt_tokens(resp)
    completion.completion_tokens = get_usage_completion_tokens(resp)
    completion.total_tokens = get_usage_total_tokens(resp)

    if user_id:
        completion.user_id = user_id
    else:
        completion.ip_id = ip_id

    session = db_session.create_session()
    session.add(completion)
    session.commit()
    session.close()


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
    try:
        return completion.to_dict()
    except AttributeError:
        return None

# todo: handle the case where the response is empty


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


def validate_openai_response(resp):
    return None