import whisper, os

model = whisper.load_model("base")

folder_path = 'videos'
audios = []

with os.scandir(folder_path) as entries:
    for entry in entries:
        if entry.is_file():
            audios.append(entry.name) 

results = []
for audio in audios:
    result = model.transcribe(audio)
    results.append(result["text"])

