function [bwImg, RGB, img_adjust] = lumenSegmentation(img_origin)
%对数变换
img_adjust_ori=mat2gray(log(1+double(img_origin)));
%高斯滤波
W = fspecial('gaussian',[5,5],1);
img_adjust = imfilter(img_adjust_ori, W, 'replicate');
[m,n]=size(img_adjust);

%分块二值化
bw = block_binarize(img_adjust,5,8);

for i = 1:m
    if size(find(bw(i,:) == 1),2) > 800 %去除横跨整张图片的条形噪声
        bw(i,:)=0;
    end
end
se=strel('disk',1);
bw=imerode(bw,se);
%% 对连通域进行处理

bw = removeCatheter(bw);


BW2nd=verticalCut(bw, 30);
BW2nd=imfill(BW2nd,'holes');


bw=bwareaopen(bw,200,4);
bw = removeArtifacts(bw);
bw=imdilate(bw,se);

bw = verticalCut(bw, 20);
bw = removeArtifacts(bw);
bw=imfill(bw,'holes');


%% 以下部分为插值相关

y = interpolateLumenBoundary(bw, 100);

bw=false(m,n);
for j=1:m
    for k=1:n
        if k>y(j)
            bw(j,k)=1;
        end
    end
end
bw5=edge(bw);

%% 恢复管壁区域
plist4=regionprops(BW2nd,'PixelList');
list4=regionprops(BW2nd,'PixelIdxList');
[r,c,~]=find(bw5==1);
edge4=[c,r];
t=length(edge4);
l=length(plist4);
for p=1:l
    for q=1:t
        logc4(q) = ismember(edge4(q,:),plist4(p).PixelList,'rows');
    end
    if logc4==0
        BW2nd(list4(p).PixelIdxList)=0;
    end
end

y2 = interpolateLumenBoundary(BW2nd,50);
bwImg = false(m,n);
for j=1:m
    for k=1:n
        if k>y2(j)
            bwImg(j,k)=1;
        end
    end
end

bw2=edge(bwImg);
[X,map]=gray2ind(B2,65536);
RGB=ind2rgb(X,map);
[m1,n1]=size(RGB(:,:,1));
for i=1:m1
    for j=1:n1
        if bw2(i,j)==1
            RGB(i,j,1)=255;
            RGB(i,j,2)=0;
            RGB(i,j,3)=0;
        end
    end
end
end

function bw = verticalCut(bw, consecutiveNum)
q=0;
[m,n] = size(bw);
for i = 1:m %去除竖直长条状连通域
    for p=1:n/5
        if bw(i,p)==1
            q=q+1;
        end
        if q<consecutiveNum&&bw(i,p)==0 %若连续像素点小于阈值则去除
            for j=(p-q):p
                bw(i,j)=0;
            end
            q=0;
        elseif q>consecutiveNum&&bw(i,p)==0
            q=0;
        end
    end
    q=0;
end
end

function bw = removeCatheter(bw)

% try to use the regionprops function to the orientation of the binary
% picture
shapeProps = regionprops(bw,'Orientation');
shapearea = regionprops(bw);

orientations = zeros(1, length(shapeProps));
for nRegion = 1:length(shapeProps)
    if shapearea(nRegion).Area>50&&shapearea(nRegion).BoundingBox(3)<30
        orientations(nRegion) = shapeProps(nRegion).Orientation;
    end
end % nRegion
imgBWLabel= bwlabel(bw);
for nRegion = 1:length(shapeProps)
    idx = find(imgBWLabel == nRegion);
    if abs(shapeProps(nRegion).Orientation - 90) < 22&&shapearea(nRegion).BoundingBox(3)<30&&shapearea(nRegion).Centroid(2)<n/5
        bw(idx) = 0;
    end
    
    if abs(shapeProps(nRegion).Orientation + 90) < 22  &&shapearea(nRegion).BoundingBox(3)<30&&shapearea(nRegion).Centroid(2)<n/5
        bw(idx) = 0;
    end
end
end

function bw = removeArtifacts(bw)
%当两个连通域拥有同样的行数，并满足一定的限制条件，则去除位置靠左的连通域
stats0=bwlabel(bw,4);
plist0=regionprops(stats0,'PixelList');
list0=regionprops(stats0,'PixelIdxList');
area0=regionprops(stats0,'Area');
t=length(plist0);
for k=1:t-1
    q=1;
    while k+q<=t
        a=intersect(plist0(k).PixelList(:,2),plist0(k+q).PixelList(:,2));
        if ~isempty(a)
            bw = removeOnce(bw, plist0,area0,list0, a, k, q);
        end
        q=q+1;
    end
end
end

