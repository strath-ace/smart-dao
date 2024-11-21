# Centralised Crop Type Detection with UNet

These are used to compare the loss ratios, number of crop classes and the softmax thresholding values and the associated F1-scores from the output. 
- `centralised_model.ipynb` will train the model. 
- `centralised_model_testset.ipynb` will test the model and produce metrics.


## Setup for `centralised_model.ipynb`
Firstly you need to change the number of crop classes used, the loss ratio used and the thresholding values used throughout the document. Secondly, there are 3 occurances of this code. These can be uncommented and the file name changed if you would like to save the data in google colab.
```python
# Can add a save line in for google colab here:
# !cp model_save/* drive/MyDrive/bla_bla_bla/.
```


## Setup for `centralised_model_testset.ipynb`

This code block needs edited by the user. Either decide to run on something like google colab and use the first `!cp` commands or have the model saved in the working directory of where this code is running. Then don't forget to remove the Exception line of code.
```python
raise Exception("Need to add model loader from wherever it is saved")
# The code should look something like this if coming from google drive on google colab
"""
!cp drive/MyDrive/bla_bla_bla/model_temp model_save/.
!cp drive/MyDrive/bla_bla_bla/learning_temp.json model_save/.
"""
# Or you can just have it in your working directory
model.load_state_dict(torch.load("model_save/model_temp"))
```