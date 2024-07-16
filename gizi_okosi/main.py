import os
from scripts.transcribe import transcribe_audio
from scripts.correct import process_file

def main():
    audio_dir = "audio"
    transcription_dir = "transcriptions"
    corrected_dir = "corrected_transcriptions"

    if not os.path.exists(transcription_dir):
        os.makedirs(transcription_dir)
    if not os.path.exists(corrected_dir):
        os.makedirs(corrected_dir)

    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".wav"):
            transcription_file = transcribe_audio(os.path.join(audio_dir, audio_file), transcription_dir)
            process_file(transcription_file, corrected_dir)

if __name__ == "__main__":
    main()
