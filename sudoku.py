import numpy as np
import time
from matplotlib.pylab import *

def generateSudoku():
    attemptsIx = 0
    isValid = False
    while not isValid:
        attemptsIx += 1
#        print 'Generating Sudoku...'
        template = np.zeros((9,9))

        # loop over column
        for columnIx in np.arange(0,9):
            # loop over row
            for rowIx in np.arange(0,9):
                # set boolean for valid entry to False
                isValid = False
                # Find valid entry
                testArray = np.arange(1,10)
                np.random.shuffle(testArray)
                for testIx,testValue in enumerate(testArray):
#                    value = np.random.randint(1,10)
                    column = template[:,columnIx] # vertical slice
                    row = template[rowIx,:] # horizontal slice
                    # grab square
                    squareRowStart = rowIx - (rowIx % 3)
                    squareColumnStart = columnIx - (columnIx % 3)
                    square = template[squareRowStart:squareRowStart+3,squareColumnStart:squareColumnStart+3].reshape(-1)
                    if (testValue not in row) and (testValue not in column) and (testValue not in square):
                        template[rowIx,columnIx] = testValue
                        break
        if template.sum() == 405:
            isValid = True
    return template


def csvImportSudoku(path,fileName = ''):
    with open(path + fileName,'r') as f:
        rawData = f.read()

    data = []
    rawData = rawData.strip('\n').split('\n')
    for each in rawData:
        data.append(each.split(','))
        
    mySudoku = np.zeros((9,9))
    for rowIx,row in enumerate(data):
        for columnIx, value in enumerate(row):
            if value == '':
                mySudoku[rowIx,columnIx] = np.nan
            else:
                mySudoku[rowIx,columnIx] = value


    return mySudoku

def csvSaveSudoku(path,fileName = '',mySudoku=np.nan*np.ones((9,9))):
    with open(path + fileName,'w') as f:
        for rowIx, row in enumerate(mySudoku):
            for columnIx, value in enumerate(row):
                if np.isnan(value):
                    f.write('')
                else:
                    f.write('%i'%value)
                if not (columnIx == 8):
                    f.write(',')
            f.write('\n')




def printSudoku(mySudoku):
    row_ix = 1
    for row_ix in range(9):
        if row_ix == 0:
            print('+' + 3*'-----------' + '--+')
        elif (row_ix % 3) == 0 :
            print('|' + 3*'-----------|')

        printString = ''
        for column_ix in range(9):
            if column_ix == 0:
                printString += '| '
            elif (column_ix % 3) == 0:
                printString += ' | '
            if np.isnan(mySudoku[row_ix,column_ix]):
                printString += '   '
            else:
                printString += ' ' + str(int(mySudoku[row_ix,column_ix])) + ' '
        print(printString + ' |')
    print('+' + 3*'-----------' + '--+')

def calcSudokuErrors(mySudoku):
    errors = 0
    for row_ix in range(9):
        for column_ix in range(9):
            tempSudoku = mySudoku.copy()
            value = tempSudoku[row_ix,column_ix]
            if np.isnan(value):
                value = 0
            tempSudoku[row_ix,column_ix] = -1 # set number to -1 to avoid counting as error
            tempSudoku -= value
            # grab row
            row = tempSudoku[row_ix,:]
            # grab column
            column = tempSudoku[:,column_ix]
            # grab square
            squareRowStart = row_ix - (row_ix % 3)
            squareColumnStart = column_ix - (column_ix % 3)
            square = tempSudoku[squareRowStart:squareRowStart+3,squareColumnStart:squareColumnStart+3].reshape(-1)
            # calculate number of errors
            for r in row:
                if r == 0:
                    errors += 1
            for c in column:
                if c == 0:
                    errors += 1
            for s in square:
                if s == 0:
                    errors += 1
    return errors

def calcMissing(mySudoku):
    missing_values = 0
    for row_ix in range(9):
        for column_ix in range(9):
            value = mySudoku[row_ix,column_ix]
            if np.isnan(value):
                missing_values += 1

    return missing_values


