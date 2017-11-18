# Weathercock Nerf Gun Shield


##### Install OpenCV on MacOSX

```sh
brew tap homebrew/science
brew install pyenv-virtualenv pyenv-virtualenvwrapper opencv
sudo su
echo "/usr/local/lib/python2.7/site-packages/" > /Library/Python/2.7/site-packages/opencv.pth
echo "/usr/local/lib/python3.6/site-packages/" > /Library/Python/3.6/site-packages/opencv.pth
```


##### Install app dependencies on MacOSX

```sh
brew install cmake --with-python3
brew install boost-python --with-python3

pip install virtualenv virtualenvwrapper
mkvirtualenv cv -p python3
workon cv
pip install -r ../requirements.txt
```


##### Install app dependencies on Pi

- [OpenCV](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
- [Face Recognition library](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65)

```sh
workon cv
pip install -r ../requirements.txt
```

##### Encode portraits

```sh
python face_encoder.py /tmp/images encodings
```


##### Run

```sh
python main.py -h
python main.py --src_dir encodings --recognizer recognition --simulation  # Desktop
python main.py --src_dir encodings --recognizer detection --headless      # Pi
```
