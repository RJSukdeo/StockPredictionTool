import Tkinter
import datetime
import resultsProcessor

from dateutil.parser import parse


# This class is responsible for managing any GUI related tasks such as creation of the GUI and error checking the inputs
# from the GUI.
class IntroGUI:

    def __init__(self):
        xDimension = 1024
        yDimension = 475
        self.createIntroScreen("Stock Prediction Tool", xDimension, yDimension)

    def createIntroScreen(self, title, xDimension, yDimension):
        # Create Intro GUI window.
        self.window= Tkinter.Tk()
        self.window.title(title)
        self.window.geometry(str(xDimension)+"x"+str(yDimension))

        # Define checks parameters that need to be defined.
        self.tickerCollection = []
        self.isTrainingStartDateValidFormat = False
        self.isTrainingEndDateValidFormat = False
        # self.isStartProjectionDateValidFormat = False
        self.isEndProjectionDateValidFormat = False
        self.correctTickers = False

        # Set projection start date to today.
        self.projectionStartDate = str(datetime.date.today())

        # Create Intro GUI.
        self.createTrainingInputFrame()
        self.populateTrainingDatesFrame()

        self.createProjectionFrame()
        self.populateProjectionDateFrame()

        self.createTickerFrame()
        self.populateTickerFrame()

        self.createButtonFrame()
        self.populateButtonFrame()

        # Defining bindings.
        self.startDateEntry.bind('<Return>', self.getStartTrainingDateFromEntry)
        self.endDateEntry.bind('<Return>', self.getEndTrainingDateFromEntry)
        self.projectionEndDateEntry.bind('<Return>', self.getProjectionEndDateFromEntry)
        self.TickerEntry.bind('<Return>', self.getTickerFromEntry)

        self.window.mainloop()

    def createTrainingInputFrame(self):
        self.trainingDateframe = Tkinter.Frame(self.window, borderwidth=5, relief="sunken", width=300, height=250)
        self.trainingDateframe.grid(row=0, column=0, padx=205, pady=10)

    def createProjectionFrame(self):
        self.projectionDateframe = Tkinter.Frame(self.window, borderwidth=5, relief="sunken", width=300, height=250)
        self.projectionDateframe.grid(row=1, column=0, padx=205, pady=10)

    def createTickerFrame(self):
        self.tickerframe = Tkinter.Frame(self.window, borderwidth=5, relief="sunken", width=300, height=250)
        self.tickerframe.grid(row=2, column=0, padx=205, pady=10)

    def createButtonFrame(self):
        self.buttonFrame = Tkinter.Frame(self.window, borderwidth=5, relief="sunken", width=300, height=300)
        self.buttonFrame.grid(row=3, column=0, padx=205, pady=10)

    def populateTrainingDatesFrame(self):
        borderLabel = Tkinter.Label(self.trainingDateframe, text="==================================================================", font="bold")
        borderLabel.grid(columnspan= 3)
        trainingDatesHeadingLabels = Tkinter.Label(self.trainingDateframe, text = "Model Training Dates", justify = "center", font="bold")
        trainingDatesHeadingLabels.grid(row=1, columnspan= 3)

        # Defining label and entry for start training date.
        startDateLabel = Tkinter.Label(self.trainingDateframe, text="Start Date (YYYY-MM-DD):")
        startDateLabel.grid(column=0, row=2, padx= 10, pady= 3, sticky= "W")
        self.startDateEntry = Tkinter.Entry(self.trainingDateframe, bd=5)
        self.startDateEntry.grid(column=1, row=2, padx= 10, pady= 3)

        self.startDateStringVar = Tkinter.StringVar()
        self.startDateStringVar.set("Result: Not Loaded")
        self.startDateResultLabel = Tkinter.Label(self.trainingDateframe, textvariable=self.startDateStringVar)
        self.startDateResultLabel.grid(column=2 ,row=2, padx= 10, pady= 3)

        # Defining label and entry for end training date.
        endDateLabel = Tkinter.Label(self.trainingDateframe, text="End Date (YYYY-MM-DD):")
        endDateLabel.grid(column=0, row=3, padx= 10, pady= 3, sticky= "W")
        self.endDateEntry = Tkinter.Entry(self.trainingDateframe, bd=5)
        self.endDateEntry.grid(column=1, row=3, padx= 10, pady= 3)

        self.endDateStringVar = Tkinter.StringVar()
        self.endDateStringVar.set("Result: Not Loaded")
        self.endDateResultLabel = Tkinter.Label(self.trainingDateframe, textvariable=self.endDateStringVar)
        self.endDateResultLabel.grid(column=2 ,row=3, padx= 10, pady= 3)

    def populateProjectionDateFrame(self):

        borderLabel = Tkinter.Label(self.projectionDateframe, text="==================================================================", font="bold")
        borderLabel.grid(columnspan= 3)

        # Defining label and entry for projection date.
        ProjectionHeadingLabel = Tkinter.Label(self.projectionDateframe, text = "Projection Date", justify = "center", font="bold")
        ProjectionHeadingLabel.grid(row=1, columnspan= 3)

        projectionEndDateLabel = Tkinter.Label(self.projectionDateframe, text="Date (YYYY-MM-DD):")
        projectionEndDateLabel.grid(column=0, row=3, padx= 10, pady= 3, sticky= "W")

        self.projectionEndDateEntry = Tkinter.Entry(self.projectionDateframe, bd=5)
        self.projectionEndDateEntry.grid(column=1, row=3, padx= 10, pady= 3)

        self.projectionEndDateStringVar = Tkinter.StringVar()
        self.projectionEndDateStringVar.set("Result: Not Loaded")
        self.projectionEndDateResultLabel = Tkinter.Label(self.projectionDateframe, textvariable=self.projectionEndDateStringVar)
        self.projectionEndDateResultLabel.grid(column=2, row=3, padx= 10, pady= 3)

    def populateTickerFrame(self):

        borderLabel = Tkinter.Label(self.tickerframe, text="==================================================================", font="bold")
        borderLabel.grid(columnspan= 3)

        # Defining label and entry for tickers.
        tickersHeadingLabel = Tkinter.Label(self.tickerframe, text = "Stock Tickers", justify = "center", font="bold")
        tickersHeadingLabel.grid(row=1, columnspan=3,)

        TickerLabel = Tkinter.Label(self.tickerframe, text="Enter Tickers:")
        TickerLabel.grid(column=0, row=2, padx= 10, pady= 3, sticky= "W")
        self.TickerEntry = Tkinter.Entry(self.tickerframe, bd=5)
        self.TickerEntry.grid(column=1, row=2, padx= 10, pady= 3)

        self.tickerStringVar = Tkinter.StringVar()
        self.tickerStringVar.set("Result: Not Loaded")
        self.projectionStartDateResultLabel = Tkinter.Label(self.tickerframe, textvariable=self.tickerStringVar)
        self.projectionStartDateResultLabel.grid(column=2, row=2, padx= 10, pady= 3)

    def populateButtonFrame(self):

        self.button = Tkinter.Button(self.buttonFrame, state="disabled", command=self.processButtonPressed, text= "Run Model!!!")
        self.button.grid()

        self.processLabelStringVar = Tkinter.StringVar()
        self.processLabelStringVar.set("Please Input All Required Fields!")
        self.processLabel = Tkinter.Label(self.buttonFrame, textvariable=self.processLabelStringVar)
        self.processLabel.grid(column=0, row=1)

    def getStartTrainingDateFromEntry(self, event=None):

        dateEntry = self.startDateEntry.get()

        if self.isValidDateFormat(dateEntry):
            self.isTrainingStartDateValidFormat = True
            self.startTrainingDate = dateEntry
            self.startDateStringVar.set("Start Training Date: "+dateEntry)
            self.startDateEntry.delete(0, 'end')
            self.displayProcessButton()
        else:
            self.startDateStringVar.set("Result: Date format must be YYYY-MM-DD.")

    def getEndTrainingDateFromEntry(self, event=None):

        dateEntry = self.endDateEntry.get()

        if self.isValidDateFormat(dateEntry):
            self.isTrainingEndDateValidFormat = True
            self.endTrainingDate = dateEntry
            self.endDateStringVar.set("End Training Date: "+ dateEntry)
            self.endDateEntry.delete(0, 'end')
            self.displayProcessButton()
        else:
            self.endDateStringVar.set("Result: Date format must be YYYY-MM-DD.")

    def getProjectionEndDateFromEntry(self, event=None):

        dateEntry = self.projectionEndDateEntry.get()

        if self.isValidDateFormat(dateEntry):
            self.isEndProjectionDateValidFormat = True
            self.projectionEndDate = dateEntry
            self.projectionEndDateStringVar.set("Projection Date: " + dateEntry)
            self.projectionEndDateEntry.delete(0, 'end')
            self.displayProcessButton()
        else:
            self.projectionEndDateStringVar.set("Result: Date format must be YYYY-MM-DD.")

    def getTickerFromEntry(self, event=None):

        tickerEntry = str(self.TickerEntry.get()).upper()

        if tickerEntry not in self.tickerCollection:
            self.correctTickers = True
            self.tickerCollection.append(tickerEntry)
            self.tickerStringVar.set(tickerEntry+" added successfully.")
            self.TickerEntry.delete(0, 'end')
            self.displayProcessButton()
        else:
            self.tickerStringVar.set(tickerEntry+" already inputted.")

    def isValidDateFormat(self, date):

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def displayProcessButton(self):

        if self.isTrainingStartDateValidFormat and self.isTrainingEndDateValidFormat and self.isEndProjectionDateValidFormat and self.correctTickers:

            if self.isStartDateBeforeEndDateForTraining():
                if self.isStartDateBeforeEndDateForProjection():
                    if self.isThereEnoughTrainingData():
                        self.button["state"]= "normal"

    def isStartDateBeforeEndDateForTraining(self):

        isStartBeforeEndTrainingDate = False
        if self.startTrainingDate < self.endTrainingDate:
            isStartBeforeEndTrainingDate = True
        else:
            self.processLabelStringVar.set("Training start date must be before training end date.")

        return isStartBeforeEndTrainingDate

    def isStartDateBeforeEndDateForProjection(self):

        isStartBeforeEndProjectionDate = False
        if self.projectionStartDate < self.projectionEndDate:
            isStartBeforeEndProjectionDate = True
        else:
            self.processLabelStringVar.set("Projection start date must be before projection end date.")

        return isStartBeforeEndProjectionDate

    def isThereEnoughTrainingData(self):

        isEnoughData = False

        #  You must have enough of training data in order to train your models, this condition checks that.
        if (parse(self.endTrainingDate) - parse(self.startTrainingDate)).days > (parse(self.projectionEndDate) - parse(self.projectionStartDate)).days:
            isEnoughData = True
        else:
            self.processLabelStringVar.set("Not enough training data for given projection dates.")

        return isEnoughData

    def processButtonPressed(self, event=None):

        try:
            results = resultsProcessor.ResultsProcessor(self.startTrainingDate, self.endTrainingDate,
                                                    self.tickerCollection, self.projectionEndDate,
                                                    self.projectionStartDate)

            results.processResults()
            self.processLabelStringVar.set("Complete!!!")

        except Exception as e:
            self.processLabelStringVar.set("Exception: " +str(e))
            raise
