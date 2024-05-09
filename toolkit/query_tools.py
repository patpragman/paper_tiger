from openai import OpenAI
from io import BytesIO
import tiktoken
from pydub import AudioSegment
from prompts.prompts import ExecutiveSummarizer, NewsCaster, Lecturer, Prompt


def join_snippets(snippets: list[AudioSegment]) -> AudioSegment:
    combined = AudioSegment.empty()
    for snippet in snippets:
        combined += snippet

    return combined


def num_tokens_from_string(string: str, encoding: tiktoken.Encoding = tiktoken.get_encoding('cl100k_base')) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_text_summary(text: str,
                     context: ExecutiveSummarizer,
                     text_model: str = 'gpt-4-turbo-preview',
                     ) -> str:
    openAI_client = OpenAI()

    response = openAI_client.chat.completions.create(
        model=text_model,
        messages=[{"role": "system", "content": context.context},
                  {"role": "user", "content": f"analyze the following text please:\n{text}"}]
    )

    return response


def get_audio_from_text(text: str, audio_model="tts-1", voice="nova", speed=1) -> AudioSegment:
    """
    Take in text, output an AudioSegment

    :param speed: speed of speech
    :param voice: voice choice
    :param model: the text to speech model to use
    :param text: a string with the text you wish to use
    :return:  an audio segment of spoken text
    """
    openAI_client = OpenAI()

    response = openAI_client.audio.speech.create(
        model=audio_model,
        voice=voice,
        speed=speed,
        input=text
    )

    audio_segment = AudioSegment.from_file(BytesIO(response.content), format="mp3")
    return audio_segment


def route_model(tool_choice: str, *args, **kwargs):
    mapping = {
        "executive": ExecutiveSummarizer(),
        "newscast": NewsCaster(),
        "lecturer": Lecturer(),
    }
    if tool_choice in mapping:
        return generic_function(*args, context_obj=mapping[tool_choice.lower()], **kwargs)
    else:
        raise ValueError(f'The following tool:  {tool_choice} is not available.')

def generic_function(content: str = "Testing 1,2, 3", context_obj: Prompt = Lecturer,
             text_model: str = "gpt-4-turbo-preview", audio_model='tts-1', voice='nova') -> AudioSegment:
    return join_snippets([
        get_audio_from_text(t.message.content, audio_model=audio_model, voice=voice)
        for t in get_text_summary(content, context_obj, text_model=text_model).choices],
    )


