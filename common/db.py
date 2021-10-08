import pymysql
import sqlite3
from flask import g

class Dao:

    def __init__(self):
        # 조회화면 : 전력량계량기, 모뎀바코드 정보 조회
        self.__SELECT_ALL = '''
        select electricity_meter_tb.serial_cd as serial_cd,
        modem_tb.modem_cd as modem_cd ,
        electricity_meter_tb.electricity_filename as electricity_filename, 
        date_format(electricity_meter_tb.electricity_save_date, '%Y-%m-%d %H:%i:%s') as electricity_save_date 
        from electricity_meter_tb 
        left join modem_tb 
        on modem_tb.serial_cd = electricity_meter_tb.serial_cd 
        where electricity_meter_tb.del_flag = 0
        ORDER BY electricity_save_date DESC;
        '''
        # 상세화면 : 전력량계량기, 모뎀 정보 조회
        self.__SELECT_ONE = '''
        select  
        electricity_meter_tb.serial_cd as serial_cd,  
        electricity_meter_tb.supply_type as supply_type, 
        electricity_meter_tb.typename as typename, 
        electricity_meter_tb.electricity_filename as electricity_filename, 
        date_format(electricity_meter_tb.electricity_save_date, '%%Y-%%m-%%d %%H:%%i:%%s') as electricity_save_date,  
        modem_tb.modem_cd as modem_cd, 
        modem_tb.modem_filename as modem_filename,
        date_format(modem_tb.modem_save_date, '%%Y-%%m-%%d %%H:%%i:%%s') as modem_save_date  
        from electricity_meter_tb 
        left join modem_tb 
        on modem_tb.serial_cd = electricity_meter_tb.serial_cd  
        where electricity_meter_tb.del_flag = 0 
        and electricity_meter_tb.serial_cd =  %s 
        '''
        
        # 상세화면 : 이미지 전처리 파일 조회
        self.__SELECT_PRE_IMAGE = '''
        select 
        electricity_preprocessing_tb.pre_filename as pre_filename
        from electricity_meter_tb 
        join electricity_preprocessing_tb 
        on electricity_preprocessing_tb.serial_cd = electricity_meter_tb.serial_cd
        where electricity_meter_tb.del_flag = 0
        and electricity_meter_tb.serial_cd = %s
        '''

        self.__SELECT_BY_SERIAL_CD = '''
        select serial_cd 
        from electricity_meter_tb 
        where serial_cd = %s
        '''

    #  데이터베이스 연결 메소드
    def connect(self):
        try :
            # 연결
            self.con = pymysql.connect(host='localhost',
                                       port=3306,
                                       user='flaskServer',
                                       passwd='20210420',
                                       db='electricitydb',
                                       charset='utf8')
            # 데이터베이스 사용 객체 생성
            self.cursor = self.con.cursor()
        except Exception as err:
            print('DBConnection Error : ', err)
            return False
        return True

    # 데이터베이스 연결 해제 메소드
    def close(self):
        self.con.close()

    # 전체 데이터 가져오기
    def select_all(self):
        # 데이터베이스 연결
        result = True
        li = []
        connect_result = self.connect()
        if not connect_result:
            return connect_result, li
        try:

            # sql 문 실행
            self.cursor.execute(self.__SELECT_ALL)
            data = self.cursor.fetchall()
            # 데이터를 저장할 list
            for temp in data:
                item = {}
                item['serial_cd'] = temp[0]
                item['modem_cd'] = temp[1]
                item['electricity_filename'] = temp[2]
                item['electricity_save_date'] = temp[3]
                li.append(item)


        except self.cursor.Error as err:
            # insert 실패시 False 반환
            result = False
            print('MySQL Error <select_all> : ', err)
        self.close()
        return result, li

    # dict형태로 데이터를 받아서 삽입하는 메소드
    def select_one(self, serial_cd):
        print("server 들어옴")
        result = True
        item = {}
        li = []
        connect_result = self.connect()
        if not connect_result:
            return connect_result, li
        try:

            self.cursor.execute(self.__SELECT_ONE, serial_cd)
            data = self.cursor.fetchone()
            print("상세데이터 출력 : ", data)
            item['serial_cd'] = data[0]
            item['supply_type'] = data[1]
            item['typename'] = data[2]
            item['electricity_filename'] = data[3]
            item['electricity_save_date'] = data[4]
            item['modem_cd'] = data[5]
            item['modem_filename'] = data[6]
            item['modem_save_date'] = data[7]

            self.cursor.execute(self.__SELECT_PRE_IMAGE, serial_cd)
            imageList = self.cursor.fetchall()

            images = []
            for temp in imageList:
                images.append(temp[0])
            item['pre_filenames'] = images
            li.append(item)
        except self.cursor.Error as err:
            # insert 실패시 False 반환
            result = False
            print('MySQL Error <select_one> : ', err)
        self.close()
        return result, item
    
    #전력계량기 정보 저장
    def insert_meter(self, meter):
        # 결과를 저장할 변수
        result = False
        self.connect()

        data = self.cursor.execute('select serial_cd from electricity_meter_tb where serial_cd = %s',
                                   (meter['serial_cd']))
        print('data::', type(data), ' ', data)

        if data == 0:

            # data = self.cursor.fetchone()
            # itemid = 1
            # # 데이터가 존재하는 경우는 가장 큰 itemid+1
            # if data[0] != None:
            #     itemid = int(data[0]) + 1
            try:

                self.cursor.execute('insert into electricity_meter_tb ' +
                                    '(serial_cd, supply_type, typename,' +
                                    ' electricity_filename, region_cd) ' +
                                    'values(%s,%s,%s,%s,%s)',
                                    (meter['serial_cd'], meter['supply_type'], meter['typename'],
                                     meter['electricity_filename'], meter['region_cd']))
                # 성공여부 확인 rowcount는 영향받은 행의 개수
                if self.cursor.rowcount >= 1:
                    result = True

            except Exception as e:
                print(e)
                result = False

        self.con.commit()
        self.close()

        return result

        # 바코드 정보 입력

    def insert_barcode(self, barcode):
        # 결과를 저장할 변수
        result = False
        self.connect()

        data = self.cursor.execute('select serial_cd from electricity_meter_tb where serial_cd = %s',
                                   (barcode['serial_cd']))
        print('data::', type(data), ' ', data)

        # self.cursor.execute('select max(itemid) from item')
        # data = self.cursor.fetchone()
        # itemid = 1
        # # 데이터가 존재하는 경우는 가장 큰 itemid+1
        # if data[0] != None:
        #     itemid = int(data[0]) + 1
        print("DAO::", barcode)
        if data == 1:
            try:

                self.cursor.execute('insert into modem_tb ' +
                                    '(modem_cd, serial_cd, modem_filename) ' +
                                    'values(%s,%s,%s)',
                                    (barcode['modem_cd'], barcode['serial_cd'], barcode['modem_filename']))
                # 성공여부 확인 rowcount는 영향받은 행의 개수
                if self.cursor.rowcount >= 1:
                    result = True

            except Exception as e:
                print(e)
                result = False

        self.con.commit()
        self.close()

        return result


    def insert_roi_image(self,roi):
        # 결과를 저장할 변수
        result = False
        self.connect()
        print("dao:",roi)
        try:

            self.cursor.execute('insert into electricity_preprocessing_tb ' +
                                '(serial_cd, pre_filename) ' +
                                'values(%s,%s)',
                                (roi['serial_cd'], roi['pre_filename']))

            # 성공여부 확인 rowcount는 영향받은 행의 개수
            if self.cursor.rowcount >= 1:
                result = True

        except Exception as e:
            print(e)
            result = False

        self.con.commit()
        self.close()

        return result