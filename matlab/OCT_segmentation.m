clear;close all;
addpath(genpath('.'));

% allpoint: the point cloud of the blood vessel.
% AREA: The cross-sectional area
% Please store these two value for mixing the OCT & DSA
% Or you can encapsulated this script to a function.


file_path =  'C:\Users\18139\Documents\OCT_Processing\imagesequence\狭窄病变 无支架\罗金枝_855513_20220719093641\855513_罗金枝_56\2022_06_15__13_55_47\';% 图像文件夹路径
mkdir(strcat(file_path,'\binary'));
mkdir(strcat(file_path,'\label'));
img_path_list = dir(strcat(file_path,'*.tif'));%获取该文件夹中所有.tif格式的图像
img_num = length(img_path_list);%获取图像总数
% % load('C:\Users\18139\OneDrive\文件\大创\FFR\blood sequence\shadow10.mat');
% Y=cell(1,img_num);
% AREA=zeros(img_num,1);
if img_num > 0 %有满足条件的图像
    for pn = 1:img_num %逐一读取图像
        image_name = img_path_list(pn).name;
        fprintf('%d %s\n',pn,strcat(file_path,num2str(pn-1)));
        img_origin = imread(strcat(file_path,image_name));
        [bw, RGB, ~] = lumenSegmentation(img_origin);
        imwrite(bw ,strcat(file_path, 'binary\', num2str(pn), '.png'));
        imwrite(RGB ,strcat(file_path, 'label\', num2str(pn), '.png'));
        clearvars -except img_path_list file_path img_num pn
    end
end