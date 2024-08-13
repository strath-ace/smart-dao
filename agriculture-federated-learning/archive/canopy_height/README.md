# Canopy Height Test Model

Data comes from [META](https://registry.opendata.aws/dataforgood-fb-forests/) and [META2](https://research.facebook.com/blog/2023/4/every-tree-counts-large-scale-mapping-of-canopy-height-at-the-resolution-of-individual-trees/)

## Setup

This method uses google colab. Other methods may also work.

### Download and Prepare Data

1. Make sure AWS CLI is installed. [HERE](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

2. Setup venv. Currently tested with python 3.10
```bash
python -m venv venv

# Linux
venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r ./requirements.txt
```

3. Download data from AWS. This may take some time.
```bash
aws s3 --no-sign-request cp s3://dataforgood-fb-data/forests/v1/models/data.zip .
```

4. Unzip data.zip

5. Run cropper tool
```bash
python cropper.py
```

6. Zip `cropped` folder.

7. Place `cropped.zip` and `cropped_data.npy` in google drive with `cropped_data.npy`

8. You are now ready to run the model on google colab

### Run the model

Set the correct paths at begining of colab file

Open the .ipynb file and change url from `github.com` to `githubtocolab.com` 