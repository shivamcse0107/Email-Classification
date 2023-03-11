create env 

```bash
conda create -n emailClassification python=3.8.13 -y
```

activate env
```bash
conda activate emailClassification
```

created a req file

install the req
```bash
pip install -r requirements.txt
```
```bash
git init
```
```bash
dvc init 
```
```bash
dvc add data_given/*.csv
```
```bash
git add .
```
```bash
git commit -m "first commit"
```

oneliner updates  for readme

```bash
git add . && git commit -m "update Readme.md"
```
```bash
git remote add origin https://github.com/shivamcse0107/Email-Classification.git
git branch -M main
git push origin main
```
