import glob
import re
from collections import defaultdict
from os import rename
from os import mkdir
from os.path import isdir
from os.path import basename
import shutil


def imgtypes():
    types = ('*.jpg', '*.jpeg', "*.png", '*.gif')
    return types

def vidtypes():
    types = ('*.avi', '*.wmv', "*.mkv", '*.flv', '*.mpg', '*.mpeg', '*.mp4')
    return types

def getfiles(path='f:\\', type='all'):
    files_grabbed = []
    try:
        if type == 'all':
            files_grabbed = glob.glob(path+'*')
        elif type == 'img':
            for files in imgtypes():
                files_grabbed.extend(glob.glob(path+files))
        elif type == 'vid':
            for files in vidtypes():
                files_grabbed.extend(glob.glob(path + files))
    except TypeError as e:
        print(e)
    return files_grabbed

def filematcher(imgs, vids):
    matches = defaultdict(list)
    vidnamechecker = re.compile(r'(?P<mk>[a-zA-Z]{3,6})(-|)(?P<no>[0-9]{2,5})')
    for vidfile in vids:
        matcher = vidnamechecker.search(vidfile)
        if bool(matcher):
            prodno = (str(matcher.group('mk'))+'-'+str(matcher.group('no'))).upper()
            compr = re.compile(prodno)
            for imgfile in imgs:
                submatcher = compr.search(imgfile.upper())
                if bool(submatcher):
                    matches[prodno].append([imgfile, vidfile])
    return matches

def movefiles(matcheddict):
    for prodno in matcheddict:
        folderpath = 'f:\\'+prodno
        mkdir(folderpath)
        #print('mkdir : '+folderpath)
        for filelist in matcheddict[prodno]:
            for filename in filelist:
                file = basename(filename)
                shutil.move(filename, folderpath+'\\'+file)
                #print(filename+' || '+folderpath+'\\'+file)

def insertimgintofolder(imgs):
    #matcher = re.compile(r'(?P<mk>[a-zA-Z]{3,6})(-|)(?P<no>[0-9]{2,5})')
    for item in getfiles():
        try:
            matcher = re.search(r'(?P<mk>[a-zA-Z]{3,6})(-|)(?P<no>[0-9]{2,5})', item)
            if all([isdir(item), bool(matcher)]):
                vfoldername = str(matcher.group('mk'))+'-'+str(matcher.group('no')).upper() #not real
                m2 = re.compile(vfoldername)
                for imgfile in imgs:
                    if bool(m2.search(imgfile.upper())):
                        shutil.move(imgfile, item+'\\'+basename(imgfile))
                        #print(imgfile, item+'\\'+basename(imgfile))
        except FileNotFoundError as e:
            print(e)






# using img file init below
'''
plchecker = re.compile(r'(?P<path>f:\\)([\d]{2,4}|)(?P<mk>[a-zA-Z]{2,5})([-]|)(?P<no>[\d]{2,4})(pl|)(?P<exp>[\.]jpg)')
imgs = list()
for filename in getfiles(type='img'):
    matcher = plchecker.search(filename)
    if bool(matcher):
        newname = str(matcher.group('path'))+str(matcher.group('mk'))+'-'+str(matcher.group('no'))+str(matcher.group('exp'))
        rename(filename, newname)
        imgs.append(newname)
    else:
        imgs.append(filename)
        '''
imgs = getfiles(type='img')
vids = getfiles(type='vid')

matchfile = filematcher(imgs, vids)
movefiles(matchfile)
insertimgintofolder(imgs)

