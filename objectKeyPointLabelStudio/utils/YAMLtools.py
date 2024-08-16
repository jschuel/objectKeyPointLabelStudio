import yaml
import os

'''Read yaml file'''
def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data

'''Utility function to save YAML files'''
def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

'''Utility function for saving lists to YAML outputs'''
def represent_list(flow_style):
    def _represent_list(dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=flow_style)
    return _represent_list

'''Load master configuration'''
def load_configuration(file_path):
    #Read yoloConf field of yaml file
    conf = read_config_file(file_path)
    return conf

'''Create Ultralytics configuration for training/evaluating YOLO'''
def create_keypoint_config(master_config_path):
    master_config = load_configuration(master_config_path)
    
    # Extract relevant data from master configuration
    max_num_keypoints = master_config['yoloConf']['maxNumKeyPoints']
    objects = master_config['Objects']
        
    # Add enabled classes to the 'names' dictionary
    class_id = 0
    for obj, enabled in objects.items():
        if enabled:
            yolo_config['names'][class_id] = obj
            class_id += 1

    # Register representer for formatting lists with flow style
    yaml.add_representer(list, represent_list(flow_style=True))
