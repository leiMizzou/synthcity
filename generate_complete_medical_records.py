"""
生成完整的合成患者医疗病历数据
包括结构化数据和非结构化文本（一诉五史、病程记录等）
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
from pathlib import Path

print("=" * 80)
print("完整医疗病历数据生成系统")
print("=" * 80)

# ============================================================================
# 医疗数据模板库
# ============================================================================

# 常见疾病列表
DISEASES = [
    "2型糖尿病", "高血压", "冠心病", "慢性阻塞性肺疾病", "胃炎",
    "脂肪肝", "甲状腺功能减退", "骨关节炎", "慢性肾病", "支气管哮喘"
]

# 症状模板
SYMPTOMS = {
    "2型糖尿病": ["口渴、多饮、多尿", "乏力、体重下降", "视物模糊"],
    "高血压": ["头晕、头痛", "心悸", "胸闷"],
    "冠心病": ["胸闷、胸痛", "气短", "心悸、乏力"],
    "慢性阻塞性肺疾病": ["咳嗽、咳痰", "气促", "呼吸困难"],
    "胃炎": ["上腹痛、腹胀", "恶心、反酸", "食欲不振"]
}

# 既往史模板
PAST_HISTORY = [
    "既往体健", "高血压病史5年", "糖尿病病史3年",
    "冠心病病史2年", "否认肝炎、结核病史"
]

# 个人史模板
PERSONAL_HISTORY = [
    "无吸烟史，偶尔饮酒", "吸烟史20年，每日1包",
    "否认吸烟、饮酒史", "饮酒史10年，每日50ml白酒"
]

# 家族史模板
FAMILY_HISTORY = [
    "父母健在，体健", "父亲有高血压病史", "母亲有糖尿病病史",
    "否认家族遗传性疾病史", "家族中有心脏病史"
]

# 过敏史模板
ALLERGY_HISTORY = ["无药物过敏史", "青霉素过敏", "磺胺类药物过敏", "海鲜过敏"]

# 体格检查模板
PHYSICAL_EXAM_TEMPLATE = """
一般情况: {general_condition}
生命体征: T {temp}℃, P {pulse}次/分, R {resp}次/分, BP {bp_sys}/{bp_dia} mmHg
心脏: 心率{hr}次/分，律齐，心音有力，各瓣膜听诊区未闻及病理性杂音
肺部: 双肺呼吸音清，未闻及干湿性啰音
腹部: 腹软，无压痛、反跳痛，肝脾未触及
四肢: 双下肢无水肿
神经系统: 神志清楚，言语流利，四肢活动自如
"""

# 辅助检查模板
LAB_TESTS = {
    "血常规": ["WBC", "RBC", "HGB", "PLT"],
    "生化全套": ["GLU", "ALT", "AST", "CREA", "BUN", "TC", "TG"],
    "心电图": ["窦性心律", "ST-T改变", "左心室高电压"],
    "胸部X线": ["双肺纹理增粗", "心影增大", "未见明显异常"]
}

# ============================================================================
# 数据生成函数
# ============================================================================

def generate_patient_id(index):
    """生成患者ID"""
    return f"P{datetime.now().year}{index:06d}"

def generate_basic_info(index):
    """生成患者基本信息"""
    gender = random.choice(["男", "女"])
    age = random.randint(25, 85)

    # 中文姓名库（示例）
    surnames = ["王", "李", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴"]
    given_names_male = ["伟", "强", "明", "军", "磊", "涛", "超", "杰", "鹏", "浩"]
    given_names_female = ["芳", "娟", "敏", "静", "丽", "华", "秀", "玲", "红", "艳"]

    surname = random.choice(surnames)
    if gender == "男":
        given_name = random.choice(given_names_male) + random.choice(given_names_male)
    else:
        given_name = random.choice(given_names_female) + random.choice(given_names_female)

    name = surname + given_name

    # 生成身份证号（模拟）
    id_card = f"33010119{1940 + age - 1:02d}{random.randint(1,12):02d}{random.randint(1,28):02d}{random.randint(1000,9999)}"

    # 联系方式
    phone = f"1{random.randint(3,9)}{random.randint(100000000,999999999)}"

    return {
        "患者ID": generate_patient_id(index),
        "姓名": name,
        "性别": gender,
        "年龄": age,
        "出生日期": f"{datetime.now().year - age}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "身份证号": id_card,
        "联系电话": phone,
        "婚姻状况": random.choice(["已婚", "未婚", "离异", "丧偶"]),
        "职业": random.choice(["工人", "农民", "教师", "公务员", "退休", "个体", "其他"]),
        "民族": random.choice(["汉族", "回族", "蒙古族", "藏族", "维吾尔族"])
    }

def generate_chief_complaint(disease):
    """生成主诉"""
    duration = random.choice(["3天", "1周", "2周", "1个月", "3个月", "半年"])
    symptoms = SYMPTOMS.get(disease, ["不适"])
    symptom = random.choice(symptoms)

    return f"{symptom} {duration}"

def generate_present_illness(disease, chief_complaint):
    """生成现病史"""
    templates = [
        f"患者{chief_complaint}前无明显诱因出现{SYMPTOMS.get(disease, ['不适'])[0]}，"
        f"逐渐加重，伴{random.choice(SYMPTOMS.get(disease, ['乏力']))}。"
        f"曾自服{random.choice(['对症药物', '中成药', '止痛药'])}，效果不佳。"
        f"为求进一步诊治，遂来我院就诊。"
        f"发病以来，精神尚可，食欲{'正常' if random.random() > 0.3 else '欠佳'}，"
        f"睡眠{'正常' if random.random() > 0.3 else '欠佳'}，"
        f"大小便正常，体重{'无明显变化' if random.random() > 0.5 else '下降约5kg'}。",

        f"患者于{chief_complaint}前因{random.choice(['劳累', '情绪激动', '饮食不当', '受凉'])}后出现"
        f"{SYMPTOMS.get(disease, ['不适'])[0]}，呈{random.choice(['间断性', '持续性', '阵发性'])}发作，"
        f"{'伴' if random.random() > 0.5 else '不伴'}{random.choice(['恶心呕吐', '发热', '出汗'])}。"
        f"就诊于当地医院，予{random.choice(['对症治疗', '输液治疗', '口服药物治疗'])}，"
        f"症状{'好转' if random.random() > 0.5 else '无明显好转'}。"
        f"今为求系统诊治，来我院就诊。"
    ]

    return random.choice(templates)

def generate_vital_signs(disease):
    """生成生命体征"""
    base_bp_sys = 120
    base_bp_dia = 80

    # 根据疾病调整血压
    if disease == "高血压":
        base_bp_sys = random.randint(140, 160)
        base_bp_dia = random.randint(90, 100)
    elif disease == "2型糖尿病":
        base_bp_sys = random.randint(125, 145)
        base_bp_dia = random.randint(80, 95)

    return {
        "体温": round(random.uniform(36.2, 37.2), 1),
        "脉搏": random.randint(60, 100),
        "呼吸": random.randint(16, 22),
        "收缩压": base_bp_sys,
        "舒张压": base_bp_dia,
        "心率": random.randint(60, 100),
        "血氧饱和度": random.randint(95, 100)
    }

def generate_lab_results(disease):
    """生成检验结果"""
    results = {}

    # 血常规
    results["血常规"] = {
        "白细胞计数": round(random.uniform(4.0, 10.0), 2),
        "红细胞计数": round(random.uniform(4.0, 5.5), 2),
        "血红蛋白": round(random.uniform(120, 160), 1),
        "血小板": random.randint(100, 300)
    }

    # 生化
    if disease == "2型糖尿病":
        glu = round(random.uniform(8.0, 15.0), 1)
    else:
        glu = round(random.uniform(4.5, 6.5), 1)

    results["生化全套"] = {
        "空腹血糖": glu,
        "总胆固醇": round(random.uniform(3.5, 6.5), 2),
        "甘油三酯": round(random.uniform(0.8, 2.5), 2),
        "ALT": random.randint(10, 40),
        "AST": random.randint(10, 35),
        "肌酐": round(random.uniform(50, 110), 1),
        "尿素氮": round(random.uniform(2.5, 7.5), 1)
    }

    # 心电图
    ecg_findings = ["窦性心律", "正常心电图"]
    if disease in ["高血压", "冠心病"]:
        ecg_findings = ["窦性心律", "ST-T改变", "左心室高电压"]
    results["心电图"] = random.choice(ecg_findings)

    return results

def generate_diagnosis(disease):
    """生成诊断"""
    primary = disease
    secondary = []

    if disease == "2型糖尿病":
        if random.random() > 0.5:
            secondary.append("高血压病")
        if random.random() > 0.7:
            secondary.append("脂肪肝")
    elif disease == "高血压":
        if random.random() > 0.6:
            secondary.append("2型糖尿病")

    return {
        "主要诊断": primary,
        "次要诊断": secondary if secondary else ["无"]
    }

def generate_treatment_plan(disease):
    """生成治疗方案"""
    plans = {
        "2型糖尿病": [
            "1. 饮食控制，低糖低脂饮食",
            "2. 口服降糖药物: 二甲双胍 500mg 每日3次",
            "3. 监测血糖变化",
            "4. 定期复查糖化血红蛋白",
            "5. 加强运动，控制体重"
        ],
        "高血压": [
            "1. 低盐低脂饮食",
            "2. 口服降压药: 硝苯地平缓释片 30mg 每日1次",
            "3. 监测血压变化",
            "4. 定期复查",
            "5. 避免情绪激动，适量运动"
        ],
        "冠心病": [
            "1. 绝对卧床休息",
            "2. 抗血小板聚集: 阿司匹林 100mg 每日1次",
            "3. 他汀类药物降脂",
            "4. 硝酸酯类药物扩冠",
            "5. 定期复查心电图、心肌酶谱"
        ]
    }

    return plans.get(disease, ["1. 对症治疗", "2. 定期复查"])

def generate_progress_note(disease, day):
    """生成病程记录"""
    date_str = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d %H:%M")

    templates = [
        f"{date_str} 主治医师查房记录\n"
        f"患者精神{'好转' if day > 2 else '一般'}，{'诉' if random.random() > 0.5 else '无'}不适主诉。"
        f"查体: 生命体征平稳，心肺腹查体未见明显异常。\n"
        f"辅助检查: {'复查血常规、生化，较前无明显变化' if day > 3 else '待完善相关检查'}。\n"
        f"分析: 患者诊断明确，病情{'稳定' if day > 2 else '需密切观察'}。\n"
        f"处理: 继续目前治疗方案，{'可考虑出院' if day > 5 else '继续观察'}。",

        f"{date_str} 病程记录\n"
        f"患者入院第{day}天，病情{'平稳' if random.random() > 0.3 else '好转'}。\n"
        f"主诉: {'症状较前减轻' if day > 1 else '症状同前'}。\n"
        f"查体: T {round(random.uniform(36.3, 37.0), 1)}℃, "
        f"P {random.randint(70, 85)}次/分, BP {random.randint(120, 135)}/{random.randint(75, 85)} mmHg\n"
        f"处理: {'调整用药' if random.random() > 0.7 else '继续原治疗方案'}，加强监护。"
    ]

    return random.choice(templates)

def generate_nursing_record(day):
    """生成护理记录"""
    date_str = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
    time_slots = ["08:00", "14:00", "20:00"]

    records = []
    for time in time_slots:
        temp = round(random.uniform(36.2, 37.0), 1)
        pulse = random.randint(70, 85)
        bp = f"{random.randint(120, 135)}/{random.randint(75, 85)}"

        record = (f"{date_str} {time} "
                 f"T:{temp}℃ P:{pulse}次/分 BP:{bp}mmHg "
                 f"{'神志清楚，精神可' if random.random() > 0.5 else '神志清楚，精神一般'}")
        records.append(record)

    return "\n".join(records)

# ============================================================================
# 主函数：生成完整患者病历
# ============================================================================

def generate_complete_medical_record(index):
    """生成单个完整的患者医疗病历"""
    # 基本信息
    basic_info = generate_basic_info(index)

    # 选择疾病
    disease = random.choice(DISEASES)

    # 一诉五史
    chief_complaint = generate_chief_complaint(disease)
    present_illness = generate_present_illness(disease, chief_complaint)
    past_history = random.choice(PAST_HISTORY)
    personal_history = random.choice(PERSONAL_HISTORY)
    family_history = random.choice(FAMILY_HISTORY)
    allergy_history = random.choice(ALLERGY_HISTORY)

    # 体格检查
    vital_signs = generate_vital_signs(disease)
    general_condition = random.choice(["神志清楚，精神可", "神志清楚，精神一般", "神志清楚，精神差"])

    physical_exam = PHYSICAL_EXAM_TEMPLATE.format(
        general_condition=general_condition,
        temp=vital_signs["体温"],
        pulse=vital_signs["脉搏"],
        resp=vital_signs["呼吸"],
        bp_sys=vital_signs["收缩压"],
        bp_dia=vital_signs["舒张压"],
        hr=vital_signs["心率"]
    )

    # 辅助检查
    lab_results = generate_lab_results(disease)

    # 诊断
    diagnosis = generate_diagnosis(disease)

    # 治疗方案
    treatment_plan = generate_treatment_plan(disease)

    # 病程记录（模拟5天）
    progress_notes = []
    for day in range(1, 6):
        progress_notes.append(generate_progress_note(disease, day))

    # 护理记录
    nursing_records = []
    for day in range(1, 4):
        nursing_records.append(generate_nursing_record(day))

    # 组装完整病历
    medical_record = {
        **basic_info,
        "入院日期": datetime.now().strftime("%Y-%m-%d %H:%M"),

        # 一诉五史
        "主诉": chief_complaint,
        "现病史": present_illness,
        "既往史": past_history,
        "个人史": personal_history,
        "家族史": family_history,
        "过敏史": allergy_history,

        # 体格检查
        "生命体征": vital_signs,
        "体格检查": physical_exam,

        # 辅助检查
        "实验室检查": lab_results,

        # 诊断
        "诊断": diagnosis,

        # 治疗
        "治疗方案": treatment_plan,

        # 病程记录
        "病程记录": progress_notes,

        # 护理记录
        "护理记录": nursing_records
    }

    return medical_record

# ============================================================================
# 批量生成并保存
# ============================================================================

print("\n[步骤1] 开始生成100个完整患者病历...")
all_records = []
for i in range(1, 101):
    if i % 10 == 0:
        print(f"  已生成 {i}/100 个患者病历...")
    record = generate_complete_medical_record(i)
    all_records.append(record)

print(f"✓ 成功生成 {len(all_records)} 个完整患者病历")

# ============================================================================
# 保存为不同格式
# ============================================================================

print("\n[步骤2] 保存数据...")

# 1. 保存为JSON格式（完整数据）
json_file = "/Users/leihua/Documents/GitHub/synthcity/complete_medical_records_100.json"
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(all_records, f, ensure_ascii=False, indent=2)
print(f"✓ JSON格式已保存: {json_file}")

# 2. 保存为CSV格式（结构化数据）
csv_records = []
for record in all_records:
    flat_record = {
        "患者ID": record["患者ID"],
        "姓名": record["姓名"],
        "性别": record["性别"],
        "年龄": record["年龄"],
        "联系电话": record["联系电话"],
        "入院日期": record["入院日期"],
        "主诉": record["主诉"],
        "主要诊断": record["诊断"]["主要诊断"],
        "体温": record["生命体征"]["体温"],
        "脉搏": record["生命体征"]["脉搏"],
        "收缩压": record["生命体征"]["收缩压"],
        "舒张压": record["生命体征"]["舒张压"],
        "血糖": record["实验室检查"]["生化全套"]["空腹血糖"],
        "总胆固醇": record["实验室检查"]["生化全套"]["总胆固醇"]
    }
    csv_records.append(flat_record)

df = pd.DataFrame(csv_records)
csv_file = "/Users/leihua/Documents/GitHub/synthcity/medical_records_structured.csv"
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"✓ CSV格式已保存: {csv_file}")

# 3. 保存单个病历示例（文本格式）
sample_record = all_records[0]
txt_file = "/Users/leihua/Documents/GitHub/synthcity/sample_medical_record.txt"
with open(txt_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("完整电子病历\n")
    f.write("=" * 80 + "\n\n")

    f.write("【基本信息】\n")
    f.write(f"患者ID: {sample_record['患者ID']}\n")
    f.write(f"姓名: {sample_record['姓名']}\n")
    f.write(f"性别: {sample_record['性别']}\n")
    f.write(f"年龄: {sample_record['年龄']}岁\n")
    f.write(f"联系电话: {sample_record['联系电话']}\n")
    f.write(f"入院日期: {sample_record['入院日期']}\n\n")

    f.write("【一诉五史】\n")
    f.write(f"主诉: {sample_record['主诉']}\n\n")
    f.write(f"现病史: {sample_record['现病史']}\n\n")
    f.write(f"既往史: {sample_record['既往史']}\n")
    f.write(f"个人史: {sample_record['个人史']}\n")
    f.write(f"家族史: {sample_record['家族史']}\n")
    f.write(f"过敏史: {sample_record['过敏史']}\n\n")

    f.write("【体格检查】\n")
    f.write(sample_record['体格检查'])
    f.write("\n\n")

    f.write("【辅助检查】\n")
    for test_name, results in sample_record['实验室检查'].items():
        f.write(f"{test_name}:\n")
        if isinstance(results, dict):
            for key, value in results.items():
                f.write(f"  {key}: {value}\n")
        else:
            f.write(f"  {results}\n")
    f.write("\n")

    f.write("【诊断】\n")
    f.write(f"主要诊断: {sample_record['诊断']['主要诊断']}\n")
    f.write(f"次要诊断: {', '.join(sample_record['诊断']['次要诊断'])}\n\n")

    f.write("【治疗方案】\n")
    for plan in sample_record['治疗方案']:
        f.write(f"{plan}\n")
    f.write("\n")

    f.write("【病程记录】\n")
    for note in sample_record['病程记录'][:2]:  # 只显示前2条
        f.write(f"{note}\n\n")

    f.write("【护理记录】\n")
    for note in sample_record['护理记录'][:1]:  # 只显示第1天
        f.write(f"{note}\n\n")

print(f"✓ 示例病历已保存: {txt_file}")

# ============================================================================
# 统计分析
# ============================================================================

print("\n[步骤3] 数据统计分析...")

# 疾病分布
disease_counts = {}
for record in all_records:
    disease = record['诊断']['主要诊断']
    disease_counts[disease] = disease_counts.get(disease, 0) + 1

print("\n疾病分布:")
for disease, count in sorted(disease_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {disease}: {count}例 ({count/len(all_records)*100:.1f}%)")

# 性别分布
gender_counts = {"男": 0, "女": 0}
for record in all_records:
    gender_counts[record['性别']] += 1

print(f"\n性别分布:")
print(f"  男性: {gender_counts['男']}例 ({gender_counts['男']/len(all_records)*100:.1f}%)")
print(f"  女性: {gender_counts['女']}例 ({gender_counts['女']/len(all_records)*100:.1f}%)")

# 年龄分布
ages = [record['年龄'] for record in all_records]
print(f"\n年龄统计:")
print(f"  平均年龄: {np.mean(ages):.1f}岁")
print(f"  年龄范围: {min(ages)}-{max(ages)}岁")

print("\n" + "=" * 80)
print("数据生成完成!")
print("=" * 80)

print(f"""
生成文件清单:
1. complete_medical_records_100.json  - 完整JSON格式病历 (包含所有字段)
2. medical_records_structured.csv     - 结构化CSV数据 (主要字段)
3. sample_medical_record.txt          - 示例病历文本 (第1个患者)

数据包含:
✓ 患者基本信息 (姓名、性别、年龄、联系方式等)
✓ 一诉五史 (主诉、现病史、既往史、个人史、家族史、过敏史)
✓ 体格检查 (生命体征、系统查体)
✓ 辅助检查 (血常规、生化、心电图等)
✓ 诊断 (主要诊断、次要诊断)
✓ 治疗方案 (详细用药方案)
✓ 病程记录 (5天记录)
✓ 护理记录 (3天记录)

推荐使用方式:
- 完整数据: 使用JSON文件
- 数据分析: 使用CSV文件
- 查看示例: 打开TXT文件
""")
