## Installation

Step 1: install docker before using pyclmuapp

If you are the Linux OS user, we recommend you to use `udocker` and then you are no needed to install Docker. 

- [Install Docker on Linux](https://docs.docker.com/desktop/setup/install/linux/)
- [Install Docker on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Install Docker on Windows](https://docs.docker.com/desktop/setup/install/windows-install/)


Step 2: create a conda environment

---

```bash
$ conda create -n pyclmuapp python=3.9
$ conda activate pyclmuapp
$ conda install -c conda-forge numpy pandas xarray haversine netcdf4 nc-time-axis
```

Step 3: install from source

---

```bash
$ git clone https://github.com/envdes/pyclmuapp
$ cd pyclmuapp
$ python setup.py install
```

test 
---

```bash
$ git clone https://github.com/envdes/pyclmuapp
$ cd pyclmuapp/example_data
$ python test.py
```

(Optional) install using `pip`

---

```bash
$ pip install pyclmuapp
```