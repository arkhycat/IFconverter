#!/usr/bin/python
import zipfile
from lxml import etree
import sys
from BeautifulSoup import BeautifulSoup
import textwrap
import curses
import math
import urllib2
import locale
locale.setlocale(locale.LC_ALL,"")

#http://bugs.python.org/issue1859
def wrap_paragraphs(text, width=70, **kwargs):
    return [line for para in text.splitlines() for line in textwrap.wrap(para, width, **kwargs) or ['']]

def cleanup_and_quit(screen):
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    exit()


def main(screen):
    screen.keypad(1)
    book = sys.argv[1]
    width = min(int(math.floor(curses.COLS * .8)), 80)
    for chapter in get_epub_files(book):
        if "htm" not in chapter:
            continue
        contents = read_chapter(book, chapter)
        contents = ' '.join(BeautifulSoup(contents).findAll("body",text=True))
        contents = wrap_paragraphs(contents.encode("utf-8"), width=width)
        y = 0
        for line in contents:
            if(line.isupper()):
                screen.addstr(y, 0, line + "\n", curses.A_BOLD)
            else:
                screen.addstr(y, 0, line + "\n")
            y = y + 1
            screen.refresh()
            if(y > curses.LINES - 2):
                #Wait for user input
                c = screen.getch()
                screen.clear()
                y = 0
                if c == ord('c'):
                    break #Next chapter
                elif c == ord('q'):
                    cleanup_and_quit(screen)
                elif c == curses.KEY_DOWN:
                    pass
                elif c == curses.KEY_UP:
                    continue

        #If the chapter didn't end cleanly at the end of the page, hold until the reader is ready to move on
        if(y != 0):
            screen.hline(y, 0, '-', width)
            c = screen.getch()
            if c == ord('q'):
                cleanup_and_quit(screen)

        #Clean the screen for each new chapter
        screen.clear()

def read_chapter(fname, filename):
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read("OEBPS/" + urllib2.unquote(filename))
    return txt

def get_epub_files(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:manifest',namespaces=ns)[0]

    # repackage the data
    res = p.xpath('pkg:item/@href', namespaces=ns)

    return res


def get_epub_info(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

    # repackage the data
    res = {}
    for s in ['title','language','creator','date','identifier']:
        res[s] = p.xpath('dc:%s/text()'%(s),namespaces=ns)[0]

    return res

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        exit()
    curses.wrapper(main)

