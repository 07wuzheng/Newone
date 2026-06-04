# Risk Register / 风险登记表
# AI Tool Navigator Project

---

| ID | Risk | Probability | Impact | Score | Mitigation | Contingency | Owner |
|----|------|------------|--------|-------|------------|-------------|-------|
| R01 | **技术遗忘** - 忘记Vue/Python语法 | High (4) | Medium (3) | 12 | AI辅助生成代码，边写边学，提供示例参考 | 准备代码片段速查表 | You |
| R02 | **范围膨胀** - 想加更多功能超出MVP | Medium (3) | High (4) | 12 | 严格遵循PRD的MVP范围，新功能标记为Post-MVP | PRD作为范围控制的"法律依据" | PM |
| R03 | **时间有限** - 每天仅1-2小时导致进度慢 | High (4) | Medium (3) | 12 | 任务拆成30分钟-2小时的小块，每周聚焦一个阶段 | 延期到第8/9周，灵活调整 | You |
| R04 | **部署失败** - 免费部署平台不稳定或配置复杂 | Medium (3) | Medium (3) | 9 | 准备截图+录屏作为备用演示方案 | 本地Demo + 截图 + 录屏 | You |
| R05 | **依赖版本冲突** - 库版本不兼容 | Low (2) | Medium (3) | 6 | 锁定package.json和requirements.txt版本 | 使用项目级虚拟环境/venv隔离 | You |
| R06 | **AI生成代码质量** - 需要大量调试 | Medium (3) | Low (2) | 6 | 写清楚prompt，让AI生成可测试的小块代码 | 阅读并理解生成的代码再集成 | You |

---

## Risk Scoring Matrix

```
Probability: 1=Rare, 2=Unlikely, 3=Possible, 4=Likely, 5=Almost Certain
Impact: 1=Negligible, 2=Minor, 3=Moderate, 4=Major, 5=Catastrophic
Score = Probability × Impact (Max 25)
```

## Current Risk Status

| Risk ID | Status | Last Reviewed | Notes |
|---------|--------|---------------|-------|
| R01 | 🟡 Active | Week 0 | AI监控中，随时可提供代码示例 |
| R02 | 🟢 Monitoring | Week 0 | PRD已定稿，作为范围控制基准 |
| R03 | 🟡 Active | Week 0 | 任务已拆分为小块 |
| R04 | 🟢 Planning | Week 0 | 部署方案待定 |
| R05 | 🟢 Planning | Week 0 | 依赖版本将在搭建时锁定 |
| R06 | 🟢 Monitoring | Week 0 | 使用小块Prompt策略 |
