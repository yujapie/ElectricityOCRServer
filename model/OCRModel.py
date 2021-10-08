import os

from model.android_prep import prep


class OCRModel:
    #ROI 결과를 반환하는 함수
    def get_roi_images(self,file_path,file_name):
        sava_images = []

        pr = prep(file_path,file_name.split('.')[0])
        # 전처리 및 문자 인식
        result_roi, serial_id = pr.no_box()

        if result_roi == 1:
            sava_images = self.get_file_list(file_path, file_name)


        return result_roi, sava_images, serial_id

    #파일경로에 파일이름이 포함된 파일 목록을 만들어주는 메소드
    def get_file_list(self, file_path, file_name):

        #확장자 제거
        file_name = file_name.split('.')[0]
        #경로에 모든 파일 불러오기
        all_img = os.listdir(file_path)

        save_files = []
        for name in all_img:
            if name.find(file_name) > -1 and len(name.split('_'))==3:
                save_files.append(name)
        return save_files