import json
import os, sys, argparse
import logging
from annotation import Formatter # noqa
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')


parser = argparse.ArgumentParser(description='Convert My json format to'
                                             'ASAP json format')
# parser.add_argument('--json_path', default=r'dataset/process/json/', type=str,
#                     help='Path to the input annotation in json format')
# parser.add_argument('--xml_path', default=r'dataset/annotation/', metavar='XML_PATH', type=str,
#                     help='Path to the output ASAP xml annotation')



def main():
    logging.basicConfig(level=logging.INFO)

    # args = parser.parse_args()
    xml_path = '/nas/tangwenhao/data/camelyon16/pre_test/lesion_annotations'
    for xml in os.listdir(xml_path):
        xml_wholepath = os.path.join(xml_path, xml)
        (xml_path, xml_name_ext) = os.path.split(xml_wholepath)  # 分离文件路径和文件名
        (xml_name, extension) = os.path.splitext(xml_name_ext)  # 分离文件名和后缀
        out_json = '/nas/tangwenhao/data/camelyon16/pre_test/json/%s.json' % xml_name
        Formatter.camelyon16xml2json(xml_wholepath, out_json)
        print("finish,{}\n".format(xml_name))


if __name__ == "__main__":
    main()
