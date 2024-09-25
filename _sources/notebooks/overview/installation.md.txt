## Installation

Step 1: install docker before using pyclmuapp

- [How to install Docker on Linux?](https://envdes.github.io/clmu-app/container/install_docker.html)
- [How to install Docker Desktop](https://www.docker.com/products/docker-desktop/)

**If you would like to you use the python package, then,**

Step 2: create a conda environment

---

```bash
$ conda create -n pyclmuapp python=3.9
$ conda activate pyclmuapp
$ conda install -c conda-forge numpy pandas xarray haversine netcdf4 nc-time-axis
```

Step 3: install using `pip`

---

```bash
$ pip install pyclmuapp
```

(optional) install from source

---

```bash
$ git clone https://github.com/envdes/pyclmuapp
$ cd pyclmuapp
$ python setup.py install
```