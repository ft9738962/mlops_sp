from pathlib import Path
import typing as t
import warnings

import mlflow
import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor


warnings.filterwarnings('ignore')

if __name__ == '__main__':
    class CusModel(mlflow.pyfunc.PythonModel):
        def load_context(self, context):
            from autogluon.tabular import TabularPredictor as tbl
            self.predictor = tbl.load(
                context.artifacts["model_path"])

        def predict(self, context, model_input):
            return self.predictor.predict(model_input)

    tracking_uri = Path('C:\\Users\\qiuchen5\\Music\\pprojects\\mlops_sp\\mlruns')
    mlflow.set_tracking_uri(f'file://{str(tracking_uri)}')
    experiment_id = mlflow.create_experiment('test')

    with mlflow.start_run(
        run_name = 'test_run',
        experiment_id=experiment_id,
        tags={"version": "v1", "priority": "P1"},
        description="test",
    ) as run:
        data_url = 'https://raw.githubusercontent.com/mli/ag-docs/main/knot_theory/'
        train_data = TabularDataset(f'{data_url}train.csv')
        label = 'signature'
        pred_pth = str(tracking_uri / run.info.experiment_id / run.info.run_id / 'artifacts' / 'autogluon_model')
        predictor = TabularPredictor(
            label=label,
            path=pred_pth).fit(train_data)
        
        artifacts = {
            'model_path': pred_pth
        }
        mlflow.pyfunc.log_model(
            artifact_path='autogluon_model', 
            python_model=CusModel(),
            artifacts = artifacts)

        test_data = TabularDataset(f'{data_url}test.csv')
        predictor = mlflow.pyfunc.load_model(pred_pth)
        y_pred = predictor.predict(test_data.drop(columns=[label]))
        print(y_pred.head())
