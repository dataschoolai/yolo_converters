#Import libraries for file and folder handling
from pathlib import Path
#Import libraries for JSON handling
import json
import shutil
#Import library for visualization progress bar
from tqdm import tqdm
#Import utility for creating a folder
from utils import make_output_dir

#Import the libarary for image processing
import cv2
#Import the library for command line arguments
import argparse

input_dir = '/home/buntuml/github/damage.ai/CrackDetectionDataset/CONCRETE_DATASET_YOLOv5/valid'
output_dir = 'DATASET_JSON'

#Define the function for converting YOLOv3 format to COCO format
def get_bbox(instance:list,width:int,height:int):
    #Create a list to store the bounding boxes
    bboxes = []
    #Loop through all instances
    for inst in instance:
        #Get coordinates of the bounding box
        x_center = float(inst[0])*width
        y_center = float(inst[1])*height
        w = float(inst[2])*width
        h = float(inst[3])*height
        #Get COCO format bounding box
        bbox = [int(x_center - w/2), int(y_center - h/2), int(w), int(h)]
        #Add bounding box to the list
        bboxes.append(bbox)
    #Return the list of bounding boxes
    return bboxes
    
        




#Define the function for converting YOLOv3 output to JSON
def yolo_to_json(input_dir: Path, output_dir: Path, classes: list):
    #Create a list of all annotation files
    annotation_path = list(input_dir.glob('**/*.txt'))

    #Loop through all annotation files
    for idx,path in enumerate((annotation_path)):
        #Get the label id
        label_id = path.stem
        #Print the label id
        print(label_id)
        #Open the annotation file
        with open(path, 'r') as f:
            #Read the annotation file
            #Split the annotation file into lines
            lines = f.read().splitlines()
            
        #Create a list to store the bounding boxes
        data = []
        #Loop through all lines
        for line in lines:
            #Split the line into space
            line = line.split(' ')
            #add the bounding box to the list
            #Get the class name
            class_name = line[0]
            #Get the bounding box coordinates from the line and than add to data
            data.append(line[1:])
            

        
        #Define the input image path
        image_path = input_dir/f'images/{label_id}.jpg'
        #Define the output image path
        output_path = output_dir/f'images/{label_id}.jpg'
        shutil.copy(image_path, output_path)


          
        #Get the image size
        img = cv2.imread(str(image_path))
        height, width, _ = img.shape
        #Get the bounding boxes
        bboxes = get_bbox(data,width,height)
        #Create a dictionary for the annotation file
        annotations = {
            'annotations':[],
        }
        #Annotate the image
        annotations['images']=[{
            'file_name':path.stem,
            'height':height,
            'width':width,
            'id':1
        }]

        #Loop through all bounding boxes
        for bbox in bboxes:
            #Get the bounding box coordinates
            x1,y1,w,h = bbox
            #add the bounding box to the dictionary
            annotations['annotations'].append({
                'bbox':[x1,y1,w,h],
                'category_id':1,#classes.index(class_name),
                'image_id':1,
                'id':idx,
                'iscrowd':0,
                'area':w*h
            })

        #Write the annotation file
        with open(output_dir/f'labels/{label_id}.json', 'w') as f:
            json.dump(annotations, f)


#Create the output directory
make_output_dir(output_dir)
#Convert the YOLOv3 output to JSON
yolo_to_json(Path(input_dir), Path(output_dir), classes=[])