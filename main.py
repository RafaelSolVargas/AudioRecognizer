import time
from typing import List
import speech_recognition as sr
import moviepy.editor as mp
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
from threading import Thread, Lock

# Configure the settings:
SIZE_OF_CHUNKS_SECONDS = 30  # Size of each chunk of audio in seconds
PATH_OF_VIDEO_FILE = "./exemplo.mp4"
SYNC_LOCK = Lock()

RECOGNITION_RESULTS_LIST = []


def recognizeAudioWithGoogle(audio: AudioSegment, chunkIndex: int) -> str:
    """ Function to recognize an piece of the audio and store the result into the RECOGNITION_RESULTS_LIST """
    global SIZE_OF_CHUNKS_SECONDS
    global RECOGNITION_RESULTS_LIST
    global SYNC_LOCK

    # Calculate the start and end time
    startTime = SIZE_OF_CHUNKS_SECONDS * chunkIndex
    endTime = SIZE_OF_CHUNKS_SECONDS * (chunkIndex + 1)
    # Convert into minute and seconds
    startMinute = startTime // 60
    startSeconds = startTime % 60
    endMinute = endTime // 60
    endSeconds = endTime % 60

    text = f'--> Audio de {startMinute}:{startSeconds} ate {endMinute}:{endSeconds}\n'

    # Save the received audio in a .wav file and load again as a AudioFile instance
    chunkFilePath = f'audio{chunkIndex}.wav'
    audio.export(chunkFilePath, format='wav')
    audioFile = sr.AudioFile("./" + chunkFilePath)

    recognizer = sr.Recognizer()
    with audioFile as source:
        # Reads the data from the audioFile
        audioData = recognizer.record(source)
        try:
            # Tries to recognize the text with the language portuguese
            text += recognizer.recognize_google(audioData, language='pt-BR')
        except Exception as e:
            text += f'Nao identificado'

    SYNC_LOCK.acquire()
    RECOGNITION_RESULTS_LIST[chunkIndex] = text
    SYNC_LOCK.release()

    os.remove(chunkFilePath)


def compileResultsIntoFile():
    """ Function to read all the results and store into an external file"""
    global RECOGNITION_RESULTS_LIST

    file = open('translation.txt', 'w')

    for result in RECOGNITION_RESULTS_LIST:
        print(f'{result}\n')
        file.write(f'{result}\n')

    file.close()


# Load the video called exemplo.mp4 in the current directory
videoFile = mp.VideoFileClip(PATH_OF_VIDEO_FILE).subclip()

# Extract the audio form the videoFile and store into a file called audio.mp3
videoFile.audio.write_audiofile("./audio.mp3")

# Load the extracted audio from the file
audioFile = AudioSegment.from_file("./audio.mp3", "mp3")

# Cut the loaded audio into multiple chunks to process parallel, passing the time in milliseconds
chunks = make_chunks(audioFile, SIZE_OF_CHUNKS_SECONDS * 1000)

# Create a list to store the result of each chunk created
RECOGNITION_RESULTS_LIST = [None for _ in range(len(chunks))]

# Create one Thread for each chunk and start each of them
threads: List[Thread] = []
for chunkIndex, fileChunk in enumerate(chunks):
    newThread = Thread(target=recognizeAudioWithGoogle, args=(fileChunk, chunkIndex))
    newThread.start()
    threads.append(newThread)

print('Começando a esperar')
# Wait until all threads finish the process
for thread in threads:
    thread.join()

print('Terminou de processar')

# Compile into an external file
compileResultsIntoFile()
