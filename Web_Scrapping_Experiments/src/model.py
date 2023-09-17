""" convinience class for keeping track of model and its metadata """

class Model:
    """ model class used to keep track of the model we have 
    selected and some additional parameters """
    def __init__(self):
        self.name = None
        self.model = None
        self.model_fit = None
        self.mse = None
        self.order = None

    def set_name(self, name):
        """
        Setter method for the name attribute.
        """
        self.name = name

    def set_model(self, model):
        """
        Setter method for the model attribute.
        """
        self.model = model

    def set_model_fit(self, model_fit):
        """
        Setter method for the model_fit attribute.
        """
        self.model_fit = model_fit

    def set_mse(self, mse):
        """
        Setter method for the mse attribute.
        """
        self.mse = mse

    def set_order(self, order):
        """
        Setter method for the order attribute.
        """
        self.order = order
