
import csv
def save_state_csv(state, csv_file, delimiter=","):
    """
    Save the given state in CSV file format
    :param state: The state to record
    :param csv_file_writer: The file writer
    :return: None
    """
    csv_file_writer = csv.writer(csv_file, delimiter=delimiter)
    csv_file_writer.writerow(state.get_value())
