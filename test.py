from typing import List
import fileinput
import csv
import os


class Catalog:
    """The Catalog class is used to work with the telephone directory.
    
    The main application is working with the telephone directory using the console.
    
    Attributes
    ----------
    current_dir: str
        path of the current directory
    catalog_file: str
        path of the catalog file
    catalog_fields: List[str]
        fields of catalog file
    
    Methods
    -------
    __check_file_exists()
        checks if catalog file exists.
        returns bool

    __fill_fields()
        fill fields with input data

    _read_records()
        output records page by page from catalog file

    _edit_record()
        edits the record selected by id

    _add_record()
        add new record to the catalog file

    _search_by_id()
        allows to search a record by id

    _search_by_fields()
        allows to search a record with certain data

    main()
        main part of program.
    """    
    def __init__(self):
        self.current_dir: str = os.getcwd()
        self.catalog_file: str = os.path.join(self.current_dir, 'catalog.csv')
        self.catalog_fields: List[str] = [
            'Last name', 'First name',
            'Patronymic', 'Organization name',
            'Work phone', 'Personal phone (cell)'
        ]


    def __check_file_exists(self) -> bool:
        """Checks if catalog file exists and returns
        info if file exists in the directory or not 

        Returns
        -------
            bool
        """        
        return os.path.exists(self.catalog_file)


    def __fill_fields(self) -> List[str]:
        """Fill fields with input data

        Returns:
            List[str]: List of input data
        """        
        filled_fields = []
        for field in self.catalog_fields:
            filled_fields.append(input(f'{field}: ')) # input data for every field
        return filled_fields


    def _read_records(self) -> None:
        """Output records page by page
        from catalog file
        """        
        with open(self.catalog_file, 'r') as file:
            page: int = 1
            while True:
                read_choose: str = input('\nEnter any key to continue. \nEnter 0 to exit.\n')
                if read_choose == '0': # stop reading
                    break
                else:
                    print(f'Records {page}..{page+9}')
                    print(f'ID - {" - ".join(self.catalog_fields)}\n')

                    for i in range(10): # outputs 10 records by page
                        line: str = file.readline().strip()
                        if not line:
                            break
                        print(f'{page + i} - {line}')
                    page += 10

                if not line:
                    break


    def _edit_record(self, id: str, record: List[str]) -> None:
        """Edits the record selected by id

         Parameters
        ----------
        id: str
            id of record
        record: List[str]
            list of filled data
        """
        with fileinput.FileInput(self.catalog_file,
                                inplace = True,
                                backup ='.bak') as file:
            line_number: int = 1
            for line in file:
                # stdout (print) used for file editing
                if id == str(line_number): # edit found record
                    print(f'{";".join(record)}', end ='\n')
                else:
                    print(line, end ='')
                line_number += 1


    def _add_record(self, record: str) -> None:
        """Add new record to the catalog file
        
        Parameters
        ----------
        record: str
            data for new record
        """
        with open(self.catalog_file, 'a+', newline='') as file:
            csvwriter = csv.writer(file, delimiter=';')
            # write record to the end of file
            csvwriter.writerow(record)


    def _search_by_id(self, id: str) -> None:
        """Allows to search a record by id

        Parameters
        ----------
        id: str
            ID of record 

        """
        record_id: int = 1
        with open(self.catalog_file, 'r') as file:
            while True:
                record: str = file.readline().strip()
                if not record:
                    break
                if id == str(record_id):
                    print(f'ID - {" - ".join(self.catalog_fields)}\n')
                    print(f'{record_id} - {record}')
                    break
                record_id += 1


    def _search_by_fields(self, search_fields: List[str]) -> List[list]:
        """Allows to search a record with certain data

        Parameters
        ----------
        search_fields: List[str]
            list of filled fields used for search a record 
        
        Returns
        -------
            List[list]
                list of lists with id and record 
        """
        with open(self.catalog_file, 'r') as file:
            results: list = []
            record_id: int = 1
            while True:
                record: str = file.readline().strip()
                if not record:
                    break

                splited_record: List[str] = record.split(';')
                check_list: List[bool] = []

                for i in range(6): # check all 6 fields
                    # compares search data with all fields of record
                    # empty '' search data is ignored
                    if search_fields[i] == '' or search_fields[i] in splited_record[i].lower():
                        check_list.append(True)
                    else:
                        check_list.append(False)
                        break
                if all(check_list): # if all search fields compared are true
                    results.append([record_id, record])
                record_id += 1

        return results


    def main(self):
        """Main part of program.
        runs a program in while cycle and
        accepts commands from user.
        """
        # check if file exist, else create it
        if not self.__check_file_exists():
            with open(self.catalog_file, 'a+', newline='') as file: 
                csvwriter = csv.writer(file, delimiter=';')

        # run main part of program
        while True:
            print('==========')
            choose: str = input('Choose an option: \n1 - Read records.  ' \
                                '2 - Add new record.  3 - Edit record.  ' \
                                '4 - Find record.  0 - exit.\n')
            print('==========')

            if choose == '0': # exit
                print('Goodbye!')
                break

            elif choose == '1': # read records
                if self.__check_file_exists():
                    self._read_records()
                else:
                    print("File is empty. Write data into file before reading.")

            elif choose == '2': # add new record
                new_record: List[str] = self.__fill_fields()
                self._add_record(new_record)

            elif choose == '3': # edit record in file
                record_id: str = input('Write an ID of record:\n')
                if record_id.isdigit(): # if record is a number
                    new_record: List[str] = self.__fill_fields()
                    self._edit_record(record_id, new_record)
                else:
                    print('\nWrite a number!')

            elif choose == '4': # search records by id or input data
                if self.__check_file_exists():
                    searching_id: str = input(f'ID (Leave empty to search with fields):\n')
                    if searching_id:
                        self._search_by_id(searching_id)

                    else:
                        print('Fill in the fields to search records. \nLeave the field empty so as not to use it.\n')

                        search_fields: List[str] = self.__fill_fields()
                        # check if at least 1 field was filled
                        if not all(x == '' for x in search_fields):
                            results: List[list] = self._search_by_fields(search_fields)

                            # output results
                            print(f'\nFind {len(results)} records')
                            print(f'ID - {" - ".join(self.catalog_fields)}\n')
                            for res in results:
                                print(f'{res[0]} - {res[1]}')
                        else:
                            print('Fill at least one field!')
                else:
                    print("File is empty. Write data into file before reading.")


if __name__ == '__main__':
    catalog = Catalog()
    catalog.main()
