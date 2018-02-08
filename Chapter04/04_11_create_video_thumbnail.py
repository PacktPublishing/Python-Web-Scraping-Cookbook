import subprocess
video_file = 'BigBuckBunny.mp4'
thumbnail_file = 'thumbnail.jpg'
subprocess.call(['ffmpeg', '-i', video_file, '-ss', '00:01:03.000', '-frames:v', '1', thumbnail_file, "-y"])