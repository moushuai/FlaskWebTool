__author__ = 'shuai'
import os.path
import argparse
import logging

DESCRIPTION = ""
VIDEO_RESULT_FILE = 'result.txt'
EVALUATION_FILE = 'evaluation.txt'
DISTRIBUTION_FILE = 'distribution.txt'
COMPARISON_FILE = 'comparison.txt'


def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     formatter_class=
                                     argparse.RawTextHelpFormatter)
    # parser.add_argument('task', type=str, choices=['tencent', 'tupu', 'deepir'], help='api')
    parser.add_argument('-i', '--input_dir', type=str, help='input dir')
    parser.add_argument('-o', '--output_file', type=str, help='output file')
    parser.add_argument('-g', '--ground_truth_file', type=str, help='ground truth file')
    # parser.add_argument('-e', '--evaluation_file', type=str, help='evaluation file')
    parser.add_argument("--log", type=str, default="INFO",
                        help="log level")
    return parser.parse_args()


def evaluation(args):
    assert (args.ground_truth_file is not None)
    assert (args.output_file is not None)

    ground_truth = {}
    num = 0
    total = 0
    with open(args.ground_truth_file) as fh:
        lines = fh.readlines()
        for line in lines:
            print line
            img, label = line.strip('\n').split(' ')
            ground_truth[img] = label
        fh.close()
    with open(os.path.join(args.output_file, VIDEO_RESULT_FILE)) as fh:
        lines = fh.readlines()
        for line in lines:
            path, label = line.strip('\n').split(' ')
            total += 1
            # img = path.split(":")[1]
            if img in ground_truth:
                # print img
                if ground_truth[img] == label:
                    num += 1
        fh.close()
    percent = (float(num) / float(total)) * 100
    file_writer = open(os.path.join(args.output_file, EVALUATION_FILE), 'w')
    file_writer.write('correct number: %d (%.2f%%)' % (int(num), percent))


def distribution(args):
    assert (args.output_file is not None)
    result_file = os.path.join(args.output_file, VIDEO_RESULT_FILE)
    if os.path.exists(result_file) is not True:
        print 'No result to compute distribution!'
        return
    file_writer = open(os.path.join(args.output_file, DISTRIBUTION_FILE), 'w')
    porn_num = 0
    normal_num = 0
    sexy_num = 0
    with open(result_file, 'r') as fh:
        video_result_list = fh.readlines()
        for line in video_result_list:
            path, label = line.strip('\n').split(' ')
            if label == '0':
                normal_num += 1
            elif label == '1':
                porn_num += 1
            else:
                sexy_num += 1
        fh.close()
    total = normal_num + porn_num + sexy_num
    percent0 = (float(normal_num)/total)*100
    percent1 = (float(porn_num)/total)*100
    percent2 = (float(sexy_num)/total)*100
    file_writer.write('normal: %d %2f porn: %d %f sexy: %d %.2f'
                      % (normal_num, percent0, porn_num, percent1, sexy_num, percent2))
    file_writer.close()


def comparison(args):
    assert (args.ground_truth_file is not None)
    assert (args.output_file is not None)
    result_file = os.path.join(args.output_file, VIDEO_RESULT_FILE)
    if os.path.exists(result_file) is not True:
        print 'No result to compare!'
        return
    file_writer = open(os.path.join(args.output_file, COMPARISON_FILE), 'a')
    ground_truth = {}
    with open(args.ground_truth_file, 'r') as fh:
        ground_truth_list = fh.readlines()
        for line in ground_truth_list:
            path, label = line.strip('\n').split(' ')
            ground_truth[path] = label

    with open(result_file, 'r') as fh:
        video_result_list = fh.readlines()
        for line in video_result_list:
            path, label = line.strip('\n').split(' ')
            if path in ground_truth:
                file_writer.write('%s %s %s\n' % (path, label, ground_truth[path]))
        fh.close()
    file_writer.close()


def result_deepir_process(args):
    assert (args.input_dir is not None)
    assert (args.output_file is not None)

    video_list = os.listdir(args.input_dir)
    file_writer = open(os.path.join(args.output_file, VIDEO_RESULT_FILE), 'a')
    for video in video_list:
        with open(os.path.join(args.input_dir, video)) as fh:
            img_list = fh.readlines()
            porn = False
            hot = False
            for img in img_list:
                print img
                # name = img.split('\t')[0]
                # if name == 'IMAGE_NAME':
                #     continue
                name, label, score = img.strip('\n').split(' ')

                print label + ' ' + score
                if label == 'porn':
                    porn = True
                    hot = False
                    break
                elif label == 'sexy':
                    hot = True
            video_label = os.path.basename(args.input_dir)
            if porn is True:
                line = '%s:%s %d' % (video_label, video.replace('txt', 'mp4'), 1)
                file_writer.write(line + '\n')
            elif hot is True:
                line = '%s:%s %d' % (video_label, video.replace('txt', 'mp4'), 2)
                file_writer.write(line + '\n')
            else:
                line = '%s:%s %d' % (video_label, video.replace('txt', 'mp4'), 0)
                file_writer.write(line + '\n')
        fh.close()
    file_writer.close()


if __name__ == '__main__':
    args = get_args()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: " + args.log)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=numeric_level)
    # if args.task == 'tencent':
    #     result_tencent_process(args)
    # elif args.task == 'tupu':
    #     result_tupu_process(args)
    # elif args.task == 'deepir':
    result_deepir_process(args)
    evaluation(args)
    distribution(args)
    comparison(args)
