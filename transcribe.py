import os
import glob
import openai
from logger import logger

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Необходимо задать переменную окружения OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

AUDIO_FOLDER = "audio"
OUTPUT_FILE = "output.txt"

SUPPORTED_EXTENSIONS = ["*.mp3", "*.mp4", "*.mpeg", "*.mpga", "*.m4a", "*.wav", "*.webm"]

def get_audio_files():
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(glob.glob(os.path.join(AUDIO_FOLDER, '**', ext), recursive=True))
    return files

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        return transcript["text"] if isinstance(transcript, dict) else transcript.text
    except openai.error.OpenAIError as api_err:
        logger.error(f"Ошибка OpenAI API при обработке {file_path}: {api_err}")
        raise
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при обработке {file_path}: {e}")
        raise

def main():
    audio_files = get_audio_files()
    if not audio_files:
        logger.info("Не найдено аудиофайлов в папке audio.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        for file_path in audio_files:
            filename = os.path.basename(file_path)
            logger.info(f"Обработка файла: {filename}...")
            try:
                transcription = transcribe_audio(file_path)
                output.write(f"{filename}\n===\n{transcription}\n\n")
            except Exception as e:
                output.write(f"{filename}\n===\nОшибка: {e}\n\n")

if __name__ == "__main__":
    main()


