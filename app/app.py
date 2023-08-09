from flask import Flask, render_template, request
import pandas as pd

# 模拟数据
data = {
    '特征编号': range(1, 101),
    '特征名称': [f'特征{i}' for i in range(1, 101)],
    '特征描述': [f'描述{i}' for i in range(1, 101)],
    '特征类型': ['类型A'] * 50 + ['类型B'] * 50
}
df = pd.DataFrame(data)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sort_column = request.args.get('sort_column', '特征编号')
    sort_order = request.args.get('sort_order', 'none')
    search_term = request.args.get('search', '')
    lock_search = request.args.get('lock_search', 'false') == 'true'
    page_number = int(request.args.get('page_number', '1'))

    # 处理搜索
    search_df = df if lock_search \
        else df[df['特征名称'].str.contains(
        search_term) | df['特征描述'].str.contains(
        search_term, regex=True)]

    # 处理排序
    sorted_df = search_df if sort_order == 'none' \
        else search_df.sort_values(
        by=sort_column, ascending=(sort_order == 'asc'))

    # 处理分页
    rows_per_page = 10
    start_index = (page_number - 1) * rows_per_page
    page_df = sorted_df.iloc[start_index: start_index + rows_per_page]

    return render_template('index.html', 
        df=page_df, sort_column=sort_column, 
        sort_order=sort_order, page_number=page_number, 
        lock_search=lock_search, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
