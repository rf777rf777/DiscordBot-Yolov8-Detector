#!/bin/bash

#COMMON PATHS
buildFolder=$(pwd)
slnFolder=$(realpath "$buildFolder/../")
outputFolder="$buildFolder/outputs"
appFolder="$slnFolder/source"  #Discord 應用的文件夾
containerName="discordbot-yolov8-detector"
accountName="rf777rf777"
version=":1.0.7"
latest=":latest"

## CLEAR ######################################################################

#刪除舊的 outputs 文件夾
rm -rf "$outputFolder"
#創建新的 outputs 文件夾
mkdir -p "$outputFolder"

## COPY APP FILES #############################################################

#將app目錄的內容複製到 outputs/Host 目錄
outputHostFolder="$outputFolder/Host"
mkdir -p "$outputHostFolder"
cp -R "$appFolder/"* "$outputHostFolder"

## REMOVE __pycache__ #########################################################

#刪除outputs/Host中的__pycache__文件夾（遞歸刪除）
find "$outputHostFolder" -type d -name "__pycache__" -exec rm -rf {} +

#刪除outputs/Host中包含"venv"字樣的資料夾（遞歸刪除）
find "$outputHostFolder" -type d -name "*venv*" -exec rm -rf {} +

## CREATE DOCKER IMAGES #######################################################

#切換到 Host 文件夾，準備 Docker 映像構建
cd "$outputHostFolder"

#構建 Docker 映像
#使用 buildx 構建多架構 Docker 映像
docker buildx create --use || true
docker buildx build --push -t "$accountName/$containerName$version" -t "$accountName/$containerName$latest" --platform linux/amd64,linux/arm64 .
#替 Docker 映像標記版號
#docker tag "$accountName/$containerName$version" "$accountName/$containerName$latest"

#推送 Docker 映像到 Docker Hub
#docker push "$accountName/$containerName$version"
#docker push "$accountName/$containerName$latest"

##FINALIZE ###################################################################

#返回初始的工作目錄
cd "$buildFolder"
