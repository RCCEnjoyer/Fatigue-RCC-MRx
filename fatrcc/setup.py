"""Set up file of the library"""

from setuptools import setup, find_packages

DESCRIPTION = 'Tools for RCC-MRx fatigue calculation'
LONG_DESCRIPTION = ''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="fatrcc",
        version="0.0.1",
        author="Luis Angel Fernandez",
        author_email="<lafernandez@essbilbao.org>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages("fatrcc"),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'
        keywords=['RCC-MRx', 'fatigue'],
        zip_safe=False
)
