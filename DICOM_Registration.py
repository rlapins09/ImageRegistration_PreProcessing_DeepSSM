import Registration_Functions as RF

stack1 = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA/ST_001_L"
stack2 = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA/ST_004_R"

image1 = RF.import_dicom_series(stack1)
image2 = RF.import_dicom_series(stack2)
print("Image Data Imported")

#resample
img1 = RF.resample_image_with_scaling(image1, 3.0)
img2 = RF.resample_image_with_scaling(image2, 3.0)

#reflect if left footed
image1,ref1 = RF.reflect_image_if_needed(img1, stack1)
image2,ref2 = RF.reflect_image_if_needed(img2, stack2)   

RF.save_image_as_nrrd(img1, "ST_001_L_resampled.nrrd")
RF.save_image_as_nrrd(image1, "ST_001_L_reflected.nrrd")

################ REFLECT STL ################
stl1 = "ST_001_Talus 1.stl"
stl1_out = "ST_001_Talus 1_reflected.stl"
stl2 = "ST_004_Talus_NoHoles 1.stl"

# Reflect the mesh across the x-axis
if ref1:
    stl_mesh1 = RF.reflect_stl_mesh(stl1, axis='x')
    print("Reflected: " + stl1)
    if ref2:
        stl_mesh2 = RF.reflect_stl_mesh(stl2, axis='x') 
        print("Reflected: " + stl2)
    else:
        stl_mesh1 = RF.read_stl(stl1)
        stl_mesh2 = RF.read_stl(stl2)        


################ IMG REGISTRATION ################
transform = RF.register_images(image1, image2)
# RF.show_registration(image1, image2, transform)
transformed_image = RF.apply_transform_to_img(transform, image2, image1)  
import SimpleITK as sitk 
sitk.WriteImage(transformed_image, "ST_004_R_transformed.nrrd")  

transformed_stl = RF.apply_transform_to_stl(transform, stl_mesh2,"ST_004_Talus_reflected_transformed.stl")
