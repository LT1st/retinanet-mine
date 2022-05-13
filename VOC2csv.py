import os
import xml.etree.ElementTree as ET
import random
import math
import argparse
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir', type=str,default='D:\workspace\datasets\VOCtrainval_11-May-2012\VOCdevkit\VOC2012')
    parser.add_argument('-p', '--percent', type=float, default=0.2)
    parser.add_argument('-t', '--train', type=str, default='./datasets/train.csv')
    parser.add_argument('-v', '--val', type=str, default='./datasets/val.csv')
    parser.add_argument('-c', '--classes', type=str, default='./datasets/class.csv')
    args = parser.parse_args()
    return args

#获取特定后缀名的文件列表，以list的形式返回
def get_file_index(indir, postfix):
    print(indir)
    file_list = []
    for root, dirs, files in os.walk(indir):
        for name in files:
            if postfix in name:
                file_list.append(os.path.join(root, name))
    return file_list

#写入标注信息
def convert_annotation(csv, address_list):
    cls_list = []
    with open(csv, 'w') as f:
        for i, address in enumerate(tqdm(address_list)):
            in_file = open(address, encoding='utf8')
            strXml =in_file.read()
            in_file.close()
            root=ET.XML(strXml)
            for obj in root.iter('object'):
                #从xml文件中获取类别
                cls = obj.find('name').text
                cls_list.append(cls)
                xmlbox = obj.find('bndbox')
                #从xml文件中获取bbox的四个值，并转化为int类型
                b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)),
                     int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
                f.write(file_dict[address_list[i]])
                f.write( "," + ",".join([str(a) for a in b]) + ',' + cls)
                f.write('\n')
    return cls_list


if __name__ == "__main__":
    args = parse_args()
    file_address = args.indir
    test_percent = args.percent
    train_csv = args.train
    test_csv = args.val
    class_csv = args.classes
    #
    Annotations = get_file_index(file_address+'/Annotations', '.xml')
    Annotations.sort()
    # 可根据自己数据集图片后缀名修改 这是你VOC数据集的JPEGImage的路径 每一人路径不一样 我一般用的就是绝对路径
    JPEGfiles = get_file_index(file_address+'/JPEGImages', '.jpg')
    JPEGfiles.sort()
    # 若XML文件和图片文件名不能一一对应即报错
    assert len(Annotations) == len(JPEGfiles)
    #标签路径和图片路径以dict的形式一一对应
    file_dict = dict(zip(Annotations, JPEGfiles))
    num = len(Annotations)
    #根据百分比将划分训练集合测试集
    test = random.sample(k=math.ceil(num*test_percent), population=Annotations)
    train = list(set(Annotations) - set(test))

    cls_list1 = convert_annotation(train_csv, train)
    cls_list2 = convert_annotation(test_csv, test)
    cls_unique = list(set(cls_list1+cls_list2))

    with open(class_csv, 'w') as f:
        for i, cls in enumerate(cls_unique):
            f.write(cls + ',' + str(i) + '\n')
