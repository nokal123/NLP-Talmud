# File: ScapeAlgo

import xlsxwriter
from nltk.tokenize import sent_tokenize

class ScrapeAlgo:
    file = open('../../PunctuatedText/Berakhot.txt', mode='r', encoding='utf8')
    file_txt = file.read()
    sentences = sent_tokenize(file_txt)
    workbook = xlsxwriter.Workbook('Berakhot.xlsx')
    worksheet = workbook.add_worksheet('daf_1')
    row = 0
    column = 0
    for sentence in sentences:
        if sentence.find(';') != -1:
            sentence = sentence.replace(';', '*;')
            splitSentence = sentence.split('*')
            for element in splitSentence:
                worksheet.write(row, column, element)
                row += 1
            continue
        elif sentence.find('\n') != -1:
            sentence = sentence.replace('\n', '*')
            splitSentence = sentence.split('*')
            for element in splitSentence:
                worksheet.write(row, column, element)
                row += 1
            continue
        worksheet.write(row, column, sentence)
        row += 1

    workbook.close()



