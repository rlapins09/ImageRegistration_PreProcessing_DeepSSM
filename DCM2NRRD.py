import Registration_Functions as RF
import os
import SimpleITK as sitk
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import numpy as np

def check_laterality(image, pt_name, threshold=300):

    img = sitk.GetArrayFromImage(image)   

    img_thresholded = img > threshold

    img_filled = ndi.binary_fill_holes(img_thresholded[400,:,:])
    img_filled = ndi.binary_opening(img_filled, structure=np.ones((3,3)))
    img_filled = ndi.binary_closing(img_filled, structure=np.ones((5,5)))
    img_filled = ndi.binary_fill_holes(img_filled)
    img_filled = ndi.label(img_filled)[0] > 0

    # plt.imshow(img_filled,cmap='gray')
    # plt.show()

    _, img_num_objects = ndi.label(img_filled)
    print(img_num_objects)

    if img_num_objects >= 4:
        if pt_name.endswith("_R") or pt_name.endswith("_Right"):
            img_cropped = img[:,:, :img.shape[1]//2]
            plt.imshow(img_cropped[400,:,:])
            plt.show()
            img_cropped = sitk.GetImageFromArray(img_cropped)  
            img_cropped.SetOrigin(image.GetOrigin())
            img_cropped.SetDirection(image.GetDirection())
        else:
            img_cropped = img[:,:,img.shape[1]//2:]
            plt.imshow(img_cropped[400,:,:])
            plt.show()
            img_cropped = sitk.GetImageFromArray(img_cropped)
            new_origin = list(image.GetOrigin())
            new_origin[0] += image.GetSpacing()[0]*(img.shape[1]//2)
            img_cropped.SetOrigin(new_origin)
            img_cropped.SetDirection(image.GetDirection())
    else:
        img_cropped = sitk.GetImageFromArray(img)
        img_cropped.SetOrigin(image.GetOrigin())
        img_cropped.SetDirection(image.GetDirection())

    img_cropped.SetSpacing(image.GetSpacing())

    return img_cropped


path = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA"
nrrd_path = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/06_Projects/STOA/STOA_DeepSSM_7_10_2024/images"

pts = os.listdir(path)

for i in range(0,1):
    ii = pts[i]
    dcm_path = os.path.join(path, ii)
    
    dcm_img = RF.import_dicom_series(dcm_path)
    dcm = check_laterality(dcm_img,ii)
    # dcm_sitk = sitk.GetImageFromArray(dcm)
    dcm_down = RF.resample_image_with_scaling(dcm, 5.0) 

    print(dcm_down.GetSpacing())

    nrrd_file_path = os.path.join(nrrd_path, ii + ".nrrd")

    RF.save_image_as_nrrd(dcm_down, nrrd_file_path)
    print( nrrd_file_path)

