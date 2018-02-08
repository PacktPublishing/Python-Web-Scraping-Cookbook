import moviepy.editor as mp
clip = mp.VideoFileClip("BigBuckBunny.mp4")
clip.audio.write_audiofile("movie_audio.mp3")
