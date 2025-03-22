import os
import glob
import subprocess
import tempfile
import openai
from logger import logger

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Необходимо задать переменную окружения OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

AUDIO_FOLDER = "audio"
OUTPUT_FILE = "output.txt"

SUPPORTED_EXTENSIONS = [
    "*.mp3", "*.mp4", "*.mpeg", "*.mpga", "*.m4a", "*.wav", "*.webm", "*.ogg"
]

def get_audio_files():
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(glob.glob(os.path.join(AUDIO_FOLDER, '**', ext), recursive=True))
    return files

def convert_ogg_to_wav(ogg_path):
    """
    Конвертирует .ogg файл во временный .wav файл с помощью ffmpeg.
    Возвращает путь к временному файлу.
    """
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav.close() 
    command = ["ffmpeg", "-y", "-i", ogg_path, temp_wav.name]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Ошибка конвертации файла {ogg_path}: {result.stderr.decode()}")
    return temp_wav.name

def transcribe_audio(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".ogg":
        logger.info(f"Конвертация .ogg файла: {file_path}")
        try:
            converted_file = convert_ogg_to_wav(file_path)
        except Exception as e:
            logger.error(f"Ошибка конвертации .ogg файла {file_path}: {e}")
            raise
        target_file = converted_file
        is_temp = True
    else:
        target_file = file_path
        is_temp = False

    try:
        with open(target_file, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        text = transcript["text"] if isinstance(transcript, dict) else transcript.text
    except openai.error.OpenAIError as api_err:
        logger.error(f"Ошибка OpenAI API при обработке {target_file}: {api_err}")
        raise
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при обработке {target_file}: {e}")
        raise
    finally:
        if is_temp:
            try:
                os.remove(target_file)
            except Exception as cleanup_err:
                logger.error(f"Ошибка удаления временного файла {target_file}: {cleanup_err}")
    return text

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