function bw = removeOnce(bw, plist0, area0,list0, a, k, q)
pixel0=plist0(k+q).PixelList(plist0(k+q).PixelList(:,2)==a(1),:);
pixel2=plist0(k).PixelList(plist0(k).PixelList(:,2)==a(1),:);
pixel=pixel0(end,:);
pixel3=pixel2(1,:);
pixel5=pixel2(end,:);
pixel7=pixel0(1,:);
index1=[];
for j=1:length(a)
    index1= [index1;find(plist0(k+q).PixelList(:,2)==a(j))];
end
pixel8=plist0(k+q).PixelList(index1,:);
clear index1;
index2=[];
for j=1:length(a)
    index2= [index2;find(plist0(k).PixelList(:,2)==a(j))];
end
pixel9=plist0(k).PixelList(index2,:);
clear index2;
if pixel5(1)<pixel7(1)
    if area0(k).Area(1)<area0(k+q).Area(1)*4&&length(pixel9)>0.15*area0(k).Area
        
        bw(list0(k).PixelIdxList)=0;
    end
end
if pixel(1)<pixel3(1)
    if 4*area0(k).Area(1)>area0(k+q).Area(1)&&length(pixel8)>0.15*area0(k+q).Area
        %
        bw(list0(k+q).PixelIdxList)=0;
    end
end
end

function y2 = interpolateLumenBoundary(bw, smoothParam)
tmp = bw;
[m,n] = size(bw);
for i=1:m
    if size(find(tmp(i,:) == 1),2) < 5
        if i-5>0 && i+5<=m
            bw((i-5):(i+5),:)=0;
        elseif i-5<=0
            bw(1:(i+5),:)=0;
        elseif i+5>m
            bw((i-5):m,:)=0;
        end
    end
end
nonz = zeros(1,m);
for i = 1:m
    if size(find(bw(i,:) == 1),2) > 0
        nonz(i) = find(bw(i,:) ~= 0, 1 );
        if nonz(i)>(2*n/3)
            nonz(i)=0;
        end
    end
end
num = length(find(nonz > 0));
x = zeros(1,num);
y = x;
k = 1;
for i = 1:m%i循环的是原图的Y值
    if nonz(i) > 0
        y(k) = i;%将nonz中大于0的数据的列数保存在y中，其实对应原图的Y值
        x(k) = nonz(i);%将nonz中大于0的数（对应原图的X值）保存在x中
        k = k+1;%统计y的总个数
    end
end
x1 = y;%x1为将nonz中大于0的数据的列数(对应原图的Y值)保存在x1中
y1 = x;%将nonz中大于0的数（对应原图的X值）保存在x(y1)中

if max(x1)<m
    x1 =[x1,m];
    y1=[y1,y1(1)];
end
if min(x1)>1
    x1 =[1,x1];
    y1=[y1(end),y1];
end
x2 = 1:m;%x1最后一个数一定得包括最大宽度
y2= interp1(x1,y1,x2,'pchip');%双立方插值，将导引丝挡住的部分填充出来，插值出y2来
y2=smoothdata(y2,'rloess',smoothParam);%用合适的阈值平滑插值出的曲线
end


function bw = block_binarize(img,blocknum_l,blocknum_h)
[m,n]=size(img);
lengthSide = floor(m/blocknum_l);  %每个分块长度
heightSide = floor(n/blocknum_h);  %每个分块宽度
bw=img;
%开始分块处理
for p = 1:blocknum_h
    for q = 1:blocknum_l
    
        %生成模板
        block = zeros(size(bw));    %将模板初始化为0
        lini = 1 + lengthSide * (q - 1);
        hini = 1 + heightSide * (p - 1);     %分块的第一个像素在原图中的坐标
        x = lini:(lini + lengthSide - 1);
        y = hini:(hini + heightSide - 1);    %生成分块长、宽坐标序列
        block(x, y) = 1;                     %将模板上需要进行分块的部分转换成1，用来提取该分块
        
        %提取分块
        bw = im2double(bw);     %原图转换为double类型，保证和模板black同类型以做点乘
        block = block .* bw;    %将原图投影在模板上
        block = block(x, y);    %提取分块

        %阈值分割处理
        optval{p,q} = graythresh(block);
        fangcha(p,q)=std2(block);

        g = imbinarize(block,optval{p,q});      %阈值分割
        if p>0
            if  ~(max(max(block))>mean(mean(img(:,floor(3*n/4):end)))+0.1&&fangcha(p,q)>0.045)
                g=zeros(size(g));
            end
        end

        %拼接
        bw(x, y) = g;     %将阈值分割处理过的分块放回原图
    end

end

end
