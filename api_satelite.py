import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Conexão anônima com bucket público GOES-16
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    config=Config(signature_version=UNSIGNED)
)

bucket = 'noaa-goes16'
prefix = 'ABI-L2-CMIPF/2025/300/2130/'  # substitua com a data/hora que quiser

# Listar arquivos disponíveis no prefix
response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])

    # Baixar o primeiro arquivo listado
    first_file = response['Contents'][0]['Key']
    s3.download_file(bucket, first_file, 'goes_file.nc')
    print("Arquivo baixado com sucesso:", first_file)
else:
    print("Nenhum arquivo encontrado nesse prefixo.")
