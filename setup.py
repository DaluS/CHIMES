from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='CHIMES',
    version='0.9',
    description='A tensor-based dynamical system library tinkering',
    license="MIT",
    long_description=long_description,
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Ecology, Economics, Dynamical systems, Physics, Simulation",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.11",
        # In which language most of the code is written ?
        "Natural Language :: English",
    ],
    author='Paul Valcke',
    author_email='pv229@georgetown.edu',
    url="https://environmentaljustice.georgetown.edu/#",
    packages=['CHIMES'],  # same as name
    install_requires=[ # external packages as dependencies
        'numpy',
        'scipy',
        'pyvis',
        'matplotlib',
        'pandas',
        'plotly',
        'pylatexenc',
        'dill',
        'ipywidgets',
        'itables',
        'redivis',
        'tabulate',
        'python-dotenv',
    ],  v
)
