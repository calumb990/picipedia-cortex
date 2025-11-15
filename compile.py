from pipelines import classic_cnn_pipeline

if __name__ == "__main__":
    from kfp.compiler import Compiler
    
    Compiler().compile(
        pipeline_func=classic_cnn_pipeline,
        package_path="pipelines/classic_cnn_pipeline.yaml"
    )
