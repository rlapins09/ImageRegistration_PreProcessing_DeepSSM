import Registration_Functions as RF
import itk as itk

stack1 = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA/ST_001_L"
stack2 = "L:/Project_Data/Utah_WBCT/OA/DeepSSM/03_WBCT/STOA/ST_002_L"

fixed_image = itk.imread(stack1, itk.F)
moving_image = itk.imread(stack2, itk.F)

registered_image = RF.itk_elastix_register(fixed_image, moving_image)
