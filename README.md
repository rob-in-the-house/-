# -
按照地区范围和距离生成经纬度坐标

## 环境依赖
python版本3.8.8
依赖库
- folium==0.17.0
- geopy==2.4.1
- numpy==1.24.4
- shapely==2.0.5
- requests==2.31.0
- web.py==0.62

## 服务启动
python polygon.py

## 例子
http://localhost:8080/polygon?zoom=9&code=650200&distance=5
- zoom	放大倍数	取值范围3-18，一般取9-11之间
- code	地区编码	例如：克拉玛依 650200
- distance	经纬度间距	单位：公里

![0661d787c499cfab0ec2c6256953ba9](https://github.com/user-attachments/assets/72b664fa-7896-4fa4-b006-eaed5d63071e)

---
PS：地图资源需要翻墙
