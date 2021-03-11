%%
fileName = rwfeature;
label = 3;
for i=1:length(fileName)
    rw(i,:)=[fileName(i,:), label];
end

%% Concatenate complete dataset
fullDataSet = [lr;rr;lw;rw;fi];
fullDataSet = fullDataSet(:,1:size(fullDataSet,2)-1);



%%
avg = mean(fullDataSet,1); 
stdNum = std(fullDataSet,1);
for i=1:size(fullDataSet,1)
    for j=1:size(fullDataSet,2)-1
        fullDataSet(i,j)=(fullDataSet(i,j) - avg(1,j))/stdNum(1,j);
    end
end

clear featureVector

covarianceMatrix = cov(fullDataSet);
[V,D] = eig(covarianceMatrix);
featureVector(:,1)=V(:,size(fullDataSet,2)-1);
featureVector(:,2)=V(:,size(fullDataSet,2)-2);
featureVector(:,3)=V(:,size(fullDataSet,2)-3);

newele = zeros(size(fullDataSet,1),3);
for i = 1:size(fullDataSet,1)
    newele(i,:) = fullDataSet(i,:)*featureVector;
end


figure
h=scatter3(newele(1:size(lr,1),1),newele(1:size(lr,1),2),newele(1:size(lr,1),3),'filled','MarkerEdgeColor','r','MarkerFaceColor','r');
hold on
% startNum=size(lr,1);
% h=scatter3(newele(startNum+1:startNum+size(rr,1),1),newele(startNum+1:startNum+size(rr,1),2),newele(startNum+1:startNum+size(rr,1),3),'filled','MarkerEdgeColor','g','MarkerFaceColor','g');
% hold on 
% startNum=size(lr,1)+size(rr,1);
% h=scatter3(newele(startNum+1:startNum+size(lw,1),1),newele(startNum+1:startNum+size(lw,1),2),newele(startNum+1:startNum+size(lw,1),3),'filled','MarkerEdgeColor','b','MarkerFaceColor','b');
% hold on 
% startNum=size(lr,1)+size(rr,1)+size(lw,1);
% h=scatter3(newele(startNum+1:startNum+size(rw,1),1),newele(startNum+1:startNum+size(rw,1),2),newele(startNum+1:startNum+size(rw,1),3),'filled','MarkerEdgeColor','k','MarkerFaceColor','k');
% hold on 
% startNum=size(lr,1)+size(rr,1)+size(lw,1)+size(rw);
% h=scatter3(newele(startNum+1:startNum+size(fi,1),1),newele(startNum+1:startNum+size(fi,1),2),newele(startNum+1:startNum+size(fi,1),3),'filled','MarkerEdgeColor','magenta','MarkerFaceColor','magenta');
% hold on 
% axis([-3.5 3.5 -3.5 3.5])
% axis square

%%
avg = mean(fullDataSet,1); 
stdNum = std(fullDataSet,1);
for i=1:size(fullDataSet,1)
    for j=1:size(fullDataSet,2)
        fullDataSetNormed(i,j)=(fullDataSet(i,j) - avg(1,j))/stdNum(1,j);
    end
end

clear featureVector

covarianceMatrix = cov(fullDataSetNormed(1:148,:));
[V,D] = eig(covarianceMatrix);
featureVector(:,1)=V(:,1);
featureVector(:,2)=V(:,2);
featureVector(:,3)=V(:,3);
% featureVector(:,1)=V(:,size(fullDataSetNormed,2)-1);
% featureVector(:,2)=V(:,size(fullDataSetNormed,2)-2);
% featureVector(:,3)=V(:,size(fullDataSetNormed,2)-3);
newele = zeros(size(fullDataSetNormed,1),3);
for i = 1:size(fullDataSetNormed,1)
    newele(i,:) = fullDataSetNormed(i,:)*featureVector;
end

