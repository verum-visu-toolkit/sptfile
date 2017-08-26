from distutils.core import setup

setup(
    name='vvsptfile',
    version='0.0.1',
    packages=['vvsptfile'],
    url='https://github.com/verum-visu-toolkit/sptfile',
    license='MIT',
    author='Jacob Zimmerman (jczimm)',
    author_email='jczimm@jczimm.com',
    description='File format for output from verum visu analyzer',
    install_requires=[
        'numpy==1.13.1'
    ]
)

