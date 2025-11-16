from kfp.dsl import pipeline
from components import preprocess, train, test

@pipeline
def classic_cnn_pipeline():
    preprocess_task = preprocess()
    train_task = train(train_loader=preprocess_task.outputs["train_loader"])
    test(test_loader=preprocess_task.outputs["test_loader"], model_state=train_task.outputs["model_state"])
