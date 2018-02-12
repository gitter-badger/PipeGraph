
#from sklearn.datasets import load_boston

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from pipegraph.pipeGraph import PipeGraphRegressor
import matplotlib.pyplot as plt
%matplotlib qt
##
# Ejemplo 1: sc + lm
X = np.random.rand(100,1)
y = 4 * X + 0.5*np.random.randn(100,1)
scaler = MinMaxScaler()
linear_model = LinearRegression()
steps = [('scaler', scaler), ('linear_model', linear_model)]
connections = {'scaler': { 'X': 'X'}, 'linear_model': {'X': ('scaler', 'predict'),  'y': 'y' }  }
pgraph = PipeGraphRegressor(steps=steps, connections=connections)
pgraph.fit(X, y)
y_pred = pgraph.predict(X)
plt.scatter(X, y)
plt.scatter(X, y_pred)
plt.show()
linear_model.coef_

##
# Ejemplo 2: sc + feature + lm
#   usando gridsearchcv

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from pipegraph.pipeGraph import PipeGraphRegressor

import matplotlib.pyplot as plt
%matplotlib qt

X = 2*np.random.rand(100,1)-1
y = 40 * X**5 + 3*X*2 +  3*X + 3*np.random.randn(100,1)

scaler = MinMaxScaler()
polynomial_features = PolynomialFeatures()
linear_model = LinearRegression()

steps = [('scaler', scaler),
         ('polynomial_features', polynomial_features),
         ('linear_model', linear_model)]

connections = {'scaler': { 'X': 'X'},
               'polynomial_features': {'X': ('scaler', 'predict')},
               'linear_model': {'X': ('polynomial_features', 'predict'),
                                'y': 'y' }  }

param_grid = {'polynomial_features__degree': range(1, 11),
              'linear_model__fit_intercept': [True, False]}
pgraph = PipeGraphRegressor(steps=steps, connections=connections)
grid_search_regressor  = GridSearchCV(estimator=pgraph, param_grid=param_grid, refit=True, error_score=neg)
grid_search_regressor.fit(X, y)
y_pred = grid_search_regressor.predict(X)
plt.scatter(X, y)
plt.scatter(X, y_pred)
plt.show()
grid_search_regressor.best_estimator_.get_params()['linear_model'].coef_
grid_search_regressor.best_estimator_.get_params()['polynomial_features'].degree

##
# Ejemplo 3. con potencias
from sklearn.base import BaseEstimator

class CustomPower(BaseEstimator):
    def __init__(self, power=1):
        self.power=power

    def fit(self):
        return self

    def predict(self, X):
        return X**self.power


X = np.array([0, 1, 2, 3, 4, 5, 6, 7]).reshape(-1,1)
y = np.array([0, 1, 4, 9, 16, 25, 60, 85])
sample_weight= np.array([0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.1, 0.1])
scaler = MinMaxScaler()
polynomial_features = PolynomialFeatures()
linear_model = LinearRegression()
custom_power = CustomPower()

steps = [('custom_power', custom_power),
         ('scaler', scaler),
         ('polynomial_features', polynomial_features),
         ('linear_model', linear_model)]

connections = { 'custom_power': { 'X': 'sample_weight'},
                'scaler': { 'X': 'X'},
                'polynomial_features': {'X': ('scaler', 'predict')},
                'linear_model': {'X': ('polynomial_features', 'predict'),
                                'y': 'y',
                                 'sample_weight': ('custom_power', 'predict')}  }


param_grid = {'polynomial_features__degree': range(1, 11),
              'linear_model__fit_intercept': [True, False],
              'custom_power__power': [1, 5, 10]}

pgraph = PipeGraphRegressor(steps=steps, connections=connections)
grid_search_regressor  = GridSearchCV(estimator=pgraph, param_grid=param_grid, refit=True)
grid_search_regressor.fit(X, y, sample_weight=sample_weight)
y_pred = grid_search_regressor.predict(X)
plt.scatter(X, y)
plt.scatter(X, y_pred)
plt.show()
