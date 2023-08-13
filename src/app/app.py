from flask import Flask, render_template, request
import pandas as pd

# mock data
data = {
    'feature_code': range(1, 101),
    'feature_name': [f'feature_{i}' for i in range(1, 101)],
    'feature_desc': [f'desc_{i}' for i in range(1, 101)],
    'feature_type': ['int'] * 50 + ['str'] * 50
}

# shuffle data to test sort function
df = pd.DataFrame(data).sample(frac=1).reset_index(drop=True)

app = Flask(__name__)

# initiaize status dictionary
sort_status_dict, icon_status_dict = \
    {col: 'origin' for col in df.columns}, \
    {col: '' for col in df.columns}

@app.route('/', methods=['GET', 'POST'])
def index():
    sort_column = request.args.get('sort_column', None)
    sort_order_change = request.args.get('sort_order_change', None)
    search_term = request.args.get('search', '')
    lock_search = request.args.get('lock_search', 'false') == 'true'
    page_number = request.args.get('page_number', '1', 'int')
    print(page_number)

    # search
    search_df = df if lock_search \
        else df[df['feature_name'].str.contains(
        search_term) | df['feature_desc'].str.contains(
        search_term, regex=True)]
    
    def rotate_order(order_state):
        '''
        Purpose: rotate following 3 types of order status: 
                origin => ascend => desend => origin
        '''
        print(f'order_state: {order_state}')
        match order_state:
            case ('origin','sort'):
                return 'asc'
            case ('asc', 'sort'):
                return 'desc'
            case ('desc', 'sort'):
                return 'origin'
            case ('origin','icon'):
                return '-up'
            case ('asc', 'icon'):
                return '-down'
            case ('desc', 'icon'):
                return ''

    def update_status_dict(sort_dict, icon_dict, sort_column):
        input_status = sort_dict[sort_column]
        sort_dict[sort_column] = \
            rotate_order((input_status, 'sort'))
        icon_dict[sort_column] = \
            rotate_order((input_status, 'icon'))


    if sort_column and sort_order_change:
        update_status_dict(
            sort_status_dict, 
            icon_status_dict, 
            sort_column
            )

    # handle sort based on status dict
    sort_cols, ascend_cols = [], []
    for k, v in sort_status_dict.items():
        if v != 'origin':
            sort_cols.append(k) 
            ascend_cols.append(1 if v=='asc' else 0)
    
    sorted_df = search_df.sort_values(
        by=sort_cols, ascending=ascend_cols) if len(sort_cols) \
        else search_df

    # 处理分页
    rows_per_page = 10
    start_index = (page_number - 1) * rows_per_page
    page_df = sorted_df.iloc[start_index: start_index + rows_per_page]
    print(start_index)

    return render_template('index.html', 
        df=page_df, sort_column=sort_column, 
        page_number=page_number, lock_search=lock_search, 
        search_term=search_term,
        # sort_status_dict=sort_status_dict,
        icon_status_dict=icon_status_dict)

if __name__ == '__main__':
    app.run(debug=True)
