import argparse
from toolkit.query_tools import route_model

def process_audio(prompt,
                  input_file, output_file,
                  text_model, audio_model, voice,):

    with open(input_file, "r") as speech_file:
        content = "".join([line for line in speech_file.readlines() if line != "\n"])

    audio_segment = route_model(tool_choice=prompt, content=content,
                                text_model=text_model, audio_model=audio_model, voice=voice, )
    audio_segment.export(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process text files into audio format.')
    parser.add_argument("--prompt", "-p", type=str, help='Prompt selector, default: lecturer', default="lecturer")
    parser.add_argument('--voice', '-v', type=str, help="openAI voice to use, default: nova", default="nova")
    parser.add_argument('--text_processing_model', '-tpm', help='Text Processing Model, default: gpt-4-turbo-preview', default="gpt-4-turbo-preview")
    parser.add_argument('--text_to_speech_model', '-tts', help="Text to speech model, default: tts-1", default='tts-1')
    parser.add_argument('--input_file', "-i", type=str, help='Path to the text file containing the speech content.')
    parser.add_argument('--output_file', "-o", type=str, help='Path to save the output audio file.')
    args = parser.parse_args()

    process_audio(prompt=args.prompt, input_file=args.input_file, output_file=args.output_file,
                  text_model=args.text_processing_model, audio_model=args.text_to_speech_model,
                  voice=args.voice,
                  )