figure
h=scatter3(newele(1:size(lr,1),1),newele(1:size(lr,1),2),newele(1:size(lr,1),3),'filled','MarkerEdgeColor','r','MarkerFaceColor','r');
hold on
startNum=size(lr,1);
h=scatter3(newele(startNum+1:startNum+size(rr,1),1),newele(startNum+1:startNum+size(rr,1),2),newele(startNum+1:startNum+size(rr,1),3),'filled','MarkerEdgeColor','g','MarkerFaceColor','g');
hold on 
startNum=size(lr,1)+size(rr,1);
h=scatter3(newele(startNum+1:startNum+size(lw,1),1),newele(startNum+1:startNum+size(lw,1),2),newele(startNum+1:startNum+size(lw,1),3),'filled','MarkerEdgeColor','b','MarkerFaceColor','b');
hold on 
startNum=size(lr,1)+size(rr,1)+size(lw,1);
h=scatter3(newele(startNum+1:startNum+size(rw,1),1),newele(startNum+1:startNum+size(rw,1),2),newele(startNum+1:startNum+size(rw,1),3),'filled','MarkerEdgeColor','k','MarkerFaceColor','k');
hold on 
startNum=size(lr,1)+size(rr,1)+size(lw,1)+size(rw);
h=scatter3(newele(startNum+1:startNum+size(fi,1),1),newele(startNum+1:startNum+size(fi,1),2),newele(startNum+1:startNum+size(fi,1),3),'filled','MarkerEdgeColor','magenta','MarkerFaceColor','magenta');
hold on 

%%
avg = mean(fullDataSet,1); 
stdNum = std(fullDataSet,1);
for i=1:size(fullDataSet,1)
    for j=1:size(fullDataSet,2)
        fullDataSetNormed(i,j)=(fullDataSet(i,j) - avg(1,j))/stdNum(1,j);
    end    
end
avg = mean(lrfeature,1); 
stdNum = std(lrfeature,1);
for i=1:size(lrfeature,1)
    for j=1:size(lrfeature,2)
        lrNormed(i,j)=(lrfeature(i,j) - avg(1,j))/stdNum(1,j);
    end    
end
avg = mean(rrfeature,1); 
stdNum = std(rrfeature,1);
for i=1:size(rrfeature,1)
    for j=1:size(rrfeature,2)
        rrNormed(i,j)=(rrfeature(i,j) - avg(1,j))/stdNum(1,j);
    end    
end
avg = mean(lwfeature,1); 
stdNum = std(lwfeature,1);
for i=1:size(lwfeature,1)
    for j=1:size(lwfeature,2)
        lwNormed(i,j)=(lwfeature(i,j) - avg(1,j))/stdNum(1,j);
    end    
end
avg = mean(rwfeature,1); 
stdNum = std(rwfeature,1);
for i=1:size(rwfeature,1)
    for j=1:size(rwfeature,2)
        rwNormed(i,j)=(rwfeature(i,j) - avg(1,j))/stdNum(1,j);
    end    
end
avg = mean(fifeature,1); 
stdNum = std(fifeature,1);
for i=1:size(fifeature,1)
    for j=1:size(fifeature,2)
        fiNormed(i,j)=(fifeature(i,j) - avg(1,j))/stdNum(1,j);
    end    
end
%% Visualise raw features
featureArray=["mav" "wl" "ssc" "rms"];
for featureColumn = 1:4
    figure;
    subplot(3,2,1);
    plot(lrfeature(:,featureColumn),0,'o','MarkerFaceColor','r','MarkerEdgeColor','r')
%     hold on
%     plot(lrfeature(:,featureColumn+5),0,'o','MarkerFaceColor','g','MarkerEdgeColor','g')
%     hold on
%     plot(lrfeature(:,featureColumn+10),0,'o','MarkerFaceColor','b','MarkerEdgeColor','b')
    grid on
    xl1 = xlim;
    title('LR','FontSize',18)
    
    subplot(3,2,2);
    plot(rrfeature(:,featureColumn),0,'o','MarkerFaceColor','r','MarkerEdgeColor','r')
%     hold on
%     plot(rrfeature(:,featureColumn+5),0,'o','MarkerFaceColor','g','MarkerEdgeColor','g')
%     hold on
%     plot(rrfeature(:,featureColumn+10),0,'o','MarkerFaceColor','b','MarkerEdgeColor','b')
    grid on
    xl2 = xlim;
    title('RR','FontSize',18)
    
    subplot(3,2,3);
    plot(lwfeature(:,featureColumn),0,'o','MarkerFaceColor','r','MarkerEdgeColor','r')
