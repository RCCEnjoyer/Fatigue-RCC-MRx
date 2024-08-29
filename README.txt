Version 0.0.1 (10-03-2023)

	- All previous files were merged into a single module that is able to calculate the number of cycles for fatigue failure in two scenarios: Elastic analysis and elastoplastic analysis (ANSYS files given)
	- First version of the tutorial
	- Welding factor included as a correction of the maximum number of cycles and not as an increase of the load (linear and elastoplastic)
	- It is possible to extract the complete file for both the stress range and the strain range
	
Version 0.0.2 (14-03-2023):

	- Warning alerts included if the temperature, or stress are out of the available data for k_eps, k_vol. Also, warning alerts if the proposed temperature is out of range for the available data of the fatigue curves
	- Warning alert included if the strain range along the cycle is too low (negligible fatigue) or too high
	- Updated output text: Gives number of lines (nodes), the maximum stress range (elastic), the maximum strain range (with components when estimated), the number of cycles and the location of the maximum
	- New function added: It is possible to extract the file with the tensor range + von mises equivalent

Version 0.0.3 (01-04-2024): 

	- Routines always report a strain/stress range. If values are outside of RCC tables, closest values are used
	- Weld and fatigue reduction coefficients are now argumetns of the functions (Jf and f)
	- Interpolation corrected for strain-cycles curve (logaritmic)
	- Tutorial updated (Jf and f explanation included)
	
	
# TODO: Include eps2?
# TODO: Include spline interpolation option for deformation curve as a function of the temperature
# TODO: Do for other materials (data_sheets and generalize materials folder)
# TODO: External elastic modulus
# TODO: Include usage factor
# TODO: Get usage factor for a given point
# TODO: Read units of the tensor files
# TODO: Remove influence of number of columns of the input file (node number)