def plotSudoku(mySudoku,savePath = None):
    fig = figure(figsize=(6,6))
    ax = fig.add_subplot(111,aspect = 'equal')

    # Add numbers #
    for column_ix in range(9):
        for row_ix in range(9):
            value = mySudoku[row_ix,column_ix]
            if not np.isnan(value):
                text(column_ix+0.47,row_ix+0.57,'%i'%int(value),horizontalalignment = 'center',verticalalignment='center',fontsize = 24)

    tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
    tick_params(axis='y',which='both',bottom='off',top='off',labelleft='off')

    line = np.arange(10)
    # Add grid #
    for column_ix in range(10):
        if column_ix % 3 == 0:
            plot(line,np.ones_like(line)*column_ix,'k-',linewidth = 2.5)
        else:
            plot(line,np.ones_like(line)*column_ix,'k-',linewidth = 0.5)

    for row_ix in range(10):
        if row_ix % 3 == 0:
            plot(np.ones_like(line)*row_ix,line,'k-',linewidth = 2.5)
        else:
            plot(np.ones_like(line)*row_ix,line,'k-',linewidth = 0.5)

    xlim(-0.02,9.01)
    ylim(9.01,-0.02)
    if savePath is not None:
        savefig(savePath + '.png')
        savefig(savePath + '.pdf')

def plotSudokuPossibleValues(mySudoku):
    fig = figure(figsize=(6,6))
    ax = fig.add_subplot(111,aspect = 'equal')

    possible_values_dict = listPossibleValues(mySudoku)

    # Add numbers #
    for column_ix in range(9):
        for row_ix in range(9):
            value = mySudoku[row_ix,column_ix]
            if not np.isnan(value):
                text(column_ix+0.5,row_ix+0.6,'%i'%int(value),horizontalalignment = 'center',verticalalignment='center',fontsize = 24)

    # add possible values #
    for rowColumn in possible_values_dict:
        row = rowColumn[0]
        column = rowColumn[1]
        possible_values = possible_values_dict[rowColumn]
        shiftx = 0.15
        shifty = 0.1
        for valueIx,value in enumerate(possible_values):
            if valueIx < 3:
                text(column+0.15+shiftx*valueIx,row+0.25,str(value),horizontalalignment = 'center',verticalalignment = 'center', fontsize = 10)
            elif valueIx >= 3 and valueIx < 6:
                text(column+0.15+shiftx*(valueIx-3),row+0.50,str(value),horizontalalignment = 'center',verticalalignment = 'center', fontsize = 10)
            else:
                text(column+0.15+shiftx*(valueIx-6),row+0.75,str(value),horizontalalignment = 'center',verticalalignment = 'center', fontsize = 10)

    tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
    tick_params(axis='y',which='both',bottom='off',top='off',labelleft='off')

    line = np.arange(10)
    # Add grid #
    for column_ix in range(10):
        if column_ix % 3 == 0:
            plot(line,np.ones_like(line)*column_ix,'k-',linewidth = 2.5)
        else:
            plot(line,np.ones_like(line)*column_ix,'k-',linewidth = 0.5)

    for row_ix in range(10):
        if row_ix % 3 == 0:
            plot(np.ones_like(line)*row_ix,line,'k-',linewidth = 2.5)
        else:
            plot(np.ones_like(line)*row_ix,line,'k-',linewidth = 0.5)

    xlim(-0.02,9.01)
    ylim(9.01,-0.02)


def testConflict(mySudoku,row,column,checkValue):
    '''Returns True is conflict exists'''
    copySudoku = mySudoku.copy()
    copySudoku[row,column] = np.nan # remove value if it exists from sudoku

    # check row
    for value in copySudoku[row,:]:
        if not np.isnan(value):
            if value == checkValue:
                return True

    # check column
    for value in copySudoku[:,column]:
        if not np.isnan(value):
            if value == checkValue:
                return True

    # check square
    squareRowStart = row - (row % 3)
    squareColumnStart = column - (column % 3)
    square = copySudoku[squareRowStart:squareRowStart+3,squareColumnStart:squareColumnStart+3].reshape(-1)
    for value in square:
        if not np.isnan(value):
            if value == checkValue:
                return True
    

    return False

