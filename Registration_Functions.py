import numpy as np
import SimpleITK as sitk
from stl import Mesh
import matplotlib.pyplot as plt

# Import DICOM series
def import_dicom_series(directory):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directory)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    return image

# Resample Image with Scaling Factor
def resample_image_with_scaling(image, scaling_factor):
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    new_spacing = [ospc * scaling_factor for ospc in original_spacing]
    new_size = [int(round(osz / scaling_factor)) for osz in original_size]

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())
    resampler.SetTransform(sitk.Transform())
    resampler.SetDefaultPixelValue(image.GetPixelIDValue())

    resampled_image = resampler.Execute(image)
    return resampled_image

# Image Registration with SimpleITK
def register_images(fixed_image, moving_image):
    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                          moving_image,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)

    registration_method = sitk.ImageRegistrationMethod()
    registration_method.SetMetricAsMeanSquares()
    registration_method.SetInterpolator(sitk.sitkLinear)
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    
    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                  sitk.Cast(moving_image, sitk.sitkFloat32))

    return final_transform

# Save the Transform
def save_transform(transform, file_path):
    sitk.WriteTransform(transform, file_path)

# Apply the Transform to a .STL File
def apply_transform_to_stl(transform_file, stl_file, output_stl_file):
    transform = sitk.ReadTransform(transform_file)
    stl_mesh = Mesh.from_file(stl_file)

    # Create an empty list to store transformed points
    transformed_points = []

    # Iterate through each point in the mesh and apply the transform
    for point in stl_mesh.points:
        # Transform each vertex of the triangle
        p1 = transform.TransformPoint(point[0:3].tolist())
        p2 = transform.TransformPoint(point[3:6].tolist())
        p3 = transform.TransformPoint(point[6:9].tolist())
        transformed_points.append(p1 + p2 + p3)

    # Flatten the list of transformed points
    transformed_points = np.array(transformed_points).reshape(-1, 9)

    # Create a new mesh with the transformed points
    transformed_mesh = Mesh(np.zeros(transformed_points.shape[0], dtype=Mesh.dtype))
    transformed_mesh.points = transformed_points
    transformed_mesh.save(output_stl_file)

# Visualization of Registration
def show_registration(fixed_image, moving_image, transform):
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed_image)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(0)
    resampler.SetTransform(transform)
    moved_image = resampler.Execute(moving_image)

    fixed_array = sitk.GetArrayFromImage(fixed_image)
    moving_array = sitk.GetArrayFromImage(moving_image)
    moved_array = sitk.GetArrayFromImage(moved_image)

    slice_index = fixed_array.shape[0] // 2

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(fixed_array[slice_index, :, :], cmap='gray')
    axes[0].set_title('Fixed Image')
    axes[1].imshow(moving_array[slice_index, :, :], cmap='gray')
    axes[1].set_title('Moving Image')
    axes[2].imshow(moved_array[slice_index, :, :], cmap='gray')
    axes[2].set_title('Registered Image')
    plt.show()

# Write Transformed Image to .nrrd File
def write_transformed_image_to_nrrd(transformed_image, output_file_path):
    sitk.WriteImage(transformed_image, output_file_path)

def apple_transform_to_img(transform, img):
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(img)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(0)
    resampler.SetTransform(transform)
    transformed_image = resampler.Execute(img)
    return transformed_image