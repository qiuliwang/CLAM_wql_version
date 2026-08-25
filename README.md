# CLAM_USAPAT_version

**USAPAT: Unsupervised Stain-Aware Pixel-Adversarial Transfer Learning for Virtual Immunohistochemical Staining**

本仓库包含两个子项目：

| 目录 | 内容 |
|---|---|
| `code_USAPAT/` | USAPAT 主项目：无监督掩码引导的虚拟 IHC 染色生成（基于 CycleGAN-and-pix2pix 修改） |
| `code_clam/` | CLAM 个人修改版：全切片病理图像（WSI）分析（补丁提取 / 特征提取 / 热图），含 `wql_*` 系列自定义脚本 |

## 快速开始（USAPAT）

```bash
pip install -r requirements.txt          # 根目录（合并版）或 code_USAPAT/requirements.txt
python code_USAPAT/train.py --name transformer_mask_BCI --model cycle_gan ...
```

详细训练/测试命令与参数说明见 **[README_USAPAT.md](README_USAPAT.md)**。

## 目录结构

```
CLAM_USAPAT_version/
├── README.md               # 本文件（仓库入口）
├── README_USAPAT.md        # USAPAT 用法详解
├── requirements.txt        # 合并依赖（USAPAT + CLAM）
├── code_USAPAT/            # 虚拟 IHC 染色（CycleGAN 系）
│   ├── train.py / test.py / test_onlyFake.py
│   ├── models/ options/ util/ data/ scripts/ docs/
│   └── swin_transformer.py
└── code_clam/              # CLAM 个人修改版（WSI）
    ├── create_patches*.py / extract_features*.py
    ├── create_heatmaps.py / eval.py / main.py
    ├── wql_dataprocess/    # 个人数据处理脚本
    └── wsi_core/ models/ utils/ datasets/
```

## 依赖

- 根目录 `requirements.txt` 为合并版；USAPAT 单独依赖见 `code_USAPAT/requirements.txt`
- `code_clam` 需要额外安装 `openslide-python`、`byol_pytorch` 等（见 `requirements.txt` 注释）

## 备注

- `code_clam` 中的 `extract_patches_sdpc.py` 依赖本地 `sdpc` 模块，未随仓库发布（如需要请联系作者）
- `code_USAPAT/README.md` 为原始 CycleGAN-and-pix2pix 项目说明（代码基于其修改）
- CLAM 部分遵循 `code_clam/LICENSE.md`
