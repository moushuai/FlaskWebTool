# -*- coding:utf-8 -*-
# AUTHOR:   yuewu
# FILE:     tupu.py
# CREATED:  2015-08-13 14:50:01
# MODIFIED: 2015-08-13 14:50:01

from qiniu import Auth
from qiniu import put_file
from qiniu import etag
from qiniu import http

import numpy as np

import argparse
import logging
import os
# import json

import ast

DESCRIPTION = ""

remote_url = 'http://7xn4ym.com1.z0.glb.clouddn.com/'
q = Auth('0PpV8ljkJBnGPJrRe1IDnT_kWnD75rOqzcSUuOJc',
         '79_oIBEt_Gyk_4-n2sx09lg-XPFI8dLduGeCuJte')


def getargs():
    """ Parse program arguments.
    """

    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     formatter_class=
                                     argparse.RawTextHelpFormatter)
    parser.add_argument('task', type=str, choices=['upload', 'nrop', 'export'], help='bucket name')
    parser.add_argument('-b', '--bucket_name', type=str, help='bucket name')
    parser.add_argument('-r', '--remote_dir', type=str, help='remote dir')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='input file')
    parser.add_argument('-g', '--gt', type=str, help='ground truth file')
    parser.add_argument('-l', '--local_dir', type=str, help='slocal dir')
    parser.add_argument('-o', '--output_file', type=str, help='output file')
    parser.add_argument('-u', '--sure_file', type=str, help='output sure file for export')
    parser.add_argument("--log", type=str, default="INFO",
                        help="log level")

    return parser.parse_args()


def upload(args):
    """ Upload images to qiniu cloud
    """
    assert (args.bucket_name != None)
    assert (args.remote_dir != None)
    assert (args.input_file != None)
    assert (args.local_dir != None)

    bucket_name = args.bucket_name

    # with open(args.input_file) as fh:
    #     paths = filter(None, fh.readlines())
    img_num = 0
    for video in os.listdir(args.input_file):
        img_num += 1
        with open(os.path.join(args.input_file, video)) as fh:
            paths = filter(None, fh.readlines())
        mime_type = "image/jpg"

        for path in paths:
            key = (os.path.join(args.remote_dir, path)).strip('\n')
            print 'upload ', path, ' as ', key
            # path = path.split()[0]

            localfile = (os.path.join(args.local_dir, '%s' % (path))).strip('\n')
            print localfile
            token = q.upload_token(bucket_name, key)
            ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)

            assert info.status_code == 200
            assert ret['key'] == key
            assert ret['hash'] == etag(localfile)

        print '%d images uploaded' % (img_num)


def nrop(args):
    """ adult image recognition, save results to key\tjson string
    """
    assert (args.bucket_name != None)
    assert (args.remote_dir != None)
    assert (args.input_file != None)
    assert (args.output_file != None)

    bucket_name = args.bucket_name
    # with open(args.input_file) as fh:
    #     paths = filter(None, fh.readlines())
    img_num = 0
    for video in os.listdir(args.input_file):
        with open(os.path.join(args.input_file, video)) as fh:
            paths = filter(None, fh.readlines())
        print paths
        results = {}
        if os.path.exists(os.path.join(args.output_file, video)):
            with open(os.path.join(args.output_file, video), 'r') as fh:
                while True:
                    line = fh.readline().strip()
                    if len(line) == 0:
                        break
                    path, res = line.split('\t')
                    results[path] = res

        with open(os.path.join(args.output_file, video), 'a') as fh:
            try:
                for path in paths:
                    # path = path.split()[0]
                    if path not in results:
                        url = '%s/%s%s%s?nrop' % (remote_url, args.remote_dir, '%5C',
                                                  (path.replace('\\', '%5C')).strip())
                        print url
                        res = http._get(url, None, q)[0]
                        logging.info('results of %s' % path)
                        logging.info(str(res))
                        assert res['code'] == 0
                        results[path] = str(res)

                        fh.write('%s\t%s\n' % (path, results[path]))

                    else:
                        print path, ' already processed'
            except Exception as e:
                print 'error occured: ', e.message
        img_num += 1
        print '%d images recognized' % (img_num)


def load_gt(path):
    keys = []
    labels = []
    with open(path, 'r') as fh:
        gt = filter(None, fh.readlines())
    for item in gt:
        parts = item.strip().split()
        keys.append(parts[0])
        labels.append(int(parts[1]))
    return keys, np.array(labels)


def fake_prob(label, prob, cls_num):
    prob_left = 1 - prob
    probs = [0 for i in xrange(cls_num)]
    probs[label] = prob
    if label == 0:
        probs[1] = probs[2] = prob_left / 2.0
    elif label == 1:
        alpha = 2.0 / 3.0
        probs[2] = min(prob_left * alpha, probs[1])
        probs[0] = 1.0 - probs[1] - probs[2]
    else:
        alpha = 0.5
        probs[1] = min(prob_left * alpha, probs[2])
        probs[0] = 1.0 - probs[1] - probs[2]
    return probs


def export(args):
    """ export json results to svm results and sure list
    """
    assert (args.input_file != None)
    assert (args.gt != None)
    assert (args.output_file != None)
    assert (args.sure_file != None)

    # load gt
    keys, labels = load_gt(args.gt)
    # load json results
    tupu_results = {}
    with open(args.input_file, 'r') as fh:
        while True:
            line = fh.readline().strip()
            if len(line) == 0:
                break
            key, json_str = line.split('\t')
            if key in keys:
                tupu_results[key] = ast.literal_eval(json_str)

    # formalize  label
    label_map = {0: 1, 1: 2, 2: 0}
    # write results
    with open(args.output_file, 'w') as fh:
        key_num = len(keys)
        for i in xrange(key_num):
            assert (keys[i] in tupu_results)
            predict = tupu_results[keys[i]]['fileList'][0]
            # write label
            fh.write('%d' % (labels[i]))
            # write features
            probs = fake_prob(label_map[predict['label']], predict['rate'], 3)
            for k in xrange(len(probs)):
                fh.write(' %d:%f' % (k + 1, probs[k]))
            fh.write('\n')

    # export sure results
    with open(args.sure_file, 'w') as fh:
        key_num = len(keys)
        for i in xrange(key_num):
            assert (keys[i] in tupu_results)
            predict = tupu_results[keys[i]]['fileList'][0]
            # write label
            fh.write('%d\n' % (1 if predict['review'] == False else 0))


if __name__ == '__main__':
    args = getargs()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: " + args.log)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=numeric_level)
    if args.task == 'upload':
        upload(args)
    elif args.task == 'nrop':
        nrop(args)
    elif args.task == 'export':
        export(args)
