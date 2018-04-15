# pylint: disable=too-few-public-methods
# pylint: disable=missing-docstring
import os


class MostRecentFile:
    # This class creates an iterator over the most recent tanczos file.

    def __init__(self, directory):
        #Handles empty directry
        if not os.listdir(directory):
            self.max = 0
            self.current = 1
            return
        self.current = 1
        self.sorted_directory = sorted(os.listdir(directory))
        self.latest_file_name = self.sorted_directory[len(self.sorted_directory) - 1]
        self.latest_file = open(directory + '/' + self.latest_file_name, 'r')
        self.latest_file_contents = self.latest_file.readlines()
        self.max = len(self.latest_file_contents) - 1

    def __iter__(self):
        return self

    # Implementation of the iteraters next methodd
    # Note: The return value is a list with the attributes in a Tanczos file as string entries
    def __next__(self):
        if self.current <= self.max:
            attribute_list = self.latest_file_contents[self.current].split(',')
            formatted_attribute_list = ([s.replace('"', '') for s in attribute_list])
            formatted_attribute_list = ([s.strip() for s in formatted_attribute_list])
            self.current += 1
            return formatted_attribute_list
        else:
            raise StopIteration
