""" convinience class for keeping track of model and its metadata """


class Model:
    """ model class used to keep track of the model we have
    selected and some additional parameters """
    def __init__(self,
                 name: str,
                 model,
                 model_fit,
                 order):
        self.name = f'ARIMA Model for {name}'
        self.model = model
        self.model_fit = model_fit
        self.order = order

    def set_name(self):
        """
        Getter method for the name attribute.
        """
        return self.name

    def set_model(self):
        """
        Getter method for the model attribute.
        """
        return self.model

    def set_model_fit(self):
        """
        Getter method for the model_fit attribute.
        """
        return self.model_fit

    def get_order(self):
        """
        Getter method for the order attribute.
        """
        return self.order
