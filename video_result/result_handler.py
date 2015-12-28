# __author__ = 'shuai'
import os.path
DESCRIPTION = ""
VIDEO_RESULT_FILE = 'result.txt'
EVALUATION_FILE = 'evaluation.txt'
DISTRIBUTION_FILE = 'distribution.txt'
COMPARISON_FILE = 'comparison.txt'


# def get_args():
#     parser = argparse.ArgumentParser(description=DESCRIPTION,
<<<<<<< HEAD
#                                      formatter_class=
=======
#                                      formatter_class=s
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
#                                      argparse.RawTextHelpFormatter)
#     # parser.add_argument('task', type=str, choices=['tencent', 'tupu', 'deepir'], help='api')
#     parser.add_argument('-i', '--input_dir', type=str, help='input dir')
#     parser.add_argument('-o', '--output_file', type=str, help='output file')
#     parser.add_argument('-g', '--ground_truth_file', type=str, help='ground truth file')
#     # parser.add_argument('-e', '--evaluation_file', type=str, help='evaluation file')
#     parser.add_argument("--log", type=str, default="INFO",
#                         help="log level")
#     return parser.parse_args()


def evaluation(args):
    assert (args.ground_truth_file is not None)
    assert (args.output_dir is not None)

    ground_truth = {}
    num = 0
    total = 0
    print args.ground_truth_file
    with open(args.ground_truth_file) as fh:
        lines = fh.readlines()
        for line in lines:
            # print line
<<<<<<< HEAD
            video, label = line.strip('\n').split(' ')
=======
            video, label = line.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
            ground_truth[video] = label
            print video, label
        fh.close()
    with open(os.path.join(args.output_dir, VIDEO_RESULT_FILE)) as fh:
        lines = fh.readlines()
        for line in lines:
<<<<<<< HEAD
            video, label, score = line.strip('\n').split(' ')
=======
            video, label, score = line.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
            total += 1
            # img = path.split(":")[1]
            if video in ground_truth:
                # print img
                # print ground_truth[video], label
                if ground_truth[video] == label:
                    num += 1
        fh.close()
    print num, total
    percent = (float(num) / float(total)) * 100
    file_writer = open(os.path.join(args.output_dir, EVALUATION_FILE), 'w')
    file_writer.write('accuracy %d(%.2f%%)' % (int(num), percent))


def distribution(args):
    assert (args.ground_truth_file is not None)
    assert (args.output_dir is not None)
    result_file = os.path.join(args.output_dir, VIDEO_RESULT_FILE)
    if os.path.exists(result_file) is not True:
        print 'No result to compute distribution!'
        return
    ground_truth = {}
    with open(args.ground_truth_file, 'r') as fh:
        ground_truth_list = fh.readlines()
        for line in ground_truth_list:
<<<<<<< HEAD
            path, label = line.strip('\n').split(' ')
=======
            path, label = line.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
            ground_truth[path] = label
        fh.close()

    porn_porn_num = 0
    porn_normal_num = 0
    porn_sexy_num = 0
    normal_porn_num = 0
    normal_normal_num = 0
    normal_sexy_num = 0
    sexy_porn_num = 0
    sexy_normal_num = 0
    sexy_sexy_num = 0
    porn_num = 0
    normal_num = 0
    sexy_num = 0
    with open(result_file, 'r') as fh:
        video_result_list = fh.readlines()
        for line in video_result_list:
            # video_result = VideoResult()
<<<<<<< HEAD
            path, label, score = line.strip('\n').split(' ')
=======
            path, label, score = line.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
            if path in ground_truth:
                if ground_truth[path] == '0':
                    normal_num += 1
                    if label == '0':
                        normal_normal_num += 1
                    elif label == '1':
                        normal_porn_num += 1
                    else:
                        normal_sexy_num += 1
                elif ground_truth[path] == '1':
                    porn_num += 1
                    if label == '0':
                        porn_normal_num += 1
                    elif label == '1':
                        porn_porn_num += 1
                    else:
                        porn_sexy_num += 1
                else:
                    sexy_num += 1
                    if label == '0':
                        sexy_normal_num += 1
                    elif label == '1':
                        sexy_porn_num += 1
                    else:
                        sexy_sexy_num += 1
        fh.close()
<<<<<<< HEAD

