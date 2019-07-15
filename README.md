<p align="center">
  <a href="https://github.com/ipudu/mda">
    <img alt="mda: Analysis tools for MD simulations" src="https://app.pudu.io/data/uploads/mda.png" width="50%" height="50%">
  </a>
</p>

# MDA: Analysis Tools for MD Simulations

![version](https://img.shields.io/pypi/v/mda.svg?style=flat-square&logo=visual-studio-code)
![python](https://img.shields.io/pypi/pyversions/mda.svg?style=flat-square&logo=python)
![license](https://img.shields.io/pypi/l/mda.svg?style=flat-square)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **MDA**.

```bash
pip install mda
```

## Usage

```python
import mda
```

## Feature Support

**MDA** can be used to calculate following properties:

- Inertia tensor (Acylindricity, Asphericity, Shape)
- Gyration tensor
- Radial distribution function
- Radius of gyration
- Solvent accessible surface area
- and more

**MDA** can be used to download scientific papers:

```bash
# using link:
mda https://pubs.rsc.org/en/content/articlehtml/2017/cp/c7cp01602f

# using DOI number:
mda 10.1039/C7CP01602F 
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)