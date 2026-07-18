# YOLO11 FastAPI 目标检测网站

这是一个基于 FastAPI 和 Ultralytics YOLO11 的图片目标检测网站。用户在网页上传图片后，后端会调用 `yolo11n.pt` 模型进行检测，并返回带检测框的结果图、目标数量、类别和置信度。

## 功能

- 图片上传检测
- 支持 jpg、jpeg、png、bmp、webp
- 上传图片大小限制为 10MB
- 自动生成唯一文件名，避免多次检测互相覆盖
- 显示检测结果图、目标数量、检测耗时和置信度
- 支持电脑本机访问，也支持同一局域网内手机访问
<img width="1051" height="1170" alt="image" src="https://github.com/user-attachments/assets/7497b7c6-0ca0-4b82-b6ec-7a532909a1aa" />
<img width="1125" height="559" alt="image" src="https://github.com/user-attachments/assets/c19b0361-bb86-4205-89cd-a43b9fe0101e" />



## 项目结构

```text
yolo_fastapi/
├─ main.py
├─ requirements.txt
├─ run_server.bat
├─ yolo11n.pt
├─ templates/
│  └─ index.html
├─ uploads/
└─ results/
```

`uploads/` 和 `results/` 会在运行时自动创建，里面的图片不会上传到 GitHub。

## 安装依赖

建议使用独立 Python 环境：

```bash
pip install -r requirements.txt
```

## 启动网站

Windows 可以直接双击：

```text
run_server.bat
```

也可以在项目目录执行：

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8010 --reload
```

电脑本机访问：

```text
http://127.0.0.1:8010/
```

手机访问时，手机和电脑需要连接同一个 Wi-Fi，然后在手机浏览器访问：

```text
http://电脑IPv4地址:8010/
```

例如：

```text
http://172.21.3.167:8010/
```

## 注意事项

- 如果手机无法访问，检查 Windows 防火墙是否允许 Python 或 8010 端口访问。
- `yolo11n.pt` 是模型文件，项目启动时必须存在。
- 如果更换模型，把新模型放到项目目录，并在 `main.py` 中修改 `MODEL_PATH`。
