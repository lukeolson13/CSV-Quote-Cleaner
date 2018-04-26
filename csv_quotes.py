#!/usr/bin/env python
'''
Correct use of quotes in CSV
'''

__author__ = 'Luke Olson'

class CSV_Quotes():
    '''
    Clean CSV with quotes
    '''

    def __init__(self, input_file, output_file):
        '''
        Initializer
        Inputs:
            input_file, output_file
        '''
        self.input_file = input_file
        self.output_file = output_file

    def flag_cell(self, cell, index):
        count = cell.count('"')

        if ((count % 2 == 0) or 
            ( (index == 0) and (count == 1) )):
            return False

        else:
            return True

    def logic(self, line):
        start_index = 0
        start_char = ''
        end_index = None
        end_char = ''

        if line[0] == '"':
            start_index = 1
            start_char = '"'

        if line[-4:] == '","\n':
            end_index = -1
            end_char = '\n'
        elif line[-1:] == '"':
            end_index = -1
            end_char = '"'
        elif line[-2:] == '"\n':
            end_index = -2
            end_char = '"\n'
        
        out_arr = []
        flag_arr = []
        for index, cell in enumerate(line[start_index:end_index].split('","')):
            if self.flag_cell(cell, index):
                flag_arr.append(index)

            out_arr.append(cell.replace('"', '""'))

        return out_arr, flag_arr, start_char, end_char

    def get_new_line(self, out_arr, flag_arr, start_char, end_char):

        norm = True
        new_line = ''
        last_used = 0

        last_cell_index = len(out_arr) - 1
        if last_cell_index != flag_arr[len(flag_arr) - 1]:
            flag_arr.append(last_cell_index + 1)

        for index in flag_arr:
            if norm:
                new_line += '","'.join(out_arr[last_used:index])
                if last_used != index:
                    new_line += '","'
                last_used = index

            else:
                new_line += '"",""'.join(out_arr[last_used:index + 1])
                if last_used != index:
                    new_line += '","'
                last_used = index + 1

            norm = not(norm)

        new_line = new_line[:-3]
        return start_char + new_line + end_char

    def main(self):
        with open(self.input_file, 'r', encoding='ISO-8859-1') as f_in:
            with open(self.output_file, 'w') as f_out:
                for line in f_in:
                    out_arr, flag_arr, start_char, end_char = self.logic(line)
                    if flag_arr == []:
                        new_line = start_char + '","'.join(out_arr) + end_char
                    else:
                        new_line = self.get_new_line(out_arr, flag_arr, 
                                                     start_char, end_char)

                    f_out.write(new_line)

if __name__ == '__main__':
    c_q = CSV_Quotes('data/test.csv', 'data/test_new.csv')
    c_q.main()
