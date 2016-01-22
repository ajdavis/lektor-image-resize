from setuptools import setup

setup(
    name='lektor-image-resize',
    version='0.1',
    author=u'A. Jesse Jiryu Davis',
    author_email='jesse@emptysquare.net',
    license='MIT',
    py_modules=['lektor_image_resize'],
    url='https://github.com/ajdavis/lektor-image-resize',
    entry_points={
        'lektor.plugins': [
            'image-resize = lektor_image_resize:ImageResizePlugin',
        ]
    }
)
