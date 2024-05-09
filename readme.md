# Paper Tiger

This script allows you to convert a text file into an audio file using specific text processing and text-to-speech models. It is designed to handle scenarios where a prompt can select different models or processing pathways. The script is flexible with several configurable options.

## Features

- Converts text to audio using configurable text processing and text-to-speech models.
- Supports multiple voices through the use of the OpenAI API.
- Multiple starter prompts which will return different types of audio files
- Adjustable prompt selection for varying the style or type of the narration.

## Requirements

Ensure you have Python installed on your machine. The script requires additional Python libraries that can be installed using the requirements file:

```bash
pip install -r requirements.txt
```

If you want to use a virtual environment, it is similar

```bash
cd /to/working/directory/with/paper_tiger
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note: The requirements file should contain all the necessary libraries like openai, argparse, and any others needed for the script to function.

## Usage

To use this script, you must provide the necessary command line arguments. Here is an example command to run the script:

```bash
# make sure to use your openAI api key, so set the environmental variable before running
export OPENAI_API_KEY=<your key goes here>
python paper_tiger.py --input_file "path/to/input.txt" --output_file "path/to/output.mp3" --voice "nova" --prompt "lecturer" --text_processing_model "gpt-4-turbo-preview" --text_to_speech_model "tts-1"
```

Only `--input_file` and `--output_file` (or `-i` and `-o` respectively) are mandatory flags.

## Command Line Flags
* `--prompt` or `-p`: Selects the prompt type (default: "lecturer"). 
* `--voice` or `-v`: Specifies the voice to use (default: "nova"). 
* `--text_processing_model` or `-tpm`: Text processing model to use (default: "gpt-4-turbo-preview"). 
* `--text_to_speech_model` or `-tts`: Text to speech model to use (default: "tts-1"). 
* `--input_file` or `-i`: Path to the text file containing the speech content. 
* `--output_file` or `-o`: Path to save the output audio file.