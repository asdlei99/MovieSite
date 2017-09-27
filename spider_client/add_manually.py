# coding=utf-8

from ms_main import Main

if __name__ == '__main__':
    while True:
        try:
            Main().add()
        except KeyboardInterrupt:
            print 'Bye'
            break
