clear;
close all;
% load("CENT16902.mat");
config = toml.read("../config.toml");
sequenceName = config.segmentation.sequence_name;
format = config.segmentation.img_format;
st = config.segmentation.start_img;
ed = config.segmentation.end_img;
file_path = strcat("../result/binary/",sequenceName,'/');
img_path_list = dir(strcat(file_path,'*',format));%获取该文件夹中所有.tif格式的图像
img_num = length(img_path_list);                %获取图像总数
if st == 0
    st = 1;
end
if ed == 0
    ed = img_num;
end
pointCloud = zeros((ed - st + 1) * 100, 3);
if img_num > 0 %有满足条件的图像
    for pn = st:ed %逐一读取图像
        fprintf('%d %s\n',pn,strcat(file_path,num2str(pn)));
        img_origin = imread(strcat(file_path,num2str(pn),format));
        if size(img_origin,3) ~= 1
            img_origin = rgb2gray(img_origin);
        end
        img_origin = im2double(img_origin);

        bw = imbinarize(img_origin);
        bw = bwareaopen(bw,100);
        [M,N]=size(bw);
        x = [];
        y = [];
        for i = 1:5:M
            x = [x;i];
            for j = 1:N
                if bw(i, j) == 1
                    y = [y;j];
                    break;
                end
            end
        end

        theta=2*pi*x/M;
        [xx,yy]=pol2cart(theta,y);

        maxX = floor(max(xx));
        minX = ceil(min(xx));
        maxY = floor(max(yy));
        minY = ceil(min(yy));
        maxdis = 0;
        xy = zeros((maxX - minX + 1) * (maxY - minY + 1), 2);
        num = 1;
        for i = minX:maxX
            for j = minY:maxY
                xy(num,1) = i;
                xy(num,2) = j;
                num = num + 1;
            end
        end
        isValid = inpolygon(xy(:,1),xy(:,2),xx,yy);
        num = 1;
        for i = 1:length(xy)
            if isValid(num)
                dis = min((xx-xy(i,1)).^2+(yy-xy(i,2)).^2);
                if maxdis < dis
                    A = xy(i,1);%主血管中心
                    B = xy(i,2);
                    maxdis = dis;
                end
            end
            num = num + 1;
        end
       
        xx = xx - A;
        yy = yy - B;
        
%         figure;
%         scatter(r,c);
%         hold on;
%         scatter(0, 0);

        z = zeros(length(xx), 1);
        z(1:end)=(pn-1)*40;
%         z=z';
        point=[xx,yy,z];
%         AREA(pn)=length(P);
        pointCloud(((pn - 1) * 100 + 1) : (pn * 100),:) = point;
%         pointCloud=[pointCloud;point];
%         close all
    end
end
mkdir(strcat("../result/pointClouds/",sequenceName));
save(strcat("../result/pointClouds/",sequenceName,"/pointCloud.txt"), 'pointCloud', '-ascii');
% save(strcat('Area',sequenceName,".mat"),'AREA');
% scatter3(pointCloud(:,1),pointCloud(:,2),pointCloud(:,3));
% hold on
% scatter3(zeros(z(1),1),zeros(z(1),1),1:z(1));
% axis equal

