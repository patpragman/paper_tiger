from toolkit.query_tools import executive_summarizer, news_caster

with open('7may24.txt', "r") as speech_file:
    content = "".join([l for l in speech_file.readlines() if l != "\n"])

audio_segment = news_caster(content)
audio_segment.export("combined.mp3")
