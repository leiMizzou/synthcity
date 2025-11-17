"""
使用Synthcity生成100个合成患者数据
演示完整的数据生成流程
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
from synthcity.plugins import Plugins
from synthcity.plugins.core.dataloader import GenericDataLoader
from synthcity.metrics import Metrics

print("=" * 80)
print("Synthcity 患者数据生成演示")
print("=" * 80)

# ============================================================================
# 步骤1: 加载真实患者数据
# ============================================================================
print("\n[步骤1] 加载真实患者数据集...")
X, y = load_diabetes(return_X_y=True, as_frame=True)
X["target"] = y

# 添加更多真实感的列名
X.columns = ['年龄', '性别', 'BMI', '平均血压', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', '疾病进展指标']

print(f"✓ 数据集大小: {X.shape[0]} 患者, {X.shape[1]} 个特征")
print(f"\n真实数据前5行:")
print(X.head())
print(f"\n数据统计:")
print(X.describe())

# ============================================================================
# 步骤2: 创建数据加载器
# ============================================================================
print("\n[步骤2] 创建数据加载器...")
loader = GenericDataLoader(
    X,
    target_column="疾病进展指标",
    sensitive_columns=["性别"]  # 性别作为敏感属性
)
print(f"✓ 数据加载器创建成功")
print(f"  - 目标列: {loader.target_column}")
print(f"  - 特征数: {len(loader.columns)}")

# ============================================================================
# 步骤3: 选择并配置生成模型
# ============================================================================
print("\n[步骤3] 选择生成模型...")

# 测试多个生成器
generators_config = {
    "CTGAN (条件GAN)": {
        "name": "ctgan",
        "params": {
            "n_iter": 500,  # 训练迭代次数
            "batch_size": 100,
        }
    },
    "TVAE (表格VAE)": {
        "name": "tvae",
        "params": {
            "n_iter": 500,
            "batch_size": 100,
        }
    },
    "AdsGAN (匿名化GAN)": {
        "name": "adsgan",
        "params": {
            "n_iter": 500,
            "batch_size": 100,
        }
    }
}

# 选择使用CTGAN作为主要生成器
selected_generator = "CTGAN (条件GAN)"
config = generators_config[selected_generator]

print(f"✓ 选择生成器: {selected_generator}")
print(f"  - 模型: {config['name']}")
print(f"  - 训练迭代: {config['params']['n_iter']}")
print(f"  - 批次大小: {config['params']['batch_size']}")

# ============================================================================
# 步骤4: 训练生成模型
# ============================================================================
print(f"\n[步骤4] 训练 {selected_generator} 模型...")
print("  (这可能需要几分钟时间...)")

model = Plugins().get(config["name"], **config["params"])
model.fit(loader)

print(f"✓ 模型训练完成!")

# ============================================================================
# 步骤5: 生成100个合成患者数据
# ============================================================================
print("\n[步骤5] 生成100个合成患者数据...")

synthetic_loader = model.generate(count=100)
synthetic_data = synthetic_loader.dataframe()

print(f"✓ 成功生成 {len(synthetic_data)} 个合成患者数据")
print(f"\n合成数据前5行:")
print(synthetic_data.head())
print(f"\n合成数据统计:")
print(synthetic_data.describe())

# ============================================================================
# 步骤6: 数据质量评估
# ============================================================================
print("\n[步骤6] 评估合成数据质量...")

try:
    # 基本统计比较
    print("\n6.1 统计特性比较:")
    print("-" * 80)

    comparison = pd.DataFrame({
        '真实数据均值': X.mean(),
        '合成数据均值': synthetic_data.mean(),
        '差异': abs(X.mean() - synthetic_data.mean()),
        '真实数据标准差': X.std(),
        '合成数据标准差': synthetic_data.std()
    })
    print(comparison)

    # 数据范围检查
    print("\n6.2 数据范围检查:")
    print("-" * 80)
    for col in X.columns:
        real_min, real_max = X[col].min(), X[col].max()
        syn_min, syn_max = synthetic_data[col].min(), synthetic_data[col].max()
        in_range = (syn_min >= real_min * 0.9) and (syn_max <= real_max * 1.1)
        status = "✓" if in_range else "⚠"
        print(f"{status} {col:20s}: 真实[{real_min:7.2f}, {real_max:7.2f}] vs 合成[{syn_min:7.2f}, {syn_max:7.2f}]")

    # 评估指标
    print("\n6.3 质量评估指标:")
    print("-" * 80)

    # 使用简单的评估指标
    from scipy.stats import ks_2samp

    ks_scores = {}
    for col in X.columns:
        statistic, pvalue = ks_2samp(X[col], synthetic_data[col])
        ks_scores[col] = {'statistic': statistic, 'p-value': pvalue}

    print("Kolmogorov-Smirnov 检验 (p-value > 0.05 表示分布相似):")
    for col, score in ks_scores.items():
        status = "✓" if score['p-value'] > 0.05 else "⚠"
        print(f"  {status} {col:20s}: p-value = {score['p-value']:.4f}")

except Exception as e:
    print(f"⚠ 评估过程出现错误: {e}")

# ============================================================================
# 步骤7: 保存合成数据
# ============================================================================
print("\n[步骤7] 保存合成数据...")

output_file = "/Users/leihua/Documents/GitHub/synthcity/synthetic_patients_100.csv"
synthetic_data.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✓ 合成数据已保存至: {output_file}")

# ============================================================================
# 步骤8: 数据可视化比较
# ============================================================================
print("\n[步骤8] 生成数据分布可视化...")

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端

    # 创建对比图
    fig, axes = plt.subplots(3, 4, figsize=(20, 15))
    axes = axes.flatten()

    for idx, col in enumerate(X.columns):
        if idx < 12:
            ax = axes[idx]

            # 绘制直方图
            ax.hist(X[col], bins=30, alpha=0.5, label='真实数据', color='blue', density=True)
            ax.hist(synthetic_data[col], bins=30, alpha=0.5, label='合成数据', color='red', density=True)

            ax.set_title(col, fontsize=10)
            ax.set_xlabel('值')
            ax.set_ylabel('密度')
            ax.legend()
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_file = "/Users/leihua/Documents/GitHub/synthcity/synthetic_comparison.png"
    plt.savefig(plot_file, dpi=100, bbox_inches='tight')
    print(f"✓ 可视化图表已保存至: {plot_file}")

except Exception as e:
    print(f"⚠ 可视化生成失败: {e}")

# ============================================================================
# 步骤9: 生成总结报告
# ============================================================================
print("\n" + "=" * 80)
print("生成总结报告")
print("=" * 80)

print(f"""
模型信息:
  - 生成器: {selected_generator}
  - 训练样本数: {len(X)}
  - 生成样本数: {len(synthetic_data)}
  - 特征数: {len(X.columns)}

数据质量:
  - 均值差异: {abs(X.mean() - synthetic_data.mean()).mean():.4f}
  - 标准差差异: {abs(X.std() - synthetic_data.std()).mean():.4f}

输出文件:
  - 合成数据: {output_file}
  - 可视化图: {plot_file if 'plot_file' in locals() else '未生成'}

✓ 成功生成100个高质量合成患者数据!
""")

print("=" * 80)
print("数据生成完成!")
print("=" * 80)

# 显示一些示例患者数据
print("\n示例合成患者数据 (前10个):")
print("-" * 80)
print(synthetic_data.head(10).to_string())
