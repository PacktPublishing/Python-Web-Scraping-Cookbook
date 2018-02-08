from core.youtube_video_processor import YouTubeVideoProcessor
from core.youtube_playlist_videourl_extractor import YouTubePlaylistVideoUrlExtractor
from core.file_blob_writer import FileBlobWriter
import moviepy.editor as mp

class YouTubePlaylistCrawler():
    def __init__(self):
        pass

    def crawl_playlist(self, playlist_url, max_videos=None, createHTML=False, getThumbnails=False, location="."):
        print("Starting crawl of: " + playlist_url)

        url_extractor = YouTubePlaylistVideoUrlExtractor()
        urls = url_extractor.get(playlist_url).urls

        print("# of videos found: ", len(urls))

        vp = YouTubeVideoProcessor()

        i=0
        if max_videos is None:
            max_videos = len(urls)

        writer = FileBlobWriter(location)

        videos = []
        for url in urls:
            vi = vp.get_video_info_via_url(url)
            print(vp.filename)
            videos.append(vi)

            #vp.download("mp4", location=location, video_id=vp.video_id)

            print("Ripping MP3")
            clip = mp.VideoFileClip(location + "/" + vp.video_id + ".mp4")
            clip.audio.write_audiofile(location + "/" + vp.video_id + ".mp3")

            getThumbnails = False
            if getThumbnails:
                vp.get_thumbnails()
                for thumbnail_key in vp.thumbnails:
                    thumbnail_filename=vp.video_id + "_" + thumbnail_key + ".jpg"
                    thumbnail_bytes = vp.thumbnails[thumbnail_key]
                    writer.write(thumbnail_filename, thumbnail_bytes)
                    print("Wrote thumbnail: " + thumbnail_filename)

            i += 1
            if i == max_videos:
                print("Reached max number of videos - stopping")
                break

        if createHTML:
            # create HTML
            print("Writing HTML")
            with open(location + "/" + "index.html", "w") as tf:
                tf.write("<HTML><BODY>")
                for v in videos:
                    tf.write("<P>")
                    tf.write("<IMG SRC='" + v.video_id + "_sddefault.jpg' /><br/>")
                    tf.write("<H2>" + v.title + "</H2>")
                    tf.write("<A HREF='" + v.video_id + ".mp4'>Watch</A><BR/>")
                    tf.write("<A HREF='" + v.video_id + ".mp3'>Listen</A><BR/>")
                    tf.write("<P>")
                tf.write("</BODY></HTML>")
