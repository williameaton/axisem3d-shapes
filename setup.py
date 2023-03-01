import setuptools


# Get long description as readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="axisem3Dshapes",
    version="1.0.3",
    author="W Eaton",
    author_email="weaton@princeton.edu",
    description="3D model shapes for AxiSEM-3D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williameaton/axisem3d-shapes/blob/main/README.md",
    project_urls={
        "Bug Tracker": "https://github.com/williameaton/axisem3d-shapes/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["axisem3dshapes"],
    python_requires=">=3.8",
)