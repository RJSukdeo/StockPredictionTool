import logging

# This class is responsible for filtering the raw data from Quandl for fields that the user is interested in.
class DataFilter:
    filters = []

    def addFilters(self, filters):
        for filter in filters:
            self.filters.append(filter)
            logging.info('[DataFilter]: '+filter+' added to filter list.')

    def removeFilters(self, filters):
        for filter in filters:
            if filter in self.filters:
                self.filters.remove(filter)
                logging.info('[DataFilter]: '+filter+' removed from filter list.')
            else:
                logging.warning('[DataFilter]: '+filter + 'to be removed not found in filter list.')

    def applyFilters(self, rawDataCollection):
        filteredDataCollection = {}

        for key in rawDataCollection.keys():
            filteredDataCollection.update({key: rawDataCollection[key][self.filters]})

        return filteredDataCollection

    def applyFiltersAndFillMissingData(self, rawDataCollection):
        filteredDataCollection = self.applyFilters(rawDataCollection)

        for key in filteredDataCollection.keys():
            filteredDataCollection[key].fillna(method='ffill')
            filteredDataCollection[key].fillna(method='bfill')

        return filteredDataCollection
