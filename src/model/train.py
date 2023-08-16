from pathlib import Path
import typing as t
import warnings

from autogluon.multimodal import MultiModalPredictor as mmp
import pandas as pd
from sklearn.model_selection import train_test_split as tts

from src.utils.config import get_config
from src.utils.directory_utils import find_root

warnings.filterwarnings('ignore')

def prepare_train_test_data(
        file: Path,
        seed_num: int,
        label: str='score'
    ):
    '''
    '''
    raw_df = pd.read_csv(file)
    return tts(raw_df[['comment', label]], test_size=0.2, 
        random_state=seed_num, stratify=raw_df[label])

def train_model(
        train_data: pd.DataFrame, 
        model_path: Path,
        label: str='score',
        verbosity: int=2,
        *kwargs):
    predictor = mmp(
        label=label, 
        eval_metric='acc', 
        path=model_path
    )
    predictor.set_verbosity(verbosity)
    predictor.fit(train_data, *kwargs)
    return predictor

def eval_model(predictor: mmp, test_data: pd.DataFrame = None):
    if test_data is None:
        test_data = test_data
    test_score = predictor.evaluate(
        test_data)
    print(test_score)

if __name__ == '__main__':
    config = get_config()
    csv_file = find_root() / config['file_path']['cleaned_csv']
    model_path = find_root() / config['file_path']['model_path']
    seed_num = config['model']['seed_num']

    train_data, test_data = prepare_train_test_data(
        csv_file, seed_num, 'score'
    )
    print(type(train_data))
    predictor = train_model(train_data, model_path)
    eval_model(predictor, test_data)