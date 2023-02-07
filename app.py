from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from youtube_downloader import VideoDownloader, PlaylistDownloader
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Powerful Secret Key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    if "VideoLinkInput" in request.form:
        if request.form["VideoLinkInput"] == '':
            flash("Enter the URL.")
            return render_template('index.html')
        elif str(request.form["VideoLinkInput"]).find('?v=') == -1:
            flash("Enter a valid URL.")
            return render_template('index.html')
        
        video_id = request.form["VideoLinkInput"].split('?v=')[1]
        return redirect(url_for('download_video',vid_id = video_id))

    if "PlaylistLinkInput" in request.form:
        if request.form["PlaylistLinkInput"] == '':
            flash("Enter the URL.")
            return render_template('index.html')
        elif str(request.form["PlaylistLinkInput"]).find('playlist?list=') == -1:
            flash("Enter a valid URL.")
            return render_template('index.html')
        
        playlist_id = request.form["PlaylistLinkInput"].split('playlist?list=')[1]
        return redirect(url_for('download_playlist',pl_id = playlist_id))

@app.route('/download/video/<string:vid_id>', methods=['GET', 'POST'])
def download_video(vid_id):
    try:
        video = VideoDownloader(f"""https://www.youtube.com/watch?v={vid_id}""")
    except:
        flash("Enter a valid URL.")
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('download_video.html', title = video.title, thumbnail = video.thumbnail_url,
                                resolutions = video.GetAvailableResolutions())
    return send_file(
        BytesIO(video.StreamToBuffer(request.form['SelectedResolution'])),
        as_attachment = True,
        download_name=f"""{video.title}.mp4""")

@app.route('/download/playlist/<string:pl_id>', methods=['GET', 'POST'])
def download_playlist(pl_id):
    try:
        playlist = PlaylistDownloader(f"""https://www.youtube.com/playlist?list={pl_id}""")
        videos = playlist.GetVideos()
    except:
        flash("Enter a valid URL.")
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('download_playlist.html', title = playlist.title, videos = videos)
    
    # Create a ZipFile object in memory
    in_memory = BytesIO()
    with ZipFile(in_memory, 'w') as zip:
        # Add multiple files to the zip file
        for file in videos:
            zip.writestr(f"""{file.title}.mp4""",file.StreamToBuffer(request.form['SelectedResolution']))

    # Set the zip file as the response
    in_memory.seek(0)
    return send_file(in_memory, download_name=f"""{playlist.title}.zip""", as_attachment=True)
