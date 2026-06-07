# pyRevit 按钮清单

> 基于 `pyrevit/YangAgent.extension/YangAgent.tab/` 下的实际按钮整理。
> 更新日期：2026-06-07

---

## 面板结构

```
YangAgent 选项卡
├── 设置 (Settings.panel)
│   └── 系统设置
└── 导出报告 (Reports.panel)
    ├── 导出路径
    ├── 导出模型快照
    ├── 模型健康报告
    ├── 回归测试清单
    ├── AI分析提示词
    ├── 预览缺失标记
    ├── 预览缺失房间编号
    ├── 预览重复房间编号
    ├── 预览未上图视图
    ├── 预览视图命名
    ├── 应用门窗标记
    └── 应用房间编号
```

---

## 按钮清单

| # | 按钮名称 | 中文显示 | 类型 | 是否修改模型 | 预期输出 | 需人工确认 | 需 Revit Undo |
|---|---------|---------|------|------------|---------|----------|-------------|
| 1 | SystemSettings | 系统设置 | 配置 | ❌ 否 | 保存用户设置（语言、简称、主题、AI 习惯等） | ❌ | ❌ |
| 2 | ReportExportPath | 导出路径 | 配置 | ❌ 否 | 设置报告输出目录 | ❌ | ❌ |
| 3 | ExportModelSnapshot | 导出模型快照 | 只读 | ❌ 否 | JSON / CSV 模型数据快照 | ❌ | ❌ |
| 4 | ModelHealthReport | 模型健康报告 | 只读 | ❌ 否 | Markdown 模型健康检查报告 | ❌ | ❌ |
| 5 | ExportRegressionChecklist | 回归测试清单 | 只读 | ❌ 否 | Markdown 标准工具测试清单 | ❌ | ❌ |
| 6 | ExportAIReviewPrompt | AI分析提示词 | 只读 | ❌ 否 | 安全 AI 分析提示词 + 最近报告清单 | ❌ | ❌ |
| 7 | PreviewMissingDoorWindowMarks | 预览缺失标记 | dry-run | ❌ 否 | Markdown + CSV：缺少标记的门窗列表 | ❌ | ❌ |
| 8 | PreviewMissingRoomNumbers | 预览缺失房间编号 | dry-run | ❌ 否 | Markdown + CSV：缺少编号的房间列表 | ❌ | ❌ |
| 9 | PreviewDuplicateRoomNumbers | 预览重复房间编号 | dry-run | ❌ 否 | Markdown + CSV：重复编号的房间列表 | ❌ | ❌ |
| 10 | PreviewUnplacedViews | 预览未上图视图 | dry-run | ❌ 否 | Markdown + CSV：可能未放置到图纸的视图列表 | ❌ | ❌ |
| 11 | PreviewViewNamingRules | 预览视图命名 | dry-run | ❌ 否 | Markdown + CSV：视图命名规则问题列表 | ❌ | ❌ |
| 12 | ApplyMissingDoorWindowMarks | 应用门窗标记 | apply | ✅ 是 | apply Markdown 日志 + CSV 结果 | ✅ 必须 | ✅ 必须验证 |
| 13 | ApplyMissingRoomNumbers | 应用房间编号 | apply | ✅ 是 | apply Markdown 日志 + CSV 结果 | ✅ 必须 | ✅ 必须验证 |

---

## 类型说明

| 类型 | 说明 | 风险 |
|------|------|------|
| **配置** | 设置用户偏好，不碰模型 | 无 |
| **只读** | 从模型读取信息并导出 | 无 |
| **dry-run** | 模拟检查，生成报告但不写入模型 | 无 |
| **apply** | 读取 dry-run CSV，确认后写入模型 | 低（可撤销） |

---

## apply 工具的安全机制

两个 apply 按钮都遵循相同的安全流程：

1. **只能读取对应 dry-run 产生的 CSV** — 不接受其他来源的文件。
2. **CSV 字段校验** — 字段不对时给出明确错误码。
3. **apply 前显示影响数量** — 弹窗告知将要修改的元素数。
4. **Revit Transaction 名称清晰** — 方便从 Undo 列表中找到并整批撤销；是否一次 Ctrl+Z 生效需要在测试模型验证。
5. **输出 apply 日志** — Markdown + CSV 双份记录，事后可查。
6. **跳过已被人工修改的元素** — 不会覆盖你已经手动改过的内容。

---

## apply 常见错误码速查

### 应用房间编号

| 错误码 | 含义 | 处理 |
|--------|------|------|
| YA-APPLY-ROOM-001 | CSV 文件名不符合要求 | 选择 `missing_room_numbers_*.csv` |
| YA-APPLY-ROOM-002 | CSV 缺少必要字段 | 重新运行 `预览缺失房间编号` |
| YA-APPLY-ROOM-003 | element_id 无效 | 检查 CSV 是否被手工改坏 |
| YA-APPLY-ROOM-004 | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| YA-APPLY-ROOM-005 | 找不到房间编号参数 | 检查模型房间参数 |
| YA-APPLY-ROOM-006 | 房间编号参数只读 | 跳过该房间，人工处理 |

### 应用门窗标记

| 错误码 | 含义 | 处理 |
|--------|------|------|
| YA-APPLY-MARK-001 | CSV 文件名不符合要求 | 选择 `missing_door_window_marks_*.csv` |
| YA-APPLY-MARK-002 | CSV 缺少必要字段 | 重新运行 `预览缺失标记` |
| YA-APPLY-MARK-003 | element_id 无效 | 检查 CSV 是否被手工改坏 |
| YA-APPLY-MARK-004 | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| YA-APPLY-MARK-005 | 找不到 Mark 参数 | 检查族或参数 |
| YA-APPLY-MARK-006 | Mark 参数只读 | 跳过该元素，人工处理 |
