#Author='MouShuai'

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import zipfile
import result_handler
import time
from result_structure import Record, ImageResult, VideoResult

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/data/greendam/website/video_result/app/files/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_ZIP_EXTENSIONS'] = set(['zip'])
app.config['ALLOWED_TXT_EXTENSIONS'] = set(['txt'])
# This is the path to the processed result files
RESULT_FOLDER = 'result_folder'
ZIP_FOLDER = 'zip_folder'
LABEL = ['normal', 'porn', 'sexy']


# For a given file, return whether it's an allowed type or not
def allowed_zip_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_ZIP_EXTENSIONS']


def allowed_txt_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_TXT_EXTENSIONS']


class args:
    input_dir = ''
    ground_truth_file = ''
    output_dir = ''


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/history')
def history():
    record_path = os.listdir(app.config['UPLOAD_FOLDER'])
    record_list = []
    for record_time_name in record_path:
        record = Record()
        record.time = (record_time_name.replace('_', ' ')).replace('~', ':')
        record_path = os.path.join(app.config['UPLOAD_FOLDER'], record_time_name)
        zip_path = os.path.join(record_path, ZIP_FOLDER)
        zip_file_list = os.listdir(zip_path)
        for zip_file_name in zip_file_list:
            record.name = zip_file_name
        record_list.append(record)

    record_list.sort(key=lambda x: x.time, reverse=True)
    return render_template('history.html', record_list=record_list)


@app.route('/video/<video_path>')
def video_play(video_path):
    print video_path
    video_path = video_path.replace('_', '/')
    return render_template('video_play.html', video_path=video_path)


@app.route('/video_result/<video_time>/<video_name>')
def video_result(video_time, video_name):
    record_time_path = os.path.join(app.config['UPLOAD_FOLDER'], video_time)
    record_zip_folder_path = os.path.join(record_time_path, ZIP_FOLDER)
    record_list = os.listdir(record_zip_folder_path)
    for record in record_list:
        img_result_list = []
        record_folder = os.path.join(record_zip_folder_path, record)
        print video_name
        video_file = os.path.join(record_folder, video_name.replace('mp4', 'txt'))
        video_path = ''
        with open(video_file) as fh:
            lines = fh.readlines()
            for line in lines:
                img_result = ImageResult()
                line_arr = []
                line_arr = line.strip().split(' ')
                if line_arr.__len__() > 3:
                    pos = line_arr.__len__() - 1
                    img_result.score = line_arr[pos]
                    img_result.pre_label = line_arr[pos-1]
                    for i in range(pos - 1):
                        if i < pos - 2:
                            img_result.path += line_arr[i] + ' '
                        else:
                            img_result.path += line_arr[i]
                else:
                    img_result.path, img_result.pre_label, img_result.score = line.strip().split(' ')
                img_result.name = os.path.basename(img_result.path)
                img_result_list.append(img_result)
            video_path = os.path.dirname(lines[0]) + '.mp4'
    return render_template('video_result.html', img_result_list=img_result_list, video_path=video_path)


