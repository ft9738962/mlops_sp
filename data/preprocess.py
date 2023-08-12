import csv
import re

def read_comments(file, limit=None):
    with open(file, "r") as f:
        comments = []
        comment = ''
        for line in f.readlines():
            if '<>?' not in line:
                comment += line
            else:
                comment += line[:line.index('<>?')]
                comments.append(comment)
                comment = line[line.index('<>?') + 3:]
                if limit and len(comments) >= limit:
                    break
        return comments

def date_format(origin_dt):
    pass

def clean_comments_to_csv(comments):
    score_pattern = r'^(10|[0-9])\/10' # 开始必须有10分制打分
    date_pattern = re.compile("""
        ([1-9]|0[1-9]|[12][0-9]|3[01])  # day (1-31)
        \s                               # space
        (January|February|March|April
        |May|June|July|August|September
        |October|November|December)      # month
        \s                               # space
        (\d{4})                          # year
    """, re.VERBOSE)
    end_pattern = r'\d+ out of \d+'

    with open("comments.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "comment", "score"])
        
        for comment in comments:
            if not re.match(score_pattern, comment):
                continue
            else:
                score = re.search(score_pattern, comment).group(0).split('/')[0]
                date = re.search(date_pattern, comment).group(0)
                cmt_start_index = re.search(date_pattern, comment).end(0)
                cmt_end_index = re.search(end_pattern, comment).start(0)
                comment_content = comment[cmt_start_index:
                    cmt_end_index].replace('\r\n','\n').replace('\n','')
                writer.writerow([date, comment_content, score])

if __name__ == "__main__":
    comments = read_comments('corpus.txt')
    clean_comments_to_csv(comments)