def listCellPossibleValues(mySudoku,row,column):
    if np.isnan(mySudoku[row,column]):
        # determine possible values
        possible_values = list(np.arange(1,10))
        removed_values = []

        # check row
        for value in mySudoku[row,:]:
            if not np.isnan(value):
                possible_values.remove(value)
                removed_values.append(value)

        # check column
        for value in mySudoku[:,column]:
            if not np.isnan(value) and (value not in removed_values):
                possible_values.remove(value)
                removed_values.append(value)


        # check square
        squareRowStart = row - (row % 3)
        squareColumnStart = column - (column % 3)
        square = mySudoku[squareRowStart:squareRowStart+3,squareColumnStart:squareColumnStart+3].reshape(-1)
        for value in square:
            if not np.isnan(value) and (value not in removed_values):
                possible_values.remove(value)
    
    # If the sudoku value is not NaN, then it is already defined
    else:
        possible_values = [mySudoku[row,column]]

    return possible_values


def listPossibleValues(mySudoku):
    possible_values_dict = {}
    for row in range(9):
        for column in range(9):
            if np.isnan(mySudoku[row,column]):
                # determine possible values
                possible_values = list(np.arange(1,10))
                removed_values = []

                # check row
                for value in mySudoku[row,:]:
                    if not np.isnan(value):
                        possible_values.remove(value)
                        removed_values.append(value)

                # check column
                for value in mySudoku[:,column]:
                    if not np.isnan(value) and (value not in removed_values):
                        possible_values.remove(value)
                        removed_values.append(value)


                # check square
                squareRowStart = row - (row % 3)
                squareColumnStart = column - (column % 3)
                square = mySudoku[squareRowStart:squareRowStart+3,squareColumnStart:squareColumnStart+3].reshape(-1)
                for value in square:
                    if not np.isnan(value) and (value not in removed_values):
                        possible_values.remove(value)

#                print 'the possible values are: ',possible_values
                # add list to dict
                possible_values_dict[(row,column)] = possible_values
    return possible_values_dict

def simplifySudoku(mySudoku):
    testSudoku = mySudoku.copy() # grab copy
    ix = 0

    # add single possible values to Sudoku
    changed = True
    while changed:
        ix+=1
        testSudokuBackup = testSudoku.copy()
        possible_values_dict = listPossibleValues(testSudoku)
        for rowColumn in possible_values_dict:
            possible_values = possible_values_dict[rowColumn]
            if len(possible_values) == 1:
                # add value to Sudoku
                row = rowColumn[0]
                column = rowColumn[1]
                testSudoku[row,column] = possible_values[0]


        if ((testSudokuBackup == testSudoku) | (np.isnan(testSudokuBackup) & np.isnan(testSudoku))).all():
            changed = False
        print(ix)
    return testSudoku
    

def annealingSolve(mySudoku):
    # Create copy

    # if already solved, return
    if calcSudokuErrors(mySudoku) != 0:
        raise ValueError('Initial Sudoku Contains Contradition')
    if calcMissing(mySudoku) == 0:
            return mySudoku

    tempSudoku = mySudoku.copy()

    # Fill in Sudoku with random values
    for row_ix in range(9): 
        for column_ix in range(9):
            if np.isnan(mySudoku[row_ix,column_ix]):
                randomValue = (np.random.randint(9) + 1)
                tempSudoku[row_ix,column_ix] = randomValue

    # Start Simulated Annealing algorithm
    iter = 0

    start_time = time.time()

    # Annealing
    while True:
        random_row = np.random.randint(9)
        random_column = np.random.randint(9)
        if not np.isnan(mySudoku[random_row,random_column]):
            continue

        errors = calcSudokuErrors(tempSudoku)
        if errors == 0:
            solvedSudoku = tempSudoku.copy()
            break
        newSudoku = tempSudoku.copy()

        possibleValues = listCellPossibleValues(mySudoku,random_row,random_column)
        random_ix = np.random.randint(len(possibleValues))

        newSudoku[random_row,random_column] = possibleValues[random_ix]
        newErrors = calcSudokuErrors(newSudoku)
        if np.exp((errors - newErrors)/1) >= np.random.rand(1)[0]:
            tempSudoku = newSudoku

        if (iter % 100) == 0:
            printSudoku(tempSudoku)
            print('Errors:',errors)
            duration = time.time() - start_time
            print('Time Elapsed: %0.03f s'%duration)
        iter+=1
    printSudoku(solvedSudoku)
    duration = time.time() - start_time
    print('Total Time Required: %0.03f s'%duration)
    return solvedSudoku

