import os
import sys
import moviepy.editor as mp
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from pydub.utils import make_chunks


"""def downloadWithURL(url: str) -> None:
    options = {'format': 'bestaudio/best',
               'default_search': 'auto',
               'playliststart': 0,
               'extract_flat': True,
               'playlistend': 1,
               'quiet': True,
               'ignore_no_formats_error': True
               }
    with YoutubeDL(options) as downloader:
        try:
            alreadyExistingVideos = os.listdir('./')
            newAlreadyExistingVideos = []
            for file in alreadyExistingVideos:
                if file.find('webm') != 0:
                    newAlreadyExistingVideos.append(file)

            print(alreadyExistingVideos)

            info = downloader.extract_info(url, download=True)
            videoPath = None

            # Try to find the video
            alreadyExistingVideos = os.listdir('./')
            for file in alreadyExistingVideos:
                if file.find('webm') != 0 and file not in newAlreadyExistingVideos:
                    videoPath = f'./{file}'
                    return videoPath

            print(alreadyExistingVideos)

            if 'title' in info.keys:
                videoTitle = info['title']
                print(videoTitle)
                for file in alreadyExistingVideos:
                    if videoTitle in file:
                        videoPath = f'./{file}'
                        return videoPath

            sys.exit(
                "Não foi possível encontrar o video após ser baixado, altere o nome dele e torne o link do video igual a None")

        except Exception as e:  # Any type of error in download
            print(f'DEVELOPER NOTE -> Error: {e}')
            return None
"""

# INSERT HERE THE YOUTUBE VIDEO LINK, IF IS NONE WILL SEARCH A VIDEO ALREADY DOWNLOADED
# LINK_OF_YOUTUBE_VIDEO = None
# LINK_OF_YOUTUBE_VIDEO = 'https://www.youtube.com/watch?v=Si_5ebTbqd8'
# if LINK_OF_YOUTUBE_VIDEO is not None:
#    PATH_OF_FILE_VIDEO = downloadWithURL(LINK_OF_YOUTUBE_VIDEO)

# if LINK_OF_YOUTUBE_VIDEO is None or PATH_OF_FILE_VIDEO is None:
# INSERT HERE THE PATH TO THE FILE VIDEO

PATH_OF_FILE_VIDEO = './cutVideo.mp4'
START_SECOND = 8.5
FINISH_SECOND = 13.5
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
