<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
<style>
@media screen and (max-width: 768px) {
    body { padding-top: 0px; }
} body { padding-top: 70px; }
</style>

<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
  <div class="container">
    <ul class="nav navbar-nav">
      <li><a href="#introduction">Introduction</a></li>
      <li><a href="#download">Download</a></li>
      <li><a href="#statistics">Statistics</a></li>
      <li><a href="#considerations">Usage Considerations</a></li>
      <li><a href="#work">Work</a></li>
      <li><a href="#acknowledgements">Acknowledgements</a></li>
    </ul>
  </div>
</nav>

<div class="container">

<a name="introduction"></a>

PASCAL Regions Dataset
======================

This dataset is a set of additional annotations for PASCAL VOC 2010. It goes beyond both object detection bounding boxes and object segmentation by providing whole scene semantic segmentation. This boils down to a per-pixel class label.

Below are some example segmentations from the dataset. The statistics section below has a full list of labels.

<a name="download"></a>

Download
--------

<div class="well row">
<div class="col-md-6">

### Training and Validation Set

The following download contains *only* the annotations for the training/validation set and a text file (`labels.txt`) containing the integer-to-name mapping.

<a class="btn btn-primary btn-lg" href="trainval.tar.gz">trainval.tar.gz (30.7 MB)</a>

Original images for the dataset can be downloaded from the PASCAL VOC 2010 website: <a href="http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2010/">http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2010/</a>

</div>
<div class="col-md-6">

### Testing Set

PASCAL VOC 2010 released their testing set, and this set was also annotated. Since we are not hosting a challenge the testing set will be made available soon.

<a class="btn btn-primary btn-lg" disabled="disabled" href="#">test.tar.gz (coming soon)</a>

Original images for the test set can be downloaded from the PASCAL VOC 2010 website: <a href="http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2010/#testdata">http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2010/#testdata</a>

</div>
</div>

[back to top](#)

<a name="work"></a>

Statistics
----------

Since the dataset is an annotation of PASCAL VOC 2010 it shares the same set numbers. `trainval` contains 10,103 images while `test` contains 10,417 images.

[back to top](#)

<a name="considerations"></a>

Usage Considerations
-------

The classes are not drawn from a fixed pool. Instead labelers are free to both select or type in what they believe to be the appropriate class and to determine what the appropriate object granularity is. This leads to some interesting ambiguities and post-processing. 

[back to top](#)

Work
----

### The Role of Context for Object Detection and Semantic Segmentation in the Wild

Roozbeh Mottaghi, Xianjie Chen, Xiaobai Liu, Nam-Gyu Cho, Seong-Whan Lee, Sanja Fidler, Raquel Urtasun, Alan Yuille (CVPR 2014)

- [mottaghi_et_al_cvpr14.pdf](mottaghi_et_al_cvpr14.pdf)

[back to top](#)

<a name="acknowledgements"></a>

Acknowledgements
----------------

- [Korea University](http://www.korea.ac.kr/mbshome/mbs/university/index.do)
- [University of California, Los Angeles](http://www.ucla.edu/)
    - [Department of Statistics](http://statistics.ucla.edu/)

[back to top](#)

<a name="statistics"></a>

</div>
