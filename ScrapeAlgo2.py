# File: ScapeAlgo
import xlsxwriter
import io
from sample_readin_ner import tsv_to_tagged_corpus
from nltk.tokenize import sent_tokenize

class StringBuilder(object):

  def __init__(self):
    self._stringio = io.StringIO()

  def __str__(self):
    return self._stringio.getvalue()

  def append(self, *objects, sep=' ', end=''):
    print(*objects, sep=sep, end=end, file=self._stringio)

class ScrapeAlgo2:
    arrayOfTsv, _ = tsv_to_tagged_corpus('../../AlignedText/Berakhot.tsv')
    sb = StringBuilder()
    array_of_inside = arrayOfTsv
    last_punc = False
    for i in range(0, len(array_of_inside), 2):
        current_sentence = arrayOfTsv[i]
        for j in range(len(current_sentence)-1):
            word = arrayOfTsv[i][j][5]
            if word not in ['-']:
                if word not in ['!','?','.',':']:
                    sb.append(' ')
                    sb.append(word)
                    last_punc = False
                else:
                    last_punc = True
                    sb.append(word)

        # This is for edge case when a sentence spans two chunks in shtiensalz but not english
        if i+1 < len(arrayOfTsv) and arrayOfTsv[i+1] !=[] and not last_punc:
            last_punc_eng = arrayOfTsv[i+1][-1][0][-1]# trying to avoid ]? cases
            last_punc_heb = arrayOfTsv[i][-1][5][-1]
            if last_punc_heb not in ['!','?','.',':']:
                if last_punc_eng in ['!','?','.',':']:
                    if last_punc_heb not in [',', '-']:
                        sb.append(' ')
                        sb.append(arrayOfTsv[i][-1][5]) # for when its an entire word
                    sb.append(last_punc_eng)
                    continue
            whole_last_word = arrayOfTsv[i][-1][5]
            if whole_last_word not in ['!','?','.',':',',', '-']:
                sb.append(' ')
            if whole_last_word not in [',', '-']: # the ones above will still get printed and words will have a space before them
                sb.append(arrayOfTsv[i][-1][5])
    sentences = sent_tokenize(str(sb))
    workbook = xlsxwriter.Workbook('TsvBerakhot.xlsx')
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



