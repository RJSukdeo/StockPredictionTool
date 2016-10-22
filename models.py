from sklearn import linear_model
from sklearn import metrics
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor


# This class trains three models: linear regression model, KNN model and tree regression model. Ensemble model is not
# trained in this class.
class Models():

    def trainLinearModel(self, xTraining, yTraining, xValidation, yValidation):

        model = linear_model.LinearRegression()
        model.fit(xTraining, yTraining)

        return model

    def trainDecisionTree(self, xTraining, yTraining, xValidation, yValidation):

        max_depth_parameters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        min_sample_parameters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for max_depth_parameter in max_depth_parameters:
            for min_sample_parameter in min_sample_parameters:
                model = DecisionTreeRegressor(max_depth=max_depth_parameter, min_samples_split=min_sample_parameter)
                model.fit(xTraining, yTraining)
                mse_estimate = metrics.mean_squared_error(yValidation, model.predict(xValidation))

                if max_depth_parameter == 1 and min_sample_parameter == 1:
                    min_mse = mse_estimate
                    best_model = model

                if mse_estimate < min_mse:
                    min_mse = mse_estimate
                    best_model = model

        return best_model

    def trainKNN(self, xTraining, yTraining, xValidation, yValidation):

        neighbour_parameters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for neighbour_parameter in neighbour_parameters:

            model = KNeighborsRegressor(n_neighbors=neighbour_parameter)
            model.fit(xTraining, yTraining)
            mse_estimate = metrics.mean_squared_error(yValidation, model.predict(xValidation))

            if neighbour_parameter == neighbour_parameters[0]:
                min_mse = mse_estimate
                best_model = model

            if mse_estimate < min_mse:
                    min_mse = mse_estimate
                    best_model = model

        return best_model
