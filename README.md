# Pi experiments

### Programs


##### LCD screen


Pin connections as defined on [rototron](https://www.rototron.info/lcd-display-tutorial-for-raspberry-pi/).

```sh
make exec PROGRAM=lcd
```


##### Stepper motor

For Nema-17 12V 350mA: red-grey-_blank_-yellow-green

```sh
make exec PROGRAM=motor
```

### Random


##### SD card images


Card to image:

```sh
sudo dd if=/dev/rdisk2 of=raspberry-opencv.dmg bs=1m
```

Image to card:

```sh
diskutil unmountDisk /dev/disk2
sudo newfs_msdos -F 16 /dev/disk2
sudo dd if=raspberry-opencv.dmg of=/dev/rdisk2 bs=1m
```

Notes:
- Usage of raw disk _rdisk2_ and block size of 1M to improve copy speed dramatically (10-15x)
- Use _Ctrl+T_ to show progress in the console


##### USB microphone


Check microphone connection:

```sh
lsusb
amixer
```

Record:

```sh
arecord -D plughw:1 --duration=10 -f cd -vv ~/rectest.wav
```

Play:

```sh
aplay ~/rectest.wav
# or
scp -r pi@pi2.local:~/rectest.wav .
open rectest.wav
```


# Camera


Take a picture and check it:

```sh
raspistill -o ~/cam.jpg
scp -r pi@pi2.local:~/cam.jpg .
open cam.jpg
```
