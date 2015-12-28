# __author__ = 'shuai'
import os.path


def initial_file_list(input_folder, save_folder):

    folder_list = os.listdir(input_folder)
    for video in folder_list:
        # file_list = []
        print video
        if(os.path.isdir(os.path.join(input_folder, video))):
            file_writer = open(save_folder + video + ".txt", 'w')
            for img in os.listdir(os.path.join(input_folder, video)):
                # file_list.append(os.path.join(video, img))
                print img
                file_writer.write(os.path.join(video, img) + '\n')
            file_writer.close()

if __name__ == '__main__':
    input_folder = 'D:/SMU/PornDetector/video/porn'
    save_folder = 'D:/SMU/PornDetector/video/porn_list/'
    initial_file_list(input_folder, save_folder)
