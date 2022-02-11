# Create your views here.

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Code_name
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from django.db.models import Q
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import math
import numpy as np
import FinanceDataReader as fdr
import time
import random


epochs = 100  # 학습반복수


def s_index(request):
    """
    종목 출력
    """
    page1 = request.GET.get('page1', '1')
    kw1 = request.GET.get('kw1', '')  # 검색어

    stock_list = Code_name.objects.order_by('created_date')
    if kw1:
        stock_list = stock_list.filter(
            Q(stock_name__icontains=kw1) | # 종목이름검색
            Q(stock_code__icontains=kw1) |# 종목코드검색
            Q(market__icontains=kw1) # 상장구분 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(stock_list, 10)

    page_obj = paginator.get_page(page1)

    context = {'stock_list': page_obj, 'page1': page1, 'kw1': kw1}  # {'key' : value}
    return render(request, 'stockpredapp/stock_list.html', context)

# def result(request, stock_id):
#     '''
#     분석결과 출력
#     '''
#     #stock = Code_name.objects.get(id=stock_id)
#     stock = get_object_or_404(Code_name, pk=stock_id)
#     context = {'stock': stock}
#     return render(request, 'stockpredapp/stock_result.html', context)

# def loading(request, stock_id):
#     context = {'stock_id':stock_id}
#     return render(request, 'stockpredapp/loading.html', context)


def random_pred(request):
    random_stock = random.randrange(1,15782)
    stock = Code_name.objects.get(id=random_stock)
    context = {'random_stock':random_stock,
               'stock':stock}
    return render(request, 'stockpredapp/random_pred.html', context)


def main_loading(request):
    return render(request, 'stockpredapp/main_loading.html')


def main_loading2(request):
    return render(request, 'stockpredapp/main_loading2.html')


def jisu(request):
    end = datetime.today() # 오늘 날짜
    start = end - relativedelta(months=1)
    start = start.strftime("%Y-%m-%d") # 문자열 변환
    end = end.strftime("%Y-%m-%d") # 문자열 변환

    kospi = fdr.DataReader(symbol='KS11', start=start, end=end).reset_index()  # 코스피 1년 데이터 클롤링
    kospi = kospi.loc[:, 'Close'] # 종가 데이터 추출
    kospi = list(kospi) # 리스트 변환

    kosdaq = fdr.DataReader(symbol='KQ11', start=start, end=end).reset_index()  # 코스닥 1년 데이터 크롤링
    date = kosdaq.loc[:, 'Date']  # 날짜 데이터 추출
    date = list(date)
    for i in range(len(date)):  # datetime -> str 변환
        date[i] = date[i].strftime("%Y-%m-%d")
    kosdaq = kosdaq.loc[:, 'Close']  # 종가 데이터 추출
    kosdaq = list(kosdaq)  # 리스트 변환

    dows = fdr.DataReader(symbol='DJI', start=start, end=end).reset_index()  # 다우지수
    dows = dows.loc[:, 'Close'] # 종가 데이터 추출
    dows = list(dows)  # 리스트 변환

    nasdaq = fdr.DataReader(symbol='IXIC', start=start, end=end).reset_index()  # 나스닥지수
    nasdaq = nasdaq.loc[:, 'Close']  # 종가 데이터 추출
    nasdaq = list(nasdaq)  # 리스트 변환

    # sp500 = fdr.DataReader(symbol='US500', start=start, end=end).reset_index()  # S&P 500
    # sp500 = sp500.loc[:, 'Close']  # 종가 데이터 추출
    # sp500 = list(sp500)  # 리스트 변환

    context = {'kospi':kospi,
               'kosdaq':kosdaq,
               'date':date,
               'start':start,
               'end':end,
               'dows':dows,
               'nasdaq':nasdaq,
               # 'sp500':sp500
               }
    return render(request, 'stockpredapp/jisu.html', context)


def loading(request, stock_id):
    stock = Code_name.objects.get(id=stock_id)
    name = Code_name.objects.get(id=stock_id).stock_name
    context = {'stock':stock,
               'stock_id':stock_id,
               'name':name}
    return render(request, 'stockpredapp/loading.html', context)


def result(request, stock_id):
    '''
    분석결과 출력
    '''

    stock = Code_name.objects.get(id=stock_id)
    name = Code_name.objects.get(id=stock_id).stock_code
    end = datetime.today()
    start = end - relativedelta(months=12)
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    try:
        Result = rnn(name, start=start, end=end)
        result = Result[0]  # rnn 함수결과를 변수에 할당
        result_d1 = Result[1]
        result_d2 = Result[2]
        result_d3 = Result[3]
        result_d4 = Result[4]
        result_d5 = Result[5]
        result_d6 = Result[6]
        result_d7 = Result[7]
        result_max = Result[8]
        result_min = Result[9]
        train_RMSE = Result[10]
        test_RMSE = Result[11]
        runtime = Result[12]
        dataset = Result[13]
        trainPredictPlot = Result[14]
        testPredictPlot = Result[15]
        predPlot = Result[16]
        date = Result[17]
        if result_min >= dataset[-1]: # 예측값의 최소값이 실제데이터의 가장 최근 날짜보다 크면 매수
            recommend = '매수'
        elif result_min < dataset[-1]: # 예측값의 최소값이 실제데이터의 가장 최근 날짜보다 작으면 매도
            recommend = '매도'

        context = {'stock': stock,  # 분석결과 페이지에 보낼 데이터 정리
                   'result': result,
                   'result_d1': result_d1,
                   'result_d2': result_d2,
                   'result_d3': result_d3,
                   'result_d4': result_d4,
                   'result_d5': result_d5,
                   'result_d6': result_d6,
                   'result_d7': result_d7,
                   'result_max': result_max,
                   'result_min': result_min,
                   'train_RMSE': train_RMSE,
                   'test_RMSE': test_RMSE,
                   'runtime': runtime,
                   'dataset': dataset,
                   'trainPredictPlot': trainPredictPlot,
                   'testPredictPlot': testPredictPlot,
                   'predPlot': predPlot,
                   'date': date,
                   'start': start,
                   'end': end,
                   'recommend' : recommend
                   }
        return render(request, 'stockpredapp/stock_result.html', context)
    except:
        context = {'stock':stock}
        return render(request, 'stockpredapp/error.html', context)

# def error(request):
#     return render(request, 'stockpredapp/error.html')


def rnn(code, start, end):  # 순환신경망(RNN)분석 함수
    s = time.time() # 분석 시작 시간
    df = fdr.DataReader(symbol=code, start=start, end=end).reset_index() # 데이터 크롤링
    date = df['Date'] # 날짜 데이터 추출
    date = list(date) # 리스트 변환
    for i in range(len(date)): # datetime -> str 변환
        date[i] = date[i].strftime("%Y-%m-%d")
    date.append('d+1')
    date.append('d+2')
    date.append('d+3')
    date.append('d+4')
    date.append('d+5')
    date.append('d+6')
    date.append('d+7')

    dataset = df['Close'].values  # 종가 데이터 추출
    dataset = dataset.reshape(dataset.shape[0], 1)  # 1차원배열을 2차원으로 변경
    dataset = dataset.astype('float32')  # int -> float변환
    scaler = MinMaxScaler(feature_range=(0, 1))  # 최대값을 1로 설정
    Dataset = scaler.fit_transform(dataset)
    train_data, test_data = train_test_split(Dataset, test_size=0.2, shuffle=False)  # 8:2로 tarin, test 분리

    def create_dataset(dataset, look_back):  # 종속변수와 독립변수를 생성하는 함수
        x_data = []  # 빈 리스트 생성
        y_data = []

        for i in range(len(dataset) - look_back):
            data = dataset[i: (i + look_back), 0]
            x_data.append(data)
            y_data.append(dataset[i + look_back, 0])
        return np.array(x_data), np.array(y_data)

    look_back = 7  # 7개의 데이터로 예측
    x_train, y_train = create_dataset(train_data, look_back)  # train_data 생성
    x_test, y_test = create_dataset(test_data, look_back)  # test 데이터 생성

    X_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))  # 3차원으로 변경
    X_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))  # 3차원으로 변경

    model = Sequential()  # model 옵션
    model.add(SimpleRNN(3, input_shape=(1, look_back)))
    model.add(Dense(1, activation="linear"))
    model.compile(loss='mse', optimizer='adam')

    model.fit(X_train, y_train, epochs=epochs, batch_size=1, verbose=1)  # train_data학습

    trainPredict = model.predict(X_train)  # train_data를 이용하여 예측
    testPredict = model.predict(X_test)  # test_data를 이용하여 예측

    TrainPredict = scaler.inverse_transform(trainPredict)  # Min-Max변환된 값을 원래대로 되돌림
    Y_train = scaler.inverse_transform([y_train])  # Min-Max변환된 값을 원래대로 되돌림
    TestPredict = scaler.inverse_transform(testPredict)  # Min-Max변환된 값을 원래대로 되돌림
    Y_test = scaler.inverse_transform([y_test])  # Min-Max변환된 값을 원래대로 되돌림

    train_RMSE = math.sqrt(mean_squared_error(Y_train[0], TrainPredict[:, 0]))  # train_RMSE
    train_RMSE = round(train_RMSE, 2)
    test_RMSE = math.sqrt(mean_squared_error(Y_test[0], TestPredict[:, 0]))  # test_RMSE
    test_RMSE = round(test_RMSE, 2)

    x_pred = np.zeros(look_back * look_back, dtype=float)  # 예측값을 저장할 array생성
    x_pred = x_pred.reshape(look_back, 1, look_back)  # 3차원으로 변환

    for i in range(look_back):
        if i == 0:
            x_pred[0][0][:-1] = Dataset[-6:].reshape(6)  # 최근 6일 데이터를 pred의 1번째 row, 1~6번째 인덱스에 저장
            x_pred[0][0][-1] = model.predict(
                Dataset[-7:].reshape(1, 1, look_back))  # 최근 7일 데이터를 이용한 예측값을 pred의 1번째 row, 7번째 인덱스에 저장
        elif i > 0:
            x_pred[i][0][:-1] = x_pred[i - 1][0][1:]  # pred의 이전 row의 2~7번째 데이터를 다음 row의 1~6번째 인덱스에 저장
            x_pred[i][0][-1] = model.predict(
                x_pred[[i - 1]])  # pred의 이전 row의 1~7번째 데이터를 이용하여 데이터 예측 후, 다음 row의 7번재 인덱스에 저장

    trainPredictPlot = np.zeros(len(dataset) + 7) # 시각화를 위한 array 생성
    trainPredictPlot = trainPredictPlot.reshape(trainPredictPlot.shape[0], 1) # 2차원으로 변환
    trainPredictPlot[:, :] = np.nan # 모든 값을 결측치로 변경
    trainPredictPlot[look_back:len(TrainPredict) + look_back] = TrainPredict # 예측값 대입
    trainPredictPlot = trainPredictPlot.reshape(len(trainPredictPlot)) # 1차원으로 변환
    trainPredictPlot = np.round(trainPredictPlot, 2) # 소수 둘째 자리만 표시
    trainPredictPlot = list(trainPredictPlot) # 리스트로 변환
    trainPredictPlot = json.dumps(trainPredictPlot) # json형태로 변환

    testPredictPlot = np.zeros(len(dataset) + 7)
    testPredictPlot = testPredictPlot.reshape(testPredictPlot.shape[0], 1)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(TrainPredict) + (look_back) * 2: len(dataset), :] = TestPredict
    testPredictPlot = testPredictPlot.reshape(len(testPredictPlot))
    testPredictPlot = np.round(testPredictPlot, 2)  # 소수 둘째 자리만 표시
    testPredictPlot = list(testPredictPlot)
    testPredictPlot = json.dumps(testPredictPlot)

    predPlot = np.zeros(len(dataset) + 7)
    predPlot = predPlot.reshape(predPlot.shape[0], 1)
    predPlot[:, :] = np.nan
    predPlot[-7:] = x_pred[6].reshape(x_pred.shape[0], 1)
    predPlot = scaler.inverse_transform(predPlot)  # Min-Max변환된 값을 원래대로 되돌림
    predPlot = predPlot.reshape(len(predPlot))
    predPlot = np.round(predPlot, 2)  # 소수 둘째 자리만 표시
    dataset = dataset.reshape(len(dataset)) # 주식 true값을 1차원으로 변경
    dataset = list(dataset) # 리스트 변환

    result = np.round(predPlot[-7:].reshape(look_back), 2) # 일주일 예측 결과값(반올림)
    predPlot = list(predPlot) # 예측값 리스트 변환
    predPlot = json.dumps(predPlot) # json형태로 변환
    result_d1 = result[0] # d+n일 후 예측값
    result_d2 = result[1]
    result_d3 = result[2]
    result_d4 = result[3]
    result_d5 = result[4]
    result_d6 = result[5]
    result_d7 = result[6]
    result_max = result.max() # 예측 최대값
    result_min = result.min() # 예측 최소값
    e = time.time() # 분석 종료시간
    runtime = e - s # 분석에 걸린 시간
    runtime = round(runtime)
    return result, result_d1, result_d2, result_d3, result_d4, result_d5, result_d6, result_d7, result_max, result_min, train_RMSE, test_RMSE, runtime, dataset, trainPredictPlot, testPredictPlot, predPlot, date


