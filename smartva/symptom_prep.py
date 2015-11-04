import csv
import os
import re

from smartva.data_prep import DataPrep
from smartva.loggers import status_logger
from smartva.utils import status_notifier
from smartva.utils.conversion_utils import additional_headers_and_values

FILENAME_TEMPLATE = '{:s}-symptom.csv'


class SymptomPrep(DataPrep):
    """Prepare symptom data for tariff processing.

    The main goal of this step is to complete the conversion of symptom answers to binary data.

    Notes:
        Change sex from female = 2, male = 1 to female = 1, male = 0
        Unknown sex will default to 0 so it contributes nothing to the tariff score as calculated in the
        tariff 2.0 algorithm.

        For all indicators for different questions about injuries (road traffic, fall, fires) We only want
        to give a VA a 1 (yes) response for that question if the injury occurred within 30 days of death
        (i.e. s163<=30) Otherwise, we could have people who responded that they were in a car accident 20
        years prior to death be assigned to road traffic deaths.
    """

    def __init__(self, input_file, output_dir, short_form):
        super(SymptomPrep, self).__init__(input_file, output_dir, short_form)
        self.data_module = None

    def _init_data_module(self):
        self.AGE_GROUP = self.data_module.AGE_GROUP

    def run(self):
        super(SymptomPrep, self).run()
        status_logger.info('{} :: Processing symptom data'.format(self.AGE_GROUP.capitalize()))
        status_notifier.update({'progress': 1})

        with open(self.input_file_path, 'rb') as fi:
            reader = csv.DictReader(fi)
            matrix = [row for row in reader]

        status_notifier.update({'sub_progress': (0, len(matrix))})

        headers = reader.fieldnames

        additional_data = {}
        additional_data.update(self.data_module.GENERATED_VARS_DATA)
        additional_headers, additional_values = additional_headers_and_values(headers, additional_data.items())

        headers.extend(additional_headers)
        self.rename_headers(headers, self.data_module.VAR_CONVERSION_MAP)

        keep_list = [header for header in headers if re.match(self.data_module.KEEP_PATTERN, header)]
        drop_list = self.data_module.DROP_LIST

        headers = sorted([header for header in headers if header in keep_list and header not in drop_list],
                         key=lambda t: (t != 'sid', t[1].isdigit(), t))

        for index, row in enumerate(matrix):
            if self.want_abort:
                return False

            status_notifier.update({'sub_progress': (index,)})

            self.expand_row(row, dict(zip(additional_headers, additional_values)))
            self.rename_vars(row, self.data_module.VAR_CONVERSION_MAP)

            self.copy_variables(row, self.data_module.COPY_VARS)

            # Compute age quartiles.
            self.process_progressive_value_data(row, self.data_module.AGE_QUARTILE_BINARY_VARS.items())

            self.process_cutoff_data(row, self.data_module.DURATION_CUTOFF_DATA.items())

            self.process_injury_data(row, self.data_module.INJURY_VARS.items())

            # Dichotomize!
            self.process_binary_vars(row, self.data_module.BINARY_CONVERSION_MAP.items())

            # Ensure all binary variables actually ARE 0 or 1:
            self.post_process_binary_variables(row, self.data_module.BINARY_VARS)

        status_notifier.update({'sub_progress': None})

        self.write_output_file(headers, matrix)

        return True

    @staticmethod
    def copy_variables(row, copy_variables_map):
        """Copy data from one variable to another.

        Copy Variables Map Format:
            'read variable': 'write variable'

        Args:
            row (dict): Row of VA data.
            copy_variables_map (dict): Read and write answer variables.
        """
        for read_header, write_header in copy_variables_map.items():
            row[write_header] = row[read_header]

    @staticmethod
    def process_cutoff_data(row, cutoff_data_map):
        """Change read variable to 1/0 if value is greater/less or equal to cutoff, respectively.

        Cutoff data map Format:
            variable: cutoff
        Args:
            row (dict): Row of VA data.
            cutoff_data_map (dict): Cutoff data in specified format.
        """
        for read_header, cutoff_data in cutoff_data_map:
            try:
                row[read_header] = int(float(row[read_header]) >= cutoff_data)
            except ValueError:
                row[read_header] = 0

    @staticmethod
    def process_injury_data(row, injury_variable_map):
        """Cut off injuries occurring more than 30 days from death, set variable to 0.

        Injury variable map Format:
            'read variable': [list of injury variables]

        Args:
            row (dict): Row of VA data.
            injury_variable_map (dict): Map of injury variables in specified format.
        """
        for read_data, injury_list in injury_variable_map:
            read_header, cutoff = read_data
            if float(row[read_header]) > cutoff:
                for injury in injury_list:
                    row[injury] = 0

    @staticmethod
    def post_process_binary_variables(row, binary_variables):
        """Ensure all binary variables are actually 1 or 0.

        Binary variables Format:
            [list of binary variables]

        Args:
            row (dict): Row of VA data.
            binary_variables (list): Binary variable list.
        """
        for read_header in binary_variables:
            try:
                value = int(row[read_header])
            except ValueError:
                value = 0
            row[read_header] = int(value == 1)

    def write_output_file(self, headers, matrix):
        """Write intermediate symptom data.

        Args:
            headers (list): List of headers to be retained.
            matrix (list): Matrix of VA answers.
        """
        with open(os.path.join(self.output_dir, FILENAME_TEMPLATE.format(self.AGE_GROUP)), 'wb') as fo:
            writer = csv.DictWriter(fo, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(matrix)
