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
    current_directory = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    #Check the Ultralytics fields in master_configuration.yaml based on if we're using noise and linear or log scale images
    conf['yoloConf']['project_dir'] = current_directory+'/'+conf['yoloConf']['project_dir']
    if conf['yoloConf']['noise'] == True:
        if conf['yoloConf']['log_scale'] == True:
            conf['yoloConf']['project'] = conf['yoloConf']['project_dir']+'/models/noise_log'
        else:
            conf['yoloConf']['project'] = conf['yoloConf']['project_dir']+'/models/noise_linear'
    else:
        if conf['yoloConf']['log_scale'] == True:
            conf['yoloConf']['project'] = conf['yoloConf']['project_dir']+'/models/log'
        else:
            conf['yoloConf']['project'] = conf['yoloConf']['project_dir']+'/models/linear'
    conf['yoloConf']['suffix'] = '_'+os.path.split(conf['yoloConf']['project'])[1]
    return conf

'''Create Ultralytics configuration for training/evaluating YOLO'''
def create_keypoint_config(master_config_path):
    master_config = load_configuration(master_config_path)
    
    # Extract relevant data from master configuration
    max_num_keypoints = master_config['yoloConf']['maxNumKeyPoints']
    objects = master_config['Objects']
    
    # Create new YOLO config
    yolo_config = {
        'path': master_config['yoloConf']['project_dir'] + '/datasets/',
        'train': 'train%s/'%(master_config['yoloConf']['suffix']),
        'val': 'valid%s/'%(master_config['yoloConf']['suffix']),
        'test': 'test%s/'%(master_config['yoloConf']['suffix']),
        'kpt_shape': [max_num_keypoints, 2],
        'names': {}
    }
    
    # Add enabled classes to the 'names' dictionary
    class_id = 0
    for obj, enabled in objects.items():
        if enabled:
            yolo_config['names'][class_id] = obj
            class_id += 1

    # Register representer for formatting lists with flow style
    yaml.add_representer(list, represent_list(flow_style=True))

    # Save new YOLO config
    outfile = master_config['yoloConf']['project_dir']+'/configs/keypoint.yaml'
    if not os.path.exists(os.path.split(outfile)[0]):
        os.makedirs(os.path.split(outfile)[0])
    save_yaml(yolo_config, outfile)
    print(f"Created YOLO configuration saved to {outfile}")
