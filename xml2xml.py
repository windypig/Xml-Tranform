# -*- coding: UTF-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import sys
import shutil

src_dir = sys.argv[1]
des_dir = sys.argv[2]
map_dir = sys.argv[3]
pic_dir = sys.argv[4]
dir_map_dir = sys.argv[5]

dir_file = open(dir_map_dir, 'w')


dir_num = -1

head = '<?xml version="1.0" encoding="gbk" ?> \n<Composition Type="Recog_OK"> \n   <Page Type="Text">\n'
#xml头部
bottom = '   </Page>\n</Composition>'
#xml尾部
pHead = '&lt;paragraphBegin&gt;'
pHeadRe = '{p2}'
pEnd = '&lt;/paragraphEnd&gt;'
pEndRe= '{/p2}'
textHead = '&lt;textBegin&gt;'
textHeadRe = ''
textEnd = '&lt;/textEnd&gt;'
textEndRe = ''
titleHead = '&lt;texttitleBegin&gt;'
titleHeadRe = '{p12}'
titleEnd = '&lt;/texttitleEnd&gt;'
titleEndRe = '{/p12}'




def search_line(line):
    try:
       outline = line.replace("<txt  text= \"", "").replace("\" />", '').replace(pHead, pHeadRe).replace(pEnd, pEndRe) \
              .replace(textHead, textHeadRe).replace(textEnd, textEndRe).replace(titleHead, titleHeadRe).replace(titleEnd, titleEndRe)
       outline = "        " + "<Line Text=\"" + outline.strip() + "\" />"
    except:
        print line
    return outline


point = []

m = open(map_dir, 'w')

for root, dirs, files in os.walk(src_dir, True):
   for dir in dirs:
       dir_num += 1
       dir_file.write(str(dir) + "\t" + str(dir_num) + "\n")
       print dir
       var = 1   #文件命名
       boo = 0
       range = open(os.path.join(des_dir, str(dir_num) + "_" + str(var) + '.xml'), 'w')
       range.write(head)
       files = os.listdir(os.path.join(root, dir))
       files.sort()
       for file in files:
           print file
           file_flag = 0
           if file.endswith(".xml"):      #以xml结尾的文件
               namepath = open(os.path.join(root, dir, file), 'r')
               not_txt_flag = False
               for line in namepath.readlines():
                      if '<txt' in line.strip():
                         not_txt_flag = True
                         outline = search_line(line)
                         range.write(outline.encode('gbk') + "\n")
                        #替换字符
                      if re.search('textBegin', line):
                         boo = 1
                      if boo == 1 and file_flag == 0:
                          m.write(str(dir_num) + "_" + file.replace('xml', 'jpg') + '\t')
                          if os.path.exists(os.path.join(root, dir, file.replace('xml', 'jpg'))):
                             shutil.copyfile(os.path.join(root, dir, file.replace("xml", 'jpg')), os.path.join(pic_dir, str(dir_num) + "_" + file.replace('xml', 'jpg')))
                          else:
                             shutil.copyfile(os.path.join(root, dir, file.replace('xml', 'png')), os.path.join(pic_dir, str(dir_num) + "_" + file.replace('xml', 'jpg')))
                          file_flag = 1
                      if re.search('textEnd', line):
                         range.write("        " + "<Line Text=\"#{/p2}\" />")
                         range.write(bottom + '\n')
                         range.close()
                         m.write(str(dir_num) + "_" + str(var)+'.xml'+'\n')
                         var += 1
                         range = open(os.path.join(des_dir, str(dir_num) + "_" + str(var) + '.xml'), 'w')
                         print os.path.join(des_dir, str(dir_num) + "_" + str(var) + '.xml')
                         range.write(head)
                         file_flag = 0
                         boo = 0
               if not_txt_flag == False:
                  point.append(os.path.join(root, dir, file).replace('xml', 'jpg'))
       range.close()
       os.remove(os.path.join(des_dir, str(dir_num) + "_" + str(var) + '.xml')) 
m.close()

dir_file.close()