@app.route('/record_result/<record_time>')
def record_result(record_time):
    print record_time
    record_time_filename = (record_time.replace(' ', '_')).replace(':', '~')
    record_file = os.path.join(app.config['UPLOAD_FOLDER'], record_time_filename)
    result_folder = os.path.join(record_file, RESULT_FOLDER)
    video_list = []
    with open(os.path.join(result_folder, result_handler.COMPARISON_FILE)) as fh:
        lines = fh.readlines()
        for line in lines:
            video = VideoResult()
            line_arr = []
            line_arr = line.strip().split(' ')
            if line_arr.__len__() > 4:
                pos = line_arr.__len__() - 1
                video.score = line_arr[pos]
                video.pre_label = line_arr[pos-1]
                video.ground_truth_label = line_arr[pos - 2]
                for i in range(pos - 2):
                    if i < pos - 2:
                        video.path += line_arr[i] + ' '
                    else:
                        video.path += line_arr[i]
            else:
                video.path, video.ground_truth_label, video.pre_label, video.score = line.strip().split(" ")
            video.ground_truth_label = LABEL[int(video.ground_truth_label)]
            video.pre_label = LABEL[int(video.pre_label)]
            video.name = os.path.basename(video.path)
            video.path = video.path.replace('/', '_')
            video.time = record_time_filename
            video_list.append(video)
        fh.close()
    distributions = []
    with open(os.path.join(result_folder, result_handler.DISTRIBUTION_FILE)) as fh:
        lines = fh.readlines()
        for line in lines:
            distribution = []
            normal_percent, porn_percent, sexy_percent = line.strip().split(' ')
            distribution.append(normal_percent)
            distribution.append(porn_percent)
            distribution.append(sexy_percent)
            distributions.append(distribution)
        fh.close()
    accuracy = ''
    with open(os.path.join(result_folder, result_handler.EVALUATION_FILE)) as fh:
        accuracy = fh.readline().strip().split(' ')[1]
        fh.close()
    return render_template('record_result.html', video_list=video_list,
                           distributions=distributions, accuracy=accuracy, labels=LABEL)


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    result_zip_file = request.files['ResultZipFile']
    ground_truth_file = request.files['GroundTruthFile']
    print result_zip_file.filename
    print ground_truth_file.filename
    # filenames = []
    if result_zip_file and allowed_zip_file(result_zip_file.filename) \
            and ground_truth_file and allowed_txt_file(ground_truth_file.filename):
        filename = secure_filename(result_zip_file.filename)
        zip_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        result_zip_file.save(zip_file_path)

        ground_truth_filename = secure_filename(ground_truth_file.filename)
        ground_truth_file_path = os.path.join(app.config['UPLOAD_FOLDER'], ground_truth_filename)
        ground_truth_file.save(ground_truth_file_path)

        timestamp = time.strftime('%Y-%m-%d_%H~%M~%S', time.localtime(time.time()))
        zip_file = zipfile.ZipFile(zip_file_path, 'r')
        record_path = os.path.join(app.config['UPLOAD_FOLDER'], timestamp)
        zip_path = os.path.join(record_path, ZIP_FOLDER)
        zip_file.extractall(zip_path)
        folder_list = os.listdir(zip_path)
        zip_file.close()
        video_list = []
        for folder in folder_list:
            args.ground_truth_file = ground_truth_file_path
            args.input_dir = os.path.join(zip_path, folder)
            args.output_dir = os.path.join(record_path, RESULT_FOLDER)

            if os.path.exists(args.output_dir) is not True:
                os.makedirs(args.output_dir)

            result_handler.result_deepir_process(args)
            result_handler.evaluation(args)
            result_handler.distribution(args)
            result_handler.comparison(args)

        result_folder = os.path.join(os.path.join(record_path, RESULT_FOLDER))
        with open(os.path.join(result_folder, result_handler.COMPARISON_FILE)) as fh:
            lines = fh.readlines()
            for line in lines:
                video = VideoResult()
                line_arr = []
		line_arr = line.strip().split(' ')
		if line_arr.__len__() > 4:
                    pos = line_arr.__len__() - 1
                    video.score = line_arr[pos]
                    video.pre_label = line_arr[pos-1]
                    video.ground_truth_label = line_arr[pos - 2]
                    for i in range(pos - 2):
                        if i < pos - 2:
                            video.path += line_arr[i] + ' '
			else:
                            video.path += line_arr[i]
		else:
                    video.path, video.ground_truth_label, video.pre_label, video.score = line.strip().split(" ")
                video.ground_truth_label = LABEL[int(video.ground_truth_label)]
                video.pre_label = LABEL[int(video.pre_label)]
                video.name = os.path.basename(video.path)
                video.path = video.path.replace('/', '_')
                video.time = timestamp
                video_list.append(video)
            fh.close
        os.remove(os.path.join(os.getcwd(), zip_file_path))
        os.remove(os.path.join(os.getcwd(), ground_truth_file_path))
        distributions = []
        with open(os.path.join(result_folder, result_handler.DISTRIBUTION_FILE)) as fh:
            lines = fh.readlines()
            for line in lines:
                distribution = []
                normal_percent, porn_percent, sexy_percent = line.strip('').split(' ')
                distribution.append(normal_percent)
                distribution.append(porn_percent)
                distribution.append(sexy_percent)
                distributions.append(distribution)
            fh.close()
        accuracy = ''
        with open(os.path.join(result_folder, result_handler.EVALUATION_FILE)) as fh:
            accuracy = fh.readline().strip('\n').split(' ')[1]
            fh.close()
    return render_template('upload.html', video_list=video_list,
                           distributions=distributions, accuracy=accuracy, labels=LABEL)


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
# http://www.sharejs.com
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/data/<filename>')
def data(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(
        debug=True
    )

