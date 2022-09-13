from typing import Optional, Union
import src.db_models.db_session as db_session
from src.db_models.completions import Completion
from openai import Completion as ai_completion


def add_completion_to_db(resp: dict, prompt: str, ip_id: str = None, user_id: int = None):
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


def call_openai(prompt: str, max_tokens: int = 250) -> Optional[ai_completion]:
    """ Make a completion """

    completion = ai_completion.create(
        model="text-davinci-002",
        prompt=f"Computer Science Tutor: I am a computer science tutor.\nYou: I have a variable that stores a dictionary about bird data, like species, wingspan, and so on. Should I name it bird_dictionary?\nComputer Science Tutor: When naming variables, keep them concise and descriptive. Also, a variable name should be independent from its data type, so it should not contain the word dictionary or dict. Consider naming it bird instead, or perhaps bird_data.\nYou: {prompt}",
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["You:"]
    )
    return completion.to_dict()

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


# todo: add more validation to the completion

def validate_prompt_len(prompt: str) -> Union[bool, str]:
    """ Validate the completion prompt """
    return None if len(prompt) <= 200 else 'Prompt too long'


def get_completion_by_id(completion_id: int) -> Optional[Completion]:
    """ Get a completion by id """
    session = db_session.create_session()
    return session.query(Completion).filter(Completion.id == completion_id).first()


def get_all_completions() -> list[Completion]:
    """ Get all completions """
    session = db_session.create_session()
    return session.query(Completion).all()
