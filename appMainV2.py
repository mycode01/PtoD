import glob
import os
from models import pornFile
import re
from pprint import pprint
import sqlite3
import shutil

def imgtypes():
    types = ('*.jpg', '*.jpeg', "*.png", '*.gif')
    return types


def vidtypes():
    types = ('*.avi', '*.wmv', "*.mkv", '*.flv', '*.mpg', '*.mpeg', '*.mp4')
    return types


def getfiles(path='f:\\', type='all'):
    files_grabbed = []
    metaType = imgtypes() if type == 'img' else vidtypes()
    try:
        for files in metaType:
            for fn in glob.glob(os.path.join(path, files)):
                matcher = search(fn)
                if bool(matcher):
                    files_grabbed.append(
                        pornFile(type, fn, (str(matcher.group('mk')) + '-' + str(matcher.group('no'))).upper()))
                else:
                    pass
        if type != 'img':
            for fn in next(os.walk('f:\\'))[1]:
                matcher = search(fn)
                if bool(matcher):
                    files_grabbed.append(
                        pornFile('folder', fn, (str(matcher.group('mk')) + '-' + str(matcher.group('no'))).upper()))
                else:
                    pass

    except TypeError as e:
        print(e)
    return files_grabbed

def search(fn):
    prdNameReg = re.compile(r'(?P<mk>[a-zA-Z]{2,6})(-|)(?P<no>[0-9]{2,5})')
    matcher = prdNameReg.search(fn)
    if len(fn) > 30:
        return None
    if bool(matcher):
        if len(fn) >= 23 :
            print(fn)
            if input('파일 길이가 김, 계속?(y / Anything): ') == 'y':
                print('%s 포함함' % fn, end='\n\n')
                return matcher
            else:
                return None
        return matcher
    else:
        return None

def dbInitailize():
    print('initailizing..')
    global conn
    conn = sqlite3.connect('porns.db')
    global c
    c = conn.cursor()
    try:
        c.execute(
            'select * from products'
        )
    except sqlite3.OperationalError as e:
        print('Create Table..')
        c.execute(
            '''CREATE TABLE products
            (seq Integer PRIMARY KEY AUTOINCREMENT, fileType varchar(4), rawName varchar(255), prodName varchar(255),
            CreateDT datetime)'''
        )


def fileMapper(porns):
    global c
    global conn
    for prod in porns:
        c.execute('''insert into products (fileType, rawName, prodName, CreateDT) values
        ("%s", "%s", "%s", datetime('now', 'localtime'))''' % (prod.fileType, prod.rawName, prod.prodName))
    #conn.commit()

    c.execute('''
    select * from products where prodname in (
        select prodname from products
          group by prodname
          having count(*) > 1
        )
        order by prodname
        ''')
    col = list(map(lambda x: x[0], c.description))
    #rows = [list(zip(col, x)) for x in c.fetchall()]
    rows = c.fetchall()

    folders = list(filter(lambda x: x[1] == 'folder', rows))
    videos = list(filter(lambda x: x[1] == 'vid', rows))
    images = list(filter(lambda x: x[1] == 'img', rows))
    try:
        for fd in folders:
            fo = pornFile(relation=list(filter(lambda x: x[3] == fd[3], images)),
                     fileType=fd[1], rawName=fd[2], prodName=fd[3])
            if len(fo.relation) < 1:
                continue
            for i in fo.relation:
                print("%s to %s"% (i[2], 'f:\\'+fo.rawName+ '\\' + fo.prodName+os.path.splitext(i[2])[1]), end='\n\n')
                shutil.move(i[2], 'f:\\'+fo.rawName+ '\\' + fo.prodName+os.path.splitext(i[2])[1])
        for vd in videos:
            vo = pornFile(relation=list(filter(lambda x: x[3] == vd[3], images)),
                          fileType=vd[1], rawName=vd[2], prodName=vd[3])
            if len(vo.relation) < 1:
                continue
            nd = 'f:\\' + vo.prodName
            print('%s to %s'%(vo.rawName, nd+'\\'+vo.prodName+os.path.splitext(vo.rawName)[1]))
            os.mkdir(nd)
            shutil.move(vo.rawName, nd+'\\'+vo.prodName+os.path.splitext(vo.rawName)[1])
            for i in vo.relation:
                print("%s to %s" % (i[2], nd + '\\' + vo.prodName+os.path.splitext(i[2])[1]), end='\n\n')
                shutil.move(i[2], nd + '\\' + vo.prodName+os.path.splitext(i[2])[1])
    except FileNotFoundError as e:
        print(e)
    #print(rows)

dbInitailize()
porns = getfiles(type='img')
porns.extend(getfiles(type='vid'))
fileMapper(porns)



