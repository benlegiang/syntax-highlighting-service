from src.utils.SHModelUtils import *

def start():
    pythonModel = SHModel(PYTHON3_LANG_NAME, "PythonModel")
    res1 = fine_tune(pythonModel)
    res2 = predict(pythonModel)

    print(res1)
    print(res2)

def predict(model):
    # tokenIds from LToks for prediction
    model.setup_for_prediction()
    p = model.predict([1, 25, 30, 44, 55])
    pa = model.predict([55, 44, 30, 25])

    return [p, pa]

def fine_tune(model):

    # [tokenIds from LToks], [hCodes]
    # IMPORTANT: Both must be of the same length
    model.setup_for_finetuning()
    model.finetune_on([1, 25, 30, 44, 55], [0, 0, 4, 0, 3])
    loss = model.finetune_on([55, 44, 30, 25], [0, 0, 4, 8])

    return loss
    
if __name__ == '__main__':
    start()