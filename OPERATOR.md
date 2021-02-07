# OPERATOR

## 소개
* 세실리아의 음성 통합 서브시스템 중 화자인식의 운영자 메뉴얼입니다

## 사전작업
* Ubuntu 18.04 에서 작동합니다.
* Python 3.6 에서 작동합니다.
* NVIDIA CUDA 10.1를 지원하는 GPU와 그래픽 드라이버를 필요로 합니다.
* CUDA 10.1과 cuDNN 7 에서 작동합니다.
* 학습을 하기 위한 audio가 필요합니다. (16kHz, 16bit pcm .wav file)
* kaldi toolkit이 필요합니다.

## 설치
* (선택)virtualenv를 이용하여 python 가상환경을 만듭니다.
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```
* 필요한 패키지를 설치합니다.
```
$ pip install -r requirements.txt
```
* Data folder를 구성합니다.
```
Data
 ㄴtrain (학습 데이터)
  ㄴkang (화자1)
   ㄴkang1.wav
   ㄴkang2.wav
   ㄴ…
  ㄴkim (화자2)
   ㄴkim1.wav
   ㄴkim2.wav
   ㄴ…
  ㄴ…
 ㄴtest_offline (offline test data)
  ㄴkang
   ㄴkang1.wav
   ㄴkang2.wav
   ㄴ…
  ㄴkim
   ㄴkim1.wav
   ㄴkim2.wav
   ㄴ…
  ㄴ…
 ㄴtest (실제 환경에서 인식 대상)
  ㄴ test.wav(위치, 이름 고정. 실제 인식할 대상)
```
* Speaker_Recog_final/{online,extractor}/path.sh 수정
```
TF_ENV : 가상환경 들어있는 폴더
PROJECT_ROOT: 각 폴더의 절대경로
KALDI_ROOT: 칼디 프레임워크 설치된 경로
DATA_ROOT: 데이터가 저장된 경로
```

## 사용법
* speaker_recog_final.py의 DATA_DIR 학습 데이터 폴더로 변경
* Speaker_Recog_final/online으로 이동
```
$ cd Speaker_Recog_final/online
```
* configure 실행 (최초 한번만)
```
$ ./configure
```
* 화자 등록
```
$ ./run_train.sh 
```
* extractor 실행  (무한 루프 돔)
```
$ ./run_extractor.sh 
```
* test 실행( file 하나)
```
$ ./run_test.sh
$ cat result.txt
```
* offline test
```
$ cd ProjectRoot
$ python3 run_spk_recog_offline.py
```

## 문제해결
* 문제가 발생시 프로그램을 종료하고 다시 실행합니다.
