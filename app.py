# flask 웹 서버를 만들기 위해서 필수
from flask import Flask, request
from flask import send_file
from flask import render_template
from flask import jsonify
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"

from common import db
from model import model


# 앱 생성
app = Flask(__name__)

# 요청 과 요청을 받으면 처리할 함수를 생성
# 포트번호까지의 요청이 오면 templates 디렉토리의 index.html을 출력
@app.route('/')
def index():
    return render_template('index.html')

# 조회
@app.route('/list')
def list_page():
    dao = db.Dao()
    result, data = dao.select_all()
    # 출력의 형태 : json
    response = {'result': result, 'data': data}
    return jsonify(response)

# 파일 다운로드
@app.route('/listimagedownload/<pictureurl>')
def listimagedownload(pictureurl):
    file_name = 'static/img/' + pictureurl
    print(file_name)
    # file_name : 실제 파일의 경로(server쪽)
    # mimetypes : 파일의 종류
    # attachment_filename : 다운로드 되었을 때의 파일 이름(client쪽)
    return send_file(file_name, mimetype='application/octect-stream',
                     attachment_filename=pictureurl,
                     as_attachment =True)

# 상세페이지
@app.route('/detail/<serial_id>')
def detail(serial_id):
    dao = db.Dao()
    result, data = dao.select_one(serial_id)
    # 출력의 형태 : json
    response = {'result': result, 'data': data}
    return jsonify(response)



# 파일 다운로드
@app.route('/detailimagedownload/<pictureurl>')
def detailimagedownload(pictureurl):
    file_name = 'static/img/' + pictureurl
    print("상세파일 이미지 다운로드")
    # file_name : 실제 파일의 경로(server쪽)
    # mimetypes : 파일의 종류
    # attachment_filename : 다운로드 되었을 때의 파일 이름(client쪽)
    return send_file(file_name, mimetype='application/octect-stream',
                     attachment_filename=pictureurl,
                     as_attachment=True)


#계량기 정보 입력
def insert_meter(self,meter):
    # 결과를 저장할 변수
    result = False
    self.connect()

    data = self.cursor.execute('select serial_cd from electricity_meter_tb where serial_cd = %s',
                               (meter['serial_cd']))
    print('data::',type(data),' ',data)

    if data == 0:

        # data = self.cursor.fetchone()
        # itemid = 1
        # # 데이터가 존재하는 경우는 가장 큰 itemid+1
        # if data[0] != None:
        #     itemid = int(data[0]) + 1
        try:

            self.cursor.execute('insert into electricity_meter_tb '+
                                '(serial_cd, supply_type, typename,'+
                                ' electricity_filename, region_cd) '+
                                'values(%s,%s,%s,%s,%s)',
                                (meter['serial_cd'], meter['supply_type'], meter['typename'],
                                 meter['electricity_filename'],meter['region_cd']))
            #성공여부 확인 rowcount는 영향받은 행의 개수
            if self.cursor.rowcount >= 1:
                result = True

        except Exception as e:
            print(e)
            result = False


    self.con.commit()
    self.close()

    return result

# 바코드 등록
@app.route('/insertbarcode', methods=['GET', 'POST'])
def insertbarcode():
    if request.method == 'POST':
        print(request.form)
        # 받은 데이터
        barcode = {}
        barcode['modem_cd'] = request.form['modemId']
        barcode['serial_cd'] = request.form['serialId']
        # TODO:실제 파일이 저장되도록 해야함. 현재 임시 데이터 입력
        barcode['modem_filename'] = request.form['modemFilename']
        barcode['updatedate'] = request.form['updatedate']

        print("insertbarcode::", barcode)

        dao = db.Dao()
        result = dao.insert_barcode(barcode)
        # result = True
        # 출력의 형태 : json
        response = {'result': result}
        return jsonify(response)

# 전력량 계량기 등록
@app.route('/insertElectricityMeter', methods=['GET', 'POST'])
def insertElectricityMeter():
    response = {'result': False}
    print(request.form)
    if request.method == 'POST':
        f = request.files['pictureurl']
        f.save('./static/img/' + f.filename)


        # 받은 데이터
        meter = {}
        meter['updatedate'] = request.form['updatedate']

        meter['serial_cd'] = '0000000'
        meter['supply_type'] = '교류단상2선식'
        meter['typename'] = 'g-type'
        meter['electricity_filename'] = f.filename
        meter['region_cd'] = '01'
        print("insertElectricityMeter] 계량기정보 저장::", meter)

        #roi 결과 이미지 목록을 DB에 저장하기
        md = model()
        roi_images = md.get_roi_images('./static/img', f.filename)
        print('insertElectricityMeter::sava_files:', roi_images)



        # 이미지 가져오기
        # TODO:ocr인식


        dao = db.Dao()

        #전력계량기 정보 저장
        result = dao.insert_meter(meter)
        #roi 이미지 목록 insert 결과
        roi_result = False
        if result == True:
            #roi 결과 이미지 목록을 DB에 저장하기
            for img_name in roi_images:
                img_info = {}
                img_info['serial_cd'] = '0000000' #인식후 변경
                img_info['pre_filename'] = img_name
                roi_result = dao.insert_roi_image(img_info)

                if roi_result == False:
                    print("이미지 목록 저장 실패!! 실패한 이미지:",img_info)
                    result = False
                    break;





    # 출력의 형태 : json
    response = {'result': result}
    return jsonify(response)

# 자신의 IP로 접속할 수 있도록 서버를 구동
# 회사 내에서만 접속가능하게 하고 싶다면 host를 변경
app.run(host='0.0.0.0', debug=True)