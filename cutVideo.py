import os
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.utils import make_chunks

# INSERT HERE THE PATH TO THE FILE VIDEO
PATH_OF_FILE_VIDEO = './cutVideo.mp4'
START_SECOND = 55
FINISH_SECOND = 60
DURATION = FINISH_SECOND - START_SECOND

# Load the video called exemplo.mp4 in the current directory
videoFile = mp.VideoFileClip(PATH_OF_FILE_VIDEO).subclip()

# Extract the audio form the videoFile and store into a file called audio.mp3
videoFile.audio.write_audiofile("./audio.mp3")

# Load the extracted audio from the file
audioFile = AudioSegment.from_file("./audio.mp3", "mp3")

# Cut the loaded audio into multiple chunks to process parallel, passing the time in milliseconds
chunks = make_chunks(audioFile, START_SECOND * 1000)

# Extract the chunk that starts in the start duration
if START_SECOND == 0:
    audio = sum(chunks)
else:
    audio = sum(chunks[1:])

# Export to a file to load again
audio.export('cutAudio.mp3', format='mp3')
audioFile = AudioSegment.from_file("./cutAudio.mp3", "mp3")

# Export the wanted video part
chunks = make_chunks(audioFile, DURATION * 1000)
chunks[0].export('cutAudio.mp3', format='mp3')

os.remove("./audio.mp3")
