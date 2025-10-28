import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Pasta onde salvar os arquivos
local_path = "C:\\Users\\Eduardo\\Desktop\\Imagens de satélites"
arquivo_local = os.path.join(local_path, "arquivo_goes.nc")

# Conexão anônima
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    config=Config(signature_version=UNSIGNED)
)

bucket = 'noaa-goes16'
prefix = "ABI-L2-CMIPF/2017/191/00/"

response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=10)

if 'Contents' in response:
    primeiro_arquivo = response['Contents'][0]['Key']
    print("Arquivo selecionado:", primeiro_arquivo)

    # Baixar arquivo
    s3.download_file(bucket, primeiro_arquivo, arquivo_local)
    print("Arquivo baixado com sucesso em:", arquivo_local)

    # Abrir com xarray
    variaveis_img = xr.open_dataset(arquivo_local)
    print(variaveis_img)

    dados = variaveis_img['CMI']
    lat = variaveis_img['lat']
    lon = variaveis_img['lon']

    mask = (lat >= -34) & (lat <= 5) & (lon >= -74) & (lon <= -34)
    dados_brasil = dados.where(mask, drop=True)
    lat_brasil = lat.where(mask, drop=True)
    lon_brasil = lon.where(mask, drop=True)

    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    im = ax.pcolormesh(lon_brasil, lat_brasil, dados_brasil, cmap='gray')
    ax.add_feature(cfeature.BORDERS, edgecolor='red')
    ax.add_feature(cfeature.COASTLINE)
    ax.set_title('GOES-16 CMI - Brasil')
    plt.colorbar(im, label='Reflectância')
    plt.show()

else:
    print("Nenhum arquivo encontrado para esse prefixo.")