=======
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
    file_writer = open(os.path.join(args.output_dir, DISTRIBUTION_FILE), 'w')
    normal_normal_percent = 0 if normal_num == 0 else (float(normal_normal_num)/normal_num)*100
    normal_porn_percent = 0 if normal_num == 0 else (float(normal_porn_num)/normal_num)*100
    normal_sexy_percent = 0 if normal_num == 0 else (float(normal_sexy_num)/normal_num)*100
    porn_normal_percent = 0 if porn_num == 0 else (float(porn_normal_num)/porn_num)*100
    porn_porn_percent = 0 if porn_num == 0 else (float(porn_porn_num)/porn_num)*100
    porn_sexy_percent = 0 if porn_num == 0 else (float(porn_sexy_num)/porn_num)*100
    sexy_normal_percent = 0 if sexy_num == 0 else (float(sexy_normal_num)/sexy_num)*100
    sexy_porn_percent = 0 if sexy_num == 0 else (float(sexy_porn_num)/sexy_num)*100
    sexy_sexy_percent = 0 if sexy_num == 0 else (float(sexy_sexy_num)/sexy_num)*100

    file_writer.write('%d(%.2f%%) %d(%.2f%%) %d(%.2f%%)\n'
                      % (normal_normal_num, normal_normal_percent, normal_porn_num,
                         normal_porn_percent, normal_sexy_num, normal_sexy_percent))
    file_writer.write('%d(%.2f%%) %d(%.2f%%) %d(%.2f%%)\n'
                      % (porn_normal_num, porn_normal_percent, porn_porn_num,
                         porn_porn_percent, porn_sexy_num, porn_sexy_percent))
    file_writer.write('%d(%.2f%%) %d(%.2f%%) %d(%.2f%%)\n'
                      % (sexy_normal_num, sexy_normal_percent, sexy_porn_num,
                         sexy_porn_percent, sexy_sexy_num, sexy_sexy_percent))
    file_writer.close()


def comparison(args):
    assert (args.ground_truth_file is not None)
    assert (args.output_dir is not None)
    result_file = os.path.join(args.output_dir, VIDEO_RESULT_FILE)
    if os.path.exists(result_file) is not True:
        print 'No result to compare!'
        return
    file_writer = open(os.path.join(args.output_dir, COMPARISON_FILE), 'a')
    ground_truth = {}
    with open(args.ground_truth_file, 'r') as fh:
        ground_truth_list = fh.readlines()
        for line in ground_truth_list:
<<<<<<< HEAD
            path, label = line.strip('\n').split(' ')
=======
            path, label = line.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
            ground_truth[path] = label
        fh.close()
    # result_list = []
    with open(result_file, 'r') as fh:
        video_result_list = fh.readlines()
        for line in video_result_list:
            # video_result = VideoResult()
<<<<<<< HEAD
            path, label, score = line.strip('\n').split(' ')
=======
            path, label, score = line.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
            if path in ground_truth:
                # video_result.name = path
                # video_result.ground_truth_label = ground_truth[path]
                # video_result.pre_label = label
                # video_result.score = score
                file_writer.write('%s %s %s %s\n' % (path, ground_truth[path], label, score))
            # result_list.append(video_result)
        fh.close()
    file_writer.close()
    # return result_list


def result_deepir_process(args):
    assert (args.input_dir is not None)
    assert (args.output_dir is not None)

    video_list = os.listdir(args.input_dir)
    file_writer = open(os.path.join(args.output_dir, VIDEO_RESULT_FILE), 'a')
    for video in video_list:
        with open(os.path.join(args.input_dir, video)) as fh:
            img_list = fh.readlines()
            porn = False
            hot = False
            porn_score = 0.0
            hot_score = 0.0
            normal_score = 0.0
            name = ''
            for img in img_list:
                # print img
                # name = img.split('\t')[0]
                # if name == 'IMAGE_NAME':
                #     continue
<<<<<<< HEAD
                name, label, score_str = img.strip('\n').split(' ')
=======
                name, label, score_str = img.strip().split(' ')
>>>>>>> 9eccc5e387486e02d3fd0ae6a5c58b7fd7f79923
                score = float(score_str)
                # print label + ' ' + score
                if label == 'porn':
                    porn = True
                    hot = False
                    porn_score = score
                    break
                elif label == 'sexy':
                    hot = True
                    if score > hot_score:
                        hot_score = score
                else:
                    if score > normal_score:
                        normal_score = score
            path = os.path.dirname(name)
            video_name = path + '.mp4'
            if porn is True:
                line = '%s %d %.2f' % (video_name, 1, porn_score)
                file_writer.write(line + '\n')
            elif hot is True:
                line = '%s %d %.2f' % (video_name, 2, hot_score)
                file_writer.write(line + '\n')
            else:
                line = '%s %d %2.f' % (video_name, 0, normal_score)
                file_writer.write(line + '\n')
        fh.close()
    file_writer.close()
