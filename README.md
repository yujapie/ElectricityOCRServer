# ⚡ 전력량계량기 OCR프로젝트

- **⚡ 전력량계량기 OCR프로젝트**
  - 📁Repository 구조
  - 📌프로젝트 개요
  - 🕑개발 기간
  - 🛠프로젝트 구조
  - ✅분석 환경 및 도구
- **⚙ Server 구현**
  - 전처리 및 OCR 모델
  - DB 구축
  - Server 구현(Flask)
- **[📱 Android 구현](https://github.com/yujapie/ElectricityMeterOCR) 👈Repository 이동**

- **✨ 애플리케이션 실행영상**



## 📁Repository 구조

```
ElectricityOCRServer
├── 📁common
|	└── 📃db.py				    	        # database 연결DTO
├── 📁model
|	├── 📃OCRModel.py					# 이미지 전처리 호출및 파일저장처리
|	└── 📃android_prep.py					# 이미지 전처리 및 OCR모델
├── 📁static
|	└──📁 img					        # 이미지 저장폴더
├── 📁templates
|	└── 📃index.html
└──📃app.py					                # Service연결 Controller
```



## 📌프로젝트 개요

### 1) 프로젝트 주제 및 선정 배경

[프로젝트 초기 계획서](https://magical-goldenrod-6ed.notion.site/65b0ddbbdc774add97819917c1eb5dd9)

전력량계량기에는 전력량을 한국전력공사에 전송하도록 해주는 통신 모뎀이 부착됨. 전력량 정보를 송수신 및 관리를 위해서 전력량계량기의 기기정보와 통신 모뎀의 바코드 정보를 데이터베이스에 저장 해야함.

**전력량계량기의 정보**와 **통신 모뎀에 부착된 바코드정보를** **일일이 기재하는데 시간이 걸리고 기재내용과 실제 정보에 차이가 발생**

![image](https://user-images.githubusercontent.com/58774664/136534302-29f47d5d-fff7-4101-af8b-ca3b8143c832.png)



### 2) 프로젝트 목적

OCR인식을 통해 손쉽게 읽어 들여 모뎀 설치의 기재시간을 줄이고, 기재 내용의 정확도를 높이고자 함



### 3) 프로젝트 목표

- 전체 이미지 중 8-segment ROI 탐지 : **80.9%** (638개 중 789개)
  - 이미지 당 ROI 2개 탐지한 경우 : 5개
  - 실제 ROI좌표가 반드시 포함되어 있음
  - 두 개의 ROI 중 실제 ROI를 판별 가능함



- ROI를 탐지한 이미지 중 OCR 수행 : **92.6%** (591개 중 638개)
  - 계량기 식별에 가장 중요한 데이터인 “제조번호” 의 데이터 길이
     기준으로 평가함
  - 제조번호는 15개의 숫자와 3개의 하이픈(‘-‘)으로 이어져 있음
  - OCR로 읽어낸 제조번호와 실제 제조번호는 추후 비교할 예정임



- 문자 검출, 문자 인식에 대해 순차적으로 평가 :  **74.9%** (591개 / 789개)
  - 전체 789개 이미지 중 591개 이미지에 대해 OCR 수행하여 제조번호 15개를 읽어냄



## 🕑개발 기간

- 2021.8.31 ~ 10.6 (5주)

| **구분**          | **기간**        | **활동**                                                  | **비고**                   |
| ----------------- | --------------- | --------------------------------------------------------- | -------------------------- |
| **사전 기획**     | **▶** 8/31~9/6  | **▶** 기획서 작성                                         | **▶** OpenCV 학습          |
| **데이터 수집**   | **▶** 8/31~9/15 | **▶** 외부 데이터 수집                                    | **▶** 협약기업 데이터 제공 |
| **데이터 전처리** | **▶** 9/6~10/6  | **▶** OCR 모델 개선을 위한 이미지 전처리                  |                            |
| **모델링**        | **▶** 9/24~10/4 | **▶** OCR모델 인식                                        |                            |
| **서비스 구축**   | **▶** 9/24~10/6 | **▶** 모바일 서비스 시스템 설계  **▶** 모바일 플랫폼 구현 |                            |
| **총 개발기간**   | **▶** 8/31~10/6 |                                                           |                            |



## 🛠프로젝트 구조

![image](https://user-images.githubusercontent.com/58774664/136537726-bc984ae7-7562-4519-abc0-c8ef9ccaec4d.png)



## ✅분석 환경 및 도구

- HW/Server
  - Window (ver 10 / CPU i7 / RAM 16)
  - Flask
- Language
  - Python (ver 3.7)
  - MySQL(ver 8.0.26)
  - Java(ver 11)
  - json
- Tools
  - Github
  - Slack
  - Google Drive
  - eXERD
- IDE
  - PyCharm
  - Android Studio
  - DBeaver
  - Eclipse
- Library
  - OpenCV (ver 4.5)
  - TensorOCR (=Tesseract)
  - Numpy (ver 1.19)



# ⚙Server

## 1.전처리 및 OCR 모델

[이미지 처리과정](https://whimsical.com/ocr-Sw9iyj7nFJ9JicHAZP1dAT)





## 2.DataBase

- [DB 구축 SQL](https://github.com/2SEHI/OCR-Text-Detection/blob/main/db/CreateTableSQL.sql)

- [eXERD 파일](https://github.com/2SEHI/OCR-Text-Detection/blob/main/db/Electricitydb_MySQL.exerd)

- [DB 명세서](https://magical-goldenrod-6ed.notion.site/DB-96c709ac9e3e4577abfe26913d14922e)

![image](https://user-images.githubusercontent.com/58774664/136549647-fcb7a7e7-2fcf-42b3-ba1f-fa974d161d5a.png)

## 3.Controller

- [API 문서](https://magical-goldenrod-6ed.notion.site/API-5b7ebb411af64518a58d5e12d65899bd)



# [📱Android 구현](https://github.com/yujapie/ElectricityMeterOCR) 👈Repository 이동

## 1.Flow Chart

- [화면흐름도(Flow Chart)](https://whimsical.com/ocr-HQB6W3DWodaLZ3mFEXkQZg)

![image](https://user-images.githubusercontent.com/58774664/136650937-20e6d1e9-8a0d-4dce-9894-3ae28ffd1251.png)

## 2.모뎀 바코드 인식

-  Google Mobile Vision API 의 [Barcode scanning 라이브러리](https://developers.google.com/ml-kit/vision/barcode-scanning) 사용하여 모뎀의 바코드 정보를 읽어냄

- 정확도



# ✨애플리케이션 실행영상
https://user-images.githubusercontent.com/58774664/136656792-0b65ea74-449f-4061-b1e9-e3987fb32381.mp4
