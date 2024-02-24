import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

data_path = 'AirPassengers.csv'
air_passengers = pd.read_csv(data_path)
air_passengers['Month'] = pd.to_datetime(air_passengers['Month'])
air_passengers.set_index('Month', inplace=True)


sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
plt.plot(air_passengers, marker='o', linestyle='-', color='b')
plt.title('Air Passengers Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Passengers')
plt.show()

decomposition = seasonal_decompose(air_passengers['#Passengers'], model='multiplicative')
plt.figure(figsize=(14, 8))
plt.subplot(411)
plt.plot(air_passengers['#Passengers'], label='Original', color='blue')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(decomposition.trend, label='Trend', color='red')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(decomposition.seasonal, label='Seasonality', color='green')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(decomposition.resid, label='Residuals', color='black')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

dftest = adfuller(air_passengers['#Passengers'], autolag='AIC')
dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
for key, value in dftest[4].items():
    dfoutput['Critical Value (%s)' % key] = value
print(dfoutput)

air_passengers_diff = air_passengers['#Passengers'].diff().dropna()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(air_passengers_diff, lags=40, ax=ax1)
plot_pacf(air_passengers_diff, lags=40, ax=ax2)
plt.tight_layout()
plt.show()

model = ARIMA(air_passengers['#Passengers'], order=(2,1,2))
results = model.fit()
print(results.summary())

forecast = results.get_forecast(steps=24)
forecast_conf_int = forecast.conf_int()
plt.figure(figsize=(12, 6))
plt.plot(air_passengers, label='Historical Monthly Passengers')
plt.plot(forecast.predicted_mean, label='Forecast', color='red')
plt.fill_between(forecast_conf_int.index, forecast_conf_int.iloc[:, 0], forecast_conf_int.iloc[:, 1], color='pink', alpha=0.3)
plt.title('Air Passengers Forecast')
plt.xlabel('Year')
plt.ylabel('Number of Passengers')
plt.legend()
plt.show()