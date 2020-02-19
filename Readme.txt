Stock Prediction Tool - Ryan Sukdeo

Welcome, this is the right place to learn more about the Stock Prediction Tool.

Contents
1) Introduction
2) Software Requirements
3) How to get started
4) How to use the GUI
5) Interpreting outputs

1) Introduction
The purpose of the Stock Prediction Tool is to allow the user to forecast equity adjusted closing prices. In my opinion, it is very difficult if not impossible to have a single model that can forecast every stock price well. I built this tool with flexibly that allows the tool to choose the right model for every stock the user is interested in forecasting. The tool chooses between linear regression, a decision tree regression, a KNN and an ensemble model.

Selectable stocks are constrained to the WIKI database on the Quandl data service. This is due to the WIKI database being a free to use database on Quandl. Users interact with the tool through a simple GUI, all results are then stored on disk in a generated folder called 'Results'. 

2) Software Requirements
In this section we will cover the software that is required to compile the stock prediction tool:
  - Python 2.7.10
  - Package: numpy
  - Package: matplotlib
  - Package: Tkinter
  - Package: sklearn
  - Package: scipy
  - Package: quandl
  
3) How to get started
In this section we will discuss the initial process to get this tool up and running. The process is as follows:
  - Register for a free Quandl API key.
  - Create a file named 'QuandlAPIKey.txt' in the same folder that the code resides.
  - Paste Quandl API key into 'QuandlAPIKey.txt'.
  - Run 'tradingApplication.pyc'.
  
4) How to use the GUI
The GUI has four sections that will be discussed separately.

4.1) Model Training Dates

Start Date
This is the start date of the training data set. Enter the start date and press Enter, if the model accepts the input then the date will be cleared from the entry box and the message on the right of the entry box will be updated.

Note that the user will be not able to input dates that are in a form other than YYYY-MM-DD also the start date cannot be before the end date. The check regarding the start date being before the end date will occur when the user tries to run the model not when the user is inputting the dates.

End Date
This is the end date of the training data set. Enter the end date and press Enter, if the model accepts the input then the date will be cleared from the entry box and the message on the right of the entry box will be updated.

Note that the user will be not able to input dates that are in a form other than YYYY-MM-DD also the start date cannot be before the end date. The check regarding the start date being before the end date will occur when the user tries to run the model not when the user is inputting the dates.

4.2) Projection Date

Date
This is the date the user wants to project the adjusted close stock prices to. The projection date must be in the form YYYY-MM-DD. 

Note it is always assumed that the user is projecting from today to the projection date. The tool will determine if there is any data from Quandl for the date the user ran the tool, if there is no data it will find the date with the most current data.

4.3) Stock Tickers

Enter Tickers
This field is responsible for the collection of tickers that the user is interested in. Tickers must be entered individually i.e. the user needs to type one ticker name and press Enter then type in the next ticker and so forth. When the user successfully enters a ticker the message on the right will alert the user that the ticker has been inputted successfully.

Note that the input is agnostic to upper and lower case letters. Make sure that all tickers entered are in the WIKI database, if the ticker is not in WIKI then an exception will be thrown at runtime. This is a potential area of improvement, to check that all tickers are indeed found in WIKI and avoid any runtime exceptions.

4.4) Run Model Button
Initially the 'Run Model!!!' button is greyed out, it will only selectable once all other inputs have inputted correctly. 

Note in order for a value to be inputted correctly the user must press Enter once the value is populated in the relevant field.

5) Interpreting outputs

When the model has run successfully the message under the 'Run Model!!!' button will display 'Complete!!!'. 

When the stock prediction tool has completed its run it will create a Results folder in the same folder that the user ran 'tradingApplication.pyc' from. If a Results folder exists the tool will delete all content in the folder and populate the folder with new results.

In the results folder a text file called 'final_results.txt' will be created that will contain the projected stock prices. The tool will also create a folder for each stock the user specified. If the user specified a stock that does not exist between the start and end training dates then that stock will not be included in the analysis, a folder will be created for that stock with two text files but those text files will mention that the stock did not exist in the training dates hence will be excluded from analysis.

The stock folders will contain the following files:
  - prediction_results.txt
  - train_results.txt
  - Linear_Prediction.pdf
  - Linear_Differences.pdf
  - Tree_Prediction.pdf
  - Tree_Differences.pdf
  - KNN_Prediction.pdf
  - KNN_Differences.pdf
  - Ensemble_Prediction.pdf
  - Ensemble_Differences.pdf
  
5.1) prediction_results.txt
This file contains information on the stock's prediction. It contains the date that the most current data is available for the stock as well as the trained model results and which model was eventually chosen. At the end of the file you will see the projected stock price.
 
Note the final projected adjusted close stock price for every stock is consolidated in the 'final_results.txt' file in the Results folder.
 
5.2) train_results.txt
This file contains information on the stock's training models. If the user wants more granular information on the training process this text file will contain that information. It gives statistics for each potential model and lets the user know which model amongst the available models will be used for projection. It also contains the absolute mean % difference between the predicted values and the actual values, this gives some indication on the accuracy of the models.
 
5.3) Linear_Prediction.pdf
A graph showing the actual vs predicted stock prices using a linear regression model.

5.4) Linear_Differences.pdf
Shows the absolute percentage differences between actual and predicted stock prices as well the mean absolute difference. The prediction is done using a linear regression model.
 
5.5) Tree_Prediction.pdf
A graph showing the actual vs predicted stock prices using a tree regression model.
 
5.6) Tree_Differences.pdf
Shows the absolute percentage differences between actual and predicted stock prices as well the mean absolute difference. The prediction is done using a tree regression model.

5.7) KNN_Prediction.pdf
A graph showing the actual vs predicted stock prices using a KNN model.
 
5.8) KNN_Differences.pdf
Shows the absolute percentage differences between actual and predicted stock prices as well the mean absolute difference. The prediction is done using a KNN model.
 
5.9) Ensemble_Prediction.pdf
A graph showing the actual vs predicted stock prices using an ensemble model.
 
5.10) Ensemble_Differences.pdf
Shows the absolute percentage differences between actual and predicted stock prices as well the mean absolute difference. The prediction is done using an ensemble model.  
  
-- END --
