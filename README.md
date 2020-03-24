# Instantaneous Accuracy

This repository contains the code of the Instantaneous Accuracy metric. The metric was presented [here](http://openaccess.thecvf.com/content_ICCVW_2019/papers/HBU/Baptista-Rios_The_Instantaneous_Accuracy_a_Novel_Metric_for_the_Problem_of_ICCVW_2019_paper.pdf) and extended [here](https://ieeexplore.ieee.org/document/8939455).

<p align="center">
  <img src="./png/ia.png" alt="Online Evaluation for Online Action Detection" title="Instantaneous Accuracy" width="652" zoom="343" align="center" />
</p>


### Citation

If you find anything of this repository useful for your projects, please consider citing these works:

```bibtex
@inproceedings{Baptista2019iccvw,
  Title     = {The Instantaneous Accuracy: a Novel Metric for the Problem of Online Human Behaviour Recognition in Untrimmed Videos},
  Author    = {M. {Baptista-Ríos} and R. J. {López-Sastre} and F. {Caba-Heilbron} and J. {van Gemert}},
  Booktitle = {IEEE International Conference on Computer Vision Workshop (ICCVW)},
  pages     = {1282-1284},
  Year      = {2019},
  doi       = {10.1109/ICCVW.2019.00162},
  month     = {October}
}
```

```bibtex
@article{Baptista2019ieeea,
	author  = {M. {Baptista-Ríos} and R. J. {López-Sastre} and F. {Caba Heilbron} and J. C. {Van Gemert} and F. J. {Acevedo-Rodríguez} and S. {Maldonado-Bascón}},
	journal = {IEEE Access},
	title   = {Rethinking Online Action Detection in Untrimmed Videos: A Novel Online Evaluation Protocol},
	year	= {2020},
	volume  = {8},
	pages   = {5139-5146},
	doi     = {10.1109/ACCESS.2019.2961789},
	ISSN	= {2169-3536}
}
```

### How to obtain the performance of your model

You can find here how to use the code to obtain the performance of your model with this metric.

###### Ground Truth file

The code of the metric accepts ground truth files with `.json` format following the next structure (based on ActivityNet annotation):

```json
database: {
    video_test_0000006: {
        subset: "Test",
        duration: 67.11,
        annotations: [
            {
                label: "VoleyballSpiking",
                segment: [18.8, 57.3],
            }
        ],
    }
}
```

For Thumos'14 and TVSeries datasets, we have converted their original annotations to this format. We provide them. ActivityNet dataset annotations can be used directly.

###### Prediction file

The code of the metric accepts result files with `.json` format following the next structure:

```json
results: {
    video_test_0000006: [
        {
            segment: [22.3, 47.8]
            label: "VoleyballSpiking",
        }
    ]
}
```

###### Usage

*(The code has been tested using Python 3, specifically we have used python 3.7. Additionally, the python installation requires*`Numpy` *and* `Pickle` *packages.)*

Once you have the results of your method in the correct format, just run the  next command to obtain the performance:

```bash
python compute_instantaneous_accuracy.py -d Thumos14 -gt ../annotations/gt-thumos14.json -subset Test -pred ../data/c3d-thumos14.json -pkl ./c3d-thumos14-ia.pkl

```

You must provide the following options:

- `-d`: name of the dataset.
- `-gt`: path to a `.json` ground truth file with the correct structure.
- `-subset`: subset of the dataset which you are evaluating your method on.
- `-pred`: path to a `.json` prediction file with the correct structure.
- `-pkl`: path file where the `.pkl` generated file will be stored.

After running the command, the script will prompt the mean average Instantaneous Accuracy of your model. Additionally, the code generates a `.pkl` with extra information obtained during the computation of the metric.

### Results

We have conducted several experiments with some baselines and other available state-of-the-art model. You can find more information in the publications. However, as an example, we give the `.json` file with the results for Thumos'14 dataset of our 3D-CNN baseline based on the C3D network. 

We also show the results of the 3D-CNN baseline model for the all datasets in the next table:

|              | Thumos'14 | TVSeries | ActivityNet |
| ------------ | --------- | -------- | ----------- |
| **maIA (%)** | 58.10     | 28.95    | 27.38       |

