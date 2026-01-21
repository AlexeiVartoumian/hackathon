#!/bin/bash


echo "Creating Lambda layer for gspread..."


mkdir -p lambda-layer/python

pip install \
    gspread \
    google-auth \
    google-auth-oauthlib \
    google-auth-httplib2 \
    --target lambda-layer/python \
    --break-system-packages


cd lambda-layer
zip -r ../gspread-layer.zip python/
cd ..

echo "Layer created: gspread-layer.zip"
echo ""
echo "Upload this to AWS Lambda Layers:"
echo "1. Go to Lambda Console → Layers → Create Layer"
echo "2. Name: gspread-dependencies"
echo "3. Upload gspread-layer.zip"
echo "4. Compatible runtimes: Python 3.9, Python 3.10, Python 3.11, Python 3.12"
echo ""
echo "Size: $(du -h gspread-layer.zip | cut -f1)"