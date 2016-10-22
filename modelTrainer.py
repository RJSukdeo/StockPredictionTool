import models
import scipy.optimize
import numpy

from sklearn import cross_validation
from dateutil.parser import parse
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from directoryManipulator import DirectoryManipulator
from sklearn import preprocessing


# This class uses the models class to train all four models and logging of the results. Ensemble model is also derived
#  in this class.
class ModelTrainer:

    def __init__(self, marketData, currentDate, projectionDate):
        self.marketData = marketData
        self.projectionDate = projectionDate
        self.currentDate = currentDate

    def trainModels(self, yColumn, xColumns, testPercent):
        directoryManipulator = DirectoryManipulator()
        modelGenerator = models.Models()
        dateLag = (parse(self.projectionDate) - parse(self.currentDate)).days
        self.modelDictionary = {}
        self.rSquareDictionary = {}
        self.transformDictionary = {}

        for key in self.marketData.keys():

            # Lag data and standardize the independant variables.
            laggedYData = self.marketData[key][yColumn][dateLag:]
            laggedXData = self.marketData[key][xColumns][:-dateLag]

            dataTransformer = preprocessing.StandardScaler()
            dataTransformer.fit(laggedXData)
            self.transformDictionary.update({key: dataTransformer})
            standardisedLaggedXData = dataTransformer.transform(laggedXData)


            # Create train test split.
            self.xTrainData, xTestData,  self.yTrainData, yTestData= cross_validation.train_test_split(standardisedLaggedXData, laggedYData, test_size=testPercent)

            # Create test validation split, validation data will be 33% of test data.... 10% of overall data.
            xTestData, xValidationData, yTestData, yValidationData = cross_validation.train_test_split(xTestData, yTestData, test_size=0.3333333)

            # Train linear model and document results.
            self.linearModel = modelGenerator.trainLinearModel(self.xTrainData, self.yTrainData, xValidationData, yValidationData)
            self.linearModelValidationScore = r2_score(yValidationData, self.linearModel.predict(xValidationData))
            directoryManipulator.editStockTrainingTextFile(key, "--- LINEAR MODEL ---")
            directoryManipulator.editStockTrainingTextFile(key, "Training r2: " + str(r2_score(self.yTrainData, self.linearModel.predict(self.xTrainData))) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Validation r2: " + str(self.linearModelValidationScore) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Test r2: " + str(r2_score(yTestData, self.linearModel.predict(xTestData))) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "")

            # Create linear model pdfs.
            directoryManipulator.createLinearModelPredictionsPlot(key, laggedXData.index.values,  laggedXData.index.values, self.linearModel.predict(standardisedLaggedXData), laggedYData.values)
            directoryManipulator.createLinearModelDifferencesPlot(key, laggedXData.index.values, (abs(laggedYData.values - self.linearModel.predict(standardisedLaggedXData)))/laggedYData.values)

            # Train tree model and document results.
            self.treeModel = modelGenerator.trainDecisionTree(self.xTrainData, self.yTrainData, xValidationData, yValidationData)
            self.treeModelValidationScore = r2_score(yValidationData, self.treeModel.predict(xValidationData))
            directoryManipulator.editStockTrainingTextFile(key, "--- TREE MODEL ---")
            directoryManipulator.editStockTrainingTextFile(key, "Max depth parameter chosen: " + str(self.treeModel.max_depth) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Min sample split parameter chosen: " + str(self.treeModel.min_samples_split) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "")
            directoryManipulator.editStockTrainingTextFile(key, "Training r2: " + str(r2_score(self.yTrainData, self.treeModel.predict(self.xTrainData)))+".")
            directoryManipulator.editStockTrainingTextFile(key, "Validation r2: " + str(self.treeModelValidationScore)+".")
            directoryManipulator.editStockTrainingTextFile(key, "Test r2: " + str(r2_score(yTestData, self.treeModel.predict(xTestData)))+".")
            directoryManipulator.editStockTrainingTextFile(key, "")

            # Create tree model pdfs.
            directoryManipulator.createTreeModelPredictionsPlot(key, laggedXData.index.values, laggedXData.index.values, self.treeModel.predict(standardisedLaggedXData), laggedYData.values)
            directoryManipulator.createTreeModelDifferencessPlot(key, laggedXData.index.values, (abs(laggedYData.values - self.treeModel.predict(standardisedLaggedXData)))/laggedYData.values)

            # Train KNN model and document results.
            self.knnModel = modelGenerator.trainKNN(self.xTrainData, self.yTrainData, xValidationData, yValidationData)
            self.knnModelValidationScore = r2_score(yValidationData, self.knnModel.predict(xValidationData))
            directoryManipulator.editStockTrainingTextFile(key, "--- KNN MODEL ---")
            directoryManipulator.editStockTrainingTextFile(key, "N neighbours parameter chosen: " + str(self.knnModel.n_neighbors)+".")
            directoryManipulator.editStockTrainingTextFile(key, "")
            directoryManipulator.editStockTrainingTextFile(key, "Training r2: " + str(r2_score(self.yTrainData, self.knnModel.predict(self.xTrainData))) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Validation r2: " + str(self.knnModelValidationScore) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Test r2: " + str(r2_score(yTestData, self.knnModel.predict(xTestData))) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "")

            # Create KNN model pdfs.
            directoryManipulator.createKNNModelPredictionsPlot(key, laggedXData.index.values, laggedXData.index.values, self.knnModel.predict(standardisedLaggedXData), laggedYData.values)
            directoryManipulator.createKNNModelDifferencesPlot(key, laggedXData.index.values, (abs(laggedYData.values - self.knnModel.predict(standardisedLaggedXData)))/laggedYData.values)

            bnds = ((0.0, 0.5), (0.0, 0.5), (0.0, 0.5))
            ensembleModelParameters = scipy.optimize.minimize(self.optimizationFuction,
                                                              numpy.array([0.333, 0.333, 0.333]),
                                                              method='SLSQP',
                                                              bounds=bnds,
                                                              constraints=[{'type': 'eq', 'fun': self.optimizationConstraints}])

            self.modelDictionary.update({key: (self.linearModel, self.treeModel, self.knnModel, ensembleModelParameters)})

            self.ensembleModelValidationScore = r2_score(yValidationData, self.predictNoDataFrame(xValidationData, key))

            self.rSquareDictionary.update({key: (self.linearModelValidationScore, self.treeModelValidationScore, self.knnModelValidationScore, self.ensembleModelValidationScore)})
            directoryManipulator.editStockTrainingTextFile(key, "--- ENSEMBLE MODEL ---")
            directoryManipulator.editStockTrainingTextFile(key, "Linear model weight: " + str(ensembleModelParameters.x[0]) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Tree model weight: " + str(ensembleModelParameters.x[1]) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "KNN model weight: " + str(ensembleModelParameters.x[2]) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "")
            directoryManipulator.editStockTrainingTextFile(key, "Training r2: " + str(r2_score(self.yTrainData, self.predictNoDataFrame(self.xTrainData, key))) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Validation r2: " + str(self.ensembleModelValidationScore) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "Testing r2: " + str(r2_score(yTestData, self.predictNoDataFrame(xTestData, key))) + ".")
            directoryManipulator.editStockTrainingTextFile(key, "")

            # Create ensemble model pdfs.
            directoryManipulator.createEnsemblePredictionsPlot(key, laggedXData.index.values, laggedXData.index.values, self.predictNoDataFrame(standardisedLaggedXData, key), laggedYData.values)
            directoryManipulator.createEnsembleDifferencesPlot(key, laggedXData.index.values, (abs(laggedYData.values - self.predictNoDataFrame(standardisedLaggedXData, key)))/laggedYData.values)

            # Create entries for mean differences.
            directoryManipulator.editStockTrainingTextFile(key,"--- Model Differences ---")
            directoryManipulator.editStockTrainingTextFile(key,"Linear model mean % difference on test dataset: " + str(numpy.mean((abs(yTestData.values - self.linearModel.predict(xTestData)))/yTestData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"Tree model mean % difference on test dataset: " + str(numpy.mean((abs(yTestData.values - self.treeModel.predict(xTestData)))/yTestData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"KNN model mean % difference on test dataset: " + str(numpy.mean((abs(yTestData.values - self.knnModel.predict(xTestData)))/yTestData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"Ensemble model mean % difference on test dataset: " + str(numpy.mean((abs(yTestData.values - self.predictNoDataFrame(xTestData, key)))/yTestData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"")
            directoryManipulator.editStockTrainingTextFile(key,"Linear model mean % difference on training dataset: " + str(numpy.mean((abs(self.yTrainData.values - self.linearModel.predict(self.xTrainData)))/self.yTrainData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"Tree model mean % difference on training dataset: " + str(numpy.mean((abs(self.yTrainData.values - self.treeModel.predict(self.xTrainData)))/self.yTrainData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"KNN model mean % difference on training dataset: " + str(numpy.mean((abs(self.yTrainData.values - self.knnModel.predict(self.xTrainData)))/self.yTrainData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"Ensemble model mean % difference on training dataset: " + str(numpy.mean((abs(self.yTrainData.values - self.predictNoDataFrame(self.xTrainData, key)))/self.yTrainData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"")
            directoryManipulator.editStockTrainingTextFile(key,"Linear model mean % difference on validation dataset: " + str(numpy.mean((abs(yValidationData.values - self.linearModel.predict(xValidationData)))/yValidationData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"Tree model mean % difference on validation dataset: " + str(numpy.mean((abs(yValidationData.values - self.treeModel.predict(xValidationData)))/yValidationData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"KNN model mean % difference on validation dataset: " + str(numpy.mean((abs(yValidationData.values - self.knnModel.predict(xValidationData)))/yValidationData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"Ensemble model mean % difference on validation dataset: " + str(numpy.mean((abs(yValidationData.values - self.predictNoDataFrame(xValidationData, key)))/yValidationData.values)))
            directoryManipulator.editStockTrainingTextFile(key,"")


    def optimizationConstraints(self, weights):

        weightSum = weights[0] + weights[1] + weights[2]

        return weightSum - 1

    def optimizationFuction(self, weights):

        linearModelPrediction = weights[0] * self.linearModel.predict(self.xTrainData)
        treeModelPrediction = weights[1] * self.treeModel.predict(self.xTrainData)
        knnModelPrediction = weights[2] * self.knnModel.predict(self.xTrainData)

        prediction = linearModelPrediction + treeModelPrediction + knnModelPrediction

        return mean_squared_error(self.yTrainData, prediction)

    def predictNoDataFrame(self, xData,key):

        linearModelPrediction = self.modelDictionary[key][0].predict(xData)*self.modelDictionary[key][3].x[0]
        treeModelPrediction = self.modelDictionary[key][1].predict(xData)*self.modelDictionary[key][3].x[1]
        knnModelPrediction = self.modelDictionary[key][2].predict(xData)*self.modelDictionary[key][3].x[2]

        return linearModelPrediction + treeModelPrediction + knnModelPrediction

    def predictEnsemble(self, xDataFrame, xColumns, key):

        linearModelPrediction = self.modelDictionary[key][0].predict(xDataFrame)*self.modelDictionary[key][3].x[0]
        treeModelPrediction = self.modelDictionary[key][1].predict(xDataFrame)*self.modelDictionary[key][3].x[1]
        knnModelPrediction = self.modelDictionary[key][2].predict(xDataFrame)*self.modelDictionary[key][3].x[2]

        return linearModelPrediction + treeModelPrediction + knnModelPrediction

    def predictLinear(self, xDataFrame, xColumns, key):

        return self.modelDictionary[key][0].predict(xDataFrame)

    def predictTree(self, xDataFrame, xColumns, key):

        return self.modelDictionary[key][1].predict(xDataFrame)

    def predictKNN(self, xDataFrame, xColumns, key):

        return self.modelDictionary[key][2].predict(xDataFrame)

    def predict(self, xDataFrame, xColumns, key):

        # Standardise the market data before it is used.
        xDataFrame = self.transformDictionary[key].transform(xDataFrame[key][xColumns])

        directoryManipulator = DirectoryManipulator()

        directoryManipulator.editStockPredictionTextFile(key, "Linear model validation r2: " + str(self.rSquareDictionary[key][0]))
        directoryManipulator.editStockPredictionTextFile(key, "Tree model validation r2: " + str(self.rSquareDictionary[key][1]))
        directoryManipulator.editStockPredictionTextFile(key, "KNN model validation r2: " + str(self.rSquareDictionary[key][2]))
        directoryManipulator.editStockPredictionTextFile(key, "Ensemble model validation r2: " + str(self.rSquareDictionary[key][3]))
        directoryManipulator.editStockPredictionTextFile(key, "")

        if self.rSquareDictionary[key][0] > self.rSquareDictionary[key][1] and self.rSquareDictionary[key][0] > self.rSquareDictionary[key][2] and self.rSquareDictionary[key][0] > self.rSquareDictionary[key][3]:
            linearPrediction = self.predictLinear(xDataFrame, xColumns, key)

            directoryManipulator.editStockTrainingTextFile(key, "Linear model has greatest validation r2, has been chosen as model for "+key+".")
            directoryManipulator.editStockPredictionTextFile(key, "Linear model has greatest validation r2, has been chosen as model for "+key+".")
            directoryManipulator.editStockPredictionTextFile(key, key + ": " + str(linearPrediction))
            directoryManipulator.editFinalPredictionTextFile(key + ": " + str(linearPrediction))

            return linearPrediction

        if self.rSquareDictionary[key][1] > self.rSquareDictionary[key][0] and self.rSquareDictionary[key][1] > self.rSquareDictionary[key][2] and self.rSquareDictionary[key][1] > self.rSquareDictionary[key][3]:
            treePrediction = self.predictTree(xDataFrame, xColumns, key)

            directoryManipulator.editStockTrainingTextFile(key, "Tree model has greatest validation r2, has been chosen as model for "+key+".")
            directoryManipulator.editStockPredictionTextFile(key, "Tree model has greatest validation r2, has been chosen as model for "+key+".")
            directoryManipulator.editStockPredictionTextFile(key, key + ": " + str(treePrediction))
            directoryManipulator.editFinalPredictionTextFile(key + ": " + str(treePrediction))

            return treePrediction

        if self.rSquareDictionary[key][2] > self.rSquareDictionary[key][0] and self.rSquareDictionary[key][2] > self.rSquareDictionary[key][1] and self.rSquareDictionary[key][2] > self.rSquareDictionary[key][3]:
            knnPrediction = self.predictKNN(xDataFrame, xColumns, key)

            directoryManipulator.editStockTrainingTextFile(key, "KNN model has greatest validation r2, has been chosen as model for "+key+".")
            directoryManipulator.editStockPredictionTextFile(key, "KNN model has greatest validation r2, has been chosen as model for "+key+".")
            directoryManipulator.editStockPredictionTextFile(key, key + ": " + str(knnPrediction))
            directoryManipulator.editFinalPredictionTextFile(key + ": " + str(knnPrediction))

            return knnPrediction

        ensemblePrediction = self.predictEnsemble(xDataFrame, xColumns, key)

        directoryManipulator.editStockTrainingTextFile(key, "Ensemble model has greatest validation r2, has been chosen as model for "+key+".")
        directoryManipulator.editStockPredictionTextFile(key, "Ensemble model has greatest validation r2, has been chosen as model for "+key+".")
        directoryManipulator.editStockPredictionTextFile(key, key + ": " + str(ensemblePrediction))
        directoryManipulator.editFinalPredictionTextFile(key + ": " + str(ensemblePrediction))

        return ensemblePrediction