# Generate Sudoku for Testing Purposes
#mySudoku = np.r_[
#        [
#        [5, 3, np.nan, np.nan, 7, np.nan, np.nan, np.nan, np.nan],
#        [6, np.nan, np.nan, 1, 9, 5, np.nan, np.nan, np.nan],
#        [np.nan, 9, 8, np.nan, np.nan, np.nan, np.nan, 6, np.nan],
#        [8, np.nan, np.nan, np.nan, 6, np.nan, np.nan, np.nan, 3],
#        [4, np.nan, np.nan, 8, np.nan, 3, np.nan, np.nan, 1],
#        [7, np.nan, np.nan, np.nan, 2, np.nan, np.nan, np.nan, 6],
#        [np.nan, 6, np.nan, np.nan, np.nan, np.nan, 2, 8, np.nan],
#        [np.nan, np.nan, np.nan, 4, 1, 9, np.nan, np.nan, 5],
#        [np.nan, np.nan, np.nan, np.nan, 8, np.nan, np.nan, 7, 9]
#        ]
#        ]

#mySudoku = np.r_[
#        [
#        [1, np.nan, np.nan, 5, np.nan, np.nan, 9, np.nan, 6],
#        [np.nan, np.nan, 5, np.nan, np.nan, np.nan, 2,np.nan,np.nan],
#        [4,np.nan,np.nan,8,np.nan,np.nan,7,5,np.nan],
#        [np.nan,np.nan,3,6,8,np.nan,4,np.nan,np.nan],
#        [np.nan,np.nan,1,np.nan,9,2,np.nan,np.nan,np.nan],
#        [np.nan,7,np.nan,np.nan,4,np.nan,np.nan,np.nan,8],
#        [np.nan,1,7,9,3,np.nan,np.nan,2,np.nan],
#        [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
#        [2,np.nan,np.nan,np.nan,6,4,1,3,np.nan]
#        ]
#        ]

mySudoku = np.r_[
        [
        [2, np.nan, np.nan, 3, np.nan, 7, 1, np.nan, np.nan],
        [np.nan, np.nan, np.nan, np.nan, 6, 2, 8,np.nan,np.nan],
        [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,6,5,2],
        [5,1,np.nan,np.nan,2,np.nan,np.nan,np.nan,6],
        [7,np.nan,np.nan,np.nan,4,np.nan,5,np.nan,1],
        [4,3,np.nan,np.nan,np.nan,5,np.nan,np.nan,8],
        [6,np.nan,3,np.nan,1,np.nan,np.nan,8,np.nan],
        [9,2,np.nan,np.nan,3,np.nan,np.nan,1,np.nan],
        [8,np.nan,1,np.nan,np.nan,np.nan,np.nan,6,np.nan]
        ]
        ]

if __name__ == '__main__':
    # generate Sudoku
    testSudoku = generateSudoku()
    errors = calcSudokuErrors(testSudoku)
    printSudoku(testSudoku)
    plotSudoku(testSudoku)
    print(errors)

    possible_values_dict = listPossibleValues(mySudoku)
    for key in possible_values_dict:
        print(key, possible_values_dict[key])


    plotSudoku(mySudoku)
    plotSudokuPossibleValues(mySudoku)
    print('starting to simplifiy')
    simpSudoku = simplifySudoku(mySudoku)
    print('plotting simplified sudoku')
    plotSudokuPossibleValues(simpSudoku)
    print('done')
    solvedSudoku = annealingSolve(simpSudoku)
    printSudoku(solvedSudoku)
    plotSudoku(solvedSudoku)

    show()
