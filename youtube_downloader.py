from pytube import YouTube, Playlist
from io import BytesIO

class VideoDownloader:
    def __init__(self, url: str) -> None:
        self.url = url
        self.youtube = YouTube(url)
        # self.streams = self.youtube.streams
        self.title = self.youtube.title
        self.thumbnail_url = self.youtube.thumbnail_url
    
    def StreamToBuffer(self, resolution: str = 'low') -> bytes:
        buffer = BytesIO()
        if resolution == 'high':
            self.youtube.streams.filter(file_extension='mp4').get_highest_resolution().stream_to_buffer(buffer)
        elif resolution == 'low':
            self.youtube.streams.filter(file_extension='mp4').get_lowest_resolution().stream_to_buffer(buffer)
        else:
            self.youtube.streams.filter(res=resolution, file_extension='mp4').first().stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer.read()

    def GetAvailableResolutions(self) -> dict:
        res = set()
        result = {}
        for i in self.youtube.streams.filter(file_extension='mp4'):
            if i.resolution:
                res.add(i.resolution)
        for i in sorted(list(res)):
            size = self.youtube.streams.filter(file_extension='mp4', res=i).first().filesize_mb
            result[i] = float("{:.1f}".format(size))
        return result        

class PlaylistDownloader:
    def __init__(self, url) -> None:
        self.playlist = Playlist(url)
        self.title = self.playlist.title
        self.video_urls = self.playlist.video_urls

    def GetVideosURL(self) -> list:
        return list(self.video_urls)
    
    def GetVideosTitles(self) -> list[str]:
        lst = []
        for i in self.playlist.videos:
            lst.append(i.title)
        return lst

    def GetVideos(self) -> list[VideoDownloader]:
        return [VideoDownloader(v) for v in self.GetVideosURL()]

# playlist = PlaylistDownloader('https://www.youtube.com/playlist?list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX')
# for i in playlist.GetVideosURL():
#     print(i)

# video = VideoDownloader('https://www.youtube.com/watch?v=a8DM-tD9w2I')

# with open(f'{video.title}.{video.extension}','wb') as f:
#     f.write(video.StreamToBuffer('720p'))
