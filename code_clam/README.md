# CLAM_wql_version

CLAM（Cluster-constrained Attention Multiple instance learning）的个人修改版。

基于 [CLAM](https://github.com/mahmoodlab/CLAM)（Mahmood Lab）修改，用于全切片病理图像（WSI）的补丁提取、特征提取与热图生成。

## 本版本的修改/新增

- `wql_dataprocess/` — 个人数据处理脚本
- `create_patches_wql.py` / `extract_patches_wql.py` — 自定义补丁提取
- `extract_features_wql` 系列（`extract_features_byol.py` 等）— 自定义特征提取
- `create_patches_sdpc.py` / `extract_patches_SDPC.py` — SDPC 格式切片处理（依赖本地私有 `sdpc` 模块，未随仓库发布）

## 快速开始

```bash
pip install openslide-python byol_pytorch
python create_patches_fp.py --source <WSI目录> --save_dir <输出> --patch_size 1024 --seg --patch --stitch
python extract_features_fp.py --data_h5_dir <h5目录> --data_slide_dir <切片目录> --csv_path <csv> --feat_dir <特征输出> --batch_size 1024 --slide_ext .svs
```

许可遵循本目录 `LICENSE.md`。
