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
            input_file - file to clean
            output_file - output location and name
        '''
        self.input_file = input_file
        self.output_file = output_file

    def flag_cell(self, cell, index):
        '''
        Flag cell in there are an odd number of quotes used (quote spans multiple "cells")
        Input:
            cell - current cell (according to first pass parser)
            index - index of cell in row
        Returns:
            True if the cell needs to be considered for a multi-cell long quote
        '''
        count = cell.count('"')

        if ((count % 2 == 0) or 
            ( (index == 0) and (count == 1) )): # edge case of multiple line row with only single quote in first cell of current line
            return False

        else:
            return True

    def logic(self, line):
        '''
        Take care of beggining and ending quotes and parse line
        Inputs:
            line - current line in file
        Returns:
            out_arr - each cell in a list
            flag_arr - indices of cells with odd number of quotes
            start_char - starting character of line (if applicable)
            end_char - ending character(s) of line (if applicable)
        '''
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
        '''
        Create new file line if any of the cells get flagged
        Inputs:
            out_arr - each cell in a list
            flag_arr - indices of cells with odd number of quotes
            start_char - starting character of line (if applicable)
            end_char - ending character(s) of line (if applicable)
        Returns:
            Full line to add to output
        '''
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
        '''
        Open files and run above logic
        '''
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
    input_file = 'data/test.csv'
    output_file = 'data/test_new.csv'
    c_q = CSV_Quotes(input_file, output_file)
    c_q.main()
