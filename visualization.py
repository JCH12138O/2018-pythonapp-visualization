# this project for visualization. User enters keywords and select movie names and return charts by specific requirement.
# first chart creates a line chart to compare average rating score from different age groups.
# second chart creates a bar chart to show gender and age distribution of a specific movie.
# Please put the data subfolder under current working direction.Charts are saved under cwd
# Please enter 'data' as the name of subfolder
import pandas as pd
import matplotlib.pyplot as plt
import os, os.path

TITLE = 'Title'
UNDER18 = 'VotesU18'
FROM1829 = 'Votes1829'
FROM3044 = 'Votes3044'
ABOVE44 = 'Votes45A'
GENRE = 'Genre1'
UNDER18F = 'CVotesU18F'
UNDER18M = 'CVotesU18M'
FROM1829F = 'CVotes1829F'
FROM1829M = 'CVotes1829M'
FROM3044F = 'CVotes3044F'
FROM3044M = 'CVotes3044M'
ABOVE44F = 'CVotes45AF'
ABOVE44M = 'CVotes45AM'


# read IMDB file
def fileDoc(filepath):
    file = pd.read_csv(filepath)
    return file


# query in the existing film csv to get list of film which contains the keyword
def pickMovieWithKeyword(keyword,filepath):
    file = fileDoc(filepath)
    file.index = file[TITLE].str.upper()
    aa = list(file[TITLE])  # make a list of all film titles with all title uppercase as index for better query
    titleList = []
    for i in aa:
        titleList.append([i.upper(), i])  # make a list of film titles in uppercase
    lst = [titleList[i][1] for i in range(len(titleList)) if titleList[i][0].__contains__(keyword.upper())]  # find all films contains keywords
    return lst  # return a list of films found


# check if there is any movie under the keyword. select movie if there are more than 1 movie that contains keyword
def nameSelected(numberOfMovie,filepath):
    nameOfMovieSelected = []
    print('Select ' + str(numberOfMovie) + ' movies')
    for i in range(numberOfMovie):  # for each movie in the number wanted
        count = 0
        while count == 0:   # check if user want single movie chart or a comparison of several movie
            print()
            keyword = input('Enter Movie Keyword:')
            movieWithKeyword = pickMovieWithKeyword(keyword, filepath)
            if len(movieWithKeyword) != 0:  # if there is at least 1 movie contain the keyword
                if len(movieWithKeyword) == 1:  # if there is only 1 movie contain the keyword
                    print('Movie #', i+1, ': ', movieWithKeyword[0])
                    nameOfMovieSelected.append(movieWithKeyword[0])
                    count = count + 1
                else:  # if there are more than 1 movie contain the keyword
                    print('Which if the following movies would you like to pick (enter number )')
                    length = len(movieWithKeyword)
                    for x in range(length):
                        print('     ', x+1, movieWithKeyword[x])
                    count = count + 1
                    numberSelected = eval(input('enter a number: '))
                    nameOfMovieSelected.append(movieWithKeyword[numberSelected-1])
                    print('Movie #', i+1, ': ', movieWithKeyword[numberSelected-1])
            # if there is no movie that contains keyword
            else:
                print('Please try again')
    return nameOfMovieSelected  # return a list of all movie needed


# create plot 1 of 'Ratings by age groups'
def plot1(listOfName,filepath):
    file = fileDoc(filepath)
    lst = []
    for x in listOfName:  # search for the movie we wanted and find the values of 4 columns we needed and combined title with gener
        lst.append([list(file[file[TITLE] == x][TITLE]+'('+file[file[TITLE] == x][GENRE] + ')'), list(file[file[TITLE] == x][UNDER18]), list(file[file[TITLE] == x][FROM1829]), list(file[file[TITLE] == x][FROM3044]), list(file[file[TITLE] == x][ABOVE44])])
    for i in range(len(lst)):  # make the plot
        plt.plot(['<18', '18-29', '30-44', '>44'], lst[i][1:], '-o', label=lst[i][0])
        plt.annotate(lst[i][0][0], ('<18', lst[i][1][0]))  # make the label
    plt.grid(linestyle='-.')
    plt.xlabel('Age range')
    plt.ylabel('Rating')
    plt.title('Ratings by age group')
    plt.savefig('plot1.jpg')  # save as plot1.jpg under current working direc
    plt.close()


# create plot 2 of 'Distribution of gender and age groups'
def plot2(filepath):
    print('-'*100)
    print('Plot2: Percentage of raters within gender-age. Select a movie:')
    count = 0
    # try again if no movie founded
    while count == 0:
        keyword = input("Enter movie keyword:")
        movieWithKeyword = pickMovieWithKeyword(keyword, filepath)
        if len(movieWithKeyword) != 0:  # if there is at least 1 movie contains keyword
            if len(movieWithKeyword) == 1:  # if there is only 1 movie contains kw
                a = movieWithKeyword
                print('Movie: ', end='')
                print("'", a[0], "'")
            elif len(movieWithKeyword) > 1:  # if there are >1 movies contains kw
                print('Which if the following movies would you like to pick (enter number )')
                length = len(movieWithKeyword)
                for x in range(length):
                    print('     ', x + 1, movieWithKeyword[x])
                count = count + 1
                numberSelected = eval(input('enter a number: '))  # select movie
                a = [movieWithKeyword[numberSelected - 1]]
                print('Movie: ', end='')
                print("'", a[0], "'")
            count += 1
        elif len(movieWithKeyword) == 0:  # if no movie contains kw, try again
            print('Please try again')
    file = fileDoc(filepath)
    lst = []
    # find all columns of age and gender from csv file, create a list of voter number in 8 demographic groups
    lst.append([list(file[file[TITLE] == a[0]][UNDER18F]), list(file[file[TITLE] == a[0]][FROM1829F]),
                list(file[file[TITLE] == a[0]][FROM3044F]), list(file[file[TITLE] == a[0]][ABOVE44F]),
                list(file[file[TITLE] == a[0]][UNDER18M]), list(file[file[TITLE] == a[0]][FROM1829M]),
                list(file[file[TITLE] == a[0]][FROM3044M]), list(file[file[TITLE] == a[0]][ABOVE44M])])
    sum = 0
    lst = lst[0]
    for i in range(len(lst)):
        sum = sum + lst[i][0]  # count for the sum of total number of voters in 8 groups
    lst2 = []
    for i in range(len(lst)):
        lst2.append(round(lst[i][0]/sum*100, 1))  # make a list contains percentage of total number
    lstName = ['<18f', '18-29f', '30-44f', '>44f', '<18m', '18-29m', '30-44m', '>44m']
    for i in range(0, 4):
        female =plt.bar(lstName[i], lst2[i], label='female', fc='purple')
    for i in range(4, 8):
        male = plt.bar(lstName[i], lst2[i], label='male', fc='g')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('% of raters')
    plt.title('Percentage of raters within gender-age group for '+"'"+a[0]+"'")
    for x, y in zip(lstName, lst2):
        plt.text(x, y, str(y)+'%', ha='center', va='bottom')
    plt.savefig('plot2.jpg')
    plt.close()

def main():
    folder = input('Please enter the name of subfolder with the data file:')
    print('Plot1:  ratings by age group')
    numberOfMovie = eval(input('How many of the 118 movies would you like to pick (enter number)'))
    folderpath = os.path.join(os.getcwd(), folder)
    filepath = os.path.join(folderpath, 'IMDB.csv')
    listOfName = nameSelected(numberOfMovie, filepath)
    plot1(listOfName, filepath)
    plot2(filepath)

main()
