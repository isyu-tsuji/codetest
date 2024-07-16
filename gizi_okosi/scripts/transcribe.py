
import whisper
import os

def transcribe_audio(file_path, output_dir):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".wav", ".txt"))
    with open(output_file, "w") as f:
        f.write(result['text'])
    return output_file

if __name__ == "__main__":
    audio_dir = "audio"
    transcription_dir = "transcriptions"
    if not os.path.exists(transcription_dir):
        os.makedirs(transcription_dir)

    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".wav"):
            transcribe_audio(os.path.join(audio_dir, audio_file), transcription_dir)
