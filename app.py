from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from youtube_downloader import VideoDownloader
from io import BytesIO

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
        return redirect(url_for('download',vid_id = video_id))

    if "PlaylistLinkInput" in request.form:
        pass

@app.route('/download/<string:vid_id>', methods=['GET', 'POST'])
def download(vid_id):
    try:
        video = VideoDownloader(f"""https://www.youtube.com/watch?v={vid_id}""")
    except:
        flash("Enter a valid URL.")
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('download.html', title = video.title, thumbnail = video.thumbnail_url,
                                resolutions = video.GetAvailableResolutions())
    return send_file(
        BytesIO(video.StreamToBuffer(request.form['SelectedResolution'])),
        as_attachment = True,
        download_name=f'{video.title}.mp4')