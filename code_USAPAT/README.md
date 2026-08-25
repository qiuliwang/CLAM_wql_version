# USAPAT 代码说明

本目录为 **USAPAT**（Unsupervised Stain-Aware Pixel-Adversarial Transfer Learning for Virtual Immunohistochemical Staining）的代码，基于 [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)（Jun-Yan Zhu / Taesung Park 等）修改而来。

主要入口：

- `train.py` — 训练（用法见仓库根目录 `README_USAPAT.md`）
- `test.py` / `test_onlyFake.py` — 测试/生成
- `models/` — 生成器/判别器（含 `resnet_6blocks_vit` 等结构）
- `swin_transformer.py` — Swin-Transformer 相关实现

原始 CycleGAN-and-pix2pix 项目的完整说明请参见原仓库。
