
"""
 Initialises the visualisation taxonomy database entries
 according to TVCG definitions
"""

from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem, Reference
import random

lorem = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.".split()

generate_fake_detail = True

entry_likelihood = 0.2
reference_likelihood = 0.05

def random_reference():
	all_references = list(Reference.objects.all())
	return all_references[int((len(all_references)-1) * random.random())]

def gen_detail_html():
	if random.random() < entry_likelihood:
		i = 0
		output_str = ""
		while i < len(lorem):
			output_str += lorem[i] + ' '
			if random.random() < reference_likelihood:
				output_str += '{{' + random_reference().entry_id + '}} '
			i += 1 
		return output_str	
	else:
		return "" 

def save_item(name, category):
	detail_html = gen_detail_html() if generate_fake_detail else ""
	TaxonomyItem(name=name, category=category, detail_html=detail_html).save()

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

	r = TaxonomyCategory(name="Theory of Visual Analysis", area=a)
	r.save()

	save_item(name="Taxonomies", category=r)
	save_item(name="Visual Analysis Models", category=r)
	save_item(name="Visualization Models", category=r)

	r = TaxonomyCategory(name="Visual Analysis and Knowledge Discovery", area=a)
	r.save()
	save_item(name="Hypothesis Forming", category=r)
	save_item(name="Hypothesis Testing, Visual Evidence", category=r)
	save_item(name="Knowledge Externalization", category=r)
	save_item(name="Visual Knowledge Discovery", category=r)
	save_item(name="Visual Knowledge Representation", category=r)

	r = TaxonomyCategory(name="Data Handling, Processing and Analysis", area=a)
	r.save()
	save_item(name="Data Acquisition and Management", category=r)
	save_item(name="Data Aggregation", category=r)
	save_item(name="Data Cleaning", category=r)
	save_item(name="Data Clustering", category=r)
	save_item(name="Data Fusion and Integration", category=r)
	save_item(name="Data Registration", category=r)
	save_item(name="Data Segmentation", category=r)
	save_item(name="Data Smoothing", category=r)
	save_item(name="Data Transformation and Representation", category=r)
	save_item(name="Feature Detection and Tracking", category=r)
	save_item(name="Machine Learning", category=r)

	r = TaxonomyCategory(name="Non-Spatial Data and Techniques", area=a)
	r.save()
	save_item(name="Dimensionality Reduction", category=r)
	save_item(name="Graph/Network Data", category=r)
	save_item(name="Hierarchy Data", category=r)
	save_item(name="High-Dimensional Data", category=r)
	save_item(name="Parallel Coordinates", category=r)
	save_item(name="Pixel-oriented Techniques", category=r)
	save_item(name="Statistical Graphics", category=r)
	save_item(name="Tabular Data", category=r)
	save_item(name="Text and Document Data", category=r)
	save_item(name="Time Series Data", category=r)

	r = TaxonomyCategory(name="Spatial Data and Techniques", area=a)
	r.save()
	save_item(name="Extraction of Surface (Isosurfaces, Material Boundaries)", category=r)
	save_item(name="Geometry-based Techniques", category=r)
	save_item(name="Irregular and Unstructured Grids", category=r)
	save_item(name="PDE's and Visualization", category=r)
	save_item(name="Point-based Data", category=r)
	save_item(name="Scalar Field Data", category=r)
	save_item(name="Tensor Field Data", category=r)
	save_item(name="Topology-bsaed Techniques", category=r)
	save_item(name="Vector Field Data", category=r)
	save_item(name="Volume Modeling", category=r)
	save_item(name="Volume Rendering", category=r)

	r = TaxonomyCategory(name="Interaction Techniques", area=a)
	r.save()
	save_item(name="Coordinated and Multiple Views", category=r)
	save_item(name="Data Editing", category=r)
	save_item(name="Focus + Context Techniques", category=r)
	save_item(name="Human Factors", category=r)
	save_item(name="Human-Computer Interaction", category=r)
	save_item(name="Interaction Design", category=r)
	save_item(name="Manipulation and Deformation", category=r)
	save_item(name="User Interfaces", category=r)
	save_item(name="Zooming and Navigation Techniques", category=r)

	r = TaxonomyCategory(name="Display and Interaction Technology", area=a)
	r.save()
	save_item(name="Haptics for Visualization", category=r)
	save_item(name="Immersive and Virtual Environments", category=r)
	save_item(name="Large and High-res Displays", category=r)
	save_item(name="Multimodel Input Devices", category=r)
	save_item(name="Stereo Displays", category=r)

	r = TaxonomyCategory(name="Evaluation", area=a)
	r.save()
	save_item(name="Field Studies", category=r)
	save_item(name="Laboratory Studies", category=r)
	save_item(name="Metrics and Benchmarks", category=r)
	save_item(name="Qualitative Evaluation", category=r)
	save_item(name="Quantitative Evaluation", category=r)
	save_item(name="Task and Requirements Analaysis", category=r)
	save_item(name="Usability Studies", category=r)

	r = TaxonomyCategory(name="Perception and Cognition", area=a)
	r.save()
	save_item(name="Attention and Blindness", category=r)
	save_item(name="Cognition Theory", category=r)
	save_item(name="Cognitive and Perceptual Skill", category=r)
	save_item(name="Color Perception", category=r)
	save_item(name="Distributed Cognition", category=r)
	save_item(name="Embodied / Enactive Cognition", category=r)
	save_item(name="Motion Perception", category=r)
	save_item(name="Perception Theory", category=r)
	save_item(name="Perception Cognition", category=r)
	save_item(name="Scene Perception", category=r)
	save_item(name="Texture Perception", category=r)

	r = TaxonomyCategory(name="Hardware Acceleration", area=a)
	r.save()
	save_item(name="CPU and GPU Clusters", category=r)
	save_item(name="Distributed Systems and Grid Environments", category=r)
	save_item(name="GPUs and Multi-core Architectures", category=r)
	save_item(name="Parallel Systems", category=r)
	save_item(name="Special Purpose Hardware", category=r)
	save_item(name="Volume Graphics Hardware", category=r)

	r = TaxonomyCategory(name="Large Data Vis", area=a)
	r.save()
	save_item(name="Compression Techniques", category=r)
	save_item(name="Multi-field, Multi-modal and Multi-variate Data", category=r)
	save_item(name="Multidimensional Data", category=r)
	save_item(name="Multiresolution Techniques", category=r)
	save_item(name="Petascale Techniques", category=r)
	save_item(name="Streaming Data", category=r)
	save_item(name="Time-varying Data", category=r)

	r = TaxonomyCategory(name="General Topics and Techniques", area=a)
	r.save()
	save_item(name="Aesthetics in Visualization", category=r)
	save_item(name="Animation", category=r)
	save_item(name="Collaborative and Distributed Visualization", category=r)
	save_item(name="Design Studies", category=r)
	save_item(name="Glyph-based Techniques", category=r)
	save_item(name="Illustrative Rendering", category=r)
	save_item(name="Integrating Spatial and Non-spatial Data Visualization", category=r)
	save_item(name="Mathematical Foundations for Visualization", category=r)
	save_item(name="Mobile and Ubiquitous Visualization", category=r)
	save_item(name="Presentation, Production and Dissemination", category=r)
	save_item(name="Scalability Issues", category=r)
	save_item(name="Sonification", category=r)
	save_item(name="Uncertainty Visualization", category=r)
	save_item(name="View-dependent Visualization", category=r)
	save_item(name="Visual Design", category=r)
	save_item(name="Visualization System and Toolkit Design", category=r)

	r = TaxonomyCategory(name="Applications", area=a)
	r.save()
	save_item(name="Bioinformatics Visualization", category=r)
	save_item(name="Biomedical and Medical Visualization", category=r)
	save_item(name="Business and Finance Visualization", category=r)
	save_item(name="Data Warehousing, Data Visualization and Data Mining", category=r)
	save_item(name="Flow Visualization", category=r)
	save_item(name="Geographic/Geospatial Visualization", category=r)
	save_item(name="Molecular Visualization", category=r)
	save_item(name="Multimedia (Image/Video/Music) Visualization", category=r)
	save_item(name="Software Visualization", category=r)
	save_item(name="Terrain Visualization", category=r)
	save_item(name="Visualization for the Masses", category=r)
	save_item(name="Visualization in Earth, Space and Environmental Sciences", category=r)
	save_item(name="Visualization in Education", category=r)
	save_item(name="Visualization in Mathematics", category=r)
	save_item(name="Visualization in Physical Sciences and Engineering", category=r)
	save_item(name="Visualization in Social and Information Sciences ", category=r)
	save_item(name="Visualization in the Humanities", category=r)

	r = TaxonomyCategory(name="Visual Analytics Applications", area=a)
	r.save()
	save_item(name="Emergency/Disaster Management", category=r)
	save_item(name="Intelligence Analysis", category=r)
	save_item(name="Network Security and Intrusion", category=r)
	save_item(name="Privacy and Security", category=r)
	save_item(name="Sensor Networks", category=r)
	save_item(name="Situational Awareness", category=r)
	save_item(name="Time Critical Applications", category=r)

if __name__ == "__main__":
	taxonomy_init()
