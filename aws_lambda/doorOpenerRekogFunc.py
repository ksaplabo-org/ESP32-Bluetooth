import json
import os
import boto3
import math

iot = boto3.client('iot-data')
IOT_TOPIC = "ksap-dooropenerSub"

def lambda_handler(event, context):
    try:
        # TODO implement
        bucket = "ksap-dooropener-image"
        for record in event['Records']:
            #データ取得
            imn = record['dynamodb']['NewImage']['ImageName']['S']
            tm =  record['dynamodb']['NewImage']['GetDateTime']['S']
            imn = "img/"+imn
            image = {"S3Object": {"Bucket": bucket,"Name": imn}}
                
            #rekognitionのクライアント作成
            client=boto3.client('rekognition')
            
            #rekognition呼び出し
            response = client.detect_faces(Image=image,Attributes=["ALL"])
            
            #rekognition結果をDynamoDBへ更新
            if len(response['FaceDetails'])>0 :
                faceDetail = response['FaceDetails'][0]
                lowAge = faceDetail["AgeRange"]["Low"]
                highAge = faceDetail["AgeRange"]["High"]
                gender = faceDetail["Gender"]["Value"]
                print(highAge)
                print(lowAge)
                if gender=="Male":
                    age = highAge
                else :
                    age = math.floor((lowAge+highAge)/2)
                
                # DynamoDB接続設定
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('ksap-dooropener-analyze-tbl')
                    
                # DynamoDB登録処理
                ret = table.put_item(
                    Item={
                        'GetDateTime': tm,
                        'ImageName':imn,
                        'Gender': gender,
                        'Age': age
                    }
                )
                
                payload = {
                    'GetDateTime': tm,
                    'Gender':gender,
                    'Age': age
                }
                
                iot.publish(
                    topic=IOT_TOPIC,
                    qos=1,
                    payload=json.dumps(payload, ensure_ascii=False)
                )
                
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
        
    return {
        'statusCode': 200,
        'body': ""
    }
