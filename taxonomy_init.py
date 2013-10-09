"""
 Initialises the visualisation taxonomy database entries
 according to TVCG definitions
"""

from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem
import random



def random_reference():
    all_references = list(Reference.objects.all())
    return all_references[int((len(all_references) - 1) * random.random())]


def save_item(name, category):
    TaxonomyItem(name=name, category=category).save()


def taxonomy_init():
    rs = TaxonomyArea.objects.all()
    for x in rs:
        x.delete()

    rs = TaxonomyCategory.objects.all()
    for x in rs:
        x.delete()

    rs = TaxonomyItem.objects.all()
    for x in rs:
        x.delete()

    a = TaxonomyArea(name="Visualisation")
    a.save()

    r = TaxonomyCategory(name="History and Organizational Structures of or Within Vis", area=a)
    r.save()

    save_item(name="Taxonomies/Ontologies", category=r)
    save_item(name="Visual Analysis Models", category=r)
    save_item(name="Visualization Models", category=r)
    save_item(name="Mathematical Foundations for Visualization", category=r)

    nestedCategory = TaxonomyCategory(name="Knowledge Representation Models", parent=r)
    nestedCategory.save()

    save_item(name="Hypothesis Forming", category=nestedCategory)
    save_item(name="Hypothesis Testing, Visual Evidence", category=nestedCategory)
    save_item(name="Visual Knowledge Discovery", category=nestedCategory)

    r = TaxonomyCategory(name="Empirical Studies/Evaluation", area=a)
    r.save()
    save_item(name="Qualitative Studies", category=r)
    save_item(name="Quantitative Studies", category=r)
    save_item(name="Laboratory Studies", category=r)
    save_item(name="Field Studies", category=r)
    save_item(name="Usability Studies", category=r)
    save_item(name="Task and Requirements Analysis", category=r)
    save_item(name="Metrics and Benchmarks", category=r)

    r = TaxonomyCategory(name="Design", area=a)
    r.save()
    save_item(name="Decision-making", category=r)
    save_item(name="Understanding Human Factors", category=r)
    save_item(name="Design Studies", category=r)
    save_item(name="Aesthetics in Visualization", category=r)
    save_item(name="Visual Design", category=r)
    save_item(name="Human-computer Interaction", category=r)
    save_item(name="Interaction Design", category=r)

    nestedCategory = TaxonomyCategory(name="Perception and Cognition", parent=r)
    nestedCategory.save()

    save_item(name="Attention and Blindness", category=nestedCategory)
    save_item(name="Cognition Theory", category=nestedCategory)
    save_item(name="Cognitive and Perceptual Skill", category=nestedCategory)
    save_item(name="Color Perception", category=nestedCategory)
    save_item(name="Distributed Cognition", category=nestedCategory)
    save_item(name="Embodied/enactive Cognition", category=nestedCategory)
    save_item(name="Motion Perception", category=nestedCategory)
    save_item(name="Perception Theory", category=nestedCategory)
    save_item(name="Scene Perception", category=nestedCategory)
    save_item(name="Texture Perception", category=nestedCategory)


    r = TaxonomyCategory(name="Techniques", area=a)
    r.save()

    nestedCategory = TaxonomyCategory(name="Spatial Techniques", parent=r)
    nestedCategory.save()

    save_item(name="Extraction of Surfaces", category=nestedCategory)
    save_item(name="Geometry-based Techniques", category=nestedCategory)
    save_item(name="Irregular and Unstructured Grids", category=nestedCategory)
    save_item(name="PDE's and Visualization", category=nestedCategory)
    save_item(name="Scalar data techniques", category=nestedCategory)
    save_item(name="Pointer-based Data Techniques", category=nestedCategory)
    save_item(name="Vector Field Techniques", category=nestedCategory)
    save_item(name="Tensor Field Techniques", category=nestedCategory)
    save_item(name="Topology Based Techniques", category=nestedCategory)
    save_item(name="Volume Modeling", category=nestedCategory)
    save_item(name="Volume Rendering", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Non-Spatial Techniques", parent=r)
    nestedCategory.save()

    save_item(name="Dimensionality Reduction", category=nestedCategory)
    save_item(name="Graph/Network Techniques", category=nestedCategory)
    save_item(name="High-Dimensionality Techniques", category=nestedCategory)
    save_item(name="Pixel-oriented techniques", category=nestedCategory)
    save_item(name="Hierarchical Data Techniques", category=nestedCategory)
    save_item(name="Parallel Coordinates", category=nestedCategory)
    save_item(name="Statistical Graphics", category=nestedCategory)
    save_item(name="Text and Document Techniques", category=nestedCategory)
    save_item(name="Tabular Data Techniques", category=nestedCategory)
    save_item(name="Time Series Techniques", category=nestedCategory)
    save_item(name="Glyph Based Techniques", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Data Handling, Processing, and Analysis Techniques", parent=r)
    nestedCategory.save()

    save_item(name="Data Acquisition and Management", category=nestedCategory)
    save_item(name="Data Aggregation", category=nestedCategory)
    save_item(name="Data Clustering", category=nestedCategory)
    save_item(name="Data Registration", category=nestedCategory)
    save_item(name="Data Smoothing", category=nestedCategory)
    save_item(name="Data Cleaning", category=nestedCategory)
    save_item(name="Data Fusion and Integration", category=nestedCategory)
    save_item(name="Data Segmentation", category=nestedCategory)
    save_item(name="Data Transformation and Representation", category=nestedCategory)
    save_item(name="Feature Detection and Tracking", category=nestedCategory)
    save_item(name="Machine Learning", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Interaction Techniques", parent=r)
    nestedCategory.save()

    save_item(name="Coordinated and Multiple Views", category=nestedCategory)
    save_item(name="Focus and Context", category=nestedCategory)
    save_item(name="Data Editing", category=nestedCategory)
    save_item(name="Manipulation and Deformation", category=nestedCategory)
    save_item(name="User Interfaces", category=nestedCategory)
    save_item(name="Zooming and Navigation Techniques", category=nestedCategory)
    save_item(name="View Dependent Visualization", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Large Data Techniques", parent=r)
    nestedCategory.save()

    save_item(name="Compression Techniques", category=nestedCategory)
    save_item(name="Multi-field, Multi-modal, and Multi-variate Data Techniques", category=nestedCategory)
    save_item(name="Multi-resolution Techniques", category=nestedCategory)
    save_item(name="Petascale Techniques", category=nestedCategory)
    save_item(name="Streaming Techniques", category=nestedCategory)
    save_item(name="Time-varying Data Techniques", category=nestedCategory)
    save_item(name="Scalability Issues", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Techniques to Support Knowledge and Team Management", parent=r)
    nestedCategory.save()

    save_item(name="Knowledge and insight externalization and representation", category=nestedCategory)
    save_item(name="Collaborative and Distributed Visualization", category=nestedCategory)
    save_item(name="Presentation, Production and Dissemination", category=nestedCategory)

    # additional items
    save_item(name="Integrating Spatial and Non-Spatial Data", category=r)
    save_item(name="Uncertainty Visualization", category=r)
    save_item(name="Animation", category=r)
    save_item(name="Illustrative Rendering", category=r)


    r = TaxonomyCategory(name="Enabling or expanding technologies for \"interactive computing systems\"", area=a)
    r.save()

    nestedCategory = TaxonomyCategory(name="Display and Interaction Environments", parent=r)
    nestedCategory.save()

    save_item(name="Haptics for Visualization", category=nestedCategory)
    save_item(name="Immersive and Virtual Environments", category=nestedCategory)
    save_item(name="Large and High-Res Displays", category=nestedCategory)
    save_item(name="Multimodal Input Devices", category=nestedCategory)
    save_item(name="Stereo Displays", category=nestedCategory)
    save_item(name="Mobile and Ubiquitous Visualization", category=nestedCategory)
    save_item(name="Sonification", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Hardware", parent=r)
    nestedCategory.save()

    save_item(name="CPU and GPU Clusters", category=nestedCategory)
    save_item(name="Distributed Systems and Grid Environments", category=nestedCategory)
    save_item(name="GPUs and Multi-core Architectures", category=nestedCategory)
    save_item(name="Parallel Systems", category=nestedCategory)
    save_item(name="Special Purpose Hardware", category=nestedCategory)
    save_item(name="Volume Graphics Hardware", category=nestedCategory)

    nestedCategory = TaxonomyCategory(name="Software Toolkits", parent=r)
    nestedCategory.save()

    save_item(name="Visualization System and Toolkit Design", category=nestedCategory)
    save_item(name="Data Warehousing and Data Mining", category=nestedCategory)


    r = TaxonomyCategory(name="Applications", area=a)
    r.save()

    save_item(name="Bioinformatics", category=r)
    save_item(name="Biomedical and Medical", category=r)
    save_item(name="Flow Visualization", category=r)
    save_item(name="Geographic/Geospatial", category=r)
    save_item(name="Molecular", category=r)
    save_item(name="Multimedia", category=r)
    save_item(name="Software Visualization", category=r)
    save_item(name="Terrain Visualization", category=r)
    save_item(name="Personal Visualization and Visual Analytics", category=r)
    save_item(name="Casual Visualization", category=r)
    save_item(name="Earth, Space and Environmental Sciences", category=r)
    save_item(name="Vis in Education", category=r)
    save_item(name="Vis in Mathematics", category=r)
    save_item(name="Vis in Physical Sciences and Engineering", category=r)
    save_item(name="Vis in Social and Information Sciences", category=r)
    save_item(name="Vis in the Humanities", category=r)
    save_item(name="Emergency/Disaster Management", category=r)
    save_item(name="Intelligence Analysis", category=r)
    save_item(name="Network Security and Intrusion", category=r)
    save_item(name="Privacy and Security", category=r)
    save_item(name="Sensor Networks", category=r)
    save_item(name="Situational Awareness", category=r)
    save_item(name="Time-critical Applications", category=r)



if __name__ == "__main__":
    taxonomy_init()
