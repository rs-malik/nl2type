# NL2Type
JavaScript function type inference using Natural Language Information. Based on the ICSE '19 paper: [NL2Type](https://software-lab.org/publications/icse2019_NL2Type.pdf "NL2Type")

To reproduce the results presented in the paper, refer to [this project](https://github.com/sola-da/NL2Type).

### Requirements
python 3.6

pip

### Installation
Install some node dependencies for JsDoc parsing
```
sudo apt-get install -y nodejs
npm install -g jsdoc
```
Install python dependencies
```
pip install -r requirements.txt
```
###Running
To run:
```
python3 nl2type.py input_file_path output_file_path
```