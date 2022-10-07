clear;close all;
addpath(genpath('.'));

config = toml.read("../config.toml");
file_path = config.segmentation.original_img_path;
sequenceName = config.segmentation.sequence_name;
format = config.segmentation.img_format;
st = config.segmentation.start_img;
ed = config.segmentation.end_img;

res_path = "../result/";
binary_path = strcat(res_path,'binary/',sequenceName,'/');
label_path = strcat(res_path,'label/',sequenceName,'/');
mkdir(binary_path);
mkdir(label_path);
img_path_list = dir(strcat(file_path,'*',format));%获取该文件夹中所有.tif格式的图像
img_num = length(img_path_list);%获取图像总数
if st == 0
    st = 1;
end
if ed == 0
    ed = img_num;
end

if img_num > 0 %有满足条件的图像
    for pn = st:ed %逐一读取图像
        image_name = img_path_list(pn).name;
        fprintf('%d %s\n',pn,strcat(file_path,num2str(pn-1)));
        img_origin = imread(strcat(file_path,image_name));
        [bw, RGB, ~] = lumenSegmentation(img_origin);
        imwrite(bw ,strcat(binary_path, num2str(pn), format));
        imwrite(RGB ,strcat(label_path, num2str(pn), format));
    end
end