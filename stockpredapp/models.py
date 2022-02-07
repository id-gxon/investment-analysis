from django.db import models

# Create your models here.


class Test(models.Model): # db 테스트용
    created_date = models.DateTimeField(null=True)
    stock_code = models.CharField(max_length=200)
    stock_name = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_name


class Code_name(models.Model): # 크롤링한 종목코드와 종목이름
    created_date = models.DateTimeField(null=True)
    stock_code = models.CharField(max_length=200, null=True)  # 종목코드
    stock_name = models.CharField(max_length=200, null=True)  # 종목이름
    market = models.CharField(max_length=200, null=True, default='')  # 코스닥, 코스피 구분
    sector = models.CharField(max_length=200, null=True, default='')  # 사업분야
    industry = models.CharField(max_length=200, null=True, default='')  # 세부분야
    listing_date = models.CharField(max_length=200, null=True, default='')  # 상장일
    settle_month = models.CharField(max_length=200, null=True, default='')  #
    representative = models.CharField(max_length=200, null=True, default='')  # 대표
    homepage = models.CharField(max_length=200, null=True, default='')  # 홈페이지
    region = models.CharField(max_length=200, null=True, default='')  # 지역

    def __str__(self):
        return self.stock_name


# from stockpredapp.models import Code_name
# from django.utils import timezone
# import FinanceDataReader as fdr
#
# df_krx = fdr.StockListing("KRX")
#
# for i in range(len(df_krx)): # stock_data 크롤링
#     s = Code_name(
#     created_date=timezone.now(),
#     stock_code=df_krx.iloc[i, 0],
#     market=df_krx.iloc[i, 1],
#     stock_name=df_krx.iloc[i, 2],
#     sector=df_krx.iloc[i, 3],
#     industry=df_krx.iloc[i, 4],
#     listing_date=df_krx.iloc[i, 5],
#     settle_month=df_krx.iloc[i, 6],
#     representative=df_krx.iloc[i, 7],
#     homepage=df_krx.iloc[i, 8],
#     region=df_krx.iloc[i, 9])
#     s.save()




class Rnn_data(models.Model): # 사용자로부터 받은 데이터
    created_date = models.DateTimeField(null=True)
    user_id = models.CharField(null=True, max_length=200) # 사용자 id
    stock_code = models.CharField(max_length=200) # 종목코드
    stock_name = models.CharField(max_length=200) # 종목이름

    start = models.DateField() # 조회시작일
    end = models.DateField() # 조회종료일


class Rnn_result(models.Model): # 순환신경망 분석결과 저장
    created_date = models.DateTimeField(null=True)
    user_id = models.CharField(null=True, max_length=200)  # 사용자 id
    stock_code = models.CharField(max_length=200) # 종목코드
    stock_name = models.CharField(max_length=200) # 종목이름

    start = models.DateField() # 조회시작일
    end = models.DateField() # 조회종료일

    result_max = models.DecimalField(max_digits=10, decimal_places=2) # 예측값을 최대값
    result_min = models.DecimalField(max_digits=10, decimal_places=2) # 예측값의 최소값

    d1 = models.DecimalField(max_digits=10, decimal_places=2) # n일 후 예측치
    d2 = models.DecimalField(max_digits=10, decimal_places=2)
    d3 = models.DecimalField(max_digits=10, decimal_places=2)
    d4 = models.DecimalField(max_digits=10, decimal_places=2)
    d5 = models.DecimalField(max_digits=10, decimal_places=2)
    d6 = models.DecimalField(max_digits=10, decimal_places=2)
    d7 = models.DecimalField(max_digits=10, decimal_places=2)

    train_RMSE = models.DecimalField(max_digits=10, decimal_places=2) # train_data의 RMSE
    test_RMSE = models.DecimalField(max_digits=10, decimal_places=2) # test_data의 RMSE

    def __str__(self): # 조회할때 id 번호 대신 종목이름으로 보여주기
        return self.stock_name

