from pathlib import Path
import typing as t
import warnings

from autogluon.multimodal import MultiModalPredictor as mmp

from src.utils.config import get_config
from src.utils.directory_utils import find_root

def load_model_predictor(model_path:Path):
    '''
    Purpose: 加载预测器
    '''
    return mmp.load(model_path)