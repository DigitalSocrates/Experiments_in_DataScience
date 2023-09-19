""" all model training steps are here """
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_model import ARMAResults
from sklearn.metrics import mean_squared_error


class Trainer:
    """ model trainer main class """
    # Define the range of hyperparameters to search
    SESONAL_LIST = {True, False}
    SCORING_LIST = {'mse','mae'}
    METHOD_LIST = {'statespace','innovations_mle','hannan_rissanen',} # for ball 3, 4, and bonus -> 'innovations','burg','yule_walker'
    COV_LIST = {'opg','oim','approx','robust','robust_approx','none'}

    def __init__(self, suppress_warnings: bool = True,
                 trace: bool = True,
                 error_action: str = 'ignore',
                 maxiter: int = 100):
        self.suppress_warnings=suppress_warnings
        self.trace = trace
        self.error_action = error_action
        self.maxiter = maxiter

    def find_best_arima_model(self,
                              ts_data,
                              max_order=16):
        """
        Find the best ARIMA model for the given time series data.
        Returns the best ARIMA order.
        """
        best_order = None
        best_model = None

        for order in range(4, max_order):
            for score in self.SCORING_LIST:
                for season in self.SESONAL_LIST:
                    model = auto_arima(ts_data,
                                    trace=self.trace,
                                    error_action=self.error_action,
                                    max_order=order,
                                    suppress_warnings=self.suppress_warnings,
                                    stepwise=True,
                                    scoring=score,
                                    seasonal=season,
                                    maxiter=self.maxiter)

                    if best_model is None:
                        # Get the best ARIMA order and model
                        best_order = model.order
                        best_model = model
                    else:
                        best_model = self.compare_two_models(model1=model,
                                                            model2=best_model,
                                                            size=len(ts_data))
                        best_order = best_model.order

        return best_order, best_model

    def fit_arima_model(self, ts_data, order):
        """
        Fit an ARIMA model with the specified order to the time series data.
        Returns the fitted ARIMA model.
        """
        final_model = None
        final_model_fit = None
        best_mse = float('inf')

        arima_model = ARIMA(ts_data, order=order)

        for method in self.METHOD_LIST:
            for cov_type in self.COV_LIST:
                if method=='burg' and cov_type=='oim':
                    continue
                else:
                    model_fit = arima_model.fit(method=method, cov_type=cov_type)
                    y_pred = model_fit.predict(n_periods=1, exog=None, return_conf_int=True)

                    mse = self.calculate_mse(ts_data=ts_data, y_pred=y_pred)
                    if mse < best_mse:
                        print(f'fitting using method:{method} and cov_type:{cov_type} with mse {mse}')
                        best_mse = mse
                        final_model = arima_model
                        final_model_fit = model_fit

        return final_model, final_model_fit

    def calculate_mse(self, ts_data, y_pred):
        """
        Calculate Mean Squared Error (MSE) between the actual and predicted values.
        Returns the MSE.
        """
        mse = mean_squared_error(ts_data, y_pred)
        return mse

    def calculate_metrics(self, size, m_aic, best_order):
        """ Calculate AIC, AICc, and BIC """
        log_likelihood = -0.5 * m_aic
        num_params = best_order[0] + best_order[1] + best_order[2] + 1
        aic = -2 * log_likelihood + 2 * num_params
        aicc = aic + (2 * num_params * (num_params + 1)) / (size - num_params - 1)
        bic = -2 * log_likelihood + num_params * np.log(size)

        return aic, aicc, bic

    def compare_two_models (self, model1, model2, size):
        """ Compare and select the best model based on your preferred criterion (e.g., AIC) """
        aic1, aicc1, bic1 = self.calculate_metrics(size=size,
                                                   m_aic=model1.aic(),
                                                   best_order=model1.order)

        aic2, aicc2, bic2 = self.calculate_metrics(size=size,
                                                   m_aic=model2.aic(),
                                                   best_order=model2.order)

        if aic1 < aic2:
            best_model = model1
            best_criteria = "AIC"
        elif aic2 < aic1:
            best_model = model2
            best_criteria = "AIC"
        else:
            # If AIC is tied, you can use AICc or BIC as a tiebreaker
            if aicc1 < aicc2:
                best_model = model1
                best_criteria = "AICc"
            elif aicc2 < aicc1:
                best_model = model2
                best_criteria = "AICc"
            else:
                if bic1 < bic2:
                    best_model = model1
                    best_criteria = "BIC"
                else:
                    best_model = model2
                    best_criteria = "BIC"
        return best_model
