import csv
from datetime import datetime
import re

from src.utils.config import get_config
from src.utils.directory_utils import find_root

def read_comments(
        file: str, 
        limit: None | int=None
    ) -> list[str]:
    '''
    Purpose: 读取指定数量的原始评论
    Args:
        file: str: 原始评论文本
        limit: 需要读取的行数
    Return:
        list[str]: 拆开后的原始评论
    '''
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

def date_format_convert(
        origin_dt_str: str, 
        origin_fmt: str='%d %B %Y', 
        target_fmt: str='%Y-%m-%d'
    ) -> str:
    '''
    Purpose: 将指定样式的日期进行解析，返回指定样式的日期
    Args:
        origin_dt_str: 指定样式的日期
        origin_fmt: 原始日期样式
        target_fmt: 目标日期样式
    Return:
        str: 目标样式日期
    '''
    origin_dt = datetime.strptime(origin_dt_str, origin_fmt)
    return origin_dt.strftime(target_fmt)

def verify_comment(comment: str) -> bool:
    '''
    Purpose: 针定原始行进行校验，返回是否为有效行
    Args:
        comment: 原始行
    Return:
        bool: 是否为有效行
    '''
    score_pattern = r'^(10|[0-9])\/10' 
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

    # 必须有10分制打分
    valid_score = re.match(score_pattern, comment) is not None
    # 必须有评论
    valid_comment = len(comment[
        re.search(date_pattern, comment).end(0):
        re.search(end_pattern, comment).start(0)].replace(
        '\r','\n').replace('\n',''))>0
    return valid_score and valid_comment

def parse_comment(comment: str) -> None | tuple:
    '''
    Purpose: 解析原始评论内容，输出日期，评分和评论，如果
    Args:
        comment: 要解析的原始评论
    Return:
        None |
        Tuple(
            date: str: 指定格式日期
            score: int: 评分
            comment: str: 评论
        )
    '''
    score_pattern = r'^(10|[0-9])\/10' 
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

    score = re.search(score_pattern, comment).group(0).split('/')[0]
    date = date_format_convert(
        re.search(date_pattern, comment).group(0))
    cmt_start_index = re.search(date_pattern, comment).end(0)
    cmt_end_index = re.search(end_pattern, comment).start(0)
    comment_content = comment[cmt_start_index:
        cmt_end_index].replace('\r','\n').replace('\n','')
    return [date, score, comment_content]

def save_to_csv(file, comments):
    with open(file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "score", "comment"])
        
        for cmt in comments:
            if verify_comment(cmt):
                writer.writerow(parse_comment(cmt))

if __name__ == "__main__":
    txt_path = find_root() / get_config()['file_path']['raw_txt']
    csv_path = find_root() / get_config()['file_path']['cleaned_csv']
    save_to_csv(csv_path, read_comments(txt_path))