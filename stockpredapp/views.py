# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Code_name
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import math
import numpy as np
import FinanceDataReader as fdr
import matplotlib.pyplot as plt, mpld3
import time
import pandas as pd
import pandas_datareader as pdr # 주식데이터 크롤링

epochs = 10


def s_index(request):
    """
    종목 출력
    """
    page = request.GET.get('page', '1')

    stock_list = Code_name.objects.order_by('created_date')

    # 페이징 처리
    paginator = Paginator(stock_list, 10)

    page_obj = paginator.get_page(page)

    context = {'stock_list': page_obj}  # {'key' : value}
    return render(request, 'stockpredapp/stock_list.html', context)

# def result(request, stock_id):
#     '''
#     분석결과 출력
#     '''
#     #stock = Code_name.objects.get(id=stock_id)
#     stock = get_object_or_404(Code_name, pk=stock_id)
#     context = {'stock': stock}
#     return render(request, 'stockpredapp/stock_result.html', context)


def result(request, stock_id):
    '''
    분석결과 출력
    '''

    stock = Code_name.objects.get(id=stock_id)
    name = Code_name.objects.get(id=stock_id).stock_code
    # result = rnn(stock.stock_code+'KQ', start='2021-07-01', end='2022-01-01')
    Result = rnn(name, start='2021-01-01', end='2022-02-03')
    result = Result[0]
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

    context = {'stock':stock,
               'result': result,
               'result_d1': result_d1,
               'result_d2': result_d2,
               'result_d3': result_d3,
               'result_d4': result_d4,
               'result_d5': result_d5,
               'result_d6': result_d6,
               'result_d7': result_d7,
               'result_max':result_max,
               'result_min':result_min,
               'train_RMSE':train_RMSE,
               'test_RMSE':test_RMSE,
               'runtime':runtime,
               'dataset':dataset,
               'trainPredictPlot':trainPredictPlot,
               'testPredictPlot':testPredictPlot,
               'predPlot': predPlot

               }

    return render(request, 'stockpredapp/stock_result.html', context)


def rnn(code, start, end):  # 순환신경망(RNN)분석 함수
    s = time.time()
    # df = pdr.get_data_yahoo(code, start=start, end=end).reset_index()  # 주식 데이터 크롤링
    df = fdr.DataReader(symbol=code, start=start, end=end)
    dataset = df['Close'].values  # 종가 데이터 추출
    dataset = dataset.reshape(dataset.shape[0], 1)  # 1차원배열을 2차원으로 변경
    dataset = dataset.astype('float32')  # int -> float변환
    scaler = MinMaxScaler(feature_range=(0, 0.9))  # 최대값을 0.9로 설정
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

    trainPredictPlot = np.zeros(len(dataset) + 7)
    trainPredictPlot = trainPredictPlot.reshape(trainPredictPlot.shape[0], 1)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(TrainPredict) + look_back] = TrainPredict
    trainPredictPlot = trainPredictPlot.reshape(len(trainPredictPlot))
    trainPredictPlot = np.round(trainPredictPlot, 2)
    trainPredictPlot = list(trainPredictPlot)



    testPredictPlot = np.zeros(len(dataset) + 7)
    testPredictPlot = testPredictPlot.reshape(testPredictPlot.shape[0], 1)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(TrainPredict) + (look_back) * 2: len(dataset), :] = TestPredict

    testPredictPlot = testPredictPlot.reshape(len(testPredictPlot))
    testPredictPlot = list(testPredictPlot)



    predPlot = np.zeros(len(dataset) + 7)
    predPlot = predPlot.reshape(predPlot.shape[0], 1)
    predPlot[:, :] = np.nan
    predPlot[-7:] = x_pred[6].reshape(x_pred.shape[0], 1)
    predPlot = scaler.inverse_transform(predPlot)  # Min-Max변환된 값을 원래대로 되돌림

    dataset = dataset.reshape(len(dataset))
    dataset = list(dataset)

    # plt.figure(figsize=(20, 10))
    # plt.plot(dataset, label="true", c='green')
    # plt.plot(trainPredictPlot, label='train_predict')
    # plt.plot(testPredictPlot, label='test_predict')
    # plt.plot(predPlot, label='pred')
    # plt.legend()

    # plt.show()

    result = np.round(predPlot[-7:].reshape(look_back), 2)
    result_d1 = result[0]
    result_d2 = result[1]
    result_d3 = result[2]
    result_d4 = result[3]
    result_d5 = result[4]
    result_d6 = result[5]
    result_d7 = result[6]
    result_max = result.max()
    result_min = result.min()
    e = time.time()
    runtime = e - s
    runtime = round(runtime)
    return result, result_d1, result_d2, result_d3, result_d4, result_d5, result_d6, result_d7, result_max, result_min, train_RMSE, test_RMSE, runtime, dataset, trainPredictPlot, testPredictPlot, predPlot


