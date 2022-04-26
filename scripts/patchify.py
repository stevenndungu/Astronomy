#!/data/$USER/venvs/pybdsf/bin python3
'''
module load Python/3.8.6-GCCcore-10.2.0
source /data/$USER/venvs/pybdsf/bin/activate
'''

#Import relevant libraries
from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
from astropy import units as u
import sys
import os

def patches_center(in_img, size_x = 315,size_y = 315):
    '''
    in_img: data, numpy array of the large image to be split
    size_x: x dimension of the split patches
    size_y: y dimension of the split patches
    NB: set the size_x and size_y divisible with the w,h of the large image.
    '''
    in_img = str(in_img)[2:-1][:-1]
    print(in_img)
    hdulist = fits.open(in_img)
    img = hdulist[0].data
    img_reverse = img.reshape(img.shape[3],img.shape[2],img.shape[1],img.shape[0]) # reverse order of the shape 
    print(img_reverse.shape)
    img_2d = img_reverse.reshape(img_reverse.shape[0],img_reverse.shape[1])
    #center co-ordinate
    xcord = size_x/2; ycord = size_y/2
    centers = []; centers_dic = {}
    for i in range(int(img_2d.shape[0]/size_x)):

        for j in range(int(img_2d.shape[1]/size_y)):

            centers_dic[(str(i) + '_' + str(j))] = tuple(list((xcord + size_x*i,ycord + size_y*j)))
            centers.append(centers_dic)

    return centers

def patchify_and_save(in_img, center, size_x, size_y,out_name):
    hdulist = fits.open(in_img)
    #extract the header info and reduce the dimension 2 if > 4 
    wcs = WCS(hdulist[0].header,naxis=2)
    #specify the center of the cutout patch
    position = center
    #specify the size of the patch
    size = (size_x, size_y) 
    #use the  Cutout2D function: more details https://docs.astropy.org/en/stable/api/astropy.nddata.Cutout2D.html
    img = hdulist[0].data
    img_reverse = img.reshape(img.shape[3],img.shape[2],img.shape[1],img.shape[0]) # reverse order of the shape 
    img_2d = img_reverse.reshape(img_reverse.shape[0],img_reverse.shape[1])
    cutout = Cutout2D(img_2d, position = position, size = size, wcs = wcs)
    # Update the FITS header with the cutout WCS
    hdulist[0].header.update(cutout.wcs.to_header())
    # Put the cutout image in the FITS HDU
    hdulist[0].data = cutout.data
    # Write the cutout to a new FITS file
    patch_filename = out_name + '.fits'
    hdulist[0].writeto(patch_filename, overwrite=True)


def generate_patches(in_img):
    
    centers = patches_center(in_img, size_x = 315,size_y = 315)
    print('=== centers generation done! ===')

    #os.chdir('/home/p307791/patches')
    in_img = str(in_img)[2:-1][:-1]
    #for idx in range(len(centers)):
    for idx in range(5):#test
           
        patchify_and_save(in_img = in_img,
                        center = list(centers[0].values())[idx], 
                        size_x = 315, 
                        size_y = 315,
                        out_name = in_img.split("fits")[0] + "patch_" + list(centers[0].keys())[idx] 
                        )
        print('=== Patch cutout ' + str(idx) + ' complete! ===')

# TODO: merge patchify_and_save, patches_center and source finder for code reuse & optimization
if __name__ == "__main__":
    in_img = sys.argv[1:]
    print(in_img)
    generate_patches(in_img)
