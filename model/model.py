
from android_prep import prep

class model:
    def getresult(self,file_path,file_name):
        files = {'result':False,'filenames':[file_name.split('.')[0]]}
        print(file_path)
        print(files)

        pr = prep(file_path,file_name.split('.')[0])
        src_roi = pr.find_8seg()

        if len(src_roi[self.src_name]) != 0:
            files.update('result',True)
        else:
            print("ROI를 탐지하지 못했습니다.")

        print(files)

        return files;

    def getfilelist(self,file_name):
        pass
    # list = [file_name,file_name+_binary,file_name+]






if __name__ == '__main__':
    filename = '1234_222.jpg'
    md = model()
    md.getresult('./static/img/', '20211005_110445.jpg')