from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name='smc_py',
      version='0.1',
      description='Python based API to Stonesoft Security Management Center',
      url='http://github.com/gabstopper/smc-py',
      author='David LePage',
      author_email='dwlepage70@gmail.com',
      license='MIT',
      packages=['smc'],
      install_requires=[
          'requests',
          'ipaddress'
      ],
      include_package_data=True,
      zip_safe=False)