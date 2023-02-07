from pytube import YouTube
from io import BytesIO

class VideoDownloader:
    def __init__(self, url: str) -> None:
        self.url = url
        self.youtube = YouTube(url)
        self.streams = self.youtube.streams
        self.title = self.streams.get_lowest_resolution().title
        self.extension = self.streams.get_lowest_resolution().subtype
        self.thumbnail_url = self.youtube.thumbnail_url
    
    def StreamToBuffer(self, resolution: str = '144p') -> bytes:
        buffer = BytesIO()
        self.streams.filter(res=resolution, file_extension='mp4').first().stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer.read()

    def GetAvailableResolutions(self) -> list:
        res = set()
        for i in self.streams.filter(file_extension='mp4'):
            if i.resolution:
                res.add(i.resolution)
        return sorted(list(res))

class PlaylistDownloader:
    def __init__(self, url) -> None:
        pass

# video = VideoDownloader('https://www.youtube.com/watch?v=a8DM-tD9w2I')

# with open(f'{video.title}.{video.extension}','wb') as f:
#     f.write(video.StreamToBuffer('720p'))
