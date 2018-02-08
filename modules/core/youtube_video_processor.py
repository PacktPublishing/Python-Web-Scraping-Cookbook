import pytube as pt
from util.urls import URLUtility
import sys
import os

class YouTubeVideoProcessor():
    def __init(self):
        self._video_id = None
        self._video_info = None
        self._thumbnails = None
        self._thmbnail_names_in_order_of_quality = ['default', 'hqdefault', 'mqdefault', 'sddefault', 'maxresdefault']

    def get_video_info(self, video_id):
        self._video_id = video_id
        self._video_info = pt.YouTube("http://youtube.com/watch?v=" + video_id)

    def get_video_info_via_url(self, video_url):
        self._video_url = video_url
        self._video_info = pt.YouTube(video_url)
        return self._video_info

    def get_videos_of_type(self, video_type):
        return self._video_info.filter(video_type)

    def download(self, video_type, video_id, index=-1, on_progress = None, location="."):
        videos = self.get_videos_of_type(video_type)
        video = videos[index]

        progress = on_progress
        if progress is None:
            progress = self.print_download_status
        video.download(location, force_overwrite=True, on_progress = progress)
        from_filename = location+"/"+video.filename+"."+video.extension
        to_filenanme = location+"/"+video_id+"."+video.extension
        os.rename(from_filename, to_filenanme)
        print()

    def print_download_status(self, br, fs, start):
        pct_done = br / fs
        width=30
        seg1 = int(width * pct_done)
        output = "\r" + "|" + "*"*(seg1) + " " *(width-seg1) + "|" + "{0:.0f}%".format(pct_done*100)
        #output = "{0}% {1} {2}".format(int(br / fs * 1000) / 10, br, fs, start)
        print(output, end='')
        sys.stdout.flush()

    def get_thumbnails(self):
        self._thumbnails = {}

        thumbnail_url_base = "https://img.youtube.com/vi/"

        for i in range(0, 4):
            thumbnail_url = thumbnail_url_base + self.video_id + "/" + str(i) + ".jpg"
            print("Getting thumbnail: " + thumbnail_url)
            try:
                data = URLUtility(thumbnail_url).data
                print("Got video thumbnail # " + str(i))
                self._thumbnails[str(i)] = data
            except:
                pass

        names = ['default', 'hqdefault', 'mqdefault', 'sddefault', 'maxresdefault']
        for n in names:
            thumbnail_url = thumbnail_url_base + self.video_id + "/" + n + ".jpg"
            print("Getting thumbnail: " + thumbnail_url)
            try:
                data = URLUtility(thumbnail_url).data
                print("Got video thumbnail # " + n)
                self._thumbnails[n] = data
            except:
                pass

    def rip(self, video_filename, audio_filename):
        print("Ripping video to audio: " + video_filename + " " + audio_filename)
        clip = mp.VideoFileClip(video_filename)
        clip.audio.write_audiofile(audio_filename)
        print("Rip complete")

    @property
    def filename(self):
        return self._video_info.filename

    @property
    def title(self):
        return self._video_info.title

    @property
    def thumbnails(self):
        return self._thumbnails

    @property
    def video_id(self):
        return self._video_info.video_id

    @property
    def default_thumbnail(self):
        return self._thumbnails["default"]

    @property
    def hq_thumbnail(self):
        return self._thumbnails["hqdefault"]

    @property
    def maxres_thumbnail(self):
        return self._thumbnails["maxresdefault"]

    @property
    def mq_thumbnail(self):
        return self._thumbnails["mqthumbnail"]

    @property
    def sd_thumbnail(self):
        return self._thumbnails["sdthumbnail"]

    @property
    def thumbnail(self, index):
        return self._thumbnails[str(index)]
