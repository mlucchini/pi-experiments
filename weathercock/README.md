# Weathercock Nerf Gun Shield


##### Install OpenCV on MacOSX

```sh
brew tap homebrew/science
brew install pyenv-virtualenv pyenv-virtualenvwrapper opencv
sudo su
echo "/usr/local/lib/python2.7/site-packages/" > /Library/Python/2.7/site-packages/opencv.pth
echo "/usr/local/lib/python3.6/site-packages/" > /Library/Python/3.6/site-packages/opencv.pth
```


##### Install app dependencies

```sh
brew install cmake --with-python3
brew install boost-python --with-python3

pip install virtualenv virtualenvwrapper
mkvirtualenv cv -p python3
workon cv
pip install -r requirements.txt
```


##### Encode portraits

```sh
python face_encoder.py /tmp/images encodings
```


##### Run

```sh
python main.py encodings
# or
python main.py encodings --simulation
```