%     hold on
%     plot(lwfeature(:,featureColumn+5),0,'o','MarkerFaceColor','g','MarkerEdgeColor','g')
%     hold on
%     plot(lwfeature(:,featureColumn+10),0,'o','MarkerFaceColor','b','MarkerEdgeColor','b')
    grid on
    xl3 = xlim;
    title('LW','FontSize',18)
    
    subplot(3,2,4);
    plot(rwfeature(:,featureColumn),0,'o','MarkerFaceColor','r','MarkerEdgeColor','r')
%     hold on
%     plot(rwfeature(:,featureColumn+5),0,'o','MarkerFaceColor','g','MarkerEdgeColor','g')
%     hold on
%     plot(rwfeature(:,featureColumn+10),0,'o','MarkerFaceColor','b','MarkerEdgeColor','b')
    grid on
    xl4 = xlim;
    title('RW','FontSize',18)
    
    subplot(3,2,5);
    plot(fifeature(:,featureColumn),0,'o','MarkerFaceColor','r','MarkerEdgeColor','r')
%     hold on
%     plot(fifeature(:,featureColumn+5),0,'o','MarkerFaceColor','g','MarkerEdgeColor','g')
%     hold on
%     plot(fifeature(:,featureColumn+10),0,'o','MarkerFaceColor','b','MarkerEdgeColor','b')
    grid on
    xl5 = xlim;
    title('FI','FontSize',18)
    
    % Find leftmost xLeft
    xLeft = min([xl1(1), xl2(1), xl3(1), xl4(1)]);
    % Find rightmost xRight
    xRight = max([xl1(2), xl2(2), xl3(2), xl4(2)]);
    
    
    subplot(3,2,1);
    xlim([xLeft, xRight]);
    subplot(3,2,2);
    xlim([xLeft, xRight]);
    subplot(3,2,3);
    xlim([xLeft, xRight]);
    subplot(3,2,4);
    xlim([xLeft, xRight]);
    subplot(3,2,5);
    xlim([xLeft, xRight]);
    sgtitle(featureArray(featureColumn),'FontSize',24)
end

%% Visualise standardised features
featureArray=["mav" "wl" "ssc" "rms"];
for featureColumn = 1:4;
    figure;
    subplot(3,2,1);
    plot(lrNormed(:,featureColumn),0,'o','MarkerFaceColor','red','MarkerEdgeColor','red')
    xl1 = xlim;
    hold on
    title('LR','FontSize',18)
    subplot(3,2,2);
    plot(rrNormed(:,featureColumn),0,'o','MarkerFaceColor','green','MarkerEdgeColor','green')
    xl2 = xlim;
    hold on
    title('RR','FontSize',18)
    subplot(3,2,3);
    plot(lwNormed(:,featureColumn),0,'o','MarkerFaceColor','blue','MarkerEdgeColor','blue')
    xl3 = xlim;
    hold on
    title('LW','FontSize',18)
    subplot(3,2,4);
    plot(rwNormed(:,featureColumn),0,'o','MarkerFaceColor','k','MarkerEdgeColor','k')
    xl4 = xlim;
    hold on
    title('RW','FontSize',18)
    subplot(3,2,5);
    plot(fiNormed(:,featureColumn),0,'o','MarkerFaceColor','magenta','MarkerEdgeColor','magenta')
    xl5 = xlim;
    hold on
    title('FI','FontSize',18)
    % Find leftmost xLeft
    xLeft = min([xl1(1), xl2(1), xl3(1), xl4(1)]);
    % Find rightmost xRight
    xRight = max([xl1(2), xl2(2), xl3(2), xl4(2)]);
    
    
    subplot(3,2,1);
    xlim([xLeft, xRight]);
    subplot(3,2,2);
    xlim([xLeft, xRight]);
    subplot(3,2,3);
    xlim([xLeft, xRight]);
    subplot(3,2,4);
    xlim([xLeft, xRight]);
    subplot(3,2,5);
    xlim([xLeft, xRight]);
    sgtitle(featureArray(featureColumn),'FontSize',24)
end

%% LDA
slice=1:size(fullDataSetNormed,1)
sw=zeros(length(slice),length(slice));
for i=1:size(fullDataSetNormed,1)
    sw = sw + (bf(i,slice)-bfMean(slice))'*(bf(i,slice)-bfMean(slice));
end
sb = (bfMean(slice)-csMean(slice))'*(bfMean(slice)-csMean(slice));

[V,D] = eig(sw'*sb);
[sor,index] = sort(diag(D),'descend');
sortedEigenVector=zeros(length(slice),length(slice));
