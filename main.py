import os
import sys
import json
import subprocess
import numpy as np
import torch
from torch import nn
import timeit
from opts import parse_opts
from model import generate_model
from mean import get_mean
from classify import classify_video
import
#os.system('echo $$ > ~/myscript.pid')
if __name__=="__main__":
    opt = parse_opts()
    opt.mean = get_mean()
    opt.arch = '{}-{}'.format(opt.model_name, opt.model_depth)
    opt.sample_size = 112
    opt.sample_duration = 25
    opt.n_classes = 400

    model = generate_model(opt)
    print('loading model {}'.format(opt.model))
    model_data = torch.load(opt.model)
    assert opt.arch == model_data['arch']
    model.load_state_dict(model_data['state_dict'])
    model.eval()
    if opt.verbose:
        print(model)

    input_files = []
    with open(opt.input, 'r') as f:
        input_files = [row[:-1] for row in f]
    print("Total Number of Files is :" + str(len(input_files))+'\n')
    class_names = []
    if opt.mode == 'score':
        with open('class_names_list') as f:
            for row in f:
                class_names.append(row[:-1])
    opt.output=opt.output+'.json'
    with open(opt.output,'w') as f:
        f.write('[')
    first = True;
    start = timeit.default_timer()
    for i,input_file in enumerate(input_files):
        stop = timeit.default_timer()
        T=stop - start
        print(' Video Number: {}/{}Time taken: {} Minutes {} Seconds '.format(i,len(input_files),T//60,T%60) )
        print( '\n Progress: ' + str(((i+1)*100)//len(input_files)) + '% \n')
        video_path = os.path.join(opt.video_root, input_file)
        if os.path.exists(video_path):
            print(video_path)
            if video_path==:
                import ipdb; ipdb.set_trace()
                
            result = classify_video(video_path, input_file, class_names, model, opt)
            if result!=-1:
                with open(opt.output,'a') as f:
                    if not first:
                        f.write(', ')
                    first=False
                    json.dump(result,f)
            else:
                print("Warning Video Skipped")

        else:
            print('{} does not exist'.format(input_file))
    print('done')
    with open(opt.output,'a') as f:
        f.write(']')
