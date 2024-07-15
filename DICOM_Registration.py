import Registration_Functions as RF
import SimpleITK as sitk

stack1 = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA/ST_001_L"
stack2 = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA/ST_002_L"

image1 = RF.import_dicom_series(stack1)
image2 = RF.import_dicom_series(stack2)
print("Image Data Imported")

img1 = RF.resample_image_with_scaling(image1, 3.0)
img2 = RF.resample_image_with_scaling(image2, 3.0)
print("Images Resampled")

transformation = RF.register_images(img1, img2)
print("Images Registered")
#RF.show_registration(img1, img2, transformation)

RF.save_transform(transformation, "temp_transform.tfm") 
print("Transform Saved")

RF.apply_transform_to_stl("temp_transform.tfm", "ST_002_Talus 2.stl",
                           "ST_002_Talus 2_registered.stl")  
print("STL Transformed")

transformed_image = RF.apply_transform_to_image(img2, transformation)
RF.write_transformed_image_to_nrrd(transformed_image, "ST_002_L_registered.nrrd")
print("Registered Image Saved")