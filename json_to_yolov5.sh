#run json to yolov5
input_dir='/mnt/hdd2/aihubkr_visualization/ConcreteCrack/labels'
output_dir='/mnt/hdd2/yolov5_train/workspace'
label='ConcreteCrack'
python json_to_yolov5.py --input_dir $input_dir --output_dir $output_dir --label $label