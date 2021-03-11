


## Install 

In Ubuntu

```
apt-get install libmagic1
pip3 install python-magic
pylint ./find_sig.py
```


## Usage

```
echo -n lseek > crypty.sig
./find_sig /usr/bin crypty.sig
```