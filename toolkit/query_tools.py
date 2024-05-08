from openai import OpenAI
from io import BytesIO
import tiktoken
from pydub import AudioSegment
from prompts.prompts import ExecutiveSummarizer, NewsCaster


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
                     model: str = 'gpt-4-turbo-preview',
                     ) -> str:
    openAI_client = OpenAI()

    response = openAI_client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": context.context},
                  {"role": "user", "content": f"analyze the following text please:\n{text}"}]
    )

    return response


def get_audio_from_text(text: str, model="tts-1", voice="nova", speed=1) -> AudioSegment:
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
        model=model,
        voice=voice,
        speed=speed,
        input=text
    )

    audio_segment = AudioSegment.from_file(BytesIO(response.content), format="mp3")
    return audio_segment


def executive_summarizer(text: str, context_obj: ExecutiveSummarizer = ExecutiveSummarizer(),
                         text_model: str = "gpt-4-turbo-preview", audio_model='tts-1', voice='nova') -> AudioSegment:
    return join_snippets([
        get_audio_from_text(t.message.content, model=audio_model, voice=voice)
        for t in get_text_summary(text, context_obj, model=text_model).choices],
    )


def news_caster(text: str, context_obj: NewsCaster = NewsCaster(),
                text_model: str = "gpt-4-turbo-preview", audio_model='tts-1', voice='nova') -> AudioSegment:
    return join_snippets([
        get_audio_from_text(t.message.content, model=audio_model, voice=voice)
        for t in get_text_summary(text, context_obj, model=text_model).choices],
    )
