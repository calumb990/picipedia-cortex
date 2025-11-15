from kfp.dsl import pipeline
from components import preprocess, train, test

@pipeline
def classic_cnn_pipeline():
    preprocess()
    train()
    test()
